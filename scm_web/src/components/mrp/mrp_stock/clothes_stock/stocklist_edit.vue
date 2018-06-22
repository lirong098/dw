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
                  <el-form-item label="备料单号：">
                    <el-input class="nochange" v-text="detaMessageForm.fcst_pr.fcst_pr_no"
                              v-show="!changeStatus"></el-input>
                    <el-input class="truechange" v-model="detaMessageForm.fcst_pr.fcst_pr_no" v-show="changeStatus"
                              disabled></el-input>
                  </el-form-item>
                </el-col>
                <!--<el-col :span="12">-->
                <!--<el-form-item label="备料类型：">-->
                <!--<el-select v-model="detaMessageForm.fcst_pr.fcst_pr_type_meta_id.meta_id"-->
                <!--placeholder="请选择"-->
                <!--disabled-->
                <!--@change="setMetaList(detaMessageForm.fcst_pr.fcst_pr_type_meta_id.meta_id)">-->
                <!--<el-option label="请选择" :value="0"></el-option>-->
                <!--<el-option v-for="(item,key) in gridData" :key="item.meta_id" :label="item.meta_name"-->
                <!--:value="item.meta_id"></el-option>-->
                <!--</el-select>-->
                <!--</el-form-item>-->
                <!--</el-col>-->
                <el-col :span="12">
                  <el-form-item label="备料交期：">
                    <el-input class="nochange" v-text="detaMessageForm.fcst_pr.delivery_date"
                              v-show="!changeStatus"></el-input>
                    <el-date-picker v-model="detaMessageForm.fcst_pr.delivery_date" type="date" placeholder="选择日期"
                                    :picker-options="pickerOptions" @change="changeDate"
                                    v-show="changeStatus">
                    </el-date-picker>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="单据日期：">
                    <el-input class="nochange"
                              v-text="detaMessageForm.fcst_pr.deal_date ?detaMessageForm.fcst_pr.deal_date:'2222'"
                              v-show="!changeStatus"></el-input>
                    <el-date-picker v-model="detaMessageForm.fcst_pr.deal_date" type="date" placeholder="选择日期"
                                    :picker-options="pickerOptions" @change="changeDate"
                                    v-show="changeStatus">
                    </el-date-picker>
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
            <h4>{{itemName}}信息</h4>
          </div>
          <el-card>
            <el-col class="composition">
              <el-table ref="multipleTable"
                        :data="detaMessageForm.fcst_pr_item"
                        :row-style="tableRowStyle"
                        highlight-current-row
                        @current-change="handleCurrentChange"
                        style="width: 100%;"
                        border
                        tooltip-effect="dark">
                <el-table-column type="index" label="序号" width="70"></el-table-column>
                <el-table-column label="Model" show-overflow-tooltip>
                  <template scope="scope">
                    <el-input v-show="!changeStatus"
                              v-text="scope.row.item.model.model_code && scope.row.item.model.model_name ?
                              scope.row.item.model.spec.color ?
                                scope.row.item.model.model_code+' - '+scope.row.item.model.model_name+' - '+scope.row.item.model.spec.color
                                : scope.row.item.model.model_code+' - '+scope.row.item.model.model_name
                              :''">
                    </el-input>
                    <el-input v-show="changeStatus"
                              icon="more"
                              :on-icon-click="()=>selectModel(scope.$index,scope.row)"
                              :disabled="scope.row.disabled"
                              :value="scope.row.item.model.model_code && scope.row.item.model.model_name ?
                              scope.row.item.model.spec.color ?
                                scope.row.item.model.model_code+' - '+scope.row.item.model.model_name+' - '+scope.row.item.model.spec.color
                                : scope.row.item.model.model_code+' - '+scope.row.item.model.model_name
                              :''">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="Item" show-overflow-tooltip>
                  <template scope="scope">
                    <el-input v-show="!changeStatus"
                              v-text="scope.row.item.item_code && scope.row.item.item_name ? scope.row.item.item_code+'-'+scope.row.item.item_name:''">
                    </el-input>
                    <el-input v-show="changeStatus"
                              icon="more"
                              :on-icon-click="()=>selectItem(scope.$index,scope.row)"
                              :disabled="scope.row.disabled"
                              :value="scope.row.item.item_code && scope.row.item.item_name ? scope.row.item.item_code+'-'+scope.row.item.item_name:''">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="备料形式" show-overflow-tooltip
                                 v-if="detaMessageForm.fcst_pr_item['0'].pr_form_meta">
                  <template scope="scope">
                    <el-select v-model="scope.row.pr_form_meta.meta_id" placeholder="请选择" v-if="changeStatus"
                               :disabled="propData.length >0 ? true:false">
                      <el-option
                        v-for="(item,index) in consumeData"
                        :key="index"
                        :label="item.meta_name"
                        :value="item.meta_id">
                      </el-option>
                    </el-select>
                    <span v-else>{{scope.row.pr_form_meta.meta_name}}</span>
                  </template>
                </el-table-column>
                <el-table-column label="数量" width="140">
                  <template scope="scope">
                    <span v-if="!changeStatus">{{scope.row.quantity === 0 ? '' : scope.row.quantity}}</span>
                    <el-input v-else v-model="scope.row.quantity" :disabled="scope.row.disabled"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="单位" prop="item.model.unit_meta.meta_name" width="120"></el-table-column>
                <el-table-column label="操作" width="140" fixed="right">
                  <!--:width="column_width"-->
                  <template scope="scope">
                    <el-button size="small" @click="addCheckTab(scope.$index, scope.row)"
                               v-show="!changeStatus && detaMessageForm.fcst_pr.fcst_pr_id">查看
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
          <el-dialog :title="dialogName" style="float: left" :visible.sync="moreAddBtn" size="large">
            <modellist @getDialogInfo="getDialogInfo"
                       :model_id="model_id"
                       :onlyGetItem="onlyGetItem"
                       :tableName="tableName"
                       :tableType="tableType"
                       v-if="moreAddBtn">
            </modellist>
          </el-dialog>
        </div>
      </div>
    </div>
    <div class=" click-button">
      <el-card class="extra_card" v-if="changeStatus === false && (detaMessageForm.fcst_pr.fcst_pr_id)">
        <el-button type="primary" size="large" @click="addData">新增</el-button>
        <el-button type="danger" size="large" @click="changesMethod">修改</el-button>
        <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                      更多<i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="mrp" v-if="showDropdown">计算MRP</el-dropdown-item>
            <el-dropdown-item command="delete">删除</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-card>
      <el-card class="extra_card" v-if="changeStatus !== false || !(detaMessageForm.fcst_pr.fcst_pr_id)">
        <el-button type="success" size="primary" @click="saveBtn">保存</el-button>
        <el-button type="success" size="danger" @click="addDataSaveBtn">
          <p>保存</p>
          <p>新增</p>
        </el-button>
        <el-button type="text" size="large" @click="closeChangesMetod">取消</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
  //组件
  import modellist from "../../../common/model_dialog/dialog_model.vue";
  import mrppreview from "./mrp_preview.vue";
  //公共文件
  import requst from "../../../common/vmrequst.js";
  import showModal from '../../../common/messageBox.js';
  import {fetchAPI} from "../../../../utils/utils.js";
  import COMMON from '../../../common/common.js';

  export default {
    components: {modellist, mrppreview},
    name: 'stocklist_edit',
    props: {
      TABSValue: String,//tag显示值
      tabIndex: Number,//tag显示值
      fcstName: String,
      rowId: {
        type: Number,
        default: 0
      },//物料ID
      fcstType: {
        type: Number,
        default: 1
      }, //1 成衣备料 2 成衣实单
      propData: {//接受 detaMessageForm.fcst_pr_item
        type: Array,
        default: () => {
          return []
        }
      }
    },
    data() {
      return {
        column_width: 120,//操作列的width
        changeStatus: false, // 修改状态
        moreAddBtn: false, //控制modle 弹窗
        iconIndex: 0,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        detaMessageForm: {
          fcst_pr: {
            fcst_pr_no: "",
            fcst_pr_id: this.rowId,
            delivery_date: COMMON.formatDate(),
            deal_date: COMMON.formatDate(),
            fcst_pr_type_meta_id: {
              meta_code: "",
              meta_id: this.getStockType(),
              meta_name: "请选择",
              parent_meta_code: "",
              extend: {}
            },
            extend: {},
            spec: {}
          },
          fcst_pr_item: [{
            fcst_pr_item_id: 0,
            item: {
              item_code: "",
              item_id: 0,
              item_name: "",
              extend: {},
              spec: {},
              model: {
                model_id: 0,
                model_code: "",
                model_name: "",
                unit_meta: {
                  meta_name: ""
                }
              },

            },
            quantity: 0,
            spec: {},
            extend: {},
            pr_form_meta: {
              meta_code: "",
              meta_id: 37,
              meta_name: "",
              parent_meta_code: "",
              extend: {}
            },
            fcst_pr: this.rowId,
            disabled: false, //删除状态
            restore: false, // 恢复按钮状态
            addlocal: 0
          }],
          fcst_order_id: this.propData.length > 0 ? this.propData['0'].fcst_order_id : 0
        },
        //gridData: [],//弹窗数据
        tableRowIndex: "0", //删除状态控制参数
        itemName: "Model",//item标题信息
        dialogName: "",
        pickerOptions: { //选择日期数据
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },
        onlyGetItem: false, //model弹窗的参数 true时 只获取Item
        model_id: 0, //根据model_id显示详情页
        tableName: "成衣",//查看model详情 需要 物料种类 成衣，面料，辅料
        tableType: 1,//查看model详情 需要 物料种类
        currentRow: [], //当前高亮的数据
        showDropdown: false, //是否显示计算MRP
        consumeData: [] //备料形式 数据
      }
    },
    methods: {
      //高亮当前行
      handleCurrentChange(val) {
        this.currentRow = val;
      },
      //新增按钮
      addData() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.fcstName + ' - 新增',
          name: newTabName,
          closable: true,
          rowId: 0
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      //保存并新增
      addDataSaveBtn() {
        this.saveBtn(this.addData);
      },
      //备料类型下拉框
//      setMetaList(val) {
//        if (val === 0) return;
//        this.gridData.forEach(res => {
//          if (res.meta_id == val) {
//            this.detaMessageForm.fcst_pr.fcst_pr_type_meta_id = res;
//          }
//        });
//      },
      // 点击修改按钮
      changesMethod() {
        this.changeStatus = true;
        this.column_width = 450;
      },
      // 取消按钮
      closeChangesMetod() {
        showModal.showModal(this, this.closeChangesMetodConfirm, "", "此操作将不保存数据, 是否继续?", '操作提示', "是", "否");
      },
      //取消确定按钮执行函数
      closeChangesMetodConfirm() {
        if (this.detaMessageForm.fcst_pr.fcst_pr_id > 0) {
          //恢复原数据
          this.getRequestItem();
          this.getRequstModel();
        } else {
          //关闭新增页
          this.$emit('CloseTab');
        }
        this.tableRowIndex = "";
        this.changeStatus = false;
        this.column_width = 120;
        showModal.showMessage(this, "success", "取消成功");
      },
      // 保存按钮
      saveBtn(addFun) {
        if (this.detaMessageForm.fcst_pr.fcst_pr_no == " " || this.detaMessageForm.fcst_pr.fcst_pr_no == null || !this.detaMessageForm.fcst_pr.fcst_pr_no) {
          showModal.showModal(this, "", "", "名称不能为空，请填写！", '错误提示');
          return;
        }
        this.saveBtnConfirm(addFun);
      },
      //保存按钮 确定按钮执行函数
      saveBtnConfirm(addFun) {
        this.detaMessageForm.fcst_pr_item = this.detaMessageForm.fcst_pr_item.filter(this.isDelete);
        let url = "/api/mat_models/fcst_prs/";
        let text = "保存成功";
        let type = "post";
        if (this.detaMessageForm.fcst_pr.fcst_pr_id > 0) {
          url = "/api/mat_models/fcst_pr/";
          text = "修改成功";
          type = 'put';
        }
        console.log("shuju", this.detaMessageForm);
        requst.requst(this, url, function (that, objRes) {
          objRes.data.fcst_pr.deal_date = COMMON.formatDate();
          that.detaMessageForm = objRes.data;
          that.tableRowIndex = "";
          that.updateItem(that.detaMessageForm.fcst_pr_item);
          that.ifItemCount();
          that.changeStatus = false;
          if (typeof addFun == "function") {
            that.$emit('CloseTab');
            addFun();
          }
          showModal.showMessage(that, "success", text);
        }, type, this.detaMessageForm);
      },
      //保存按钮数据处理函数将前端新建又删除的数据剔除
      isDelete(value, key, array) {
        return (value.delete !== 0 || value.addlocal !== 0);
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
        requst.requst(this, "/api/mat_models/fcst_prs/", function (that, objRes) {
          showModal.showMessage(that, "success", "删除成功");
          that.$emit('CloseTab');
        }, 'delete', {data: [this.detaMessageForm.fcst_pr.fcst_pr_id]});
      },
      // 添加组成
      addMessage(index, row) {
        let addTableData = {
          fcst_pr_item_id: 0,
          item: {
            item_code: "",
            item_id: 0,
            item_name: "",
            extend: {},
            spec: {},
            model: {
              model_id: 0,
              model_code: "",
              model_name: "",
              unit_meta: {
                meta_name: ""
              }
            },
          },
          quantity: 0,
          spec: {},
          pr_form_meta: {
            meta_code: "",
            meta_id: 37,
            meta_name: "",
            parent_meta_code: "",
            extend: {}
          },
          extend: {},
          fcst_pr: this.rowId,
          disabled: false, //删除状态
          restore: false, // 恢复按钮状态
          addlocal: 0
        };
        this.detaMessageForm.fcst_pr_item.splice(index + 1, 0, addTableData);
      },
      // 删除组成
      removeMessage(index, row) {
        if (row.fcst_pr_item_id > 0 || row.item.item_name || row.item.model.model_code) {
          this.detaMessageForm.fcst_pr_item = this.detaMessageForm.fcst_pr_item.map(function (currentValue, key) {
            if (index === key) {
              currentValue.disabled = true;
              currentValue.delete = 0;
              currentValue.restore = true;
            }
            return currentValue;
          });
          this.tableRowIndex = this.tableRowIndex + ',' + row.fcst_pr_item_id + '-' + row.item.item_id + '-' + row.item.item_name;
        } else {
          this.detaMessageForm.fcst_pr_item.splice(index, 1);
          this.ifItemCount();
        }
      },
      //判断item条数如为零则加一条
      ifItemCount() {
        if (this.detaMessageForm.fcst_pr_item.length === 0) {
          this.addMessage(0);
        }
      },
      //控制table行样式
      tableRowStyle: function (row, index) {
        if (this.tableRowIndex.indexOf(',' + row.fcst_pr_item_id + '-' + row.item.item_id + '-' + row.item.item_name) > 0) {
          return 'background-color:#F6EEEF;'
        } else {
          return ""
        }
      },
      // 恢复组成
      restoreBtn(index, row) {
        this.detaMessageForm.fcst_pr_item = this.detaMessageForm.fcst_pr_item.map(function (currentValue, key) {
          if (index === key) {
            currentValue.disabled = false;
            delete currentValue.delete;
            currentValue.restore = false;
          }
          return currentValue;
        })
        this.tableRowIndex = this.tableRowIndex.replace(',' + row.fcst_pr_item_id + '-' + row.item.item_id + '-' + row.item.item_name, "");
      },
      //接受弹窗的数据
      getDialogInfo(row, model_id) {
        if (!this.onlyGetItem) { //false时：选择model数据
          this.getModelInfo(row, model_id);
        }
        else { //true时：选择Item数据
          this.getItemInfo(row, model_id);
        }
        this.moreAddBtn = false;
      },
      //获取选择弹窗的model信息
      getModelInfo(obj, model_id) {
        if (!obj) return;
        if (obj.model_item === "" || !obj.model_item) {
          this.detaMessageForm.fcst_pr_item[this.iconIndex].item = {
            item_code: "",
            item_id: 0,
            item_name: "",
            extend: {},
            spec: {},
            model: obj
          };
          return;
        }
        for (let i in obj.model_item) {
          if (i === '0') {
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item = {
              item_code: obj.model_item[0].item_code,
              item_id: obj.model_item[0].item_id,
              item_name: obj.model_item[0].item_name,
              extend: obj.model_item[0].extend,
              spec: obj.model_item[0].spec,
              model: obj
            };
            //           this.detaMessageForm.fcst_pr_item[this.iconIndex].quantity =0;
          } else {
            this.detaMessageForm.fcst_pr_item.splice(
              this.iconIndex + 1,
              0,
              {
                fcst_pr_item_id: 0,
                item: {
                  item_code: obj.model_item[i].item_code,
                  item_id: obj.model_item[i].item_id,
                  item_name: obj.model_item[i].item_name,
                  extend: obj.model_item[i].extend,
                  spec: obj.model_item[i].spec,
                  model: obj
                },
                quantity: 0,
                spec: {},
                pr_form_meta: {
                  meta_code: "",
                  meta_id: 37,
                  meta_name: "",
                  parent_meta_code: "",
                  extend: {}
                },
                extend: {},
                fcst_pr: this.rowId,
                disabled: false, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0
              }
            );
          }
        }
        ;
      },
      //获取选择弹窗的Item信息
      getItemInfo(obj, model_id) {
        if (obj.length === 0) return;
        for (let i in obj) {
          if (i === '0') {
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item.item_code = obj[i].item_code;
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item.item_id = obj[i].item_id;
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item.item_name = obj[i].item_name;
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item.extend = obj[i].extend;
            this.detaMessageForm.fcst_pr_item[this.iconIndex].item.spec = obj[i].spec;
          } else {
            this.detaMessageForm.fcst_pr_item.splice(
              this.iconIndex + 1,
              0,
              {
                fcst_pr_item_id: 0,
                item: {
                  item_code: obj[i].item_code,
                  item_id: obj[i].item_id,
                  item_name: obj[i].item_name,
                  extend: obj[i].extend,
                  spec: obj[i].spec,
                  model: this.detaMessageForm.fcst_pr_item[this.iconIndex].item.model
                },
                quantity: 0,
                spec: {},
                pr_form_meta: {
                  meta_code: "",
                  meta_id: 37,
                  meta_name: "",
                  parent_meta_code: "",
                  extend: {}
                },
                extend: {},
                fcst_pr: this.rowId,
                disabled: false, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0
              }
            );
          }
        }
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        console.log(row);
        this.model_id = row.item.model.model_id; //根据model_id显示详情页
        this.dialogName = row.item.model.model_name + "详情";
        this.tableName = row.item.model.model_type_meta_id.meta_name;
        this.tableType = row.item.model.model_type_meta_id.meta_id;
        this.moreAddBtn = true;
      },
      //点击Model列的选择按钮
      selectModel(index, row) {
        this.$refs.multipleTable.setCurrentRow(row);//高亮当前行
        this.onlyGetItem = false;
        this.model_id = 0;//选择modelList 将model_id 设为 0
        this.dialogName = "选择model";
        this.moreAddBtn = true;
        this.iconIndex = index;
      },
      //点击Item列的选择按钮
      selectItem(index, row) {
        this.$refs.multipleTable.setCurrentRow(row);//高亮当前行
        if (row.item.model.model_id && row.item.model.model_id > 0) {
          this.onlyGetItem = true;
          this.model_id = row.item.model.model_id;//选择Item 将model_id 设为 当前的row的model_id
          this.dialogName = "选择Item";
          this.moreAddBtn = true;
          this.iconIndex = index;
        }
        else { //没有model_id 则弹出选择model的list
          this.selectModel(index, row);
        }
      },
      //网络获取item信息的时候进行状态赋值 处理相同model合并的问题
      updateItem(resData) {
        if (resData.length === 0) return;
        // let nowmodelId = 0;
        for (let x in resData) {
//          if (nowmodelId === resData[x].item.model.model_id) {
//            resData[x]['tableColumnShow'] = false;
//          } else {
//            resData[x]['tableColumnShow'] = true;
//            nowmodelId = resData[x].item.model.model_id;
//          }
          resData[x]['disabled'] = false;
          resData[x]['restore'] = false;
        }
        this.detaMessageForm.fcst_pr_item = resData;
      },
      //获取meta列表
//      getMetaList() {
//        requst.requst(this, "/api/mat_models/metas/?parent_meta_code=fcst", function (that, objRes) {
//          console.log(objRes.data);
//          that.gridData = objRes.data;
//        });
//      },
      //网络请求model表头信息
      getRequstModel() {
        requst.requst(this, "/api/mat_models/fcst_pr/?fcst_pr_id=" + this.detaMessageForm.fcst_pr.fcst_pr_id, function (that, objRes) {
          objRes.data.fcst_pr.deal_date = COMMON.formatDate();
          that.detaMessageForm.fcst_pr = objRes.data.fcst_pr;
        });
      },
      //网络请求ITem表体信息
      getRequestItem() {
        requst.requst(this, "/api/mat_models/fcst_pr_items/?fcst_pr_id=" + this.detaMessageForm.fcst_pr.fcst_pr_id, function (that, objRes) {
          that.updateItem(objRes.data);
        });
      },
      //回调日期
      changeDate(val) {
        this.detaMessageForm.fcst_pr.delivery_date = val;
      },
      //操作更多下拉菜单触发事件
      handleCommand(command) {
        if (command == "mrp") {
          this.mrp();
        } else if (command == "delete") {
          this.deleteMessageBtn();
        }
      },
      //计算mrp按钮
      mrp() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.fcstName + " - MRP预览",
          name: newTabName,
          closable: true,
          rowId: this.detaMessageForm.fcst_pr.fcst_pr_id,
          tabName: "preview"
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      //根据类型获取参数
      getStockType() {
        let id = 0;
        switch (this.fcstType) {
          case 1:
            id = 16;
            this.showDropdown = true;
            break;
          case 2:
            id = 14;
            this.showDropdown = true;
            break;
          case 3:
            id = 13;
            break;
          case 4:
            id = 12;
            break;
          case 5:
            id = 12;
            break;
          case 6:
            id = 16;
            break;
          case 7:
            id = 12;
            break;
          case 8:
            id = 35;
            break;
        }
        return id;
      },

    },
    //实列完成后按rowid请求相应的数据
    created() {
      //this.getMetaList();
    },
    updated() {
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
      this.getStockType();
      //备料形式
      COMMON.getMetaList(this, 'pr_method').then(res => {
        this.consumeData = res.data;
      })
      if (this.detaMessageForm.fcst_pr.fcst_pr_id == 0 || this.detaMessageForm.fcst_pr.fcst_pr_id == " " || this.detaMessageForm.fcst_pr.fcst_pr_id == null) {
        this.changesMethod();
        // 请求唯一编号
        requst.make_unique_no(this, "fcst", function (that, objRes) {
          if (objRes.data.code !== 0) return;
          that.detaMessageForm.fcst_pr.fcst_pr_no = objRes.data.message;
        });
        if (this.propData.length > 0) {
          console.log("propData", this.propData);
          this.updateItem(this.propData);
        }
        return;
      }
      //请求fcst_pr信息
      this.getRequstModel();
      //请求model_item信息
      this.getRequestItem();
    }
  };
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

