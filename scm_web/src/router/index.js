import Login from '../components/Account/Login.vue';
import Home from '../components/layout/Home.vue';
import Main from '../components/Main.vue';
// import OrderList from '../components/pages/OrderList.vue'
// import OrderForm from '../components/pages/OrderForm.vue'
// import MetaList from '../components/pages/MetaList.vue'
// import EitePassword from '../components/pages/EitePassword.vue'
// import ForecaseSheet from '../components/pages/ForecaseSheet.vue'
// import CustomerManage from '../components/pages/CustomerManage.vue'
// import Profile from '../components/pages/Profile.vue'
import NotFound from '../components/Error/NotFound.vue'
import Metas from '../components/BasicMeta/metas.vue';
import Customermanage from '../components/BasicMeta/customerManage.vue';
import Productinfo from '../components/BasicMeta/productInfo.vue';
import forecaseSheet from '../components/ForecaseOrder/forecaseSheet.vue';
import orderImport from '../components/ForecaseOrder/orderImport.vue';
import orderInput from '../components/ForecaseOrder/orderInput.vue';
import materailsOrder from '../components/MaterailsManage/materailsOrder.vue';
import materailsSelect from '../components/MaterailsManage/materailsSelect.vue';
import MaterailsRule from '../components/BasicMeta/materailsRule.vue';
import MaterailsType from '../components/BasicMeta/materailsType.vue';
import Bom from '../components/mrp/bom/bom.vue'

const routes = [
  // {
  //   path: '/',
  //   redirect:'/forecasesheet'
  // },
  {
    path: '/',
    redirect: '/fcst_deal'
  },
  {
    path: '/erplogin',
    name:'系统登录',
    component: resolve => require(['../components/common/erplogin/erplogin.vue'], resolve)
  },
  {
    path: '/login',
    name: '登录',
    component: resolve => require(['../components/Account/Login.vue'], resolve)
  },
  {
    path: '/loginOut',
    component: resolve => require(['../components/Account/Login.vue'], resolve)
  },
  {
    path: '/home',
    component: resolve => require(['../components/layout/Home.vue'], resolve),
    children: [
      {
        path: '/',
        component: resolve => require(['../components/fcst/fcst_deal/fcst_deal.vue'], resolve)
        // component: resolve => require(['../components/ForecaseOrder/dashboard.vue'], resolve)
        // component: resolve => require(['../components/fcst/sampling/sampleUpload.vue'], resolve)
      },
      { // NewMrp_成衣需求
        path: '/mrp_stock_clothes',
        name: '成衣需求',
        component: resolve => require(['../components/mrp/mrp_stock/mrp_stock_parent_component.vue'], resolve) // product
      },
      // { // 新增bom页面的路由
      //   path: '/bom',
      //   name: 'BOM',
      //   component: resolve => require(['../components/mrp/bom/bom.vue'], resolve) // Bom
      // },
      /*MRP路由*/
      { // 新增成衣BOM页面的路由
        path: '/tailoring_bom_detailed',
        name: '成衣BOM详情',
        component: resolve => require(['../components/mrp/tailoringbom/tailoring_bom_detailed.vue'], resolve) // product
      },
      { // 新增成衣BOM页面的路由
        path: '/tailoring_bom',
        name: '成衣BOM',
        component: resolve => require(['../components/mrp/tailoringbom/tailoring_bom.vue'], resolve) // product
      },
      { // 新增备料管理页面的路由
        path: '/bom_import',
        name: 'BOM导入',
        component: resolve => require(['../components/mrp/bom_import/bom_import.vue'], resolve)
      },
      { // 新增备料管理页面的路由
        path: '/stock_management',
        name: 'MRP备料',
        component: resolve => require(['../components/mrp/mrp/mrp_pr.vue'], resolve)
      },
      { // MRP实单页面的路由
        path: '/mrp_pr_order',
        name: 'MRP实单',
        component: resolve => require(['../components/mrp/mrp/mrp_pr_order.vue'], resolve)
      },
      { // 手工备料页面的路由
        path: '/mrp_manual_pr',
        name: '手工备料',
        component: resolve => require(['../components/mrp/pr/mrp_manual_pr.vue'], resolve)
      },
      { // 盘点入库页面的路由
        path: '/mrp_stocktake_in',
        name: '盘点入库',
        component: resolve => require(['../components/mrp/pr/mrp_stocktake_in.vue'], resolve)
      },
      { // 盘点出库页面的路由
        path: '/mrp_stocktake_out',
        name: '盘点出库',
        component: resolve => require(['../components/mrp/pr/mrp_stocktake_out.vue'], resolve)
      },
      { // 新增成衣页面的路由
        path: '/new_product',
        name: '成衣',
        component: resolve => require(['../components/mrp/basic/new_product.vue'], resolve) // product
      },
      { // 新增面料页面的路由
        path: '/new_fabric',
        name: '面料',
        component: resolve => require(['../components/mrp/basic/new_fabric.vue'], resolve) // fabric
      },
      { // 新增辅料页面的路由
        path: '/new_accessories',
        name: '辅料',
        component: resolve => require(['../components/mrp/basic/new_accessories.vue'], resolve) // accessories
      },
      { // 成衣备料的路由
        path: '/mrp_clothes_pr',
        name: '成衣备料',
        component: resolve => require(['../components/mrp/stock/mrp_clothes_pr.vue'], resolve) // accessories
      },
      { // 成衣实单的路由
        path: '/mrp_clothes_order',
        name: '成衣实单',
        component: resolve => require(['../components/mrp/stock/mrp_clothes_order.vue'], resolve) // accessories
      },
      { // MRP备料库存的路由
        path: '/stock_inventory',
        name: '备料库存',
        component: resolve => require(['../components/mrp/mrp_stock_inventory/stock_inventory.vue'], resolve) // accessories
      },
      { // MRP_meta的路由
        path: '/mrp_meta',
        name: 'Meta',
        component: resolve => require(['../components/common/meta/meta.vue'], resolve)
      },


      /*FCST 路由*/
      { // 新增客户管理页面的路由
        path: '/customer',
        name: '客户管理',
        component: resolve => require(['../components/fcst/basic/customer/customer.vue'], resolve)
      },
      { // fcst_meta的路由
        path: '/fcst_meta',
        name: 'Meta',
        component: resolve => require(['../components/common/meta/meta.vue'], resolve)
      },
      { // clothes_model的路由
        path: '/clothes_model',
        name: '成衣Model',
        component: resolve => require(['../components/fcst/basic/model/clothes_model.vue'], resolve) // accessories
      },

      { // 新增fcst备料库存页面的路由
        path: '/stock_pr',
        name: '备料库存',
        component: resolve => require(['../components/fcst/stock_pr/stock_pr.vue'], resolve)
      },
      {
        path: "/fcst_sample_pr",
        name: "选样备料",
        component: resolve => require(['../components/fcst/stock_pr/fcst_sample_pr.vue'], resolve)
      },
      {
        path: "/fcst_pr",
        name: "预估备料",
        component: resolve => require(['../components/fcst/stock_pr/fcst_pr.vue'], resolve)
      },
      {
        path: "/fcst_manual_pr",
        name: "手工备料",
        component: resolve => require(['../components/fcst/stock_pr/fcst_manual_pr.vue'], resolve)
      },

      {
        path: "/sampleUpload",
        name: "选样导入",
        component: resolve => require(['../components/fcst/sampling/sampleUpload.vue'], resolve)
      },
      {
        path: "/fcstSampleUpload",
        name: "实单导入",
        component: resolve => require(['../components/fcst/sampling/fcstSampleUpload.vue'], resolve)
      },
      // {
      //   path: "/fcst_order",
      //   name: "选样实单",
      //   component: resolve => require(['../components/fcst/sampling/fcst_order.vue'], resolve)
      // },
      {
        path: "/fcst_sample_order",
        name: "选样实单",
        component: resolve => require(['../components/fcst/sampling/fcst_sample_order.vue'], resolve)
      },
      {
        path: "/fcst_import",
        name: "预估导入",
        component: resolve => require(['../components/fcst/fcst/fcst_import.vue'], resolve)
      },
      {
        path: "/fcst_bill",
        name: "预估订单",
        component: resolve => require(['../components/fcst/fcst/fcst_bill.vue'], resolve)
      },
      {
        path: "/fcst_order_import",
        name: "实单导入",
        component: resolve => require(['../components/fcst/fcst/fcst_order_import.vue'], resolve)
      },
      {
        path: "/fcst_order",
        name: "预估实单",
        component: resolve => require(['../components/fcst/fcst/fcst_order.vue'], resolve)
      },
      {//预估差异
        path: "/fcst_diff",
        name: "预估差异",
        component: resolve => require(['../components/fcst/da/fcst_diff.vue'], resolve)
      },
      {
        path: "/fcst_auto_pr",
        name: "智能备料",
        component: resolve => require(['../components/fcst/fcst_auto_pr/fcst_auto_pr.vue'], resolve)
      },
      {
        path: "/fcst_deal",
        name: "预估处理",
        component: resolve => require(['../components/fcst/fcst_deal/fcst_deal.vue'], resolve)
      },
      {
        path: "/sample",
        name: "选样订单",
        component: resolve => require(['../components/fcst/sampling/sample_list.vue'], resolve)
      },
      {
        path: "/fcst_order_cover",
        name: "实单覆盖",
        component: resolve => require(['../components/fcst/fcst_order_cover/fcst_order_cover.vue'], resolve)
      },

      // 欢迎页
      {
        path: "/dashboard",
        name: "Dashboard",
        component: resolve => require(['../components/ForecaseOrder/dashboard.vue'], resolve)
      },
      /*原路由*/
      {
        path: '/metas',
        name: '默认配置',
        component: resolve => require(['../components/BasicMeta/metas.vue'], resolve),
      },
      {
        path: '/productinfo',
        name: 'Model',
        component: resolve => require(['../components/BasicMeta/productInfo.vue'], resolve),
      },
      {
        path: '/customermanage',
        name: '客户管理',
        component: resolve => require(['../components/BasicMeta/customerManage.vue'], resolve)
      },
      {
        path: '/materailsrule',
        name: '备料策略',
        component: resolve => require(['../components/BasicMeta/materailsRule.vue'], resolve)
      },
      {
        path: '/materailstype',
        name: '物料类型',
        component: resolve => require(['../components/BasicMeta/materailsType.vue'], resolve)
      },
      {
        path: '/forecasesheet',
        name: '预估处理',
        component: resolve => require(['../components/ForecaseOrder/forecaseSheet.vue'], resolve)
      },
      {
        path: '/orderimport',
        name: '预估导入',
        component: resolve => require(['../components/ForecaseOrder/orderImport.vue'], resolve)
      },
      {
        path: '/importhistory',
        name: '导入历史',
        component: resolve => require(['../components/ForecaseOrder/importHistory.vue'], resolve)
      },
      {
        path: '/orderinput',
        name: '预估录入',
        component: resolve => require(['../components/ForecaseOrder/orderInput.vue'], resolve)
      },
      {
        path: '/materailsorder',
        name: '备料录入',
        component: resolve => require(['../components/MaterailsManage/materailsOrder.vue'], resolve)
      },
      {
        path: '/realorder',
        component: resolve => require(['../components/MaterailsManage/realOrder.vue'], resolve),
        name: '实单录入'
      },
      {
        path: '/materailselect',
        component: resolve => require(['../components/MaterailsManage/materailsSelect.vue'], resolve),
        name: '备料统计'
      }, {
        path: '/editpassword',
        component: resolve => require(['../components/Account/EitePassword.vue'], resolve),
        name: '修改密码'
      },
      {
        path: '/profile',
        component: resolve => require(['../components/Account/Profile.vue'], resolve),
        name: '个人信息'
      },
    ]
  },
  {
    path: '*',
    component: resolve => require(['../components/Error/NotFound.vue'], resolve),
    name: '404'
  }
]

export default routes
