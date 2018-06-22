import store from '@/store'

export default function routerBeforeEach (router) {
  router.beforeEach((to, from, next) => {
    console.log('to', to)
    document.title = to.name ? to.name : 'DouWa'
    console.log(store.state.user.username, store.state.user.username && store.state.user.username !== '')
    let profile = store.state.user.username && store.state.user.username !== ''
    if (to.path === '/login') {
      next()
      return
    }
    if (to.path === '/reset_password') {
      next()
      return
    }
    if (to.path === '/updateuser') {
      next()
      return
    }
    if (to.path === '/logout') {
      if (profile) {
        store.commit('SET_USERNAME', '')
      }
      next({
        path: '/login'
      })
      return
    }
    if (!profile) {
      next({
        path: '/login'
      })
      return
    }
    next()
  })
  router.afterEach(() => {})
}
