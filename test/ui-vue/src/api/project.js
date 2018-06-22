import {service as request, apiObj, proxy} from './request.js'
// import {axiosObj} from './axios_obj.js'
const project = {
  // 获取项目列表
  projects (type = 'get', data = {}) {
    return request({
      url: proxy + '/projects/',
      method: type,
      data: data
    })
  },
  // 获取全部镜像列表
  repositories (search) {
    return request({
      url: proxy + '/repositories' + apiObj(search)
    })
  },
  // 仓库详情、系统信息
  systeminfo () {
    return request({
      url: proxy + '/systeminfo'
    })
  },
  // 镜像的标签
  tags (name, search = {}) {
    return request({
      url: proxy + '/repositories/' + name + '/tags' + apiObj(search)
    })
  },
  // 获取镜像信息
  getRepository (name) {
    return request({
      url: proxy + '/repositories/' + name
    })
  },
  // 修改镜像
  repository (name, data) {
    return request({
      url: proxy + '/repositories/' + name,
      method: 'put',
      data: data
    })
  },
  delRepository (name) {
    return request({
      url: proxy + '/repositories/' + name,
      method: 'delete'
    })
  }
}
export default project
