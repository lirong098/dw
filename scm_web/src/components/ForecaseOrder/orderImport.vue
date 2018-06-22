<template>
  <div class="order_import" ref="order_import"
       v-loading.fullscreen.lock="fullscreenLoading"
       :element-loading-text="loadingText">
    <div class="head_tool" v-if="!isUploadSuccess">
      <div class="upload_content">
        <el-card class="box-card extra_card_extra">
          <div slot="header" class="clearfix">
            <div class="type_select">
              <el-radio-group v-model="file_type">
                <el-radio :label="1">预估订单</el-radio>
                <el-radio :label="2">选样订单</el-radio>
              </el-radio-group>
            </div>
          </div>
          <el-upload class="upload-demo" drag action=""
                     :show-file-list="false"
                     :before-upload="beforeUpload"
                     :on-progress="uploadProgress"
                     :http-request="uploadFile">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将
              <b>{{file_type == 1 ? '预估订单' : '选样订单'}}</b>
              文件拖到此处，或<em>点击上传
              </em></div>
            <div class="el-upload__tip">只能上传Excel文件</div>
          </el-upload>
        </el-card>
      </div>
    </div>
    <div class="order_content" v-else>
      <div>
        <div class="table_head_title clearfix">
          <div class="title fl">{{fileName}} 已上传成功, 预览如下
          </div>
          <div class="create_btn fr">
            <el-button type="primary"
                       @click="sunmitImport">
              生成预估订单
            </el-button>
          </div>
        </div>
        <div class="tab_table">
          <lazy-render>
            <el-tabs v-model="currenTab" v-if="file_type
            == 1">
              <el-tab-pane v-for="(item, index) in TABS"
                           :key="item.name"
                           :label="item.title"
                           :name="item.name">
                <div class="card_main_box"
                     v-show="item.name ==currenTab">
                  <div class="card_box">
                    <div class="card-header card-header-text">
                      <h4>
                        导入预览
                      </h4>
                    </div>
                    <el-card>
                      <el-table :data="moduleList[item.name]"
                                :default-sort="defaultSort1"
                                 :height="tabHeight">
                        <el-table-column width="70" fixed>
                          <template scope="scope">
                            <div class="expand_icon"
                                 v-show="scope.row.is_module"
                                 @click="handleExpand(scope.$index, scope.row,item.name)">
                              <el-icon
                                :name="scope.row.module_expand_flag ? 'arrow-down' : 'arrow-right'"></el-icon>
                            </div>
                          </template>
                        </el-table-column>
                        <el-table-column prop="vname"
                                         label="model"
                                         min-width="200"
                                         fixed></el-table-column>
                        <el-table-column :key="peroid"
                                         :label="peroid.slice(2)"
                                         v-for="peroid in modulePeroid[item.name]">
                          <template scope="scope">
                            {{scope.row[scope.row.vcode + '_' + peroid]}}
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-card>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
            <el-tabs v-model="currenTab" v-else>
              <el-tab-pane v-for="(item, index) in TABS"
                           :key="item.name"
                           :label="item.title"
                           :name="item.name">
                <div class="card_main_box" v-show="item.name ==currenTab">
                  <div class="card_box">
                    <div class="card-header card-header-text">
                      <h4>
                        导入预览
                      </h4>
                    </div>
                    <el-card>
                      <el-table :data="sampleData[item.name]"
                                :default-sort="defaultSort"
                                 :height="tabHeight">
                        <el-table-column type="expand">
                          <template scope="props">
                            <el-form
                              v-if="props.row.extend"
                              label-position="left"
                              inline
                              class="sample-data-table-expand">
                              <el-form-item
                                :label="props.row.extend.elastic_lower_ratio.name">
                                <span>{{
                                  props.row.extend.elastic_lower_ratio.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.elastic_higher_ratio.name">
                                <span>{{
                                  props.row.extend.elastic_higher_ratio.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.elastic_week_start.name">
                                <span>{{
                                  props.row.extend.elastic_week_start.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.elastic_week_end.name">
                                <span>{{
                                  props.row.extend.elastic_week_end.value }}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.pr_method.name">
                                <span>{{
                                  props.row.extend.pr_method.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.fabric_ratio.name">
                                <span>{{
                                  props.row.extend.fabric_ratio.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.rough_ratio.name">
                                <span>{{
                                  props.row.extend.rough_ratio.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.yarn_ratio.name">
                                <span>{{
                                  props.row.extend.yarn_ratio.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.delivery_week_first.name">
                                <span>{{
                                  props.row.extend.delivery_week_first.value}}</span>
                              </el-form-item>
                              <el-form-item
                                :label="props.row.extend.delivery_week_last.name">
                                <span>{{
                                  props.row.extend.delivery_week_last.value}}</span>
                              </el-form-item>
                              <el-form-item label="选样日期">
                                <span>{{
                                  props.row.date}}</span>
                              </el-form-item>
                            </el-form>
                          </template>
                        </el-table-column>
                        <el-table-column prop="Model_code"
                                         label="ModelCode"
                                         :min-width="120"
                                         :show-overflow-tooltip="true"
                        ></el-table-column>
                        <el-table-column prop="Model_name"
                                         label="ModelName"
                                         :min-width="200"
                                         :show-overflow-tooltip="true"
                        ></el-table-column>
                        <el-table-column prop="mpc"
                                         label="Mpc"
                        ></el-table-column>
                        <el-table-column prop="iman_code"
                                         label="款号"
                        ></el-table-column>
                        <el-table-column prop="quantity"
                                         label="选样结果"
                        ></el-table-column>
                      </el-table>
                    </el-card>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </lazy-render>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default{
    components: {},
    data () {
      return {
        file_type: 1,
        fullscreenLoading: false,
        loadingText: '',
        expandData: {},
        moduleList: {},
        modulePeroid: {},
        sampleData:{},
        isUploadSuccess: false,
        fileName: 'module_item.xlsx',
        TABS: [],
        currenTab: '',
        tabHeight: 500,
        import_id:0,
        defaultSort:{
          prop:'Model_code',
          order:'ascending'
        },
        defaultSort1:{
          prop:'vname',
          order:'ascending'
        }
      }
    },
    computed: {},
    created() {
      this.tabHeight = window.innerHeight - 140;
    },
    methods: {
      beforeUpload: function (file) {
        let name = file.name.replace(/.+\./, "");
        this.fileName = file.name;
//        if (name != 'xlsx') {
//          this.loadingText = '';
//          this.fullscreenLoading = false;
//          this.$message({
//            message: '不支持该文件类型',
//            type: 'warning'
//          });
//          return false
//        } else {
//          this.fullscreenLoading = true;
//          this.loadingText = file.name + '正在上传并生成预览，请稍后';
//        }
        this.fullscreenLoading = true;
        this.loadingText = file.name + '正在上传并生成预览，请稍后';
      },
      uploadProgress: function (event, file, fileList) {

      },
      uploadFile: function (uploadFile) {
        let self = this;
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
        const api = this.$store.state.DEV_API;
        fileName = encodeURIComponent(fileName.split("\\")[fileName.split("\\").length - 1]);//IE处理汉字url
        let Url = api + '/api/fcst/upload/' + fileName + '?file_type=' + self.file_type;
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("PUT", Url);
        xmlHttp.withCredentials = true;
        xmlHttp.sendAsBinary = function (datastr) {
          function byteValue(x) {
            return x.charCodeAt(0) & 0xff;
          }
          let ords = Array.prototype.map.call(datastr, byteValue);
          let ui8a = new Uint8Array(ords);
          this.send(ui8a.buffer);
        }
        xmlHttp.sendAsBinary(BinaryContent);
        xmlHttp.onreadystatechange = function () {
          if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 500) {
              self.$message({
                message: '文件导入失败,请重新上传',
                type: 'error'
              });
              self.fullscreenLoading = false;
              self.isUploadSuccess = false;
              self.loadingText = '';
            }else{
              let str = JSON.parse(xmlHttp.response);
              if(self.file_type == 1){
                self.formatForecaseData(str.data.sheets);
              }else if(self.file_type == 2){
                self.formatSampleData(str.data.sheets);
              }
              self.import_id = str.import_id;
              xmlHttp.abort();
            }
          }
        }
      },
      formatForecaseData: function (sheetTabs) {
        let moduleData = {};
        for (let tab of sheetTabs) {
          let t = {
            title: tab.Sheet_name,
            name: tab.Sheet_name
          };
          moduleData[tab.Sheet_name] = tab.Sheet_content;
          this.TABS.push(t);
        }
        this.currenTab = this.TABS[0].name;
        for (let i in moduleData) {
          this.moduleList[i] = [];
          let peroid = {};
          for (let item in moduleData[i]) {
            let module = moduleData[i][item];
            let moduleObj = {};
            moduleObj.vcode = module.Model_code;
            moduleObj.vname = module.Model_code;
            moduleObj.is_module = true;
            moduleObj.module_expand_flag = false;
            for (let total in module.total) {
              moduleObj[module.Model_code + '_' + total] = module.total[total];
              peroid[total] = total;
            }
            this.moduleList[i].push(moduleObj);
            this.expandData[i + '_' + module.Model_code] = [];
            for (let content in module.Model_content) {
              let obj = {};
              let vItem = module.Model_content[content];
              obj.vcode = vItem.Item;
              obj.vsize = vItem.Size;
              obj.is_module = false;
              obj.vname = vItem.Item + ' - ' + vItem.Size;
              for (let value in vItem.Value) {
                obj[vItem.Item + '_' + value] = vItem.Value[value]
              }
              this.expandData[i + '_' + module.Model_code].push(obj);
            }
          }
          this.modulePeroid[i] = peroid;
        }
        this.fullscreenLoading = false;
        this.isUploadSuccess = true;
        this.loadingText = '';
      },
      formatSampleData:function (sheetTabs) {
        let moduleData = {};
        for (let tab of sheetTabs) {
          let t = {
            title: tab.Sheet_name,
            name: tab.Sheet_name
          };
          moduleData[tab.Sheet_name] = tab.Sheet_content;
          this.TABS.push(t);
          this.sampleData[tab.Sheet_name] = tab.Sheet_content;
        }
        this.currenTab = this.TABS[0].name;
        this.fullscreenLoading = false;
        this.isUploadSuccess = true;
        this.loadingText = '';
      },
      handleExpand: function (index, row, name) {
        let flag = this.moduleList[name][index].module_expand_flag;
        if (this.moduleList[name][index].module_expand_flag) {//要折叠
          this.moduleList[name].splice(index + 1, this.moduleList[name][index].module_expand_num);
        } else {//要展开
          let num =
            this.expandData[name + '_' + this.moduleList[name][index].vcode] ? this.expandData[name + '_' + this.moduleList[name][index].vcode].length : 0;
          this.moduleList[name][index].module_expand_num = num;
          if (num) {
            this.moduleList[name].splice(index + 1, 0, ...this.expandData[name + '_' + this.moduleList[name][index].vcode]);
          }
        }
        this.moduleList[name][index].module_expand_flag = !flag;
      },
      sunmitImport:function () {
        this.fullscreenLoading = true;
        let text = this.file_type == 1 ? '预估处理' : '预估录入'
        this.loadingText = '正在生成预估订单，之后会跳转到'+text+'页面';
        const api = this.$store.state.DEV_API;
        let url = api + '/api/fcst/import_data/';
        url = url + '?import_id=' + this.import_id;
        fetchAPI('post',url,null,this).then(res => {
          if(res && res.status == 200){
            this.fullscreenLoading = false;
            this.loadingText = '';
            this.isUploadSuccess = false;
            if (this.file_type == 1) {
              this.$router.push({path: 'forecasesheet'});
            } else {
              this.$router.push({path:
                'orderinput'});
              this.$cookie.set('orderType',2);
            }
          }else{
            this.fullscreenLoading = false;
            this.loadingText = '';
          }
        })
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_import {
    height: 95%;
    padding: 10px;
    .card_main_box{
      padding-top: 20px;
    }
    .head_tool {
      margin-top: 16%;
      .upload_content {
        margin: 0 auto;
        width: 360px;
        position: relative;
        .upload-demo {
          .el-upload__text {
            margin: 3px 0;
          }
        }
      }
    }
    .order_content {
      .table_head_title {
        margin-bottom: 5px;
      }
      .tab_table {

      }
    }
    .diff_content{
      .group{
        border:1px solid #e8e8e8;
        position: relative;
        .row_select-first, .row_select:first-child{
          border-top:none;
        }
        .row_select{
          position: relative;
          border-top: 1px dashed #dedede;
          margin: 0 8px;
          .head{
            position: absolute;
            left: 11px;
            top: 9px;
            color: #999;
          }
          .body{
            /*padding:0 100px 0 112px;*/
            .items{
              /*height: 36px;*/
              overflow: hidden;
              .item{
                float: left;
                margin: 9px 9px 9px 0;
                /*height: 18px;*/
                color: #000;
                width: 100%;
                .item_content{
                  word-break:normal;
                  width:auto;
                  display:inline-block;
                  word-wrap : break-word ;
                  overflow: hidden ;
                }
              }
            }
          }
        }
      }
    }
  }
</style>
