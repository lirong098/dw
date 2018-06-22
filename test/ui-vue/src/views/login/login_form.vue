<template>
  <div>
    <el-form class="login-form" autoComplete="on" :model="loginForm" :rules="loginRules" ref="loginForm" label-position="left">
      <div class="title-container">
        <h3 class="title">系统登录</h3>
        <!-- <lang-select class="set-language"></lang-select> -->
      </div>
      <el-form-item prop="principal">
        <span class="svg-container svg-container_login">
          <svg-icon icon-class="user" />
        </span>
        <el-input name="principal" type="text" v-model="loginForm.principal" autoComplete="on" placeholder="username" />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input name="password" :type="passwordType" @keyup.enter.native="login" v-model="loginForm.password" autoComplete="on" placeholder="password" />
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye" />
        </span>
      </el-form-item>

      <el-button type="primary" style="width:100%;margin-bottom:10px;" :loading="loading" @click="login">登录</el-button>
      <div style="width: 100%; text-align: center;">
        <el-button type="text" @click="reset" class="mr">忘记密码</el-button>
        <el-button type="text" @click="registerDialog" class="mr">注册账号</el-button>
        <!-- <a href="http://www.baidu.com" target="view_window" class="a_button ml">第三方登录</a> -->
      </div>
      <el-card>
        <div slot="header" class="login-form-card-header">
          <span>第三方登录</span>
        </div>
        <ul class="login-form-card-main">
          <li @click="clickHref('http://dev.douwa.io/auth/githublogin')">
            <img src="https://assets.gitlab-static.net/assets/auth_buttons/github_64-84041cd0ea392220da96f0fb9b9473c08485c4924b98c776be1bd33b0daab8c0.png" alt="">
          </li>
        </ul>
      </el-card>
    </el-form>
    <el-dialog
      title="重置密码"
      :visible.sync="resetDialog"
      width="40%"
      :before-close="handleClose">
      <el-form :model="resetData" :rules="resetRules" ref="resetData">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="resetData.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="resetDialog = false">取 消</el-button>
        <el-button type="primary" @click="sendEmail('resetData')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import VueCookie from 'vue-cookie'
import { validatePassword } from './public.js'
export default {
  name: 'login_form',
  components: {},
  props: {},
  data () {
    return {
      loginForm: {
        principal: 'admin',
        password: 'Harbor12345'
      },
      loginRules: {
        principal: [{ required: true, trigger: 'blur' }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      passwordType: 'password',
      loading: false,
      resetDialog: false,
      resetData: {},
      resetRules: {
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur,change' }
        ]
      }
    }
  },
  computed: {},
  created () {},
  mounted () {},
  methods: {
    login () {
      this.loading = true
      this.$api.login.login(this.loginForm).then((res) => {
        if (res.status === 200) {
          this.loading = false
          VueCookie.set('profile', this.loginForm.principal)
          this.$store.commit('SET_USERNAME', this.loginForm.principal)
          this.$router.push({ path: '/' })
        }
      }).catch(err => {
        console.log(err, 'err')
        if (err.status === 401) {
          this.$message.error('账号或密码错误！')
          this.loading = false
        }
      })
    },
    showPwd () {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
    },
    // 忘记密码
    reset () {
      this.resetDialog = true
    },
    registerDialog () {
      this.$emit('setViews', 'register_form')
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    sendEmail (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$api.login.sendEmail({email: this.resetData.email}).then(res => {
            if (res.status === 200) {
              this.resetDialog = false
              this.$message({
                message: '请查收邮件，重置密码',
                type: 'success'
              })
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    clickHref (link) {
      window.open(link)
    }
  },
  updated () {},
  watch: {}
}
</script>
<style rel="stylesheet/scss" lang="scss" scope>
$bg:#2d3a4b;
$light_gray:#eee;
.login-form {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        &:-webkit-autofill {
          -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: #fff !important;
        }
      }
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
    .login-form-card-header {
      text-align: center;
    }
    .login-form-card-main {
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      li {
        // border: 1px solid red;
        height: 40px;
        width: 40px;
        img {
          height: 100%;
          width: 100%;
          cursor: pointer;
        }
      }
    }
    .el-card__header {
      padding: 10px 20px;
    }
  }
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;
.login-form {
  // position: absolute;
  // left: 0;
  // right: 0;
  width: 500px;
  padding: 35px 35px 15px 35px;
  margin: 120px auto;
  .a_button {
    color: #66b1ff;
    font-weight: 500;
    font-size: 14px;
  }
}
.tips {
  font-size: 14px;
  color: #fff;
  margin-bottom: 10px;
  span {
    &:first-of-type {
      margin-right: 16px;
    }
  }
}
.svg-container {
  padding: 6px 5px 6px 15px;
  color: $dark_gray;
  vertical-align: middle;
  width: 30px;
  display: inline-block;
  &_login {
    font-size: 20px;
  }
}
.title-container {
  position: relative;
  .title {
    font-size: 26px;
    font-weight: 400;
    color: $light_gray;
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
}
.show-pwd {
  position: absolute;
  right: 10px;
  top: 7px;
  font-size: 16px;
  color: $dark_gray;
  cursor: pointer;
  user-select: none;
}
.thirdparty-button {
  position: absolute;
  right: 35px;
  bottom: 28px;
}
</style>
