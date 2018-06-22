<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="clearfix forecase_sheet">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              筛选条件
            </h4>
          </div>
          <el-card>
            <el-button type="danger"
                       class="customer_add"
                       style="float: right; margin-right: 10px; position: absolute; top: 7px; left: 93%;"
                       @click="getList"
            >查询
            </el-button>
            <el-form ref="form" label-width="120px">
              <el-form-item label="起止日期 :">
                <el-date-picker v-model="startDate"
                                style="float: left;"
                                @change="startDateChange(startDate)"
                                type="date"
                                placeholder="起始日期">
                </el-date-picker>
                <el-col :span="1" style="text-align: center"> - </el-col>
                <el-date-picker v-model="endDate"
                                style="float: left;"
                                type="date"
                                placeholder="结束日期">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="成衣model ID :">
                <el-col :span="5">
                  <el-input v-model="clothesModel" placeholder="成衣model ID">

                  </el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="材料model ID :">
                <el-col :span="5">
                  <el-input v-model="materialModel" placeholder="材料model ID">

                  </el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="材料item ID :">
                <el-col :span="5">
                  <el-input v-model="materialItem" placeholder="材料item ID">

                  </el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="坯布代号 :">
                <el-col :span="5">
                  <el-input v-model="barCode" placeholder="坯布代号">

                  </el-input>
                </el-col>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
      <div class="card_box">
        <div class="card-header card-header-text">
          <h4>备料信息</h4>
        </div>
        <el-card>
          <el-table :data="getData" border v-loading="loading">
            <el-table-column prop="pr_form_meta.meta_name" label="备料形式">
            </el-table-column>
            <el-table-column prop="clothes_model.model_code" label="成衣model编号">
            </el-table-column>
            <el-table-column prop="clothes_model.model_name" label="成衣model名称">
            </el-table-column>
            <el-table-column prop="material_item.model.model_code" label="材料model编号">
            </el-table-column>
            <el-table-column prop="material_item.model.model_name" label="材料model名称">
            </el-table-column>
            <el-table-column prop="material_item.item_code" label="item编号">
            </el-table-column>
            <el-table-column prop="material_item.item_name" label="item名称">
            </el-table-column>
            <el-table-column prop="delivery_date" label="备料交期">
            </el-table-column>
            <el-table-column prop="quantity" label="库存数">
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import common from '../../common/common.js'
  export default {
    components: {},
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableData: Array
    },
    data() {
      return {
        chlidTABS: this.TABS,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        childTableData: this.tableData,
        startDate: '',
        endDate: '',
        clothesModel: '',
        materialModel: '',
        materialItem: '',
        barCode: '',
        getData: [],
        loading: false,
      }
    },
    methods: {
      // 初始获取BOM数据列表
      getList() {
        console.log('startDate',this.startDate);
        console.log('endDate',this.endDate);
        this.loading = true;
        if(this.startDate !== '' && this.endDate !== ''){
          let startDate = common.formatDate(this.startDate);
          let endDate = common.formatDate(this.endDate);
          fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/mrp_stock/?start_date=' + startDate + '&end_date=' + endDate + '&clothes_model=' + this.clothesModel + '&material_model=' + this.materialModel + '&material_item=' + this.materialItem + '&bar_code=' + this.barCode, null, this).then((res) => {
            if (res && res.status === 200) {
              this.getData = res.data;
              this.loading = false;
            }
          })
        }else {
          this.$message({
            message: '请选择起止日期',
            type: 'warning'
          });
          this.loading = false;
        }
      },
      startDateChange(startDate) {
        console.log(startDate)
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue === 1) {

        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      },
      tableData(val) {
        this.childTableData = val;
      }
    },
    updated() {

    },
    created() {

    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_main_contain {
    .toolmy {
      height: 50px;
    }
    .btnright {
      width: 100%;
      height: 90px;
      float: right;
      display: inline-block;
    }
  }

  .clearfix {
    margin-top: 20px;
  }

  .truechange {
    width: 25%;
    text-align: center;
  }

  .el-date-editor.el-input {
    width: 25%;
  }

  .el-select > .el-input {
    width: 100%;
  }

  .forecase_sheet {
    padding: 20px 10px 10px 10px;
    .el-form {
      border: 1px solid #ccc;
      .el-form-item {
        /*border:1px solid red;*/
        margin: 8px 5px;
        border-bottom: 1px dashed #ccc;
        padding-bottom: 5px;
      }
      .el-form-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
      }
    }
  }

  .eltag {
    float: left;
    margin-right: 10px;
    margin-top: 6px;
    cursor: pointer;
  }

  .el-table .cell {
    padding: 0;
    .quantity {
      background: #c9daf8;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .pr_on_line_quantity {
      background: #d9ead3;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .remaining_quantity {
      background: #f4cccc;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .arrival_quantity {
      background: #ffd966;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
  }

  .el-table .cell {
    padding: 0 !important;
  }

  .el-dialog .el-dialog--large {
    min-height: 800px !important;
  }

  .el-date-editor.el-input {
    width: 21% !important;
  }
</style>
