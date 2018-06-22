import {fetchAPI} from '../../utils/utils';
/*
* 处理时间格式
* val：有值则返回相应的日期  没有值则 返回当前日期
* 返回值：格式 yyyy-mm-dd
*/
function formatDate(val = '') {
  let date = new Date(val);
  if (val === '' || !val) {
    date = new Date();
  }
  return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
}
function getWeekNumber(src) {
  const date = new Date(src);
  date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  const week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week 1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}
function _fetchAPI(type,url, data,self) {
  return fetchAPI(type,url, data,self).then((res) => {
    return res
  }).catch((err) => {
    return err
  })
}
/*
* 获取客户信息
* self:作用域
*/
function getCustomerList(self) {
  const url = self.$store.state.NEW_API+"/api/customer/customers/?all=1";
  return _fetchAPI('get',url, null,self)
}
/*
* 获取Meta数据
* self：作用域
* val:unit/unit09/fcst...
* parameter:默认parent_meta_code 当是all时 val 必须为 1 number
* 参数说明：parent_meta_code{基础元类：0（默认），单位：unit，model：unit09，成衣备料：fcst，mrp备料：mrp，备料方式：36}*/
function getMetaList(self,val,parameter='parent_meta_code') {
  const url = self.$store.state.NEW_API+"/api/mat_models/metas/?"+parameter+"="+val;
  return _fetchAPI('get',url, null,self)
}

/*网络请求 生成内部唯一编码标识
  * self,作用的当前实例对象
  * type,{成衣：1，面料：2，辅料：3，bom：bom，item:item，备料：fcst,mrp备料：mrp}*/
function make_unique_no(self,type){
  const url = self.$store.state.NEW_API+"/api/mat_models/make_unique_no/"
  return _fetchAPI('post',url, {type:type},self)
}
//保留两位小数
//功能：将浮点数四舍五入，取小数点后2位
function fomatFloat(src,pos=2){
  return Math.round(src*Math.pow(10, pos))/Math.pow(10, pos);
}
module.exports = {
  formatDate: formatDate,
  getCustomerList:getCustomerList,
  getMetaList:getMetaList,
  make_unique_no:make_unique_no,
  fomatFloat:fomatFloat,
  getWeekNumber:getWeekNumber
}
