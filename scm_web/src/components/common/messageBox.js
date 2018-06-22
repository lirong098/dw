let showModal ={
  /*模态弹窗参数
      * content: String,//提示的内容
      * title: String,//提示的标题
      * showCancel:String, //是否显示取消按钮
      * cancelText:String,//取消按钮的文字，默认为"取消"
      * confirmText:String,//确定按钮的文字，默认为"确定"
      * type:String,//消息类型
      * confirmFun:Fuction,//确定按钮执行的函数
      * cancelFun:Fuction, //取消按钮执行的函数
      * */
  showModal(that,confirmFun="",cancelFun="",content="确定要执行此操作吗？", title="提示", confirmText="确定", cancelText="取消", type="warning") {
    that.$confirm(content, title, {
      confirmButtonText: confirmText,
      cancelButtonText: cancelText,
      type: type
    }).then(() => {
      typeof confirmFun =="function" && confirmFun(that);
      //this.showMessage("success", "操作成功");
    }).catch(() => {
      typeof cancelFun =="function" && cancelFun();
      //this.showMessage("info", "操作失败");
    });
  },
  /* 消息提醒
  * type:string,//消息类型
  * text:string//消息提示内容*/
  showMessage(that,type, text) {
    that.$message({
      type: type,
      message: text
    });
  }
};
module.exports = showModal;
