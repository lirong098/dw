export const returnMessage = (message,type,self)=>{
  self.$message({
    showClose: true,
    message: message,
    type: type
  });
};

export const commonmethod = (model)=>{
  if(model.model_id){
    let keyArr = ['model_code','model_name'];
    let tempArr = [];
    for(let i in keyArr){
      if(model[keyArr[i]])
        tempArr.push(model[keyArr[i]]);
    }
    model.spec.color?tempArr.push(model.spec.color):'';
    return tempArr.join(' - ')
  }
  if(model.item_id){
    let keyArr = ['item_code','item_name'];
    let tempArr = [];
    for(let i in keyArr)
    {
      if(model[keyArr[i]])
        tempArr.push(model[keyArr[i]]);
    }
    return tempArr.join(' - ');
  }
};

// 日期转周
export const getYearWeek = (date) => {
  let date2=new Date(date.getFullYear(), 0, 1);
  let day1=date.getDay();
  if(day1===0) day1=7;
  let day2=date2.getDay();
  if(day2===0) day2=7;
  let d = Math.round((date.getTime() - date2.getTime()+(day2-day1)*(24*60*60*1000)) / 86400000);
  return Math.floor(d /7);
};

// 周转日期方法
export const getweekdate = (date) => {
  let tDate = new Date();
  let day = (function () {
    let tYear = Number(date.substring(0, 4));
    let tWeek = Number(date.substring(4));
    tDate = new Date(((tWeek + 1) * 7 + (tYear - 1970) * 365) * 24 * 60 * 60 * 1000);
    let day = tDate.getDay();
    return (day == 0) ? 7 : day;
  })();

  let monday = new Date(tDate.getTime() - (day) * 24 * 60 * 60 * 1000);
  if((monday.getMonth()+1) === 12 && (monday.getDate()+1) > 31) {
    return (monday.getFullYear() + 1) + '-1-1';
  }
  console.log(monday.getFullYear()+'-'+(monday.getMonth()+1)+'-'+(monday.getDate()+1));
  return monday.getFullYear() + '-' + (monday.getMonth() + 1) + '-' + (monday.getDate() + 1);
};


export const keydown = (num,divname) => {
  document.onkeydown = function(e) {
    var e = window.event || e;
    var ele;
    var len;
    var lenShow = 0;
    var eleShow = []; //存显示出来input的数组
    var keyCode = e.keyCode;
    if(keyCode !== 40 && keyCode !== 39 && keyCode !== 38 && keyCode !== 37) return;
    if(divname === 'table'){
      ele = document.querySelectorAll('.table input[type=text]');
    }else if(divname === 'tableOrder'){
      ele = document.querySelectorAll('.tableOrder input[type=text]');
    }
    len = ele.length;
    for(var i = 0; i < len; i++) {
      /*过滤掉display为none的元素*/
      if(ele[i].style.display !== 'none' && ele[i].placeholder !== '选择周' && ele[i].placeholder !== '选择日期') {
        eleShow.push(ele[i]);
      }
    }
    // eleShow.splice(0,1);
    lenShow = eleShow.length;
    for(var i = 0; i < lenShow; i++) {
      if(document.activeElement === eleShow[i]) {
        if(e.keyCode === 37 && e.ctrlKey){
          e.preventDefault();
          if((i-1)<0){
            break;
          }
          eleShow[(i - 1)].focus();
          break;
        }
        if(e.keyCode === 39 && e.ctrlKey){
          e.preventDefault();
          if((i+1)>=lenShow){
            break;
          }
          eleShow[(i + 1)].focus();
          break;
        }
        switch(keyCode) {
          case 40:
            e.preventDefault();
            if((i+num)>=lenShow){
              break;
            }
            eleShow[(i + num)].focus();
            break;
          case 38:
            e.preventDefault();
            if((i-num)<0){
              break
            }
            eleShow[(i - num)].focus();
            break;
        }
        //取余从第一个开始
        break;
      }
    }
  }
};
