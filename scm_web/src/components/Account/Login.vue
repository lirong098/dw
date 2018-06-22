<template>
  <div class="login-wrap">
    <!--<div class="ms-title">-->
      <!--<div class="app_logo">-->
        <!--<img src="/statics/img/huansi_logo.png" alt="hscc">-->
      <!--</div>-->
    <!--</div>-->
    <!--<div class="ms-login">-->
        <!--<el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm">-->
            <!--<el-form-item prop="username">-->
                <!--<el-input v-model="ruleForm.username" placeholder="username"></el-input>-->
            <!--</el-form-item>-->
            <!--<el-form-item prop="password">-->
                <!--<el-input type="password" placeholder="password" v-model="ruleForm.password" @keyup.enter.native="submitForm('ruleForm')"></el-input>-->
            <!--</el-form-item>-->
            <!--<div class="login-btn">-->
                <!--<el-button type="primary" @click="submitForm('ruleForm')">-->
                  <!--<span v-if="!logining">登录</span>-->
                  <!--<span v-else>登录中...</span>-->
                <!--</el-button>-->
            <!--</div>-->
            <!--<div class="back" @click="goToAdmin">-->
              <!--管理员入口-->
              <!--<i-->
              <!--class="el-icon-d-arrow-right"></i>-->
            <!--</div>-->
        <!--</el-form>-->
    <!--</div>-->
    <div class="logo">
      <img
        src="/statics/img/huansi_logo4.png" alt="">
    </div>
    <div class="admin_box" @click="goToAdmin">
      <div>
        管理员入口
      </div>
    </div>
    <div class="full-page login-page">
      <div class="contents">
        <div class="container clearfix">
          <div class="row clearfix">
            <div
              class="col-md-4 col-sm-6 col-md-offset-4 col-sm-offset-3 box_size">
              <!--<form>-->
                <div class="card card-login">
                  <!--<div class="card-header text-center">-->
                    <!--<h4 class="card-title">-->
                      <!--Login-->
                    <!--</h4>-->
                  <!--</div>-->
                  <!--<p class="category text-center">-->
                  <!--</p>-->
                  <div class="card-content" style="margin-top:30px;">
                    <div class="input-group">
                      <span class="input-group-addon">
                          <i
                            class="icon icon24 icon_person"></i>
                      </span>
                      <div class="form-group label-floating is-empty">
                        <input type="text"
                               v-model="ruleForm.username"
                               @keydown.enter="submitForm"
                               class="form-control"
                               placeholder="用户名">
                        <span class="material-input"></span></div>
                    </div>
                    <div class="input-group">
                      <span class="input-group-addon">
                          <i class="icon icon24 icon_password"></i>
                      </span>
                      <div class="form-group label-floating is-empty">
                        <input type="password"
                               v-model="ruleForm.password"
                               @keydown.enter="submitForm"
                               class="form-control" placeholder="密码">
                        <span class="material-input"></span></div>
                    </div>
                  </div>
                  <div class="footer text-center">
                    <button
                            class="btn btn-rose btn-simple btn-wd btn-lg" @click="submitForm">登录</button>
                  </div>
                </div>
              <!--</form>-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../utils/utils';
export default {
  data: function () {
    return {
      logining: false,
      ruleForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm () {
      const self = this;
      if(!this.ruleForm.username){
        this.$message({
          message: '请输入用户名',
          type: 'error'
        });
      }else if(!this.ruleForm.password){
        this.$message({
          message: '请输入密码',
          type: 'error'
        });
      }else{
        this.logining = true
        this.toLogin()
        this.logining = false
      }
    },
    toLogin () {
      const api = this.$store.state.NEW_API;
      let loginData = {
        username: this.ruleForm.username,
        password: this.ruleForm.password
      }
      fetchAPI('post',api +
        '/api/user/login/',this.transformRequest(loginData),this).then((res) => {
        if (res && res.status === 200) {
          this.$cookie.set('profile', loginData.username,1);
          this.$cookie.set('orderType', 1212,1);
          this.$store.commit('SET_USER_NAME',loginData.username);
          this.$router.push('/fcst_deal');
//          this.$router.push('/sampleUpload');

        }
      });
    },
    transformRequest (data) {
      let ret = '';
      for (let it in data) {
        ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      }
      return ret
    },
    goToAdmin:function () {
      window.location.href = '/admin';
    }
  }
}
</script>
<style scoped lang="scss" type="text/scss">
    .login-wrap{
      position: relative;
      top:0;
      height: auto;
      min-height: 100vh;
      transform: translate3d(0px, 0, 0);
      transition: all 0.33s cubic-bezier(0.685, 0.0473, 0.346, 1);
      left: 0;
      .logo{
        position: absolute;
        top:25px;
        left: 0;
        z-index: 5;
      }
      .admin_box{
        position: absolute;
        top:25px;
        right:20px;
        color:#fff;
        z-index: 5;
        font-size: 12px;
        cursor: pointer;
      }
      input:-webkit-autofill {
        -webkit-text-fill-color: #000 !important;
        transition: background-color 50000s ease-in-out
        0s ;
      }
      input,button{
        outline:none;
      }
      .full-page{
        background: url('/statics/img/login_bg.jpeg') no-repeat center center;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
        height: 100%;
        &:before{
          display: block;
          content: "";
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          z-index: 2;
          background-color: rgba(0, 0, 0, 0.5);
        }
        &:after{
          display: block;
          content: "";
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          z-index: 2;
          opacity: .8;
        }
        .contents{
          padding-top: 18vh;
          min-height: calc(100vh - 80px);
          position: relative;
          z-index: 4;
        }
        @media (min-width: 768px){
          .container {
            width: 750px;
          }
        }
        @media (min-width: 992px){
          .container {
            width: 970px;
          }
        }
        .container {
          padding-right: 15px;
          padding-left: 15px;
          margin-right: auto;
          margin-left: auto;
          box-sizing: border-box;
        }
        @media (min-width: 1200px){
          .container {
            width: 1170px;
          }
        }
        .box_size{
          box-sizing: border-box;
        }
        .row {
          margin-right: -15px;
          margin-left: -15px;
        }
        @media (min-width: 992px){
          .col-md-4{
            float: left;
          }
        }
        @media (min-width: 768px){
          .col-sm-offset-3 {
            margin-left: 25%;
          }
          .col-sm-6 {
            width: 50%;
            float: left;
          }
        }
        @media (min-width:992px) {
          .col-md-offset-4{
            margin-left: 33.3%;
          }
          .col-md-4 {
            width: 33.33333333%;
          }
        }
        .col-sm-6{
          position: relative;
          min-height: 1px;
          padding-right: 15px;
          padding-left: 15px;
        }
        .card-login {
          box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.14);
          border-radius: 6px;
          padding-bottom: 20px;
          -webkit-transform: translate3d(0, 0, 0);
          -moz-transform: translate3d(0, 0, 0);
          -o-transform: translate3d(0, 0, 0);
          -ms-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
          webkit-transition: all 300ms linear;
          -moz-transition: all 300ms linear;
          -o-transition: all 300ms linear;
          -ms-transition: all 300ms linear;
          transition: all 300ms linear;
          color: #fff;

          &.card {
            display: inline-block;
            position: relative;
            width: 100%;
            margin: 25px 0;
            color: rgba(0,0,0, 0.87);
            background: #fff;
            box-shadow: 0 10px 30px -12px rgba(0, 0, 0, 0.42), 0 4px 25px 0px rgba(0, 0, 0, 0.12), 0 8px 10px -5px rgba(0, 0, 0, 0.2);

          }
          .card-header {
            margin: -20px 15px 0;
            border-radius: 3px;
            position: relative;
            margin-top: -40px;
            margin-bottom: 20px;
            z-index: 3;
            background: linear-gradient(60deg, #ec407a, #d81b60);
            display: block;
            .card-title {
              text-decoration: none;
              color: #FFFFFF;
              margin-top: 10px;
              margin-bottom: 10px;
              font-weight: 700;
              font-size: 1.3rem;
            }
          }
          .text-center {
            text-align: center;
          }
          .card-content {
            padding: 0px 30px 0px 10px;
            position: relative;
            box-sizing: border-box;
          }
          .input-group {
            position: relative;
            display: table;
            border-collapse: separate;
          }
          .input-group .form-control:not(:first-child):not(:last-child), .input-group-addon:not(:first-child):not(:last-child), .input-group-btn:not(:first-child):not(:last-child) {
            border-radius: 0;
          }
          .input-group-addon {
            padding: 6px 12px;
            font-size: 14px;
            font-weight: 400;
            line-height: 1;
            color: #555;
            text-align: center;
            border-radius: 4px;
            width: 1%;
            white-space: nowrap;
            vertical-align: middle;
            display: table-cell;
            border-top-right-radius: 0;
            border-bottom-right-radius: 0;
            border: 0;
            background: transparent;
            padding: 6px 15px 0px;
            .icon_person{
              background: url('/statics/img/child.svg')
              no-repeat center center;
            }
            .icon_password{
              background: url('/statics/img/password.svg')
              no-repeat center center;
            }
          }
          .form-group {
            padding-bottom: 10px;
            margin: 20px 0 0 0;
            position: relative;
            &.label-floating label.control-label, .form-group.label-placeholder label.control-label {
              top: -7px;
              font-size: 14px;
              line-height: 1.42857;
              will-change: left, top, contents;
              position: absolute;
              pointer-events: none;
              transition: 0.3s ease all;
              color: #AAAAAA;
              font-weight: 400;
              margin: 16px 0 0 0;
            }
            .form-control {
              border: 0;
              background-image: linear-gradient(#9c27b0,
                #9c27b0), linear-gradient(#D2D2D2,
                #D2D2D2) ;
              background-size: 0 2px, 100% 1px;
              background-repeat: no-repeat;
              background-position: center bottom, center calc(100% - 1px);
              background-color: transparent;
              float: none;
              box-shadow: none;
              font-weight: 400;
              display: table-cell;
              position: relative;
              z-index: 2;
              width: 100%;
              margin-bottom: 0;
              height: 36px;
              padding: 7px 0;
              font-size: 14px;
              line-height: 1.42857;
              color:#555;
              box-sizing: border-box;
            }
          }

        }
        .footer{
          color: #fff;
          .btn-wd {
            min-width: 180px;
            background-color: transparent;
            color: #e91e63;
            box-shadow: none;
            font-size: 14px;
            padding: 18px 36px;
            border: none;
            border-radius: 3px;
            position: relative;
            margin: 10px 1px;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 0;
            will-change: box-shadow, transform;
            transition: box-shadow 0.2s cubic-bezier(0.4, 0, 1, 1), background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            line-height: 1.3333333;
            display: inline-block;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            -ms-touch-action: manipulation;
            touch-action: manipulation;
            cursor: pointer;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            background-image: none;
          }
        }
      }
    }
</style>
