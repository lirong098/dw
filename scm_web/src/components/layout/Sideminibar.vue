<template>
    <div :class="{sidebar:true,sideminibar:true,
        sideBarRed:sideBarColor == 'red',
        sideBarWhite:sideBarColor == 'white',
        sideBarBlack:sideBarColor == 'black',}">
      <div class="mini_logo"></div>
      <div class="mini_bar">
        <VuePerfectScrollbar class="scroll-area">
          <el-menu :default-active="onRoutes"
                   class="el-menu-vertical-demo"
                   @select="selectMenu"
                   unique-opened router>
            <el-menu-item-group index="profile">
              <!--<div class="group_title">首页</div>-->
              <!--<span slot="title">分组一</span>-->
              <el-menu-item index="profile">
                <el-tooltip class="item" effect="light"
                            content="个人信息"
                            placement="bottom-end">
                  <i
                    class="menu_icon icon icon24 icon_profile"></i>
                </el-tooltip>
              </el-menu-item>
              <el-menu-item index="editpassword">
                <el-tooltip class="item" effect="light"
                            content="修改密码"
                            placement="bottom-end">
                  <i class="menu_icon icon icon24 icon_editpassword"></i>
                </el-tooltip>
              </el-menu-item>
              <el-menu-item index="LoginOut">
                <el-tooltip class="item" effect="light"
                            content="退出登录"
                            placement="bottom-end">
                  <i class="menu_icon icon icon24 icon_Login"></i>
                </el-tooltip>
              </el-menu-item>
            </el-menu-item-group>
            <template v-for="item in items">
              <el-menu-item-group :index="item.index" v-if="item.subs">
                <div class="group_title">{{item.index ==
                'materailsmanage' ? '备料' : item.index ==
                  'forecaseorder' ? '预估' : item.index ==
                'basicmeta' ? '默认' : ''}}
                </div>
                <el-menu-item v-for="(subItem,i) in
                     item.subs" :key="i"
                              :index="subItem.index">
                  <el-tooltip class="item" effect="light"
                              :content="subItem.title"
                              placement="bottom-end">
                    <i
                      class="menu_icon icon icon24 icon_metas"
                      v-if="subItem.index == 'metas'"></i>
                    <i
                      class="menu_icon icon icon24 icon_productinfo"
                      v-else-if="subItem.index == 'productinfo'"></i>
                    <i
                      class="menu_icon icon icon24 icon_customermanage"
                      v-else-if="subItem.index == 'customermanage'"></i>
                    <i
                      class="menu_icon icon icon24 icon_materailsrule"
                      v-else-if="subItem.index == 'materailsrule'"></i>
                    <i
                      class="menu_icon icon icon24 icon_forecasesheet"
                      v-else-if="subItem.index == 'forecasesheet'"></i>
                    <i
                      class="menu_icon icon icon24 icon_orderimport"
                      v-else-if="subItem.index == 'orderimport'"></i>
                    <i
                      class="menu_icon icon icon24 icon_orderinput"
                      v-else-if="subItem.index == 'orderinput'"></i>
                    <i
                      class="menu_icon icon icon24 icon_materailsorder"
                      v-else-if="subItem.index == 'materailsorder'"></i>
                    <i
                      class="menu_icon icon icon24 icon_materailstype"
                      v-else-if="subItem.index == 'materailstype'"></i>
                    <i
                      class="menu_icon icon icon24 icon_importhistory"
                      v-else-if="subItem.index == 'importhistory'"></i>
                    <i
                      class="menu_icon icon icon24 icon_materailselect"
                      v-else-if="subItem.index == 'materailselect'"></i>
                    <i
                      class="menu_icon icon icon24 icon_realorder"
                      v-else-if="subItem.index == 'realorder'"></i>
                  </el-tooltip>
                </el-menu-item>
              </el-menu-item-group>
            </template>
          </el-menu>
        </VuePerfectScrollbar>
      </div>
    </div>
</template>

<script>
  import VuePerfectScrollbar from 'vue-perfect-scrollbar'
    export default {
      name:'v-sideminibar',
      data () {
        return {
          iconData:{metas:''},
          systems: '',
          items: '',
          value: '',
          activeName: 'moudle',
          input2: ''
        }
      },
      props:{
        sideBarColor:{
          type:String
        }
      },
      components: {
        VuePerfectScrollbar
      },
      computed: {
        onRoutes () {
          return this.$route.path.replace('/', '')
        }
      },
      methods: {
        selectMenu(index){

        },
        changBySubSysytem (subSystem) {
          // 选择子系统
          for (var obj in this.systems) {
            if (this.systems[obj].index === subSystem) {
              this.items = this.systems[obj].moudles
            }
          }
        },
        handleClick (tab, event) {

        },
        handleIconClick (ev) {

        },
        changeCollect (mouseEvent) {
          if (mouseEvent.srcElement.className === 'el-icon-star-off collect-icon') {
            // 收藏模块
            mouseEvent.srcElement.className = 'el-icon-star-on collect-icon'
          } else {
            // 取消收藏
            mouseEvent.srcElement.className = 'el-icon-star-off collect-icon'
          }
        },
        getMenuList () {
          const api = this.$store.state.DEV_API
          this.$http.get(api + '/api/menu/menulist/', {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
            if (res.status === 200) {
              this.systems = res.data
              this.items = res.data[0].moudles
              this.value = res.data[0].title
            }
          }).catch((err) => {

          })
        }
      },
      created () {
//        this.getMenuList()
      }
    }
</script>

<style scoped lang="scss" type="text/scss">
  .sidebar{
    display: block;
    position: absolute;
    width: 48px;
    left: 0;
    top: 0px;
    bottom:0;
    .group_title{
      padding:10px 0;
      text-align: center;
      border-bottom: 1px dashed #dedede;
      border-top: 1px dashed #dedede;
      &:first-child{
        border-top: none;
      }
    }
  }
  .sideBarWhite{
    background: #3b5998;
  }
  .sideBarBlack{
    background: #000;
  }
  .sideBarRed{
    background: #d50000;
  }
  .sideminibar{
    padding-top: 60px;
    .mini_logo{
      position: absolute;
      top:0;
      left:0;
      width:48px;
      height: 60px;
      background: url(/statics/img/huansi_logo4.png)
      no-repeat -25px 15px;
      border-bottom: 1px dashed #dedede;
    }
    .mini_bar{
      height: calc(100vh - 60px);
    }
  }
  .sidebar > ul {
    height:100%;
  }
  .select{
    position:fixed;
    bottom:0;
    width:178px;
    left:2px;
  }
  .el-icon-plus{
    right:0px;
  }
  .collect-icon{
    position:absolute;
    top:21px;
    right:0px;
  }
  .el-menu-item{
    &.is-active{
      .icon_metas{
        background: url("/statics/img/metas_active.svg");
      }
      .icon_customermanage{
        background: url("/statics/img/customermanage_active.svg");
      }
      .icon_materailsrule{
        background:
          url("/statics/img/materailsrule_active.svg");
      }
      .icon_productinfo{
        background: url("/statics/img/productinfo_active.svg");
      }
      .icon_forecasesheet{
        background: url("/statics/img/forecasesheet_active.svg");
      }
      .icon_orderimport{
        background: url("/statics/img/orderimport_active.svg");
      }
      .icon_orderinput{
        background: url("/statics/img/orderinput_active.svg");
      }
      .icon_materailsorder{
        background: url("/statics/img/materailsorder_active.svg");
      }
      .icon_materailstype{
        background: url("/statics/img/materailstype_active.svg");
      }
      .icon_importhistory{
        background: url("/statics/img/importhistory_active.svg");
      }
      .icon_materailselect{
        background: url(/statics/img/materailselect_active.svg);
      }
      .icon_profile{
        background: url(/statics/img/profile_active.svg);
      }
      .icon_editpassword{
        background: url(/statics/img/editpassword_active.svg);
      }
      .icon_Login{
        background: url(/statics/img/logout_active.svg);
      }
      .icon_realorder{
        background: url(/statics/img/realorder_active.svg);
      }
    }
  }
  .menu_icon{
    &.icon_metas{
      background: url("/statics/img/metas.svg");
    }
    &.icon_customermanage{
      background: url("/statics/img/customermanage.svg");
    }
    &.icon_materailsrule{
      background: url("/statics/img/materailsrule.svg");
    }
    &.icon_productinfo{
      background: url("/statics/img/productinfo.svg");
    }
    &.icon_forecasesheet{
      background: url("/statics/img/forecasesheet.svg");
    }
    &.icon_orderimport{
      background: url("/statics/img/orderimport.svg");
    }
    &.icon_orderinput{
      background: url("/statics/img/orderinput.svg");
    }
    &.icon_materailsorder{
      background: url("/statics/img/materailsorder.svg");
    }
    &.icon_materailstype{
      background: url("/statics/img/materailstype.svg");
    }
    &.icon_importhistory{
      background: url("/statics/img/importhistory.svg");
    }
    &.icon_materailselect{
      background: url(/statics/img/materailselect.svg);
    }
    &.icon_profile{
      background: url(/statics/img/profile.svg);
    }
    &.icon_editpassword{
      background: url(/statics/img/editpassword.svg);
    }
    &.icon_Login{
      background: url(/statics/img/logout.svg);
    }
    &.icon_realorder{
      background: url(/statics/img/realorder.svg);
    }
  }
  .eltabs{
    height: calc(100% - 36px);
  }
</style>
