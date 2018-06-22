<template>
  <div :class="{header:true,
        sideBarRed:sideBarColor == 'red',
        sideBarWhite:sideBarColor == 'white',
        sideBarBlack:sideBarColor == 'black'}">
  <!--<div class="app_logo">-->
        <!--<img src="/statics/img/huansi_logo4.png" alt="hscc">-->
      <!--</div>-->
      <!--<div class="logo">后台管理系统</div>-->
      <!--<div class="split_icon_content" @click="toggleMenu">-->
        <!--<i class="split_icon icon24 icon"></i>-->
      <!--</div>-->
      <div class="user-info">
          <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                  <img class="user-logo"
                       src="/statics/img/person_yellow.png">
                  <!--{{username}}-->
              </span>
              <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="editpassword">修改密码</el-dropdown-item>
                  <el-dropdown-item command="loginout">退出</el-dropdown-item>
              </el-dropdown-menu>
          </el-dropdown>
      </div>
    </div>
</template>

<script>
    export default {
      name:'v-head',
      props:{
        sideBarColor:{
          type:String
        }
      },
      data () {
        return {
          name: ''
        }
      },
      computed: {
        username () {
          let username = this.$cookie.get('profile')
          if (username) {
            return username
          } else {
            return this.name
          }
        }
      },
      methods: {
        handleCommand (command) {
          if (command === 'loginout') {
            const api = this.$store.state.NEW_API;
            this.$http.get(api + '/api/user/logout/?user/login/').then(res => {
              if (res && res.status === 200) {
                this.$cookie.delete('profile');
                this.$router.push('/login');
              }
            })
          }
          if (command === 'editpassword') {
            this.$router.push('/editpassword')
          }
          if (command === 'profile') {
            this.$router.push('/profile')
          }
        },
        toggleMenu:function () {
          this.$store.commit('TOGGLE_MENU',!this.$store.state.toggleMenu)
        }
      }
    }
</script>

<style scoped lang="scss" type="text/scss">
    .header {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 70px;
        font-size: 18px;
        line-height: 80px;
        color: #fff;
        background-color: #20a0ff;
    }
    .header .logo{
      float: left;
      padding-left: 65px;
      font-size: 14px;
        /*width:250px;*/
        /*text-align: center;*/
    }
    .app_logo{
      position: absolute;
      height: 36px;
      top:12px;
      left: 25px;
      img{
        height: 36px;
        width: 180px;
      }
    }
    .split_icon_content{
      position: absolute;
      top:0;
      left:230px;
      border-left: 1px solid hsla(62,77%,76%,.3);
      .split_icon{
        background: url("/statics/img/split_screen.svg");
        &:hover, &.active {
          background-color: rgba(0, 0, 0, 0.25);
          border-radius: 2px;
        }
      }
    }
    .user-info {
        float: right;
        height: 70px;
        padding-right: 55px;
        font-size: 16px;
        color: #fff;
    }

    .user-info .el-dropdown{
      height: 70px;
    }

    .user-info .el-dropdown-link{
        position: relative;
        display: inline-block;
        /*padding-left: 35px;*/
        padding-left: 50px;
        color: #fff;
        cursor: pointer;
        vertical-align: middle;
    }
    .user-info .user-logo{
        position: absolute;
        left:0;
        /*top:10px;*/
        top:-25px;
        width:36px;
        height:40px;
        border-radius: 50%;
    }
    .el-dropdown-menu__item{
        text-align: center;
    }

    .sideBarWhite{
      background: #3b5998;
      opacity: 0.7;
    }
    .sideBarBlack{
      background: #000;
      opacity: 0.7;
    }
    .sideBarRed{
      background: #d50000;
      opacity: 0.7;
    }

</style>
