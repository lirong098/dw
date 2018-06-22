const state = {
  messages: 0
}

// mutations
const mutations = {
  'add': function (state, msg) {
    state.messages += msg
  }
}

const actions = {
  'add': function (store, param) {
    store.commit('add', param)
  }
}

export default {
  state,
  mutations,
  actions
}
