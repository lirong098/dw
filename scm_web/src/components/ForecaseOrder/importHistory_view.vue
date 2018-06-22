<template>
  <div class="order_edit_contain">
    <div class="order_edit_main">
      <div class="tab_table" v-loading.body="loading">
        <lazy-render>
          <el-tabs v-model="currenTab" v-if="this.historyDetailData.fcst_type_meta == '__MC_ORDER_IMPORT'">
            <el-tab-pane v-for="(item, index) in TABS"
                         :key="item.name"
                         :label="item.title"
                         :name="item.name">
              <div class="card_main_box" v-show="item.name
              ==currenTab">
                <div class="card_box">
                  <div class="card-header card-header-text">
                    <h4>
                      订单数据
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
                      订单数据
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
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default{
    name:'import-history-view',
    props:{
      historyDetail:{
        type:Object
      }
    },
    components: {

    },
    data () {
      return {
        loading:false,
        historyDetailData:Object.assign({},this.historyDetail),
        moduleList:{},
        TABS:[],
        currenTab:'',
        tabHeight:400,
        expandData:{},
        modulePeroid:{},
        sampleData:{},
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
    computed:{

    },
    created() {
      this.getHistoryDetail();
      this.tabHeight = window.innerHeight -265;
    },
    methods: {
      getHistoryDetail:function () {
        this.loading = true;
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcst/fcst_import_detail/?import_id='+this.historyDetailData.fcst_import_id,null,this).then((res) => {
          if(res && res.status == 200){
            if(this.historyDetailData.fcst_type_meta == '__MC_ORDER_IMPORT'){
              this.formatForecaseData(res.data.sheets);
            }else{
              this.formatSampleData(res.data.sheets);
            }
          }
          this.loading = false;
        });
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
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_edit_contain{
    height: 100%;
    padding:0 10px 0px 10px;
    .card_main_box{
      padding-top: 20px;
    }
    .order_edit_main{
      height: 100%;
      .head_title{
        height: 28px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 5px 12px 5px 0;
          box-sizing: border-box;
        }
      }
      .edit_order_input{
        width:300px;
      }
      .model_content{
        display: inline-block;
        width:40%;
      }
      .item_content{
        display: inline-block;
        width:50%;
      }
      .quantity_content{
        display: inline-block;
      }
    }
    .materials_content{
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
            .items{
              overflow: hidden;
              .item{
                float: left;
                margin: 9px 9px 9px 0;
                color: #000;
                width: 100%;
                .arrow{
                  margin: 0 2px;
                }
                .item_contents{
                  word-break:normal;
                  width:auto;
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
