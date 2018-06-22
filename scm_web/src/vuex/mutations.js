/**
 * Created by olivia on 2017/7/18.
 */
import * as types from './mutations-types'
export default {
  [types.SET_USER_NAME] (state, userName) {
    state.userName = userName;
  },
  [types.TOGGLE_MENU] (state, flag) {
    state.toggleMenu = flag
  }
}
