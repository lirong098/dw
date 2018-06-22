/**
 * Created by liRong on 18/02/27.
 */

export function isvalidUsername (str) {
  const validMap = ['admin', 'editor']
  return validMap.indexOf(str.trim()) >= 0
}

/**
 * 合法uri
 * @param  {[type]} textval [description]
 * @return {[type]}         [description]
 */
// remove by hellwen.wu element支持url验证
/*
export function validateURL (textval) {
  const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return urlregex.test(textval)
}
*/

/**
 * 小写字母
 */
export function validateLowerCase (str) {
  const reg = /[a-z]/
  return reg.test(str)
}

/**
 * 大写字母
 */
export function validateUpperCase (str) {
  const reg = /[A-Z]/
  return reg.test(str)
}

/**
 * 大小写字母加数字
 */
export function validatAlphabets (str) {
  const reg = /[0-9]/
  return reg.test(str)
}

/**
 * validate email
 * @param email
 * @returns {boolean}
 */
// remove by hellwen.wu element支持email验证
/*
 export function validateEmail (email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(email)
}
*/

/*
*格式化时间
*return {Y-M-D}
 */
export function formatDate (val = '') {
  let date = new Date(val)
  if (val === '' || !val) {
    date = new Date()
  }
  return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
}
