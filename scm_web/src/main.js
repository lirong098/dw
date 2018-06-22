// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router';
import routes from './router'
import axios from 'axios'
import store from './vuex/store'
// import {sync} from 'vuex-router-sync'
import ElementUI from 'element-ui'
import VueCookie from 'vue-cookie'


Vue.config.productionTip = false
// 路由
Vue.use(VueRouter);
const router = new VueRouter({
  routes: routes,
  // mode: 'history', // localhost:8080/Login 方式的路由会和后端路由冲突
  scrollBehavior: function (to, from, savedPosition) {
    return savedPosition || {x: 0, y: 0}
  }
})
import LazyRender from 'vue-lazy-render'
Vue.use(LazyRender)
// import 'element-ui/lib/theme-default/index.css'    // 默认主题
// import '../statics/css/theme-green/index.css'       // 浅绿色主题
import '../statics/css/theme-pink/index.css'       // 枚红色主题
Vue.use(VueCookie)
Vue.use(ElementUI)
axios.defaults.withCredentials = true
Vue.prototype.$http = axios

router.beforeEach((to, from, next) => {
  document.title = to.name ? to.name : 'HSCC';
  let profile = $.cookie('profile');
  if (to.path !== '/Login') {
    if(to.path === '/LoginOut' && profile){
      for (let i in $.cookie()) {
        $.removeCookie(i, {path: '/'});
        $.removeCookie(i);
      }
      next()
    }else if(to.path === '/erplogin'){
      next()
    }else{
      if (profile) {
        next()
      } else {
        next({
          path: '/Login'
        })
      }
    }
  } else {
    if(profile){
      next({
        // path:'/forecasesheet'
        path:'/fcst_deal'
      })
    }else{
      next()
    }
  }
})
router.afterEach((to, from, next) => {

});
import dwDatePicker from './components/common/datepicker/datepicker.vue'
import {keydown} from "./components/common/component.js";
Vue.prototype.keydown = keydown;
Vue.component('dw-date-picker', dwDatePicker)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
