<template>
    <div class="wrapper">
      <!--<v-head :sideBarColor="sideBarColor"></v-head>-->
      <div :class="{header_box:true,clearfix:true,left:toggleMenu}">
        <div class="toggle-box fl" @click="toggleToMenu">
          <i :class="toggleMenu ? 'icon icon24 icon_left'
          : 'icon icon24 icon_right'
"></i>
        </div>
        <div class="menu-title fl">
          {{routeName}}
        </div>
        <!--<div class="fr we_title">-->
          <!--欢迎使用预估系统-->
        <!--</div>-->
        <div class="user-info">
          <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                  <img class="user-logo"
                       src="/statics/img/avatar.jpg">
                <!--{{username}}-->
              </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="btn" style="padding: 0;">
                <div class="fixed-plugin">
                  <el-popover
                    ref="popover2"
                    placement="left"
                    width="290"
                    trigger="click">
                    <ul class="popover-fixed-plugin clearfix">
                      <li class="header-title">侧边栏背景</li>
                      <li class="adjustments-line">
                        <a href="javascript:void(0)" class="switchTrigger background-color">
                          <div class="text-center">
                  <span
                    @click="changeBg('white')"
                    :class="{badge:true,filter:true,badgeWhite:true,active:sideBarColor == 'white'}
                    "></span>
                            <span
                              @click="changeBg('black')"
                              :class="{badge:true,filter:true,badgeBlack:true,active:sideBarColor == 'black'}
                  "></span>
                            <span
                              @click="changeBg('red')"
                              :class="{badge:true,filter:true,badgeRed:true,active:sideBarColor == 'red'}
                    "></span>
                          </div>
                          <div class="clearfix"></div>
                          <div class="ripple-container"></div>
                        </a>
                      </li>
                      <li class="adjustments-line">
                        <a href="javascript:void(0)" class="switchTrigger">
                          <p>Mini 侧边栏</p>
                          <div class="togglebutton switch-sidebar-mini">
                            <el-switch
                              v-model="miniSideBar"
                              :width="35"
                              on-text=""
                              @change="toggleToMenu"
                              off-text="">
                            </el-switch>
                          </div>
                          <div class="clearfix"></div>
                          <div class="ripple-container"></div>
                        </a>
                      </li>
                      <li class="adjustments-line">
                        <a href="javascript:void(0)" class="switchTrigger">
                          <p>侧边栏背景</p>
                          <div class="togglebutton switch-sidebar-mini">
                            <el-switch
                              :width="35"
                              v-model="sideBarBg"
                              on-text=""
                              off-text="">
                            </el-switch>
                          </div>
                          <div class="clearfix"></div>
                          <div class="ripple-container"></div>
                        </a>
                      </li>
                      <li class="header-title">
                        背景图
                      </li>
                      <li :class="{bg_img:true,active:sideBarImg ==
             1}">
                        <a href="javascript:void(0)"
                           class="imgHolder switchTrigger"
                           @click="changeImg(1)">
                          <img src="/statics/img/sidebar-1.jpg"
                               alt="">
                        </a>
                      </li>
                      <li :class="{bg_img:true,active:sideBarImg ==
             2}">
                        <a href="javascript:void(0)"
                           class="imgHolder switchTrigger"
                           @click="changeImg(2)">
                          <img src="/statics/img/sidebar-2.jpg"
                               alt="">
                        </a>
                      </li>
                      <li :class="{bg_img:true,active:sideBarImg ==
             3}">
                        <a href="javascript:void(0)"
                           class="imgHolder switchTrigger"
                           @click="changeImg(3)">
                          <img src="/statics/img/sidebar-3.jpg"
                               alt="">
                        </a>
                      </li>
                      <li :class="{bg_img:true,active:sideBarImg ==
             4}">
                        <a href="javascript:void(0)"
                           class="imgHolder switchTrigger"
                           @click="changeImg(4)">
                          <img src="/statics/img/sidebar-4.jpg"
                               alt="">
                        </a>
                      </li>
                    </ul>
                  </el-popover>
                  <span class="icon_sidebar_set"
                     v-popover:popover2>个性设置</span>
                </div>
              </el-dropdown-item>
              <el-dropdown-item command="meta" style="padding: 0;">
                <div class="fixed-plugin">
                  <span class="icon_sidebar_set">Meta</span>
                </div>
              </el-dropdown-item>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="editpassword">修改密码</el-dropdown-item>
              <el-dropdown-item command="loginout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
      <!--<div class="fixed-plugin">-->
        <!--<el-popover-->
          <!--ref="popover2"-->
          <!--placement="left"-->
          <!--width="290"-->
          <!--trigger="click">-->
          <!--<ul class="popover-fixed-plugin clearfix">-->
            <!--<li class="header-title">侧边栏背景</li>-->
            <!--<li class="adjustments-line">-->
              <!--<a href="javascript:void(0)" class="switchTrigger background-color">-->
                <!--<div class="text-center">-->
                  <!--<span-->
                    <!--@click="changeBg('white')"-->
                    <!--:class="{badge:true,filter:true,badgeWhite:true,active:sideBarColor == 'white'}-->
                    <!--"></span>-->
                  <!--<span-->
                    <!--@click="changeBg('black')"-->
                    <!--:class="{badge:true,filter:true,badgeBlack:true,active:sideBarColor == 'black'}-->
                  <!--"></span>-->
                  <!--<span-->
                    <!--@click="changeBg('red')"-->
                    <!--:class="{badge:true,filter:true,badgeRed:true,active:sideBarColor == 'red'}-->
                    <!--"></span>-->
                <!--</div>-->
                <!--<div class="clearfix"></div>-->
                <!--<div class="ripple-container"></div>-->
              <!--</a>-->
            <!--</li>-->
            <!--<li class="adjustments-line">-->
              <!--<a href="javascript:void(0)" class="switchTrigger">-->
                <!--<p>Mini 侧边栏</p>-->
                <!--<div class="togglebutton switch-sidebar-mini">-->
                  <!--<el-switch-->
                    <!--v-model="miniSideBar"-->
                    <!--:width="35"-->
                    <!--on-text=""-->
                    <!--@change="toggleToMenu"-->
                    <!--off-text="">-->
                  <!--</el-switch>-->
                <!--</div>-->
                <!--<div class="clearfix"></div>-->
                <!--<div class="ripple-container"></div>-->
              <!--</a>-->
            <!--</li>-->
            <!--<li class="adjustments-line">-->
              <!--<a href="javascript:void(0)" class="switchTrigger">-->
                <!--<p>侧边栏背景</p>-->
                <!--<div class="togglebutton switch-sidebar-mini">-->
                  <!--<el-switch-->
                    <!--:width="35"-->
                    <!--v-model="sideBarBg"-->
                    <!--on-text=""-->
                    <!--off-text="">-->
                  <!--</el-switch>-->
                <!--</div>-->
                <!--<div class="clearfix"></div>-->
                <!--<div class="ripple-container"></div>-->
              <!--</a>-->
            <!--</li>-->
            <!--<li class="header-title">-->
              <!--背景图-->
            <!--</li>-->
            <!--<li :class="{bg_img:true,active:sideBarImg ==-->
             <!--1}">-->
              <!--<a href="javascript:void(0)"-->
                 <!--class="imgHolder switchTrigger"-->
                 <!--@click="changeImg(1)">-->
                <!--<img src="/statics/img/sidebar-1.jpg"-->
                     <!--alt="">-->
              <!--</a>-->
            <!--</li>-->
            <!--<li :class="{bg_img:true,active:sideBarImg ==-->
             <!--2}">-->
              <!--<a href="javascript:void(0)"-->
                 <!--class="imgHolder switchTrigger"-->
                 <!--@click="changeImg(2)">-->
                <!--<img src="/statics/img/sidebar-2.jpg"-->
                     <!--alt="">-->
              <!--</a>-->
            <!--</li>-->
            <!--<li :class="{bg_img:true,active:sideBarImg ==-->
             <!--3}">-->
              <!--<a href="javascript:void(0)"-->
                 <!--class="imgHolder switchTrigger"-->
                 <!--@click="changeImg(3)">-->
                <!--<img src="/statics/img/sidebar-3.jpg"-->
                     <!--alt="">-->
              <!--</a>-->
            <!--</li>-->
            <!--<li :class="{bg_img:true,active:sideBarImg ==-->
             <!--4}">-->
              <!--<a href="javascript:void(0)"-->
                 <!--class="imgHolder switchTrigger"-->
                 <!--@click="changeImg(4)">-->
                <!--<img src="/statics/img/sidebar-4.jpg"-->
                     <!--alt="">-->
              <!--</a>-->
            <!--</li>-->
          <!--</ul>-->
        <!--</el-popover>-->
        <!--<i class="icon icon28 icon_sidebar_set"-->
           <!--v-popover:popover2></i>-->
      <!--</div>-->
      <transition name="fade">
        <v-sideminibar v-show="toggleMenu" :sideBarColor="sideBarColor"></v-sideminibar>
      </transition>
      <!--<v-sideminibar v-if="toggleMenu"></v-sideminibar>-->
      <transition name="fade">
        <v-sidebar v-show="!toggleMenu"
                   :sideBarColor="sideBarColor"
                   :sideBarImg="sideBarImg" :sideBarBg="sideBarBg"
        ></v-sidebar>
      </transition>
      <div :class="{content:true,toggleContent:toggleMenu}">
        <transition name="move" >
          <router-view></router-view>
        </transition>
      </div>
    </div>
</template>

<script>
//    import vHead from './Header.vue';
    import vSidebar from './Sidebar.vue';
    import vSideminibar from './Sideminibar.vue';
    export default {
      name:'home',
      components: {
//        vHead,
        vSidebar,
        vSideminibar
      },
      data:function () {
        return{
          sideBarColor:'red',
          miniSideBar:false,
          sideBarBg:true,
          sideBarImg:1
        }
      },
      computed: {
        toggleMenu(){
          return this.$store.state.toggleMenu;
        },
        routeName(){
            return this.$route.name
        }
      },
      methods:{
        toggleToMenu:function () {
          this.$store.commit('TOGGLE_MENU',!this.$store.state.toggleMenu)
        },
        changeBg:function (type) {
          this.sideBarColor = type;
        },
        changeImg:function (type) {
          this.sideBarImg = type;
        },
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
          if (command === 'meta') {
            this.$router.push('/mrp_meta')
          }
        }
      }
    }
</script>
<style  scoped lang="scss" type="text/scss">
  .fixed-plugin{
    /*position: fixed;*/
    /*top:120px;*/
    /*right:0;*/
    width: 100%;
    /*background-color: #fff;*/
    /*border-radius: 8px 0 0 8px;*/
    /*text-align: center;*/
    /*z-index: 1031;*/
    /*.icon28{*/
      /*width: 28px;*/
      /*height: 28px;*/
    /*}*/
    .icon_sidebar_set{
      /*background: url(/statics/img/sidebar_set.svg)*/
      /*no-repeat center;*/
      /*padding: 10px;*/
      display: inline-block;
      width: 100%;
      padding: 0 10px;
    }
  }
  .popover-fixed-plugin{
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    li{
      display: block;
      padding: 5px 2px;
      float: left;
      position: relative;
    }
    .header-title {
      height: 30px;
      line-height: 25px;
      font-size: 12px;
      font-weight: 600;
      text-align: center;
      text-transform: uppercase;
      width: 100%;
      min-height: inherit;
    }
    a{
      transition: all .34s;
      -webkit-transition: all .34s;
      -moz-transition: all .34s;
      font-size: 13px;
      padding: 10px 20px;
      display: block;
      clear: both;
      font-weight: 400;
      line-height: 1.42857143;
      color:#333;
      white-space: nowrap;
    }
    .adjustments-line{
      width: 100%;
      height: 50px;
      min-height: inherit;
      a{
        padding-right: 0;
        padding-left: 0;
        border-bottom: 1px solid #ddd;
        border-radius: 0;
        margin: 0;
      }
      p {
        float: left;
        display: inline-block;
        margin-bottom: 0;
        font-size: 1em;
        color: #3C4858;
      }
      .togglebutton {
        float: right;
        user-select: none;
        vertical-align: middle;
      }
    }
    .text-center{
      text-align: center;
    }
    .badge {
      border: 3px solid #FFFFFF;
      border-radius: 50%;
      cursor: pointer;
      display: inline-block;
      height: 23px;
      margin-right: 5px;
      position: relative;
      width: 23px;
      transition: all .34s;
      -webkit-transition: all .34s;
      -moz-transition: all .34s;
      min-width: 10px;
      padding: 3px 7px;
      font-size: 12px;
      font-weight: 700;
      line-height: 1;
      color: #fff;
      text-align: center;
      white-space: nowrap;
      vertical-align: middle;
      box-sizing: border-box;
    }
    .badgeWhite {
      background-color: rgba(59,89,152, 1);
    }
    .badgeBlack {
      background-color: #000;
    }
    .badgeRed {
      background-color: #f44336;
    }
    .badge.active, .badge:hover {
      border-color: #00bbff;
    }
    .ripple-container {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
      width: 100%;
      height: 100%;
      overflow: hidden;
      border-radius: inherit;
      pointer-events: none;
    }
    .bg_img{
      margin: 0 5px;
      width: 20%;
    }
    .imgHolder {
      font-size: 16px;
      text-align: center;
      border-radius: 10px;
      background-color: #FFF;
      border: 3px solid #FFF;
      opacity: 1;
      cursor: pointer;
      max-height: 100px;
      overflow: hidden;
      padding: 0;
      box-sizing: border-box;
      img{
        margin-top: auto;
        border-radius: 0;
        width: 100%;
        height: 100px;
        margin: 0 auto;
        vertical-align: middle;
        border: 0;
        box-sizing: border-box;
      }
    }
    .active > a.imgHolder {
      border-color: #00bbff;
      background-color: #FFFFFF;
    }
  }
  .toggleContent{
    left: 48px;
  }
  .header_box{
    position: absolute;
    width: calc(100% - 260px);
    /*padding-top: 10px;*/
    z-index: 1029;
    /*left: 260px;*/
    left: 200px;
    padding-left: 20px;
    &.left{
      left: 30px;
      width: calc(100% - 30px);
    }
    .toggle-box{
      width: 40px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      background-color: #fff;
      border-radius: 50%;
      color: #999;
      box-shadow: 0 2px 2px 0 rgba(153, 153, 153, 0.14), 0 3px 1px -2px rgba(153, 153, 153, 0.2), 0 1px 5px 0 rgba(153, 153, 153, 0.12);
      .icon_left{
        background: url("/statics/img/icon_left.svg")
        no-repeat center;
      }
      .icon_right{
        background-image: url("/statics/img/icon_right.svg");
      }
    }
    .menu-title{
      height: 25px;
      padding: 10px 15px;
      font-size: 18px;
      color: #aaa;
    }
    .we_title{
      font-size: 14px;
      height: 25px;
      padding: 20px 50px 5px 10px;
    }
  }

  .user-info {
    float: right;
    height: 45px;
    padding-right: 55px;
    font-size: 16px;
    color: #fff;
  }

  .user-info .el-dropdown{
    height: 50px;
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
    left: -25px;
    top: -6px;
    float: left;
    width:40px;
    height:40px;
    border-radius: 50%;
  }

</style>
