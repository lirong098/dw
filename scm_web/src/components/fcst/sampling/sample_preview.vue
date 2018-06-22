<template>
  <div class="samp_preview">
    <div class="clearfix">
      <div class="card-header card-header-text">
        <h4>备料单预览</h4>
      </div>
      <div class="card_box">
        <el-card>
          <el-table ref="multipleTable"
                    :data="sampleItems"
                    @selection-change="handleSelectionChange"
                    border
                    tooltip-effect="dark"
                    style="width: 100%">
            <el-table-column type="selection"
                             fixed
                             width="55">
            </el-table-column>
            <el-table-column label="Model编码"
                             show-overflow-tooltip>
              <template scope="scope">
                {{ scope.row.item.model.model_code }}
              </template>
            </el-table-column>
            <el-table-column label="Model名称"
                             width="160"
                             show-overflow-tooltip>
              <template scope="scope">
                {{ scope.row.item.model.model_name }}
              </template>
            </el-table-column>
            <el-table-column label="款号"
                             show-overflow-tooltip
                             prop="item.model.extend.iman_code.value">
            </el-table-column>
            <el-table-column label="颜色"
                             show-overflow-tooltip
                             prop="item.model.spec.color">
            </el-table-column>
            <el-table-column label="需求数"
                             show-overflow-tooltip
                             prop="quantity">
            </el-table-column>
            <el-table-column label="色布比率"
                             show-overflow-tooltip prop="fabric_ratio">
            </el-table-column>
            <el-table-column label="毛坯比率"
                             show-overflow-tooltip prop="rough_ratio">
            </el-table-column>
            <el-table-column label="纱线比率"
                             show-overflow-tooltip prop="yarn_ratio">
            </el-table-column>
            <!--备料数-->
            <el-table-column label="备料数"
                             show-overflow-tooltip>
              <template scope="scope">
                <el-input v-model="scope.row.fcst_prepare">
                </el-input>
              </template>
            </el-table-column>

            <el-table-column label="操作" fixed="right">
              <template scope="scope">
                <el-button size="small" @click="selectModel(scope.$index,scope.row)">Model</el-button>
              </template>
            </el-table-column>

          </el-table>

        </el-card>
      </div>
    </div>

    <div class="click-button">
      <div class="el-card">
        <el-button type="danger" class="handle-del mr10" :data="multipleSelection" @click="getSample">重新计算
        </el-button>
        <el-button type="success" class="handle-del mr10" :data="multipleSelection" @click="toStockListEdit">生成备料
        </el-button>
        <el-button type="text" class="handle-del mr10" :data="multipleSelection" @click="cancelPreview">取消</el-button>
      </div>
    </div>

    <el-dialog :title="dialogName" style="float: left" :visible.sync="moreAddBtn" size="large">
      <model-list @getDialogInfo=""
                  :model_id="model_id"
                  :onlyGetItem="onlyGetItem"
                  :tableName="modelListTableName"
                  :tableType="currentTableType"
                  v-if="moreAddBtn">
      </model-list>
    </el-dialog>

  </div>
</template>

<script>
  import axios from 'axios';
  import {fetchAPI} from '../../../utils/utils';
  import showModal from '../../common/messageBox.js';
  //组件
  import modelList from "../../common/model_dialog/dialog_model.vue";

  export default {
    components :{
      modelList
    },
    name: 'sample_preview',
    props: {
      rowId: Number,
      TABSValue: String,
      tabIndex: Number,
      tableName: String,
      tableType: Number,
    },
    data() {
      return {
        multipleSelection: [],//默认选中子表行所有数据集合
        tableColumn: [],//表格列字段
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        childRowId: this.rowId,
        sampleItems: [],
        input: '',
        dialogName:"",
        moreAddBtn: false,
        fcstType:{
          type:Number,
          default:6
        },
        modelListTableName: '',
        currentTableType: this.tableType,
      }
    },
    methods: {
      handleSelectionChange(val){
        this.multipleSelection = val;
      },
      getSample() {
        const api =  this.$store.state.NEW_API;
        fetchAPI('post', api+'/api/newfcst/mrp_fcst/', {fcst_order_id: this.childRowId}, this).then((res) => {
          if (res && res.status === 200) {
            this.sampleItems = res.data;
            this.sampleItems.forEach(rew =>{
              rew.fcst_prepare = rew.mrp_quantity
            })
            console.log(res)
          }
        });
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      //点击Model按钮
      selectModel(index, row) {
        console.table(row);
        this.onlyGetItem = false;
        this.model_id = row.item.model.model_id;
        this.dialogName = "model详情";
        this.currentTableType = 1;
        this.moreAddBtn = true;
        this.iconIndex = index;
        this.fcstType.default = 6;
        this.modelListTableName = row.item.model.model_type_meta_id.meta_name+'model'
      },
      //生成备料
      toStockListEdit() {
//        let fcst_pr_item = this.toMrpStockInfo_up_data(this.sampleItems);
        let newTabName = ++this.chlidTabIndex+200 + '';
        console.log(this.sampleItems);
        this.chlidTABSValue = newTabName;
        let resData = [];
        if(this.multipleSelection.length <= 0) {
          showModal.showMessage(this, "success", "请选择");
          return
        }
        this.multipleSelection.forEach(rew => {
          resData.push({
            fcst_pr_item_id: rew.item.item_id,
            item: {
              item_code: rew.item.item_code,
              item_id: rew.item.item_id,
              item_name: rew.item.item_name,
              extend: {},
              spec: {},
              model: {
                model_id: rew.item.model.model_id,
                model_code: rew.item.model.model_code,
                model_name: rew.item.model.model_name,
                unit_meta: {
                  meta_name: rew.item.model.unit_meta.meta_name
                },
                spec: {},
                extend: rew.item.model.extend
              },
            },
            quantity: rew.fcst_prepare,
            spec: {},
            extend: {},
            disabled: false, //删除状态
            restore: false, // 恢复按钮状态
            addlocal: 0,
            fcst_order_id: this.childRowId,
            materials: Math.ceil(rew.quantity * (rew.fabric_ratio/100)),//备原料
            blank: Math.ceil(rew.quantity * (rew.rough_ratio/100)),//备毛坯
            yarn: Math.ceil(rew.quantity * (rew.yarn_ratio/100)),//备纱线
            material_type_meta_id:49,
          });
          console.log(this.multipleSelection)
          console.log(resData)
        });
        let watchChildTABS = {
          title: '选样备料',
          name: newTabName,
          closable: true,
          rowId: 0,
          rowState: 'change',
          tabName: newTabName,
          fcstType: 6,  // 物料ID
          resData: resData
        };
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS);
      },
      cancelPreview() {
        this.$emit("CloseTab");
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    updated() {

    },
    //只执行一次
    mounted() {
      this.getSample();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .samp_preview {
    margin: 0 10px 10px 10px;
    display: flex;
    flex-flow: row;
    justify-content: space-between;
    /*align-items: center;*/
  }

  .clearfix {
    width: 87%;
    margin-top:30px;
    background-color: white;
    border-radius:4px;
    border:1px solid rgb(229, 209, 214);
    box-shadow:0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
    position: relative;
    .card_box{
      margin-top:50px;
      margin-bottom:30px;
      margin-left:20px;
      margin-right:20px;
    }
  }

  .click-button {
    width: 9%;
    position: fixed;
    right: 2%;
    margin-top: 30px;
    .el-card__body {
      padding-top: 0px;
    }
    .el-card {
      display: flex;
      flex-flow: column;
      align-items: center;
      padding: 20px;
      .el-button {
        margin: 0;
        font-size: 16px;
      }

      .el-button:nth-child(2) {
        margin-top: 10px;
        margin-bottom: 5px;
      }
      .el-button--text {
        width: 70px;
        text-align: center;
        color: #4db3ff;
        font-size: 18px;
      }
      .el-button--text:hover {
        color: #ec407a;
      }
    }
  }
</style>
