<template>
  <div class="test_main_contain" v-loading.fullscreen.lock="fullscreenLoading" :element-loading-text="loadingText">
    <el-alert
      v-show="errorData.length > 0 "
      title="点击查看错误提示的文案"
      type="error"
      @close="alertClose">
  </el-alert>
    <div class="test_main_main">
      <div class="test_main_main_card">
        <el-upload class="upload-demo"
                   drag
                   action=""
                   :show-file-list="false"
                   :http-request="uploadFile">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            将文件拖到此处，或
            <em>点击上传</em>
          </div>
          <div class="el-upload__tip">只能上传Excel文件</div>
          <div class="el-upload__tip" v-if="file_type === 2">
            文件名的命名规范:{{fileImport(importType)}}
          </div>
        </el-upload>
      </div>

      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>{{listName}}</h4>
          </div>
          <el-card>
            <el-table ref="multipleTable"
                      :data="tableData"
                      border
                      tooltip-effect="dark"
                      style="width: 100%">
              <el-table-column v-for="(item,index) in tableColumn"
                               :prop="item.columnProp"
                               :label="item.columnName"
                               :key="index"
                               show-overflow-tooltip>
              </el-table-column>
              <!--<el-table-column label="操作" width="150" style="position: relative;border:5px solid blue;">-->
              <!--<template scope="scope">-->
              <!--<el-button size="small" @click="addCheckTab(scope.$index, scope.row)">查看</el-button>-->
              <!--</template>-->
              <!--</el-table-column>-->
            </el-table>
            <div class="pagination clearfix" style="line-height: 32px;">
              <div class="total fl">共 <b>{{pagedatacount}}</b> 条数据</div>
              <div class="pagination_tool fr">
                <el-pagination
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :current-page="currentPage"
                  :page-sizes="[10, 20, 50, 100]"
                  :page-size="pagesize"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="pagedatacount">
                </el-pagination>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
    <el-dialog title="文件导入错误" :visible.sync="errorShow" size="small" @close="closeDialog">
      <el-table :data="errorData"
                            border
                            tooltip-effect="dark">
        <el-table-column type="index" label="序号" width="70"></el-table-column>
        <el-table-column label="错误提示" prop="error"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';

  export default {
    name: 'sampleUpload_list',
    props: {
      TABSValue: String,
      tabIndex: Number,
      importType: Number
    },
    data() {
      return {
        tableData: [],//表格数据
        tableColumn: [],//表格列字段
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        listName: "导入记录",
        modelName: "", //查询值
        fullscreenLoading: false, //loding显示
        loadingText: "",//loding文字
        file_type: this.importType,
        errorData:[], //错误提示数据
        errorShow:false //错误弹窗显示参数
      }
    },
    methods: {
      //文件上传前
      beforeUpload: function (file) {
        let name = file.file.name.replace(/.+\./, "");
        let nameType = this.file_type === 2 ? 'xlsx' : 'xls';
        if (name != nameType) {
          this.$message({
            message: '不支持该文件类型',
            type: 'warning'
          });
          return false;
        } else {
          this.fullscreenLoading = true;
          this.loadingText = file.file.name + '正在上传，请稍后';
          return true;
        }
      },
      //文件上传
      uploadFile: function (uploadFile) {
        let self = this;
        if(!self.beforeUpload(uploadFile)) return;
        let file = uploadFile.file;
        let reader = new FileReader();
        reader.readAsBinaryString(file);
        reader.onloadend = function () {
          if (reader.error) {
            console.log(reader.error);
          } else {
            self.uploadAndSubmit(file, reader.result);
          }
        }
      },
      uploadAndSubmit: function (file, BinaryContent) {
        let self = this;
        let fileName = file.name;
        const api = this.$store.state.NEW_API;
        fileName = encodeURIComponent(fileName.split("\\")[fileName.split("\\").length - 1]);//IE处理汉字url
        let houzui = fileName.replace(/.+\./, "");
        if(houzui ==='xls'){
          fileName = fileName.replace('xls', 'xlsx');
        }
        let Url = api + '/api/newfcst/order_upload/' + fileName + '?file_type=' + self.file_type;
        let xmlHttp = new XMLHttpRequest();
        if(self.file_type === 1 || self.file_type === 2){
          xmlHttp.open("put", Url);//创建一个新的HTTP请求，并制定此请求的方法，URL以及验证信息(用户名/密码)；
        }else if(self.file_type === 3 || self.file_type === 4){
          xmlHttp.open("post", Url);//创建一个新的HTTP请求，并制定此请求的方法，URL以及验证信息(用户名/密码)；
        }
        xmlHttp.withCredentials = true; //跨域请求
        xmlHttp.sendAsBinary = function (datastr) { //二进制
          function byteValue(x) {
            return x.charCodeAt(0) & 0xff;
          }
          let ords = Array.prototype.map.call(datastr, byteValue);
          let ui8a = new Uint8Array(ords);
          this.send(ui8a.buffer); //向服务器发送请求
        }
        xmlHttp.sendAsBinary(BinaryContent);
        xmlHttp.onreadystatechange = function () { //当服务器返回信息时客户端的处理方式 指定当readyState属性值改变时的事件处理句柄(只写) ；
          if (xmlHttp.readyState == 4) { //返回当前请求的状态(只读)；
            if (xmlHttp.status == 500) {
              self.$message({
                message: '服务器内部异常，请联系管理员！',
                type: 'error'
              });
              self.fullscreenLoading = false;
              self.isUploadSuccess = false;
              self.loadingText = '';
            } else {
              let str = JSON.parse(xmlHttp.response);
              if (self.file_type === 1 || self.file_type === 2 || self.file_type === 3 || self.file_type === 4) {
                self.fullscreenLoading = false;
                if(str.length === undefined){
                  self.$message({
                    message: '文件导入成功',
                    type: 'success'
                  });
                  self.errorData = []
                  self.vmRequst();
                } else if (str.length >= 0){
                  self.errorData = str
                  self.errorShow = true
                }
                return;
                self.formatForecaseData(str.data.sheets);
              }
              self.import_id = str.import_id;
              xmlHttp.abort();
            }
          }
        }
      },

      // 分页
      handleCurrentChange: function (val) {
        this.vmRequst(this.pagesize, val);
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequst(val, 1);
      },
      /*
      * 网络请求
      */
      vmRequst(qty = 10, page = 1) {
//        let id = this.importType === 2 ? 26 : 27;
        let id = 0;
        if(this.importType === 1){
          id = 27
        }else if(this.importType === 2){
          id = 26
        }else if(this.importType === 3){
          id = 52
        }else if(this.importType === 4){
          id = 53
        }
        let url = this.$store.state.NEW_API + '/api/newfcst/fcst_imports/?page=' + page + '&pagesize=' + qty + '&fcst_import_type__meta_id=' + id;
        fetchAPI("get", url, null, this).then(res => {
          this.tableData = res.data.data;
          this.pagedatacount = res.data.total_number;
        });
      },
      //文件导入框内容  sy
      fileImport(importType){
        if(importType === 2){
          return '季节 名称.xls\' 如：“17SS 选样结果.xls'
        } else if (importType === 1){
          return "'季节 国家 品牌 客户 第几周.xls，且全部需要大写' 如：“17SS DMI NKF DOMYOS 1731.xls”"
        }
      },
      // 错误弹窗关闭事件
      closeDialog() {
        this.errorShow = false
      },
      //显示错误弹窗
      errorDialog () {
        let self = this
        $('.el-alert--error').click(function(ev,that = self){
          that.$set(that.$data,'errorShow',true)
        })
      },
      //关闭alert事件
      alertClose(even){
        event.stopPropagation()
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == '1') {
          this.vmRequst();
        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    created() {
      let tableColumn = [
        {
          columnName: "文件名称",
          columnProp: "file_name"
        }, {
          columnName: "文件路径",
          columnProp: "file_path"
        }, {
          columnName: "导入时间",
          columnProp: "import_timestamp"
        }
      ];
      this.tableColumn = tableColumn;
    },
    updated() {
    },
    //只执行一次
    mounted() {
      this.vmRequst();
      this. errorDialog ()
    }
  }
</script>

<style lang="scss" type="text/scss">
  .test_main_contain {
    .test_main_main {
      .test_main_main_card {
        margin: 0 auto;
        width: 402px;
        margin-top: 20px;
        margin-bottom: 30px;
        padding: 15px 0;
        background-color: white;
        text-align: center;
        border: 1px solid rgb(229, 209, 214);
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
        position: relative;
        .upload-demo {
          .el-icon-upload {
            margin: 15px 0px 10px 0px;
          }
        }
      }
    }
  }
</style>
