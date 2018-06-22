<template>
    <div class="editpwd-wrap">
        <!--<div class="ms-title">修改密码</div>-->
        <!--<div class="ms-editpwd">-->
            <!--<el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">-->
                <!--<el-form-item prop="oldPassword">-->
                    <!--<el-input type="password" v-model="ruleForm.oldPassword" placeholder="旧密码"></el-input>-->
                <!--</el-form-item>-->
                <!--<el-form-item prop="newPassword">-->
                    <!--<el-input type="password" placeholder="新密码" v-model="ruleForm.newPassword"></el-input>-->
                <!--</el-form-item>-->
                <!--<el-form-item prop="checkNewPass">-->
                    <!--<el-input type="password" placeholder="新密码确认" v-model="ruleForm.checkNewPass"></el-input>-->
                <!--</el-form-item>-->
                <!--<div class="editpwd-btn">-->
                    <!--<el-button @click="submitForm('ruleForm')">提交</el-button>-->
                    <!--<el-button @click="resetForm('ruleForm')">重置</el-button>-->
                <!--</div>-->
            <!--</el-form>-->
            <!--<div class="back"><a @click="back"-->
                                 <!--href="javascript:void(0)"><i-->
              <!--class="el-icon-d-arrow-left"></i>回到首页</a></div>-->
        <!--</div>-->
      <div class="editpassword_main">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              修改密码
            </h4>
          </div>
          <el-card>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm2" label-width="100px" class="demo-ruleForm">
              <el-form-item label="原密码" prop="oldPassword">
                <div class="edit_input_common">
                  <el-input type="password" v-model="ruleForm.oldPassword" auto-complete="off"></el-input>
                </div>
              </el-form-item>
              <el-form-item label="新密码" prop="newPassword">
                <div class="edit_input_common">
                  <el-input type="password" v-model="ruleForm.newPassword" auto-complete="off"></el-input>
                </div>
              </el-form-item>
              <el-form-item label="确认密码" prop="checkNewPass">
                <div class="edit_input_common">
                  <el-input type="password"
                    v-model.number="ruleForm.checkNewPass"></el-input>
                </div>
              </el-form-item>
              <el-form-item>
                <el-button type="danger"
                           @click="submitForm('ruleForm2')">提交
                </el-button>
                <el-button @click="resetForm('ruleForm2')">重置
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
    </div>
</template>

<script>
  import {fetchAPI} from '../../utils/utils';
export default {
  data: function () {
    return {
      ruleForm: {
        oldPassword: '',
        newPassword: '',
        checkNewPass: ''
      },
      rules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          {type: 'string', min: 8, message: '密码长度不能小于8位',
            trigger: 'blur'}
        ],
        checkNewPass: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          {type: 'string', min: 8, message: '密码长度不能小于8位',
            trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (this.ruleForm.newPassword !== this.ruleForm.checkNewPass) {
          this.$message({
            message: '两次密码不一致',
            type: 'error'
          });
          return false
        }
        if (valid) {
          const api = this.$store.state.NEW_API
          let PassData = {
            old_password: this.ruleForm.oldPassword,
            new_password: this.ruleForm.newPassword
          }
          fetchAPI('post',api + '/api/user/changpwd/',
            this.transformRequest(PassData),this).then(res => {
            if (res && res.status === 200) {
              this.$message({
                message: '密码修改成功',
                type: 'success'
              });
              this.ruleForm = {
                oldPassword: '',
                newPassword: '',
                checkNewPass: ''
              }
            }
          })
        } else {
          return false
        }
      })
    },
    back () {
      this.$router.push('/home')
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    transformRequest (data) {
      // Do whatever you want to transform the data
      let ret = ''
      for (let it in data) {
        ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      }
      return ret
    }
  }
}
</script>

<style scoped lang="scss" type="text/scss">
    .editpwd-wrap{
        position: relative;
        width:100%;
        height:100%;
    }
    .editpassword_main{
      padding: 20px 0px 0 10px;
    }
    .ms-title{
        position: absolute;
        top:50%;
        width:100%;
        margin-top: -230px;
        text-align: center;
        font-size:30px;
        color: #3fa88f;

    }
    .ms-editpwd{
        position: absolute;
        left:50%;
        top:50%;
        width:300px;
        height:200px;
        margin:-150px 0 0 -190px;
        padding:40px;
        border-radius: 5px;
        background: #6ebcaa;
    }
    .editpwd-btn{
        text-align: right;
    }
    .editpwd-btn button{
        width:20%;
        height:36px;
    }
    .back{
      text-align: left;
      font-size: 12px;
      color: #ffffff;
      a{
        color: #ffffff;
      }
    }
</style>
