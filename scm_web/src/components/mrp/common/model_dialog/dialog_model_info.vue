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
                    <el-input class="truechange" v-model="detaMessageForm.model.model_code" :readonly="1==1"
                              disabled></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="名称：" label-width="100px">
                    <el-input class="truechange" v-model="detaMessageForm.model.model_name"
                              :disabled="!changeStatus ? true:false"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="单位：" label-width="100px">
                    <el-select v-model="detaMessageForm.model.unit_meta.meta_id" placeholder="请选择"
                               :disabled="!changeStatus ? true:false"
                               @change="getDialogInfo(detaMessageForm.model.unit_meta.meta_id)">
                      <el-option label="请选择" :value="0"></el-option>
                      <el-option v-for="(item,key) in gridData" :key="key" :label="item.meta_name"
                                 :value="item.meta_id"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="tableType ===1">
                  <el-form-item label="颜色：" label-width="100px">
                    <el-input class="truechange" v-model="detaMessageForm.model.spec.color"
                              :disabled="!changeStatus ? true:false"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="tableType ===2">
                  <el-form-item label="坯布代号：" label-width="100px">
                    <el-input class="truechange truechangeInput" v-model="detaMessageForm.model.spec.bar_code"
                              :disabled="!changeStatus ? true:false"></el-input>
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
                <el-table-column label="操作" :width="column_width" v-if="changeStatus">
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
    <div class=" click-button">
      <el-card class="extra_card" v-if="!changeStatus">
        <el-button type="primary" size="large" @click="addData">新增</el-button>
        <el-button type="danger" size="large" @click="changesMethod">修改</el-button>
        <el-button type="text" size="large" @click="deleteMessageBtn">删除</el-button>
      </el-card>
      <el-card class="extra_card" v-if="changeStatus">
        <el-button type="primary" size="large" @click="saveBtn">保存</el-button>
        <el-button type="danger" size="large" @click="addDataSaveBtn">
          <p>保存</p>
          <p>新增</p>
        </el-button>
        <el-button type="text" size="large" @click="closeChangesMetod">取消</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../../utils/utils';
  import showModal from '../../../common/messageBox.js';

  export default {
    components: {},
    name: 'dialog_model_info',
    props: {
      TABSValue: String,//tag显示值
      tabIndex: Number,//tag显示值
      rowId: Number,//物料ID
      tableName: String,//物料种类 成衣，面料，辅料
      tableType: Number//物料种类
    },
    data() {
      return {
        column_width: 120,//操作列的width
        changeStatus: false, // 修改状态
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        detaMessageForm: {
          model: {
            model_code: "",
            model_id: this.rowId,
            model_name: "",
            model_type_meta_id: this.tableType,
            extend: {},
            spec: {
              color: "",
              bar_code: ""
            },
            unit_meta: {
              meta_id: 0,
              meta_code: "",
              parent_meta_code: "",
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
        gridData: [],//弹窗数据
        tableColumn: [],
        tableRowIndex: "0", //删除状态控制参数
        itemName: ""//item标题信息
      }
    },
    methods: {
      //新增按钮
      addData() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.tableName + '新增',
          name: newTabName,
          closable: true,
          rowId: 0,
          tabName:"modelInfo",
          tableType:this.tableType,
          tableName:this.tableName
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
          this.detaMessageForm.item = this.detaMessageForm.item.filter(this.isClose);
          this.getRequstModel();
          this.ifItemCount();
        } else {
          this.$emit('CloseTab');
        }
        showModal.showMessage(this, "success", "取消成功");
      },
      // 保存按钮
      saveBtn(addFun) {
        if (this.detaMessageForm.model.model_name == " " || this.detaMessageForm.model.model_name == null || !this.detaMessageForm.model.model_name) {
          showModal.showModal(this, "", "", "名称不能为空，请填写！", '错误提示');
          return;
        }
        this.saveBtnConfirm(addFun);
      },
      //保存按钮 确定按钮执行函数
      saveBtnConfirm(addFun) {
        this.detaMessageForm.item = this.detaMessageForm.item.filter(this.isDelete);
        let url = "/api/mat_models/models/";
        let text = "保存成功";
        let type = "post";
        if (this.detaMessageForm.model.model_id > 0) {
          url = "/api/mat_models/model/";
          text = "修改成功";
          type = 'put';
        }
        this.vmRequst(url, function (that, objRes) {
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
        this.vmRequst('/api/mat_models/models/', function (that, objRes) {
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
          this.tableRowIndex = this.tableRowIndex + ',' + row.item_id+row.item_code;
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
        if (this.tableRowIndex.indexOf(',' + row.item_id+row.item_code) > 0) {
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
        this.tableRowIndex = this.tableRowIndex.replace(',' + row.item_id+row.item_code, "");
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
          rowId: row.detaMessageForm.model.model_id,

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
      //获取meta列表
      getMetaList() {
        this.vmRequst("/api/mat_models/metas/?parent_meta_code=unit", function (that, objRes) {
          that.gridData = objRes.data;
        });
      },
      //网络请求model表头信息
      getRequstModel() {
        this.vmRequst('/api/mat_models/model/?model_id=' + this.detaMessageForm.model.model_id, function (that, objRes) {
          that.detaMessageForm.model = objRes.data.model;
        });
      }
    },
    //实列完成后按rowid请求相应的数据
    created() {
      this.getMetaList();
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
      //Model的item列表显示字段
      this.getTableColumn();
      if (this.detaMessageForm.model.model_id == 0 || this.detaMessageForm.model.model_id == " " || this.detaMessageForm.model.model_id == null) {
        this.changesMethod();
        this.vmRequst('/api/mat_models/make_model_no/', function (that, objRes) {
          if (objRes.data.code !== 0) return;
          that.detaMessageForm.model.model_code = objRes.data.message;
        }, 'post', {model_type_meta_id: this.tableType});
        return;
      }
      //请求model信息
      this.getRequstModel();
      //请求model_item信息
      this.vmRequst('/api/mat_models/items/?model_id=' + this.detaMessageForm.model.model_id, function (that, objRes) {
        that.updateItem(objRes.data);
      });

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
          text-align: center;
          color: #4db3ff;
          font-size: 18px;
        }
        .el-button--text:hover {
          color: #ec407a;
        }
      }
    }
  }
</style>

