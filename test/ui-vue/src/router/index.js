import Vue from 'vue'
import Router from 'vue-router'
import routerBeforeEach from './before_each.js'
// 按需引入 （g-layout为打包后生成的文件夹）
const login = r => require.ensure([], () => r(require('@/views/login/login.vue')), 'g-login')
const layout = r => require.ensure([], () => r(require('@/views/layout/layout.vue')), 'g-main')
// const dashboard = r => require.ensure([], () => r(require('@/views/dashboard/index.vue')), 'g-main')
const repositories = r => require.ensure([], () => r(require('@/views/repositories.vue')), 'g-main')

const repository = r => require.ensure([], () => r(require('@/views/repository/index.vue')), 'g-main')
const repositoryInfo = r => require.ensure([], () => r(require('@/views/repository/info.vue')), 'g-main')
const repositoryTags = r => require.ensure([], () => r(require('@/views/repository/tags.vue')), 'g-main')
const repositorySetting = r => require.ensure([], () => r(require('@/views/repository/setting.vue')), 'g-main')

const project = r => require.ensure([], () => r(require('@/views/project/index.vue')), 'g-main')
const projectRepositories = r => require.ensure([], () => r(require('@/views/project/repositories.vue')), 'g-main')
const projectSetting = r => require.ensure([], () => r(require('@/views/project/setting.vue')), 'g-main')
const resetPassword = r => require.ensure([], () => r(require('@/views/login/reset_password.vue')), 'g-login')
const updateUser = r => require.ensure([], () => r(require('@/views/login/update_user.vue')), 'g-login')

const svgIcons = r => require.ensure([], () => r(require('@/views/svg-icons/index.vue')), 'g-main')

Vue.use(Router)
const routers = new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/reset_password',
      name: 'resetPassword',
      component: resetPassword
    },
    {
      path: '/updateuser',
      name: 'updateuser',
      component: updateUser
    },
    {
      path: '/',
      component: layout,
      redirect: 'repositories',
      children: [
        {
          name: 'repositories',
          path: 'repositories',
          component: repositories
        },
        {
          name: 'repository',
          path: 'repository/:namespace/:name',
          component: repository,
          children: [
            {
              name: 'repository_info',
              path: 'info',
              component: repositoryInfo
            },
            {
              name: 'repository_tags',
              path: 'tags',
              component: repositoryTags
            },
            {
              name: 'repository_setting',
              path: 'setting',
              component: repositorySetting
            }
          ]
        },
        {
          name: 'project',
          path: 'project/:namespace',
          component: project,
          children: [
            {
              name: 'project_repositories',
              path: 'repositories',
              component: projectRepositories
            },
            {
              name: 'project_setting',
              path: 'setting',
              component: projectSetting
            }
          ]
        },
        {
          name: 'svg_icons',
          path: 'svgicons',
          component: svgIcons
        }
      ]
    }
  ]
})
// 全局前置守卫
routerBeforeEach(routers)
export default routers
