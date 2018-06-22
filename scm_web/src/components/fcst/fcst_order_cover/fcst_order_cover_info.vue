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
            <el-form ref="form" label-width="80px">
              <el-form-item label="客户 :">
                <div class="item"
                     v-for="item in userOption"
                     :key="item.customer_id"
                     @click="changeClient(item.customer_id)">
                  <el-tag class="eltag"
                          :type="userValue === item.customer_id ? 'success' : 'gray'">
                    {{item.customer_name}}
                  </el-tag>
                </div>
              </el-form-item>
              <el-form-item label="季节 :">
                <el-select v-model="seasonInitial" @change="seasonMethod(seasonInitial)" placeholder="请选择">
                  <el-option
                    v-for="item in seasonData"
                    :key="item.meta_id"
                    :label="item.meta_name"
                    :value="item.meta_id">
                  </el-option>
                </el-select>
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
            <el-table-column label="成衣model" width="500">
              <template scope="scope">
                <el-input v-text="commonmethod(scope.row.model)">

                </el-input>
              </template>
            </el-table-column>
            <el-table-column label="选样覆盖">
              <el-table-column prop="quantity" label="选样数量">
              </el-table-column>
              <el-table-column prop="first_order_quantity" label="选样实单数">
              </el-table-column>
              <el-table-column prop="repeat_order_quantity" label="预估实单数">
              </el-table-column>
              <el-table-column prop="diff_quantity" label="差异数">
              </el-table-column>
              <el-table-column prop="diff_ratio" label="差异比率">
              </el-table-column>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import COMMON from '../../common/common.js';

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
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 1,  // 总条数
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        childTableData: this.tableData,
        userOption: [],
        seasonInitial: 0,
        seasonData: [],
        userValue: 0,
        getData: [],
        loading: false,
      }
    },
    methods: {
      // 重组名称
      commonmethod(model) {
        if (model.model_id) {
          let keyArr = ['model_code', 'model_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          model.spec.color ? tempArr.push(model.spec.color) : '';
          return tempArr.join(' - ')
        }
        if (model.item_id) {
          let keyArr = ['item_code', 'item_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          return tempArr.join(' - ');
        }
      },
      // 获取列表方法
      getList() {
        this.loading = true;
        if (this.userValue !== 0 && this.seasonInitial !== 0) {
          let postData = {
            customer_id: this.userValue,
            season_meta_id: this.seasonInitial
          };
          fetchAPI('post', this.$store.state.NEW_API + '/api/newfcst/fcstcover/', postData, this).then((res) => {
            if (res && res.status == 200) {
              if(res.data.message){
                this.$message({
                  type: 'info',
                  message: res.data.message
                });
                this.getData = [];
                this.loading = false;
                return;
              }
              console.log(res.data);
              this.getData = res.data;
              this.loading = false;
            } else {
              this.loading = false;
            }
          })
        }
      },

      // 切换季节
      seasonMethod(seasonMes) {

      },
      // 切换用户
      changeClient(clientCode) {
        this.userValue = clientCode;
      },
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue === "1") {

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
    mounted() {

    },
    created() {
      // 获取用户列表
      fetchAPI('get', this.$store.state.NEW_API + '/api/customer/customers/?all=1', null, this).then((res) => {
        if (res && res.status == 200) {
          console.log(res.data, '111')
          this.userOption = res.data.data;
          if (this.userOption.length > 0) {
            this.userValue = this.userOption[0].customer_id;
          } else {
            this.userValue = ''
          }
          return COMMON.getMetaList(this, 43)
        }
      }).then((res) => {
        if (res && res.status === 200) {
          if (res.data.length > 0) {
            this.seasonData = res.data;
            this.seasonInitial = this.seasonData[0].meta_id;
          } else {
            this.seasonData = [];
            this.seasonInitial = '';
          }
        }
      })
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
        padding-bottom: 0px;
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
    padding: 0px !important;
  }

  marginstyle {
    margin-bottom: 5px;
  }

  .el-dialog .el-dialog--large {
    min-height: 800px !important;
  }

</style>
