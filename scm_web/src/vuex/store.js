import Vue from 'vue'
import Vuex from 'vuex'
import search from './modules/search'
import state from './state'
import mutations from './mutations';

Vue.use(Vuex)
const debug = process.env.NODE_ENV !== 'production'
export default new Vuex.Store({
  state,
  mutations,
  modules: {
    search
  },
  strict: debug
})
