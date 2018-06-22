<template>
  <div class="test_detailed_contain">
    <div class="fl test_detailed_main main-card-box">
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>基础信息</h4>
          </div>
          <el-card class="divCard">
            <el-col class="detailMessage">
              <el-form class="detaMessageForm" label-width="90px" :label-position="labelPosition">
                <el-col :span="12">
                  <el-form-item label="选样单号：">
                    <el-input class="truechange nochange" v-text="sampleData.fcst_order_no" disabled></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="客户名称：">
                    <el-input
                      class="truechange nochange"
                      v-text="sampleData.customer.customer_name"
                      disabled>
                    </el-input>
                  </el-form-item>
                </el-col>
                <div style="width: 99%">
                  <el-col :span="12">
                    <el-form-item label="季节：">
                      <el-input class="truechange nochange" v-text="sampleData.season?sampleData.season.meta_name:''"
                                disabled></el-input>
                    </el-form-item>
                  </el-col>
                </div>
                <el-col :span="12">
                  <el-form-item label="单据日期：">
                    <el-input class="truechange nochange" v-text="sampleData.deal_date" disabled></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="类型：">
                    <el-input style="height: 37px;"
                      class="truechange nochange"
                      v-text="sampleData.extend.order_type"
                      disabled>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-form>
            </el-col>
          </el-card>
        </div>
      </div>

      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>详细信息</h4>
          </div>
          <div class="table">
            <el-card>
              <el-table :data="sampleItemsTableData" border style="width: 100%">

                <el-table-column label="Model编号" width="200">
                  <template scope="scope">
                    <!--<el-input v-show="checkStatus === 'look'"-->
                    <!--v-text="scope.row.item.model.model_code">-->
                    <!--</el-input>-->
                    <!--<el-input v-show="checkStatus === 'change'"-->
                    <!--:disabled="scope.row.disabled"-->
                    <!--:readonly="true"-->
                    <!--:value="scope.row.item.model.model_code">-->
                    <!--</el-input>-->
                    <el-input v-text="scope.row.item.model.model_code">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="Model名称" width="200">
                  <template scope="scope">
                    <!--<el-input v-show="checkStatus === 'look'"-->
                    <!--v-text="scope.row.item.model.model_name">-->
                    <!--</el-input>-->
                    <!--<el-input v-show="checkStatus === 'change'"-->
                    <!--:disabled="scope.row.disabled"-->
                    <!--:readonly="true"-->
                    <!--:value="scope.row.item.model.model_name">-->
                    <!--</el-input>-->
                    <el-input v-text="scope.row.item.model.model_name">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="款号">
                  <template scope="scope">
                    <el-input v-text="scope.row.item.model.extend.iman_code.value">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="颜色">
                  <template scope="scope">
                    <el-input v-text="scope.row.item.model.spec.color">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="尺码" v-if="fcstType === 5">
                  <template scope="scope">
                    <el-input v-text="scope.row.item ? scope.row.item.item_name : ''"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="交货日期">
                  <template scope="scope">
                    <!--<el-input v-show="checkStatus === 'look'"-->
                    <!--v-text="scope.row.delivery_date">-->
                    <!--</el-input>-->
                    <!--<el-date-picker v-show="checkStatus === 'change'" type="date" placeholder="选择日期"-->
                    <!--:disabled="scope.row.disabled"-->
                    <!--:editable='false'-->
                    <!--v-model="scope.row.delivery_date"-->
                    <!--:picker-options="pickerOptions">-->
                    <!--</el-date-picker>-->
                    <el-input v-text="scope.row.delivery_date">
                    </el-input>
                  </template>
                </el-table-column>


                <el-table-column label="数量" width="100px">
                  <template scope="scope">
                    <el-input v-show="checkStatus === 'look'"
                              v-text="scope.row.quantity">
                    </el-input>
                    <el-input v-show="checkStatus === 'change'"
                              :disabled="scope.row.disabled"
                              v-model="scope.row.quantity"
                    >
                    </el-input>
                  </template>
                </el-table-column>

                <!--<el-table-column fixed label="操作" fixed="right" v-if="checkStatus === 'change'">-->
                <!--<template scope="scope">-->
                <!--<el-button size="small" @click="handleAdd()">添加</el-button>-->
                <!--<el-button size="small"-->
                <!--type="danger" v-if="scope.row.restore !== true"-->
                <!--@click="handleDelete(scope.$index, scope.row)">删除</el-button>-->
                <!--<el-button size="small"-->
                <!--type="danger" v-if="scope.row.restore === true"-->
                <!--@click="handleRestore(scope.$index, scope.row)">恢复</el-button>-->
                <!--</template>-->
                <!--</el-table-column>-->

              </el-table>
            </el-card>
          </div>

        </div>
      </div>
    </div>

    <div class="click-button">
      <el-card class="extra_card" v-show="checkStatus === 'look'">
        <el-button type="primary" @click="changeBtn">编辑</el-button>
        <!--<el-button type="danger">添加</el-button>-->
        <el-dropdown>
                    <span class="el-dropdown-link">
                      更多<i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-if="fcstType==2"><a @click="addPreviewTab(sampleData.fcst_order_id)">生成备料单</a>
            </el-dropdown-item>
            <el-dropdown-item><a @click="deleteMessageBtn()" style="display: inline-block; width: 100%;">删除</a>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-card>
      <el-card class="extra_card" v-show="checkStatus === 'change'">
        <el-button type="primary"
                   size="large"
                   @click="saveSample()"
        >保存
        </el-button>
        <el-button type="error"
                   size="large"
                   style="border: 0; color: #4db3ff;"
                   @click="cancelEdit"
        >取消
        </el-button>
      </el-card>
    </div>

    <el-dialog :title="dialogName" style="float: left" :visible.sync="moreAddBtn" size="large">
      <model-list @getDialogInfo="getDialogInfo"
                  :onlyGetItem="onlyGetItem"
                  :otherParameter="otherparameter"
                  :tableName="tableName"
                  :tableType="tableType"
                  v-if="moreAddBtn">
      </model-list>
    </el-dialog>

  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import showModal from '../../common/messageBox.js';
  //组件
  import modelList from "../../common/model_dialog/dialog_model.vue";

  export default {
    components: {
      modelList
    },
    name: 'sample_edit',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableName: String,
      tableType: Number,
      rowId: Number,
      rowMessage: Number,
      fcstType: Number,  // 6 选样实单， 5 预估实单
    },
    data() {
      return {
        labelPosition: 'left',
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        childRowId: this.rowId,
        clickIndex: 0,
        valueDate: '',
        otherparameter: {
          otherCustomerId: [],
          otherSeasonId: []
        },
        sampleData: {
          customer: {}
        },
        sampleItemsTableData: [],
        detaMessageForm: this.rowMessage,
        checkStatus: "look", // 编辑状态: change, 查看状态: look
        dialogName: "",
        moreAddBtn: false,
        arrAll: [],
        userOption: [],
        userValue: '',
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },
      }
    },
    methods: {
      //获取单个选样实单
      getSample() {
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/newfcst/fcst_order/?fcst_order_id=' + this.childRowId, {}, this).then((res) => {
          if (res && res.status === 200) {
            this.sampleData = res.data;
            console.log(this.sampleData);
          }
        });

        fetchAPI('get', api + '/api/newfcst/fcst_order_item/?fcst_order_id=' + this.childRowId, {}, this).then((res) => {
          if (res && res.status === 200) {
            this.sampleItemsTableData = res.data.data;
          }
        });
      },
      //获取客户信息
      getCustomerInfo() {
        for (let x in this.list) {
          this.arrAll.push(this.list[x])
        }
        // 获取用户列表
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/customer/customers/?all=1', null, this).then((res) => {
          if (res && res.status == 200) {
            for (let item of res.data.data) {
              this.userOption.push(item)
            }
            console.log(this.userOption);
          }
        })
      },

      //确认删除按钮
      deleteMessageBtn() {
        showModal.showModal(this, this.deleteFcstOrder, "", "此操作将永久删除该信息, 是否继续?", '操作提示', "是", "否");
      },
      deleteFcstOrder() {
        let deleteArr = [this.sampleData.fcst_order_id];
        const api = this.$store.state.NEW_API;
        fetchAPI('delete', api + '/api/newfcst/fcst_orders/', {data: deleteArr}, this).then((res) => {
          showModal.showMessage(this, "success", "删除成功");
          if (res.status === 204) {
            this.cancelPreview()
          }
        });
      },
      // 点击编辑按钮
      changeBtn() {
        const api = this.$store.state.NEW_API;
        this.checkStatus = "change";
        // 恢复原数据
        // fetchAPI('get', api + '/api/newfcst/fcst_order_item/?fcst_order_id=' + this.childRowId, {}, this).then((res) => {
        //   if (res && res.status === 200) {
        //     this.sampleItemsTableData = res.data.data;
        //     console.log('编辑', this.sampleItemsTableData)
        //   }
        // });
      },
      //点击取消按钮
      cancelEdit() {
        this.$confirm('此操作将不会保存已填写的数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // 恢复原数据
          const api = this.$store.state.NEW_API;
          fetchAPI('get', api + '/api/newfcst/fcst_order_item/?fcst_order_id=' + this.childRowId, {}, this).then((res) => {
            if (res && res.status === 200) {
              this.sampleItemsTableData = res.data.data;
              this.checkStatus = 'look';
            }
          });
        }).catch(() => {
          showModal.showMessage(this, "info", "已取消操作");
        });
      },
      handleAdd() {
        let addTableData = {
          delivery_date: '',
          fcst_order_item_id: 0,
          fcst_order_id: this.sampleData.fcst_order_id,
          extend: {},
          spec: {},
          addlocal: 0,
          disabled: false, //删除状态
          item: {
            item_code: "",
            item_id: 0,
            item_name: "",
            model: {
              model_id: 0,
              model_code: "",
              model_name: "",
            }
          },
          quantity: 0
        };
        this.sampleItemsTableData.push(addTableData)
      },
      handleDelete(index, row) {
        this.clickIndex = index;

        this.sampleItemsTableData = this.sampleItemsTableData.map(function (currentValue, key) {
          if (index === key) {
            currentValue.disabled = true;
            currentValue.delete = 0;
            currentValue.restore = true;
          }
          return currentValue;
        });

        // 判断并删除空行
        if (row.item.model.model_code === '' || row.item.model.model_name === ''
          || row.item.item_code === '' || row.item.item_name === ''
          || row.delivery_date === '' || row.delivery_date === undefined) {
          this.sampleItemsTableData.splice(index, 1);
        }

      },
      //恢复功能
      handleRestore(index, row) {
//        row.restore = false;
        this.sampleItemsTableData = this.sampleItemsTableData.map(function (currentValue, key) {
          console.log(key);
          if (index === key) {
            currentValue.disabled = false;
            currentValue.delete = 1;
            currentValue.restore = false;
          }

          return currentValue;
        });
      },
      //点击Model列的选择按钮
      selectModel(index, row) {
        console.log(row)
//        this.$refs.multipleTable.setCurrentRow(row); // 高亮当前行
        this.onlyGetItem = false;
        this.model_id = 0; // 选择modelList 将model_id 设为 0
        this.dialogName = "选择model";
        this.moreAddBtn = true;
        this.iconIndex = index;
        this.otherparameter.otherCustomerId = row.item.model.customer.customer_id
        this.otherparameter.otherSeasonId = row.item.model.season.meta_id
      },
      //点击Item列的选择按钮
      selectItem(index, row) {
//        this.$refs.multipleTable.setCurrentRow(row);//高亮当前行
        if (row.item.model.model_id && row.item.model.model_id > 0) {
          this.onlyGetItem = true;
          this.model_id = row.item.model.model_id;//选择Item 将model_id 设为 当前的row的model_id
          this.dialogName = "选择Item";
          this.moreAddBtn = true;
          this.iconIndex = index;
        } else { //没有model_id 则弹出选择model的list
          this.selectModel(index, row);
        }
      },
      getDialogInfo(row, model_id) {

        if (!this.onlyGetItem) { // false时：选择model数据
          if (row.model_item.length >= 1) {
            this.sampleItemsTableData[this.iconIndex].item.model.model_id = row.model_id;
            this.sampleItemsTableData[this.iconIndex].item.model.model_type_meta_id = row.model_type_meta_id;
            this.sampleItemsTableData[this.iconIndex].item.model.unit_meta = row.unit_meta;
            this.sampleItemsTableData[this.iconIndex].item.model.model_code = row.model_code;
            this.sampleItemsTableData[this.iconIndex].item.model.model_name = row.model_name;
            this.sampleItemsTableData[this.iconIndex].item.model.spec = row.spec;
            this.sampleItemsTableData[this.iconIndex].item.item_id = row.model_item[0].item_id;
            this.sampleItemsTableData[this.iconIndex].item.item_code = row.model_item[0].item_code;
            this.sampleItemsTableData[this.iconIndex].item.item_name = row.model_item[0].item_name;
          }

          for (let i = 1; i < row.model_item.length; i++) {
            let data = {
              item: {
                item_id: row.model_item[i].item_id,
                item_code: row.model_item[i].item_code,
                item_name: row.model_item[i].item_name,
                model: {
                  model_id: row.model_id,
                  model_type_meta_id: row.model_type_meta_id,
                  unit_meta: row.model_id,
                  model_code: row.model_code,
                  model_name: row.model_name,
                  spec: row.spec
                }
              },
              delivery_date: '',
              quantity: 0,
              fcst_order_item_id: 0,
              fcst_order_id: this.sampleData.fcst_order_id,
              extend: {},
              spec: {},
              addlocal: 0
            };
            this.sampleItemsTableData.splice(this.iconIndex + 1, 0, data);
          }

        } else { // true时：选择Item数据
          this.sampleItemsTableData[this.iconIndex].item.item_id = row[0].item_id;
          this.sampleItemsTableData[this.iconIndex].item.item_code = row[0].item_code;
          this.sampleItemsTableData[this.iconIndex].item.item_name = row[0].item_name;
        }

        // 使dialog消失
        this.moreAddBtn = false;
      },
      saveSample() {
        // 判断数据格式是否正确
        for (let i = 0; i < this.sampleItemsTableData.length; i++) {
          let item = this.sampleItemsTableData[i];
          if (item.item.model.model_code === '' || item.item.model.model_name === '') {
            showModal.showMessage(this, "info", "请补全model信息");
            return;
          }
          if (item.item.item_code === '' || item.item.item_name === '') {
            showModal.showMessage(this, "info", "请补全item信息");
            return;
          }
          if (item.delivery_date === '') {
            showModal.showMessage(this, "info", "请补全日期");
            return;
          }
//        验证quantity数据类型
          if (isNaN(item.quantity)) {
            showModal.showMessage(this, "info", "数量字段请输入数字");
            return;
          }
        }

        //格式化日期
        this.sampleItemsTableData.forEach((item) => {
          let date = new Date(item.delivery_date);
          item.delivery_date = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
        });

        // 更新数据
        const api = this.$store.state.NEW_API;
        let updateData = {
          fcst_order_info: this.sampleData,
          fcst_order_item_info: this.sampleItemsTableData
        };
        fetchAPI('put', api + '/api/newfcst/fcst_order/', updateData, this).then((res) => {
          if (res && res.status === 200) {
            this.checkStatus = 'look';
            showModal.showMessage(this, "success", "修改成功");

            fetchAPI('get', api + '/api/newfcst/fcst_order_item/?fcst_order_id=' + this.childRowId, {}, this).then((res) => {
              if (res && res.status === 200) {
                this.sampleItemsTableData = res.data.data;
              }
            });
          }
        });
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
    created() {
      let divname = 'table';
      this.keydown(1,divname);
    },
    updated() {
    },
    //只执行一次
    mounted() {
      this.getSample();
      this.getCustomerInfo();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .test_detailed_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    position: relative;
    .test_detailed_main {
      height: 100%;
      width: 88%;
      .detailMessage {
        border: 1px solid #ccc;
        margin-bottom: 30px;
        p {
          padding: 20px 0px 0px 30px;
          font-size: 24px;
        }
        .detaMessageForm {
          padding-left: 30px;
          margin-top: 10px;
          .nochange {
            width: 60%;
            text-align: center;
            border-bottom: 1px solid #ccc;
          }
          .truechange {
            width: 60%;
            text-align: center;
          }
          .el-select {
            width: 60%;
          }
          .el-date-editor--date {
            width: 60%;
          }
        }
      }
      .composition {
        border: 1px solid #ccc;
        margin-bottom: 40px;
        p {
          padding: 20px 0px 0px 30px;
          font-size: 24px;
          margin-bottom: 20px;
        }
        overflow: hidden;
      }
      overflow: hidden;
    }
    .click-button {
      width: 9%;
      padding-top: 20px;
      position: fixed;
      right: 2%;
      .extra_card {
        display: flex;
        flex-flow: column;
        align-items: center;
        .el-button {
          width: 70px;
          display: block;
          margin: 0;
          font-size: 16px;
        }
        .el-button span p:nth-child(2) {
          margin-top: 3px;
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
        .el-dropdown {
          width: 100%;
          font-size: 18px;
          text-align: center;
          color: #4db3ff;
          margin: 5px 0 0 5px;
        }
      }
    }
  }
</style>

