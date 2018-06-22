/**
 * Created by olivia on 2017/7/26.
 */
export const fetchAPI = (type,url,data,self) => {
  if(type == 'post'){
    if(data){
      return self.$http.post(url,data).then((res) => {
        if(!res || (res.status != 201 && res.status != 200)){
          httpError(self,res,'then');
          return false
        }else{
          return res
        }
      }).catch((err) => {
        httpError(self,err,'catch');
        return err
      })
    }else{
      return self.$http.post(url).then((res) => {
        if(!res || (res.status != 201 && res.status != 200)){
          httpError(self,res,'then');
          return false
        }else{
          return res
        }
      }).catch((err) => {
        httpError(self,err,'catch');
        return err
      })
    }
  }else if(type == 'delete'){
    return self.$http.delete(url,data).then((res) => {
      if(!res || res.status != 204){
        httpError(self,res,'then');
        return false
      }else{
        return res
      }
    }).catch((err) => {
      httpError(self,err,'catch');
      return err
    })
  }else if(type == 'put'){
    return self.$http.put(url,data).then((res) => {
      if(!res || res.status != 200){
        httpError(self,res,'then');
        return false
      }else{
        return res
      }
    }).catch((err) => {
      httpError(self,err,'catch');
      return err
    })
  }else if(type == 'get'){
    return self.$http.get(url).then((res) => {
      if(!res || res.status != 200){
        httpError(self,res,'then');
        return false
      }else{
        return res
      }
    }).catch((err) => {
      httpError(self,err,'catch');
      return err
    })
  }
};
export const checCode = (rule, value, callback) => {
  if (!value) {
    return callback(new Error('该项为必填项'));
  }
  let reg = /^[a-zA-Z0-9_]{1,}$/;
  setTimeout(() => {
    if (!value.match(reg)) {
      callback(new Error('请输入数字、字母或下划线'));
    } else {
      callback();
    }
  }, 1000);
};
export const getFirstDayOfWeek = () => {
  let date = new Date();
  let day = date.getDay() || 7;
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1 - day);
};

export const httpError = (self,res,type)=>{
  // console.error('返回失败');
  if(type ==='then'){
    self.$message({
      message: "数据返回失败！",
      type: 'warning'
    })
  }else if(type ==='catch'){
    console.log(res)
    if(res.response.status >=500){
      self.$message({
        message: "服务器内部异常，请联系管理员！",
        type: 'error'
      });
    }else if (res.response && res.response.status === 400){
      self.$message({
        message: res.response.data.message,
        type: 'warning'
      });
    }else if(res.response && res.response.status === 401){
      self.$message({
        message: res.response.data.message,
        type: 'warning'
      });
      for (let i in $.cookie()) {
        $.removeCookie(i, {path: '/'});
        $.removeCookie(i);
      }
      self.$router.push('/Login')
    }
  }
}
