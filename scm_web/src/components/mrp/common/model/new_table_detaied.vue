<template>
  <div class="test_detailed_contain">
    <div class="fl test_detailed_main main-card-box">
      <div clas s="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>基础信息</h4>
          </div>
          <el-card class="divCard">
            <el-col class="detailMessage">
              <el-form class="detaMessageForm" :model="detaMessageForm" ref="detaMessageForm">
                <el-col :span="12">
                  <el-form-item label="编码：" label-width="100px">
                    <el-input v-show="changeStatus" class="truechange viewTrueChange"
                              v-model="detaMessageForm.model.model_code"
                              :disabled="detaMessageForm.model.model_code && rowId>0 ?true:false"></el-input>
                    <el-input v-show="!changeStatus" class="nochange"
                              v-text="detaMessageForm.model.model_code"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="名称：" label-width="100px">
                    <el-input v-show="!changeStatus" class="nochange"
                              v-text="detaMessageForm.model.model_name"></el-input>
                    <el-input v-show="changeStatus" class="truechange"
                              v-model="detaMessageForm.model.model_name"></el-input>
                  </el-form-item>
                </el-col>
                <!--<el-col :span="12" v-if="tableType ===1">-->
                  <!--<el-form-item label="客户：" label-width="100px">-->
                    <!--<el-input v-show="!changeStatus" class="nochange"-->
                              <!--v-text="detaMessageForm.model.customer? detaMessageForm.model.customer.customer_name:''"></el-input>-->
                    <!--<el-select v-show="changeStatus" v-model="detaMessageForm.model.spec.customer_id" placeholder="请选择"-->
                               <!--:disabled="detaMessageForm.model.spec.customer_id && rowId>0 ?true:false">-->
                      <!--<el-option v-for="(item,key) in customerData" :key="key" :label="item.customer_name"-->
                                 <!--:value="item.customer_id"></el-option>-->
                    <!--</el-select>-->
                  <!--</el-form-item>-->
                <!--</el-col>-->
                <el-col :span="12" v-if="tableType ===1">
                  <el-form-item label="季节：" label-width="100px">
                    <el-input v-show="!changeStatus" class="nochange"
                              v-text="detaMessageForm.model.season? detaMessageForm.model.season.meta_name:''"></el-input>
                    <el-select v-show="changeStatus" v-model="detaMessageForm.model.spec.season_meta_id"
                               placeholder="请选择"
                               :disabled="detaMessageForm.model.spec.season_meta_id && rowId>0?true:false">
                      <el-option v-for="(item,key) in seasonData" :key="key" :label="item.meta_name"
                                 :value="item.meta_id">
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <div style="width: 100%">
                  <el-col :span="12" v-if="tableType ===1">
                    <el-form-item label="颜色：" label-width="100px">
                      <el-input v-show="!changeStatus" class="nochange"
                                v-text="detaMessageForm.model.spec.color"></el-input>
                      <el-input v-show="changeStatus" class="truechange"
                                v-model="detaMessageForm.model.spec.color"></el-input>
                    </el-form-item>
                  </el-col>
                </div>
                <el-col :span="12">
                  <el-form-item label="单位：" label-width="100px">
                    <el-input v-show="!changeStatus" class="nochange"
                              v-text="detaMessageForm.model.unit_meta.meta_name"></el-input>
                    <el-select v-show="changeStatus" v-model="detaMessageForm.model.unit_meta.meta_id" placeholder="请选择"
                               @change="getDialogInfo(detaMessageForm.model.unit_meta.meta_id)">
                      <el-option v-for="(item,key) in gridData" :key="key" :label="item.meta_name"
                                 :value="item.meta_id"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="tableType ===2">
                  <el-form-item label="坯布代号：" label-width="100px">
                    <el-input v-show="!changeStatus" class="nochange"
                              v-text="detaMessageForm.model.spec.bar_code"></el-input>
                    <el-input v-show="changeStatus" class="truechange"
                              v-model="detaMessageForm.model.spec.bar_code"></el-input>
                  </el-form-item>
                </el-col>
              </el-form>
            </el-col>
          </el-card>
        </div>
      </div>
      <table-extend v-if="tableType === 1 && tableExtendShow "
                    :extendForm="detaMessageForm.model.extend"
                    :extendChangeStatus="changeStatus">
      </table-extend>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>{{itemName}}信息</h4>
          </div>
          <div class="table">
            <el-card>
              <el-col class="composition">
                <el-table ref="multipleTable" :data="detaMessageForm.item" :row-style="tableRowStyle" style="width: 100%;"
                          border tooltip-effect="dark">
                  <el-table-column type="index" label="序号" width="70"></el-table-column>
                  <el-table-column v-for="(item,index) in tableColumn" :prop="item.columnProp" :label="item.columnName"
                                   :key="item.index">
                    <template scope="scope">
                      <el-input v-show="!changeStatus" v-text="scope.row[item.columnProp]"></el-input>
                      <el-input v-show="changeStatus" v-model="scope.row[item.columnProp]"
                                :disabled=" scope.row.disabled"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="120" v-if="changeStatus">
                    <template scope="scope">
                      <el-button size="small" @click="addCheckTab(scope.$index, scope.row)" v-show="!changeStatus">查看
                      </el-button>
                      <el-button size="small" @click="addMessage(scope.$index,scope.row)" v-show="changeStatus">+
                      </el-button>
                      <el-button size="small" @click="removeMessage(scope.$index,scope.row)"
                                 v-show="changeStatus && !scope.row.restore">-
                      </el-button>
                      <el-button size="small" @click="restoreBtn(scope.$index,scope.row)"
                                 v-show="changeStatus && scope.row.restore">恢复
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-card>
          </div>


        </div>
      </div>
    </div>
    <div class=" click-button">
      <el-card class="extra_card" v-if="!changeStatus">
        <el-button type="primary" size="large" @click="addData">新增</el-button>
        <el-button type="danger" size="large" @click="changesMethod">修改</el-button>
        <!-- <el-button type="text" size="large" @click="deleteMessageBtn">删除</el-button> -->
        <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                      更多<i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="consume" v-if="tableType == 2">备料形式损耗</el-dropdown-item>
            <el-dropdown-item command="delete">删除</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-card>
      <el-card class="extra_card" v-if="changeStatus">
        <el-button type="primary" size="large" @click="saveBtn">保存</el-button>
        <el-button type="danger" size="large" @click="addDataSaveBtn">
          <p>保存</p>
          <p>新增</p>
        </el-button>
        <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                      更多<i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="consume" v-if="tableType == 2">备料形式损耗</el-dropdown-item>
            <el-dropdown-item command="close">取消</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <!--<el-button type="text" size="large" @click="closeChangesMetod">取消</el-button>-->
      </el-card>
    </div>
    <el-dialog title="备料形式损耗" :visible.sync="consumeShow" size="tiny" @close="closeDialog">
      <div class="dialog_div">
        <el-button type="danger" size="large" @click="buttonUpdate" v-if="!consumeReset" :disabled="!changeStatus">修改</el-button>
        <el-button type="danger" size="large" @click="buttonSubmit"v-if="consumeReset">保存</el-button>
        <el-button type="error" size="large" @click="buttonReset" v-if="consumeReset">重置</el-button>
        <el-button type="error" size="large" @click="buttonCancel">取消</el-button>
      </div>
      <el-table :data="consumeData"
                border
                tooltip-effect="dark">
        <el-table-column label="备料形式" prop="meta_name"></el-table-column>
        <el-table-column label="损耗">
          <template scope="scope">
            <span v-if="!consumeReset">{{scope.row.meta_value}}</span>
            <el-input v-if="consumeReset"
                      v-model="scope.row.meta_value">
            </el-input>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
  import tableExtend from "./new_table_extend.vue";

  import {fetchAPI} from '../../../../utils/utils';
  import showModal from '../../../common/messageBox.js';
  import COMMON from '../../../common/common.js';

  export default {
    components: {tableExtend},
    name: 'new_table_detaied',
    props: {
      TABSValue: String,//tag显示值
      tabIndex: Number,//tag显示值
      rowId: Number,//物料ID
      tableName: String,//物料种类 成衣，面料，辅料
      tableType: Number//物料种类
    },
    data() {
      return {
        changeStatus: false, // 修改状态
        chlidTABSValue: this.TABSValue,//tag显示值
        chlidTabIndex: this.tabIndex,//tag显示值
        gridData: [],//下拉框 单位数据
        customerData: [],//下拉框 客户数据
        seasonData: [],//下拉框 季节数据
        tableRowIndex: "0", //删除状态控制参数
        itemName: "",//item标题信息
        consumeData: [], //备料形式
        consumeShow: false,//备料形式弹窗参数
        consumeReset: false,//备料形式弹窗重置按钮参数
        consumeImplement: false,//如新增面料model 则自动执行设置默认值 控制参数
        detaMessageForm: {
          model: {
            model_code: "",
            model_id: this.rowId,
            model_name: "",
            model_type_meta_id: this.tableType,
            extend: this.updateExtend(),
            spec: {
              color: "",
              bar_code: "",
              customer_id: "",
              season_meta_id: ""
            },
            unit_meta: {
              meta_id: '',
              meta_code: "",
              parent_meta_code: "",
              meta_name: ""
            },
            customer: {
              customer_id: 0,
              customer_name: ""
            },
            season: {
              meta_code: "",
              meta_id: 0,
              meta_name: ""
            }
          },
          item: [
            {
              item_code: "",
              item_id: "",
              item_name: "",
              model: this.rowId,
              extend: {},
              spec: {},
              disabled: false, //删除状态
              restore: false, // 恢复按钮状态
              addlocal: 0
            }
          ],
        },
        tableColumn: [],
        tableExtendShow: false, //扩展信息的展示
      }
    },
    methods: {
      //操作更多下拉菜单触发事件
      handleCommand(command) {
        if (command === "consume") {
          if (!this.consumeImplement) this.consumeImplement = true;
          this.getMetaPrList();
        } else if (command === "close") {
          this.closeChangesMetod();
        } else if (command === "delete") {
          this.deleteMessageBtn()
        }
      },
      //备料形式修改按钮
      buttonUpdate() {
        this.consumeReset = true;
      },
      //备料形式重置按钮
      buttonReset() {
        this.consumeData.forEach(row=>{
          if (row['meta_id'] === 37) {
              row['meta_value'] = 1;
            } else {
              row['meta_value'] = 1.1;
            }
        })
      },
      //备料形式保存按钮
      buttonSubmit() {
        if (!this.detaMessageForm.model.extend.consume_pr_form) this.detaMessageForm.model.extend['consume_pr_form'] = {};
        this.consumeData.forEach(row => {
          this.detaMessageForm.model.extend.consume_pr_form[row.meta_code] = row['meta_value'];
        });
        this.consumeReset = false;
      },
      //备料形式取消按钮
      buttonCancel() {
        this.closeDialog();
      },
      //关闭弹窗的回调
      closeDialog() {
        this.consumeShow = false;
        this.consumeReset = false;
      },
      //新增按钮
      addData() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.tableName + '-新增',
          name: newTabName,
          closable: true,
          rowId: 0,
          tabName: "modelInfo",
          tableType: this.tableType,
          tableName: this.tableName
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      //保存并新增
      addDataSaveBtn() {
        this.saveBtn(this.addData);
      },
      // 点击修改按钮
      changesMethod() {
        this.changeStatus = true;
      },
      // 取消按钮
      closeChangesMetod() {
        showModal.showModal(this, this.closeChangesMetodConfirm, "", "此操作将不保存数据, 是否继续?", '操作提示', "是", "否");
      },
      //取消确定按钮执行函数
      closeChangesMetodConfirm() {
        this.changeStatus = false;
        if (this.detaMessageForm.model.model_id > 0) {
          this.getRequstModel();
          this.getRequestItem();
          this.ifItemCount();
        } else {
          this.$emit('CloseTab');
        }
        showModal.showMessage(this, "success", "取消成功");
      },
      // 保存按钮
      saveBtn(addFun) {
        if (this.detaMessageForm.model.model_name === " " || this.detaMessageForm.model.model_name === null || !this.detaMessageForm.model.model_name) {
          showModal.showModal(this, "", "", "名称不能为空，请填写！", '错误提示');
          return;
        }
        if (this.tableType === 1) {
//          if (this.detaMessageForm.model.spec.customer_id === "" || !this.detaMessageForm.model.spec.customer_id) {
//            showModal.showModal(this, "", "", "客户不能为空，请选择！", '错误提示');
//            return;
//          }
          if (this.detaMessageForm.model.spec.season_meta_id === "" || !this.detaMessageForm.model.spec.season_meta_id) {
            showModal.showModal(this, "", "", "季节不能为空，请选择！", '错误提示');
            return;
          }
        }
        this.saveBtnConfirm(addFun);
      },
      //保存按钮 确定按钮执行函数
      saveBtnConfirm(addFun) {
        if (this.tableType === 1) {
          this.detaMessageForm.model.extend.elastic_week_start.value = COMMON.formatDate(this.detaMessageForm.model.extend.elastic_week_start.value);
          this.detaMessageForm.model.extend.elastic_week_end.value = COMMON.formatDate(this.detaMessageForm.model.extend.elastic_week_end.value);
          this.detaMessageForm.model.extend.delivery_week_first.value = COMMON.formatDate(this.detaMessageForm.model.extend.delivery_week_first.value);
          this.detaMessageForm.model.extend.delivery_week_last.value = COMMON.formatDate(this.detaMessageForm.model.extend.delivery_week_last.value);
        }
        this.detaMessageForm.item = this.detaMessageForm.item.filter(this.isDelete);
        let url = "/api/mrp_order/mrp_model/";
        let text = "保存成功";
        let type = "post";
        if (this.detaMessageForm.model.model_id > 0) {
          url = "/api/mrp_order/mrp_model/";
          text = "修改成功";
          type = 'put';
        }
        if (this.tableType !== 1) {
          delete this.detaMessageForm.model.spec.customer_id
          delete this.detaMessageForm.model.spec.season_meta_id
        }
        this.vmRequst(url, function (that, objRes) {
          if (objRes.data.code === 1001) {
            showModal.showModal(that, "", "", objRes.data.message, '错误提示');
          } else {
            showModal.showMessage(that, "success", text);
            that.changeStatus = false;
            that.detaMessageForm = objRes.data;
            that.tableRowIndex = "";
            that.updateItem(that.detaMessageForm.item);
            that.ifItemCount();
            if (typeof addFun == "function") { //保存新增时执行新增的事件
              that.$emit("CloseTab");
              addFun();
            }
          }
        }, type, this.detaMessageForm);
      },
      //保存按钮数据处理函数将前端新建又删除的数据剔除
      isDelete(value, key, array) {
        return ((value.delete !== 0 || value.addlocal !== 0) && (value.item_name || value.item_code));
      },
      //取消按钮数据处理函数将前端新建的数据剔除
      isClose(value, key, array) {
        return (value.addlocal !== 0);
      },
      // 删除按钮
      deleteMessageBtn() {
        showModal.showModal(this, this.deleteMessageBtnConfirm, "", "此操作将永久删除该信息, 是否继续?", '操作提示', "是", "否");
      },
      //删除按钮 确定按钮执行函数
      deleteMessageBtnConfirm() {
        this.vmRequst('/api/mrp_order/mrp_models/', function (that, objRes) {
          showModal.showMessage(that, "success", "删除成功");
          that.$emit('CloseTab');
        }, 'delete', {data: [this.detaMessageForm.model.model_id]});
      },
      // 添加组成
      addMessage(index, row) {
        let addTableData = {
          item_code: "",
          item_id: "",
          item_name: "",
          model: this.detaMessageForm.model.model_id,
          extend: {},
          spec: {},
          disabled: false, //删除状态
          restore: false, // 恢复按钮状态
          addlocal: 0
        };
        this.detaMessageForm.item.splice(index + 1, 0, addTableData);
      },
      // 删除组成
      removeMessage(index, row) {
        if (row.item_id > 0 || row.item_name || row.item_code) {
          this.detaMessageForm.item = this.detaMessageForm.item.map(function (currentValue, key) {
            if (index === key) {
              currentValue.disabled = true;
              currentValue.delete = 0;
              currentValue.restore = true;
            }
            return currentValue;
          });
          this.tableRowIndex = this.tableRowIndex + ',' + index;
        } else {
          this.detaMessageForm.item.splice(index, 1);
          this.ifItemCount();
        }
      },
      //判断item条数如为零则加一条
      ifItemCount() {
        if (this.detaMessageForm.item.length === 0) {
          this.addMessage(0);
        }
      },
      //控制table行样式
      tableRowStyle: function (row, index) {
        if (this.tableRowIndex.indexOf(',' + index) > 0) {
          return 'background-color:#F5F5F5;'
        } else {
          return ''
        }
      },
      // 恢复组成
      restoreBtn(index, row) {
        // this.tableData.splice(index, 1)
        this.detaMessageForm.item = this.detaMessageForm.item.map(function (currentValue, key) {
          if (index === key) {
            currentValue.disabled = false;
            delete currentValue.delete;
            currentValue.restore = false;
          }
          return currentValue;
        })
        this.tableRowIndex = this.tableRowIndex.replace(',' + index, "");
      },
      //接受弹窗的数据
      getDialogInfo(id) {
        this.gridData.forEach(res => {
          if (id === res.meta_id) {
            this.detaMessageForm.model.unit_meta = res;
          }
        });
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        let newTabName = ++this.chlidTabIndex + '';
        let watchChildTABS = {
          title: this.tableName + '规格详细信息',
          name: newTabName,
          closable: true,
          rowId: row.detaMessageForm.model.model_id
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS)
      },
      /*
      * 网络请求数据
      * type,//请求类型 get,post....
      * url,//路径
      * options,//post时数据*/
      vmRequst(url, successfun, type = 'get', options = 'null') {
        const api = this.$store.state.NEW_API;
        let apiUrl = api + url;
        fetchAPI(type, apiUrl, options, this).then((res) => {
          if ((res && res.status == 200) || (type == "delete" && res && res.status == 204)) {
            typeof successfun == "function" && successfun(this, res);
          }
        })
      },
      //获取item列字段
      getTableColumn() {
        switch (this.tableType) {
          case 2:
            this.itemName = "颜色";
            break;
          case 3:
            this.itemName = "规格";
            break;
          default:
            this.itemName = "尺码";
        }
        this.tableColumn = [
          {
            columnName: "编码",
            columnProp: "item_code"
          }, {
            columnName: this.itemName,
            columnProp: "item_name"
          }
        ];
      },
      //网络获取item信息的时候进行状态赋值
      updateItem(resData) {
        if (resData.length === 0) return;
        for (let x in resData) {
          resData[x]['disabled'] = false;
          resData[x]['restore'] = false;
        }
        this.detaMessageForm.item = resData;
      },
      //获取meta备料形式列表
      getMetaPrList() {
        COMMON.getMetaList(this, 36).then(res => {
          this.upConsumeData(res.data);
          this.consumeData = res.data;
          if (this.consumeImplement) this.consumeShow = true;
          if (!this.consumeImplement) this.buttonSubmit();
        });
      },
      //根据meta备料形式获取model数据中的meta备料形式的损耗值
      upConsumeData(res) {
        if (!this.detaMessageForm.model.extend.consume_pr_form) {
          res.forEach(row => {
            if (row['meta_id'] === 37) {
              row['meta_value'] = 1;
            } else {
              row['meta_value'] = 1.1;
            }
          });
          return;
        }
        res.forEach(row => {
          row['meta_value'] = this.detaMessageForm.model.extend.consume_pr_form[row.meta_code];
        });
      },
      //网络请求model表头信息
      getRequstModel() {
        this.vmRequst('/api/mrp_order/mrp_model/?model_id=' + this.detaMessageForm.model.model_id, function (that, objRes) {
          if (objRes.data.model.unit_meta === null || !objRes.data.model.unit_meta) {
            objRes.data.model.unit_meta = {
              meta_id: 0,
              meta_code: "",
              parent_meta_code: "",
              meta_name: ""
            };
          }
          that.detaMessageForm.model = objRes.data.model;
          if (that.tableType === 1) {
            that.updateExtend(true);
            that.$set(that.$data, 'tableExtendShow', true);
          }
        });
      },
      //网络请求Item表体信息
      getRequestItem() {
        this.vmRequst('/api/mrp_order/mrp_models/?model_id=' + this.detaMessageForm.model.model_id, function (that, objRes) {
          that.updateItem(objRes.data);
        });
      },
      //成衣model 更新extend
      updateExtend(extend = false) {
        let extendIntialData = {
          iman_code: {
            name: "款号",
            value: ''
          },
          mpc_code: {
            name: "MPC",
            value: ''
          },
          po_duration: {
            name: "采购天数",
            value: 56
          },
          produce_duration: {
            name: "生产天数",
            value: 24
          },
          delivery_duration: {
            name: "交货天数",
            value: 2
          },
          safe_duration: {
            name: "安全天数",
            value: 0
          },
          cut_produce_duration: {
            name: "裁剪天数",
            value: 2
          },
          pr_method: {
            name: "备料方式",
            value: null
          },
          fabric_ratio: {
            name: "色布比率",
            value: 0
          },
          rough_ratio: {
            name: "毛坯比率",
            value: 0
          },
          yarn_ratio: {
            name: "纱比率",
            value: 0
          },
          elastic_higher_ratio: {
            name: "上弹比率",
            value: 0
          },
          elastic_lower_ratio: {
            name: "下弹比率",
            value: 0
          },
          elastic_week_start: {
            name: "弹性起始周",
            value: null
          },
          elastic_week_end: {
            name: "弹性结束周",
            value: null
          },
          delivery_week_first: {
            name: "首单交期周",
            value: null
          },
          delivery_week_last: {
            name: "尾单交期周",
            value: null
          }
        };
        if (this.tableType === 1 && (this.rowId === 0 || !this.rowId)) {
          // this.tableExtendShow = true;
          return extendIntialData;
        } else if (this.tableType === 1 && this.rowId > 0 && extend) {
          let modelExtend = ['iman_code', 'mpc_code', 'po_duration', 'produce_duration', 'delivery_duration', 'safe_duration',
            'cut_produce_duration', 'pr_method', 'fabric_ratio', 'rough_ratio', 'yarn_ratio', 'elastic_higher_ratio',
            'elastic_lower_ratio', 'elastic_week_start', 'elastic_week_end', 'delivery_week_first', 'delivery_week_last']
          modelExtend.forEach(res => {
            if (!this.detaMessageForm.model.extend[res]) {
              this.detaMessageForm.model.extend[res] = {
                name: extendIntialData[res].name,
                value: ''
              }
            }
          })

        } else {
          return {}
        }
      },
      //网络获取基础数据 单位等...
      getBasicData() {
        //Model的item列表显示字段
        this.getTableColumn();
        //获取meta客户列表
        COMMON.getCustomerList(this).then(res => {
          this.customerData = res.data.data;
        });
        //单位
        COMMON.getMetaList(this, 10).then(res => {
          this.gridData = res.data;
        });
        //季节
        COMMON.getMetaList(this, 43).then(res => {
          this.seasonData = res.data;
        });
      }
    },
    //实列完成后按rowid请求相应的数据
    created() {
    },
    updated() {
      let divname = 'table';
      this.keydown(2,divname);
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    computed: {},
    mounted() {
      this.getBasicData();
      if (this.detaMessageForm.model.model_id == 0 || this.detaMessageForm.model.model_id == " " || this.detaMessageForm.model.model_id == null) {
        this.changesMethod();
        this.vmRequst('/api/mat_models/make_model_no/', function (that, objRes) {
          if (objRes.data.code !== 0) return;
          that.detaMessageForm.model.model_code = objRes.data.message;
        }, 'post', {model_type_meta_id: this.tableType});
        if (this.tableType === 1) this.$set(this.$data, 'tableExtendShow', true);
        if (this.tableType === 2) { //2为面料model
          this.getMetaPrList();
        }
        return;
      }
      //请求model信息
      this.getRequstModel();
      //请求model_item信息
      this.getRequestItem();
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
            width: 85%;
            text-align: center;
            border-bottom: 1px solid #ccc;
            height: 36px;
          }
          .el-select {
            width: 85%;
          }
          .truechange {
            width: 85%;
            text-align: center;
          }
          .viewTrueChange {
            input {
              border: none;
            }
          }
        }
      }
      .composition {
        border: 1px solid #ccc;
        margin-bottom: 40px;
      }
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
    .el-dialog {
      .dialog_div {
        margin-bottom: 10px;
        text-align: right;
        .el-button {
          margin-right: 10px;
        }
      }
    }
    .el-table__body-wrapper {
      border: 1px solid blue;
    }
  }
</style>

