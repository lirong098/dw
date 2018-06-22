import {service as request, apiObj, auth, proxy} from './request.js'
// import {axiosObj} from './axios_obj.js'
const login = {
  // 登录
  login (user) {
    console.log(user)
    return request({
      url: auth + '/login',
      method: 'post',
      data: user,
      transformRequest: [function (data) {
        let ret = ''
        for (let it in data) {
          ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
        }
        return ret
      }],
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
  },
  // 注册用户
  users (data) {
    return request({
      url: proxy + '/users',
      method: 'post',
      data: data
    })
  },
  // 获取邮箱验证码
  send (data) {
    return request({
      url: auth + '/send' + apiObj(data),
      method: 'get'
    })
  },
  // 验证用户，手机，邮箱是否已经存在
  userExists (data) {
    return request({
      url: auth + '/userExists',
      method: 'post',
      data: data,
      transformRequest: [function (data) {
        let ret = ''
        for (let it in data) {
          ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
        }
        return ret
      }],
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
  },
  // 公司规模
  companyScales () {
    return request({
      url: auth + '/company_scale '
    })
  },
  // 重置密码的邮箱
  sendEmail (data) {
    return request({
      url: auth + '/sendEmail' + apiObj(data)
    })
  },
  // 重置密码
  reset (data) {
    return request({
      url: auth + '/reset',
      method: 'post',
      data: data,
      transformRequest: [function (data) {
        let ret = ''
        for (let it in data) {
          ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
        }
        return ret
      }],
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
  },
  logOut () {
    return request({
      url: auth + '/log_out'
    })
  }
}
export default login
