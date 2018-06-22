<template>
  <div class="sidebar">
    <!--<el-menu :default-active="onRoutes"-->
    <!--class="el-menu-vertical-demo"-->
    <!--@select="selectMenu"-->
    <!--unique-opened router>-->
    <!--<el-input-->
    <!--placeholder="请输入名称检索"-->
    <!--icon="search"-->
    <!--v-model="input2"-->
    <!--:on-icon-click="handleIconClick">-->
    <!--</el-input>-->
    <!--<el-tabs v-model="activeName" @tab-click="handleClick" class="eltabs">-->
    <!--<el-tab-pane  label="模块" name="moudle">-->
    <!--<template v-for="item in items">-->
    <!--<el-menu-item-group :index="item.index" v-if="item.subs">-->
    <!--<template slot="title">-->
    <!--<el-icon class="el-icon-menu"></el-icon>-->
    <!--{{ item.title }}</template>-->
    <!--<el-menu-item v-for="(subItem,i) in-->
    <!--item.subs" :key="i"-->
    <!--:index="subItem.index">{{ subItem.title }}-->
    <!--<i class="el-icon-star-off collect-icon" @click="changeCollect"></i>-->
    <!--</el-menu-item>-->
    <!--</el-menu-item-group>-->
    <!--</template>-->
    <!--</el-tab-pane>-->
    <!--<el-tab-pane  label="收藏" name="collect">收藏</el-tab-pane>-->
    <!--</el-tabs>-->
    <!--<el-select class="select" v-model="value" @change="changBySubSysytem">-->
    <!--<el-option-->
    <!--v-for="item in systems"-->
    <!--:key="item.index"-->
    <!--:label="item.title"-->
    <!--:value="item.index">-->
    <!--</el-option>-->
    <!--</el-select>-->
    <!--</el-menu>-->

    <div class="logo">
      <div class="logo-normal">
        <a
          style="color:#d50000 "
          class="simple-text">1</a>
      </div>
      <div class="logo-img">
        <img src="/statics/img/huansi_logo4.png" alt="">
      </div>
    </div>
    <div class="sidebar-wrapper">
      <VuePerfectScrollbar class="scroll-area">
        <el-menu :default-active="onRoutes"
                 :default-openeds="defaultOpens"
                 :unique-opened="true"
                 router>
          <!--<el-menu-item index="dashboard"-->
                        <!--key="dashboard">-->
            <!--<div class="menu_child" style="margin-top: 10px;">-->
              <!--dashboard-->
            <!--</div>-->
          <!--</el-menu-item>-->
          <!--<el-submenu index="profile" key="profile"-->
          <!--class="profile-box">-->
          <!--<template slot="title">-->
          <!--&lt;!&ndash;<img src="/statics/img/avatar.jpg"&ndash;&gt;-->
          <!--&lt;!&ndash;alt="" class="portrait">&ndash;&gt;-->
          <!--<div class="profile-title">-->
          <!--{{'DASGBORARD'}}-->
          <!--</div>-->
          <!--</template>-->
          <!--<el-menu-item index="profile"-->
          <!--key="profile">-->
          <!--<div class="menu_child">-->
          <!--个人信息-->
          <!--</div>-->
          <!--</el-menu-item>-->
          <!--<el-menu-item index="editpassword"-->
          <!--key="editpassword">-->
          <!--<div class="menu_child">-->
          <!--修改密码-->
          <!--</div>-->
          <!--</el-menu-item>-->
          <!--<el-menu-item index="Login"-->
          <!--key="Login">-->
          <!--<div class="menu_child">-->
          <!--退出登录-->
          <!--</div>-->
          <!--</el-menu-item>-->
          <!--</el-submenu>-->
          <template v-for="(item,index) in items">
            <el-submenu :index="index+''" :key="index">
              <template slot="title">
                <i></i>
                {{item.title}}
              </template>
              <el-menu-item v-for="child in item.subs"
                            :index="child.index"
                            :key="child.index"
                            :class="{'is-active':onRoutes==child.index}">
                <div class="menu_child">
                  {{child.title}}
                  <div style="height: 42px; width: 22px; float: right">
                    <a @click.stop="" :target="child.index" :href="'#/'+child.index">
                      <i class="iconfont"
                         style="float: right; line-height: 45px; font-weight: 100; padding-right: 5px; z-index: 1;">
                        &#xe653;
                      </i>
                    </a>
                  </div>
                </div>
              </el-menu-item>
            </el-submenu>
          </template>
          <el-select class="select" v-model="value" @change="changBySubSysytem">
            <!--<router-link to="forecasesheet">-->
            <!--<el-option v-for="item in systems" :key="item.index" :label="item.title" :value="item.index"></el-option>-->
            <!--</router-link>-->
            <!--<router-link to="new_product">-->
            <el-option label="MRP" value="MRP"></el-option>
            <!--</router-link>-->
            <!--<router-link to="customer">-->
            <el-option label="FCST" value="FCST"></el-option>
            <!--</router-link>-->
          </el-select>
        </el-menu>
      </VuePerfectScrollbar>

    </div>
    <div
      :class="{sidebarBackground:true,
        sideBarRed:sideBarColor == 'red',
        sideBarWhite:sideBarColor == 'white',
        sideBarBlack:sideBarColor == 'black',
        sideBarImg1:sideBarBg && sideBarImg == 1,
        sideBarImg2:sideBarBg && sideBarImg == 2,
        sideBarImg3:sideBarBg && sideBarImg == 3,
        sideBarImg4:sideBarBg && sideBarImg == 4,
        }">
    </div>
  </div>
</template>

<script>
  import VuePerfectScrollbar from 'vue-perfect-scrollbar'

  export default {
    name: 'v-sidebar',
    data() {
      return {
        systems: '',
        items: '',
        value: '',
        activeName: '',
        input2: '',
        defaultOpens: ['1'],
        activeIndex: 'fcst_deal',
        isCreated: false
      }
    },
    props: {
      sideBarColor: {
        type: String
      },
      sideBarImg: {
        type: Number
      },
      sideBarBg: {
        type: Boolean
      }
    },
    components: {
      VuePerfectScrollbar
    },
    computed: {
      onRoutes() {
        return this.$route.path.replace('/', '')
      },
      username() {
        let username = this.$cookie.get('profile');
        return this.$store.state.userName || username;
      }
    },
    methods: {
      changBySubSysytem(subSystem) {
        console.log(this.value, 1);
        // 选择子系统
        if (subSystem == "MRP") {
          this.items = [
            {
              index: "model",
              subs: [
//                {
//                  index: "mrp_meta",
//                  title: "Meta"
//                },
                {
                  index: "new_product",
                  title: "成衣Model"
                },
                {
                  index: "new_fabric",
                  title: "面料Model"
                },
                {
                  index: "new_accessories",
                  title: "辅料Model"
                }
              ],
              title: "基础数据"
            },
            {
              index: "mrp",
              subs: [
                {
                  index: "bom_import",
                  title: "BOM导入"
                },
                {
                  index: "tailoring_bom",
                  title: "成衣BOM"
                },
                {
                  index: "mrp_stock_clothes",
                  title: "成衣需求"
                },
//                {
//                  index: "mrp_clothes_pr",
//                  title: "成衣备料"
//                },
//                {
//                  index: "mrp_clothes_order",
//                  title: "成衣实单"
//                },
                {
                  index: "stock_management",
                  title: "MRP备料"
                },
                {
                  index: "stock_inventory",
                  title: "备料查询"
                },
//                {
//                  index: "mrp_pr_order",
//                  title: "MRP实单"
//                }
              ],
              title: "MRP"
            }
//            {
//              index: "stock",
//              subs: [
//                {
//                  index: "mrp_manual_pr",
//                  title: "手工备料"
//                },
//                {
//                  index: "mrp_stocktake_in",
//                  title: "盘点入库"
//                },
//                {
//                  index: "mrp_stocktake_out",
//                  title: "盘点出库"
//                }
//              ],
//              title: "备料仓"
//            }
          ];
          this.defaultOpens = ["1"];
          if(!this.isCreated) {
            this.$router.push("mrp_stock_clothes")
          }
          return;
        } else if (subSystem === "FCST") {
          this.activeName = '预估处理'
          this.items = [{
            index: "model",
            subs: [
//              {
//                index: "fcst_meta",
//                title: "Meta"
//              },
              {
                index: "clothes_model",
                title: "成衣Model"
              },
              {
                index: "customer",
                title: "客户管理"
              }
            ],
            title: "基础数据"
          }, {
            index: "sampling",
            subs: [
              {
                index: "sampleUpload",
                title: "选样导入"
              },
              {
                index: "sample",
                title: "选样订单"
              },
              {
                index: "fcstSampleUpload",
                title: "实单导入"
              },
              {
                index: "fcst_sample_order",
                title: "选样实单"
              }
            ],
            title: "选样管理"
          }, {
            index: "fcst",
            subs: [
              {
                index: "fcst_import",
                title: "预估导入"
              },
              {
                index: "fcst_bill",
                title: "预估订单"
              },
              {
                index: "fcst_deal",
                title: "预估处理"
              },
              {
                index: "fcst_auto_pr",
                title: "智能备料"
              },
              {
                index: "fcst_order_import",
                title: "实单导入"
              },
              {
                index: "fcst_order",
                title: "预估实单"
              }
            ],
            title: "预估管理"
          }, {
            index: "stock",
            subs: [
              {
                index: "fcst_sample_pr",
                title: "选样备料"
              },
              {
                index: "fcst_pr",
                title: "预估备料"
              },
              {
                index: "fcst_manual_pr",
                title: "手工备料"
              },
              {
                index: "stock_pr",
                title: "备料库存"
              }
            ],
            title: "备料管理"
          }, {
            index: "da",
            subs: [{
              index: "fcst_diff",
              title: "预估差异"
            }, {
              index: "fcst_order_cover",
              title: "实单覆盖"
            }],
            title: "数据分析"
          }];
          this.defaultOpens = ["2"];
          if(!this.isCreated) {
            this.$router.push("fcst_deal")
          }
          return;
        }
//        this.defaultOpens = ["0"];
//        for (var obj in this.systems) {
//          console.log(obj, '22', this.systems);
//          if (this.systems[obj].index === subSystem) {
//            this.items = this.systems[obj].moudles
//          }
//        }
      },
      handleClick(tab, event) {

      },
      handleIconClick(ev) {

      },
      changeCollect(mouseEvent) {
        if (mouseEvent.srcElement.className === 'el-icon-star-off collect-icon') {
          // 收藏模块
          mouseEvent.srcElement.className = 'el-icon-star-on collect-icon'
        } else {
          // 取消收藏
          mouseEvent.srcElement.className = 'el-icon-star-off collect-icon'
        }
      },
      getMenuList() {
        const api = this.$store.state.DEV_API
        this.$http.get(api + '/api/menu/menulist/', {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(res => {
          if (res.status === 200) {
            console.log(res.data[0].moudles);
            this.systems = res.data;
            this.items = res.data[0].moudles;
            this.value = res.data[0].title;
          }
        }).catch((err) => {

        })
      }
    },
    created() {
      this.value = 'FCST';
      let mrppath = [
//        {
//          index: "/mrp_meta",
//          title: "Meta"
//        },
        {
          index: "/new_product",
          title: "成衣Model"
        },
        {
          index: "/new_fabric",
          title: "面料Model"
        },
        {
          index: "/new_accessories",
          title: "辅料Model"
        },
        {
          index: "/bom_import",
          title: "BOM导入"
        },
        {
          index: "/tailoring_bom",
          title: "成衣BOM"
        },
        {
          index: "/mrp_stock_clothes",
          title: "成衣需求"
        },
        {
          index: "/stock_management",
          title: "MRP备料"
        },
        {
          index: "/stock_inventory",
          title: "备料查询"
        },
      ];
      let fcstpath = [
        {
          index: "/fcst_meta",
          title: "Meta"
        },
        {
          index: "/clothes_model",
          title: "成衣Model"
        },
        {
          index: "/customer",
          title: "客户管理"
        },
        {
          index: "/sampleUpload",
          title: "选样导入"
        },
        {
          index: "/sample",
          title: "选样订单"
        },
        {
          index: "/fcstSampleUpload",
          title: "实单导入"
        },
        {
          index: "/fcst_sample_order",
          title: "选样实单"
        },
        {
          index: "/fcst_import",
          title: "预估导入"
        },
        {
          index: "/fcst_bill",
          title: "预估订单"
        },
        {
          index: "/fcst_deal",
          title: "预估处理"
        },
        {
          index: "/fcst_auto_pr",
          title: "智能备料"
        },
        {
          index: "/fcst_order_import",
          title: "实单导入"
        },
        {
          index: "/fcst_order",
          title: "预估实单"
        },{
          index: "/fcst_sample_pr",
          title: "选样备料"
        },
        {
          index: "/fcst_pr",
          title: "预估备料"
        },
        {
          index: "/fcst_manual_pr",
          title: "手工备料"
        },
        {
          index: "/stock_pr",
          title: "备料库存"
        },
        {
          index: "/fcst_diff",
          title: "预估差异"
        },
        {
          index: "/fcst_order_cover",
          title: "实单覆盖"
        }
      ];
//      mrppath.forEach(function (item,index) {
//        if(this.$router.currentRoute.path === item.index){
//
//        }
//        console.log(index)
//      });
      for(let i=0; i<mrppath.length;i++){
        if(this.$router.currentRoute.path === mrppath[i].index){
          this.value = 'MRP';
          break
        }
//        console.log(mrppath[i].index)
      }

      for(let i=0; i<mrppath.length;i++){
        if(this.$router.currentRoute.path === fcstpath[i].index){
          this.value = 'FCST';
          break
        }
//        console.log(mrppath[i].index)
      }

      this.isCreated = true
      this.changBySubSysytem(this.value)
      this.isCreated = false
//      this.getMenuList()
    }
  }
</script>

<style scoped lang="scss" type="text/scss">
  .sidebar {
    display: block;
    position: absolute;
    /*width: 260px;*/
    width: 200px;
    left: 0;
    z-index: 1;
    top: 0px;
    bottom: 0;
    background-color: #fff;
    box-shadow: 0 10px 30px -12px rgba(0, 0, 0, 0.42), 0 4px 25px 0px rgba(0, 0, 0, 0.12), 0 8px 10px -5px rgba(0, 0, 0, 0.2);
    .logo {
      padding: 15px 0px;
      /*width: 260px;*/
      width: 200px;
      margin: 0;
      display: block;
      position: relative;
      z-index: 4;
      border-bottom: 1px solid rgba(255, 255, 255, 0.3);
      .simple-text {
        text-transform: uppercase;
        padding: 5px 0px;
        display: block;
        font-size: 18px;
        color: #3C4858;
        text-align: center;
        white-space: nowrap;
        font-weight: 400;
        line-height: 30px;
        overflow: hidden;
        color: #fff;
      }
      .logo-img {
        max-height: 42px;
        img {
          top: 16px;
          /*left: 15px;*/
          left: -10px;
          position: absolute;
        }
      }
    }
  }

  .sidebar-wrapper {
    .profile-box {
      border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    }
    .profile-title {
      /*padding-left: 40px;*/
      padding-left: 0px;
    }
    .portrait {
      width: 34px;
      height: 34px;
      position: absolute;
      top: 11px;
      border-radius: 50%;
    }
  }

  .sidebar-wrapper {
    position: relative;
    height: calc(100vh - 100px);
    overflow: auto;
    width: 200px;
    z-index: 4;
  }

  .sidebar > ul {
    height: 100%;
  }

  .menu_child {
    padding-left: 40px;
    transition: all .5s ease-in-out;
  }

  .menu_child:hover {
    a {
      display: block;
    }
  }

  .select {
    position: fixed;
    bottom: 0;
    width: 200px;
    left: 0px;
  }

  .el-select-dropdown {
    left: 0px;
  }

  .el-icon-plus {
    right: 0px;
  }

  .collect-icon {
    position: absolute;
    top: 21px;
    right: 0px;
  }

  .eltabs {
    height: calc(100% - 36px);
  }

  .sidebarBackground {
    position: absolute;
    z-index: 1;
    height: 100%;
    width: 100%;
    display: block;
    top: 0;
    left: 0;
    background-size: cover;
    background-position: center center;
  }

  .sideBarImg1 {
    background-image: url("/statics/img/sidebar-1.jpg");
  }

  .sideBarImg2 {
    background-image: url("/statics/img/sidebar-2.jpg");
  }

  .sideBarImg3 {
    background-image: url("/statics/img/sidebar-3.jpg");
  }

  .sideBarImg4 {
    background-image: url("/statics/img/sidebar-4.jpg");
  }

  .sidebar .sidebarBackground:after {
    opacity: .8;
  }

  .sidebar .sideBarWhite:after {
    background: #3b5998;
  }

  .sidebar .sideBarBlack:after {
    background: #000;
  }

  .sidebar .sideBarRed:after {
    background: #d50000;
  }

  .sidebar .sidebarBackground:after {
    position: absolute;
    z-index: 3;
    width: 100%;
    height: 100%;
    content: "";
    display: block;
  }

  a:link, a:visited {
    color: #cccccc;
    text-decoration: underline;
  }

  a {
    display: none;
  }

  a:hover, a:active {
    color: #cccccc;
    text-decoration: none;
  }

  .menu_child {
    color: #fff;
  }

  .element.style {
    left: 0px;
  }

  .el-menu-item.is-active {
    color: #3C4858;
  }

  .iconfont {
    font-family: "iconfont" !important;
    font-size: 16px;
    font-style: normal;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
