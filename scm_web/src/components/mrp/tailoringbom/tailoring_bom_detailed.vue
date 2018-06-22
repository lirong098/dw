<template>
  <div class="test_detailed_contain">
    <div class="fl test_detailed_main main-card-box">
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              BOM信息
            </h4>
          </div>
          <el-card class="divCard">
            <el-col class="detailMessage">
              <el-form class="detaMessageForm"
                       :model="detaMessageForm.resData"
                       ref="detaMessageForm.resData">
                <el-col :span="12">
                  <el-form-item label="BOM_NO：">
                    <el-input class="nochange"
                              v-show="detaMessageForm.rowState === 'look'"
                              v-text="detaMessageForm.resData.bom.bom_no"
                              readonly>
                    </el-input>
                    <el-input class="truechange"
                              disabled
                              v-show="detaMessageForm.rowState === 'change'"
                              v-model="detaMessageForm.resData.bom.bom_no"
                              readonly>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="Model：">
                    <template scope="scope">
                      <el-input class="nochange"
                                style="width: 80%"
                                v-show="detaMessageForm.rowState === 'look'"
                                v-text="commonmethod(detaMessageForm.resData.bom.model_id)"
                                auto-complete="off">
                      </el-input>
                      <el-input class="truechange"
                                style="width: 80%"
                                :value="commonmethod(detaMessageForm.resData.bom.model_id)"
                                v-show="detaMessageForm.rowState === 'change'"
                                :readonly="true"
                                icon="more"
                                :on-icon-click="event => modelIconClick(event, scope.$index, scope.row)">
                      </el-input>
                    </template>
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
            <h4>
              Items
            </h4>
          </div>
          <div class="table">
            <el-card>
              <el-col class="composition">
                <el-table ref="detaMessageForm.resData.bom_item"
                          :data="detaMessageForm.resData.bom_item"
                          style="width: 100%;"
                          border
                          tooltip-effect="dark">
                  <el-table-column type="index"
                                   label="序号"
                                   width="70">
                  </el-table-column>
                  <el-table-column label="Model"
                                   width="300"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="detaMessageForm.rowState === 'look'"
                                v-text="commonmethod(scope.row.component_model)">
                      </el-input>
                      <el-input :value="commonmethod(scope.row.component_model)"
                                v-show="detaMessageForm.rowState === 'change'"
                                :readonly="true"
                                :disabled="scope.row.restore === true"
                                :icon="scope.row.restore === true?'':'more'"
                                :on-icon-click="event => showItemModel(event, scope.$index, scope.row)">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="item"
                                   width="270"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="detaMessageForm.rowState === 'look'"
                                v-text="commonmethod(scope.row.component_item)">
                      </el-input>
                      <el-input :value="commonmethod(scope.row.component_item)"
                                v-show="detaMessageForm.rowState === 'change'"
                                :readonly="true"
                                :disabled="scope.row.restore === true"
                                :icon="scope.row.restore === true?'':'more'"
                                :on-icon-click="event => showModelItem(event, scope.$index, scope.row)">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="区分Items"
                                   width="110">
                    <template scope="scope">
                      <el-checkbox v-show="detaMessageForm.rowState === 'look'"
                                   v-model="scope.row.spec.division"
                                   disabled>
                      </el-checkbox>
                      <el-checkbox v-show="detaMessageForm.rowState === 'change'"
                                   :disabled="itemCheckBox || scope.row.restore === true"
                                   v-model="scope.row.spec.division"
                                   @change="event => difItem(event, scope.$index, scope.row)">
                      </el-checkbox>
                    </template>
                  </el-table-column>
                  <el-table-column label="Items单耗"
                                   width="150">
                    <template scope="scope">
                      <el-button v-show="detaMessageForm.rowState === 'look'"
                                 :disabled="scope.row.spec.division === false ?true:false"
                                 @click="event => lookBomItem(event, scope.$index, scope.row)">
                        查看
                      </el-button>
                      <el-button v-show="detaMessageForm.rowState === 'change'"
                                 :disabled="(scope.row.spec.division) && scope.row.restore === false?false:true"
                                 @click="event => showBomItem(event, scope.$index, scope.row)">
                        编辑
                      </el-button>
                    </template>
                  </el-table-column>
                  <el-table-column label="单耗"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="detaMessageForm.rowState === 'look'"
                                v-text="scope.row.quantity">
                      </el-input>
                      <el-input class="truechange"
                                v-show="detaMessageForm.rowState === 'change'"
                                :disabled="scope.row.quantity !== 0 && scope.row.spec.division === true && scope.row.spec.consumptStatus === true"
                                v-model="scope.row.quantity">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="单位"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="detaMessageForm.rowState === 'look'"
                                v-text="scope.row.component_model.unit_meta.meta_name">
                      </el-input>
                      <el-input v-text="scope.row.component_model.unit_meta.meta_name"
                                v-show="detaMessageForm.rowState === 'change'">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="材料名称"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-text="scope.row.extend.material_name"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="部位"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-text="scope.row.extend ? scope.row.extend.part_name : ''"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="供应商"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-text="scope.row.extend ? scope.row.extend.supplier : ''"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="价格"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-text="scope.row.extend ? scope.row.extend.price : ''"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="备注"
                                   width="100"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-text="scope.row.extend ? scope.row.extend.remark : ''"></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作"
                                   :width="150"
                                   fixed="right">
                    <template scope="scope">
                      <el-button size="small"
                                 @click="addrow(scope.$index,scope.row)"
                                 v-show="scope.row.restore === false && detaMessageForm.rowState === 'change'">
                        +
                      </el-button>
                      <el-button size="small"
                                 style="margin-right: 8px;"
                                 @click="remove(scope.$index,scope.row)"
                                 v-show="scope.row.restore === false && detaMessageForm.rowState === 'change'">
                        -
                      </el-button>
                      <el-button size="small"
                                 v-show="scope.row.restore === true && detaMessageForm.rowState === 'change'"
                                 @click="changeremove(scope.$index,scope.row)">
                        恢复
                      </el-button>
                      <el-button size="small"
                                 @click="addrow(scope.$index,scope.row)"
                                 v-show="scope.row.restore === true && detaMessageForm.rowState === 'change'">
                        +
                      </el-button>
                      <el-button size="small"
                                 v-show="scope.row.bom_item_id !== 0 && detaMessageForm.rowState === 'look'"
                                 @click="event => lookModelBtn(event, scope.$index, scope.row)">查看
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-card>
          </div>
        </div>
      </div>
      <!--BomModel弹窗-->
      <el-dialog title="BomModel" style="float: left" :visible.sync="bomModellDialog" size="large">
        <modellist @getDialogInfo="getDialogInfo"
                   :noGetItem="true"
                   :exclude="2">
        </modellist>
      </el-dialog>
      <!--ItemModel弹窗-->
      <el-dialog title="ItemModel" style="float: left" :visible.sync="itemModelDialog" size="large">
        <modellist @getDialogInfo="getMetarilModel"
                   :noGetItem="false"
                   :exclude="1"
                   v-if="itemModelDialog">
        </modellist>
      </el-dialog>
      <!--item弹窗-->
      <el-dialog title="Item" style="float: left" :visible.sync="itemDialog" size="large">
        <modellist @getDialogInfo="getMetarilItem"
                   :onlyGetItem="true"
                   :model_id="detaMessageForm.resData.bom_item[clickIndex].component_model.model_id"
                   v-if="itemDialog">
        </modellist>
      </el-dialog>
      <!--区分Item弹窗-->
      <div class="tableOrder">
        <el-dialog title="单耗信息" style="float: left" :visible.sync="bomItemDialog">
          <el-table border :data="bomItem">
            <el-table-column label="成衣Item">
              <template scope="scope">
                {{scope.row.item_code_m}}
              </template>
            </el-table-column>
            <el-table-column label="单耗" >
              <template scope="scope">
                <el-input class="truechange"
                          v-show="detaMessageForm.rowState === 'look'"
                          v-text="scope.row.consumption">
                </el-input>
                <el-input class="truechange"
                          v-show="detaMessageForm.rowState === 'change'"
                          v-model="scope.row.consumption">
                </el-input>
              </template>
            </el-table-column>
          </el-table>
          <el-col :span="12" style="float: right; margin: 10px 0px;">
            <el-button @click="cancelItem"
                       v-show="detaMessageForm.rowState === 'change'"
                       style="float: right; margin: 0px 3px;">取消
            </el-button>
            <el-button @click="cancelItem"
                       v-show="detaMessageForm.rowState === 'look'"
                       style="float: right; margin: 0px 3px;">返回
            </el-button>
            <!--:disabled="this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items.length === 0"-->
            <el-button @click="saveItem"
                       style="float: right; margin: 0px 3px;"

                       v-show="detaMessageForm.rowState === 'change'">保存
            </el-button>
            <el-button @click="rescat"
                       style="float: right;"
                       v-show="detaMessageForm.rowState === 'change'">重置
            </el-button>
            <el-button @click="refresh"
                       v-show="detaMessageForm.rowState === 'change'"
                       style="float: right; margin: 0px 3px;">刷新
            </el-button>
          </el-col>
        </el-dialog>
      </div>
      <el-dialog title="查看Model" style="float: left" :visible.sync="lookModelDialog" size="large" v-if="lookModelDialog">
        <tableDetailed :tabIndex='1'
          :rowId="lookModel.component_model.model_id"
          :tableName="lookModel.component_model.model_name"
          :tableType="lookModel.component_model.model_type_meta_id.meta_id">
        </tableDetailed>
      </el-dialog>
    </div>
    <!--操作按钮-->
    <div class=" click-button">
      <el-card class="extra_card" v-show="detaMessageForm.rowState === 'look'">
        <el-button type="danger"
                   size="large"
                   @click="addnew">新增
        </el-button>
        <el-button type="primary"
                   size="large"
                   @click="changeBtn">修改
        </el-button>
        <el-button type="error"
                   size="large"
                   style="border: 0; color: #4db3ff;"
                   @click="deleteMethod(detaMessageForm.rowId)">删除
        </el-button>
      </el-card>
      <el-card class="extra_card" v-show="detaMessageForm.rowState === 'change'">
        <el-button type="primary"
                   size="large"
                   @click="saveBtn">保存
        </el-button>
        <el-button type="danger"
                   size="large"
                   @click="saveBtnAdd">保存<br />新增
        </el-button>
        <el-button type="error"
                   size="large"
                   style="border: 0; color: #4db3ff;"
                   @click="goBack">取消
        </el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import tableDetailed from '../common/model/new_table_detaied.vue';
  import modellist from "../common/model_dialog/dialog_model.vue";
  import {keydown} from "../../../components/common/component.js";
  //公共文件
  import requst from "../../common/vmrequst.js"
  import showModal from '../../common/messageBox.js';
  export default {
    components: {
      tableDetailed,
      modellist
    },
    name: 'test-detailed',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      rowMessage: Object,
      CloseTab: Function
    },
    // restore: false 恢复按钮状态
    // delete字段存在就提交后端删除
    // addlocal 与 delete字段同时存在,不提交给后端
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 0,  // 总条数
        modelIndex: 0, // 点击当前行的下标
        search: '',
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        detaMessageForm: this.rowMessage,
        clickIndex: 0,
        bomModel: [], // bomModel数据存放
        bomModellDialog: false, // bomModel弹窗控制
        itemModel: [], // itemModel数据存放
        itemModelDialog: false, // itemModel弹窗控制
        item: [], // ModelItem数据存放
        itemDialog: false, // itemModel弹窗控制
        bomItem: [], // 区分Item数据存放
        bomItemDialog: false, // 区分Item弹窗控制
        lookModel: {},
        lookModelDialog: false,
        itemCheckBox: true, // 区分Item是否可选
      }
    },
    methods: {
      // 点选备料类型
      select(val){
        this.detaMessageForm.resData.mrp_pr.mrp_pr_type_meta_id.meta_id = val;// 点选备料类型赋值
      },
      /*
     * 网络请求model
     * qty条数
     * page页数
     * model对应的model条件
     * classify传入成衣Model传'2',非成衣model传'1'*/
      vmRequst(qty = 10, page = 1,model, classify) {
        let url ='/api/mat_models/models/?page=' + page + '&pagesize=' + qty + '&exclude=' + classify;
        requst.requst(this,url, function (that,res) {
          if(model === "bomModel"){
            that.bomModel = res.data.data;
          }else if(model === "itemModel"){
            that.itemModel = res.data.data;
          }
          that.pagedatacount = res.data.total_number;
        });
      },
      //成功反馈
      /*
      * message传显示信息
      * type传状态,例:'success'*/
      returnMessage(message,type){
        this.$message({
          showClose: true,
          message: message,
          type: type
        });
      },
      // 分页
      handleCurrentChange: function (val) {
        console.log(val);
        this.pagesize = val;
        this.vmRequst(val,"1","bomModel","2");
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequst(val,"1","bomModel","2");
      },
      // item分页
      handleCurrentChangeItem: function (val) {
        this.pagesize = val;
        this.vmRequst(val,"1","itemModel","1");
      },
      handleSizeChangeItem: function (val) {
        this.vmRequst("10",val,"itemModel","1");
      },
      // 点击BomModel的icon的选择按钮
      modelIconClick(index,row){
        this.search = '';
        this.bomModellDialog = true; // 控制弹窗显示
      },
      // 点击ItemModel的icon按钮
      showItemModel(event,index,row){
        // 控制弹窗显示
        this.search = '';
        this.itemModelDialog = true;
        //点击时记录点击的是第几行item
        this.clickIndex = index;
      },
      // 点击ItemModelItem的icon按钮
      showModelItem(event,index,row){
        this.itemDialog = true;
        this.clickIndex = index;
        // 请求对应model的Item
//        let getItemIdMassage = {
//          model_id: row.component_model.model_id
//        };
//        const api = this.$store.state.NEW_API;
//        fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
//          if (res && res.status == 200) {
//            console.log(res.data);
//            this.item = res.data;
//          }
//        })
      },
      // Item按钮
      showBomItem(event,index,row){
        this.clickIndex = index;
        row.spec.division = true;
        console.log(row.spec.division,111);
        if(row.spec.consume_items.length === 0){
          console.log(1);
          let getItemIdMassage = {
            model_id: this.detaMessageForm.resData.bom.model_id.model_id
          };
          const api = this.$store.state.NEW_API;
          fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
            if (res && res.status == 200) {
              this.bomItem = [];
              console.log(2);
              row.spec.division = true;
              for(let item of res.data){
                // 区分Item重置单耗
                item.consumption = 0;
                // 显示信息
                item.item_code_m = this.commonmethod(item);
                // 将回调信息重组为需要提交的数据
                this.bomItem.push({
                  item_code: item.item_code,
                  item_code_m: item.item_code_m,
                  consumption: item.consumption,
                  division: true,
                });
              }
            }
          })
        }else {
          row.spec.division = true;
          console.log(row.spec, '11111');
          console.log(3);
          this.detaMessageForm.rowState = 'change';
          this.bomItem = row.spec.consume_items;
        }
        if(!this.detaMessageForm.resData.bom.model_id.model_id){
          // 如果没有成衣BOMModel提示
          this.returnMessage("请选择bom的Model","error")
        }else if(!this.detaMessageForm.rowId){
          console.log(4);
          row.spec.division = true;
          // 新增处理区分Item
          // 显示弹窗
          this.bomItemDialog = true;
          this.detaMessageForm.resData.bom_item[this.clickIndex].spec.division = true;
          // 请求时要发送的数据
          let getItemIdMassage = {
            model_id: this.detaMessageForm.resData.bom.model_id.model_id
          };
          const api = this.$store.state.NEW_API;
          fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
            if (res && res.status == 200) {
              if(!this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items){
                for(let item of res.data){
                  console.log(5)
                  // 区分Item重置单耗
                  item.consumption = 0;
                  // 显示信息
                  item.item_code_m = this.commonmethod(item);
                  // 将回调信息重组为需要提交的数据
                  this.bomItem.push({
                    item_code: item.item_code,
                    item_code_m: item.item_code_m,
                    consumption: item.consumption,
                    division: true,
                  });
                }
                console.log(this.bomItem,'---')
              }
            }
          })
        }else if(this.detaMessageForm.rowId){
          console.log(6)
          // 修改时区分Item操作
          // 显示对应弹窗
          this.bomItemDialog = true;
          if(this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items.length>0){
            // 将当前行的信息赋值给bomItem
            console.log(7)
            this.bomItem = this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items;
          }else {
            console.log(8);
            // 重置区分Item信息
            let getItemIdMassage = {
              model_id: this.detaMessageForm.resData.bom.model_id.model_id
            };
            const api = this.$store.state.NEW_API;
            fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
              if (res && res.status == 200) {
                console.log(res.data,'111');
                this.bomItem = [];
                for(let item of res.data){
                  item.consumption = 0;
                  item.item_code_m = this.commonmethod(item);
                  this.bomItem.push({
                    item_code: item.item_code,
                    item_code_m: item.item_code_m,
                    consumption: item.consumption,
                    itemStatus: false
                  });
                }
              }
            })
          }
        }
      },
      cancelItem(){
        this.bomItemDialog = false;
      },
      saveItem(){
        let sum = 0;
        for(let item of this.bomItem){
          sum+=item.consumption*1
        }
        // if(sum !== 0){
          this.detaMessageForm.resData.bom_item[this.clickIndex].spec.division = true;
//        }else {
//          this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consumptStatus = false;
//        }
        this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items = this.bomItem;
        this.detaMessageForm.resData.bom_item[this.clickIndex].quantity = sum/this.bomItem.length;
        this.bomItemDialog = false;
      },
      rescat(){
        let sum = 0;
        for(let item of this.bomItem){
          item.consumption = 0;
        }
        this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consumptStatus = false;
        // this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items = [];
        this.detaMessageForm.resData.bom_item[this.clickIndex].quantity = sum;
        this.bomItemDialog = false;
      },
      refresh(){
        let getItemIdMassage = {
          model_id: this.detaMessageForm.resData.bom.model_id.model_id
        };
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res.data,'111');
            var flagadd = 0;
            for(let item of res.data){
              for(let x of this.bomItem){
                if(x.item_code === item.item_code) {
                  flagadd = 1;
                  break;
                }
              }
              if(flagadd === 1){
                flagadd = 0;
              }else {
                flagadd = 0;
                item.consumption = 0;
                item.item_code_m = this.commonmethod(item);
                this.bomItem.push({
                  item_code: item.item_code,
                  item_code_m: item.item_code_m,
                  consumption: item.consumption,
                  itemStatus: false
                })
              }
            }
            console.log(this.bomItem);
            var flagremove = 0;
            for(let itemindex in this.bomItem){
              for(let xindex in res.data){
                if(this.bomItem[itemindex].item_code === res.data[xindex].item_code){
                  flagremove = 1;
                  break
                }
                flagremove = 2;
              }
              if(flagremove === 1){
                flagremove = 0;
              }else if(flagremove === 2){
                flagremove = 0;
                this.bomItem.splice(itemindex,1)
              }
            }

          }
        })
      },
      // 查看区分Item
      lookBomItem(event,index,row){
        console.log(row);
        this.bomItem = [];
        if(!row.spec.consume_items){
          // row.spec.consume_items = []
          let getItemIdMassage = {
            model_id: this.detaMessageForm.resData.bom.model_id.model_id
          };
          const api = this.$store.state.NEW_API;
          fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
            if (res && res.status == 200) {
              console.log(res.data,'111');
              this.bomItem = [];
              for(let item of res.data){
                item.consumption = 0;
                item.item_code_m = this.commonmethod(item);
                this.bomItem.push({
                  item_code: item.item_code,
                  item_code_m: item.item_code_m,
                  consumption: item.consumption,
                  itemStatus: false
                });
              }
              row.spec.consume_items = this.bomItem;
            }
          })
        }
        if(row.spec.consume_items.length>0){
          this.bomItem = row.spec.consume_items;
        }else{
          let getItemIdMassage = {
            model_id: this.detaMessageForm.resData.bom.model_id.model_id
          };
          const api = this.$store.state.NEW_API;
          fetchAPI('get', api + '/api/mat_models/items/?model_id=' + getItemIdMassage.model_id, getItemIdMassage, this).then((res) => {
            if (res && res.status == 200) {
              console.log(res.data,'111');
              this.bomItem = [];
              for(let item of res.data){
                item.consumption = 0;
                item.item_code_m = this.commonmethod(item);
                this.bomItem.push({
                  item_code: item.item_code,
                  item_code_m: item.item_code_m,
                  consumption: item.consumption,
                  itemStatus: false
                });
              }
              row.spec.consume_items = this.bomItem;
            }
          })
        }
        this.bomItemDialog = true;
      },
      // 查看Model按钮
      lookModelBtn(event,index,row){
        var _this = this;
        _this.lookModel = row;
        _this.lookModelDialog = true;
        console.log(_this.lookModel,111)
      },
      commonmethod(model){
        if(model.model_id){
          let keyArr = ['model_code','model_name'];
          let tempArr = [];
          for(let i in keyArr){
            if(model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          model.spec.color?tempArr.push(model.spec.color):'';
          return tempArr.join(' - ')
        }
        if(model.item_id){
          let keyArr = ['item_code','item_name'];
          let tempArr = [];
          for(let i in keyArr)
          {
            if(model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          return tempArr.join(' - ');
        }
      },
      addrow(index,row){
        let newrow = {
          bom_item_id: 0,
          bom: {
            bom_id: 0,
            bom_no: "",
            model_id: 0,
            item_id: 0,
            version: 0,
            spec: {
              color: ""
            },
            extend: {}
          },
          component_model: {
            model_id: 0,
            unit_meta: {
              meta_id: 0,
              meta_code: "",
              parent_meta_code: "",
              meta_name: "",
              extend: {}
            },
            model_type_meta_id: 0,
            model_code: "",
            model_name: "",
            spec: {},
            extend: {}
          },
          component_item: {
            item_id: 0,
            item_code: "",
            item_name: "",
            spec: {},
            extend: {},
            model: 0
          },
          quantity: 0,
          spec: {
            consume_items: [],
            division: false,
            consumptStatus: false,
          },
          extend: {},
          addlocal: 0,
          restore: false,
        };
        this.detaMessageForm.resData.bom_item.splice(index+1,0,newrow);
      },
      remove(index,row){
        console.log(index);
        console.log(row);
        if (row.component_model.model_id !== 0 || row.component_item.item_id !== 0) {
          row.delete = 0;
          row.restore = true;
          this.detaMessageForm.resData.bom_item[index] = row;
          console.log(row, 'asdasd')
        }else {
          if(row.addlocal === 0 && this.detaMessageForm.resData.bom_item.length>1) {
            this.detaMessageForm.resData.bom_item.splice(index, 1);
          }
        }
      },
      changeremove(index,row){
        delete row.delete;
        row.restore = false;
        this.detaMessageForm.resData.bom_item[index] = row;
      },
      saveBtn() {
        console.log(this.detaMessageForm.resData);
        if (!this.detaMessageForm.resData.bom.model_id) {
          this.returnMessage("请填写完整BOM信息！","error");
          return;
        }
        for(let x in this.detaMessageForm.resData.bom_item){
          if(!(this.detaMessageForm.resData.bom_item[x].component_model.model_id)){
            this.returnMessage("请选填写完整BOMItem信息！","error");
            return
          }else {
            if(this.detaMessageForm.resData.bom_item[x].addlocal === 0 && this.detaMessageForm.resData.bom_item[x].delete === 0){
              this.detaMessageForm.resData.bom_item.splice(x,1);
            }
          }
        }
        if(!this.detaMessageForm.resData.bom.item_id){
          this.detaMessageForm.resData.bom.item_id = {
            item_id: 0
          }
        }
        this.saveBtnConfirm();
      },
      //保存按钮 确定按钮执行函数
      saveBtnConfirm() {
        var _this = this;
        if(!(this.detaMessageForm.rowId)){
          let url = '/api/mat_models/boms/';
          let type = 'post';
          let options = this.detaMessageForm.resData;
          requst.requst(this,url, function (that, res) {
            console.log(res,'----1');
            if(!res.data.bom.item_id){
              res.data.bom.item_id = {
                item_id: 0
              }
            }
            for(let item of res.data.bom_item){
              if(!item.component_item){
                item.component_item = {
                  item_id: 0
                }
              }
            }
            that.detaMessageForm.rowId = res.data.bom.bom_id;
            that.detaMessageForm.resData = res.data;
            that.detaMessageForm.rowState = 'look';
            that.returnMessage("操作成功！","success");
          }, type, options);
        }else if(this.detaMessageForm.rowId){
          let url = '/api/mat_models/bom/';
          let type = 'put';
          let options = this.detaMessageForm.resData;
          requst.requst(this,url, function (that, res) {
            console.log(res, '----21');
            if(!res.data.bom.item_id){
              res.data.bom.item_id = {
                item_id: 0
              }
            }
            for(let item of res.data.bom_item) {
              if (!item.component_item) {
                item.component_item = {
                  item_id: 0
                }
              }
            }
            if(res.data.bom_item.length === 0){
              res.data.bom_item = [
                {
                  bom_item_id: 0,
                  bom: {
                    bom_id: 0,
                    bom_no: "",
                    model_id: 0,
                    item_id: 0,
                    version: 0,
                    spec: {
                      color: ""
                    },
                    extend: {}
                  },
                  component_model: {
                    model_id: 0,
                    unit_meta: {
                      meta_id: 0,
                      meta_code: "",
                      parent_meta_code: "",
                      meta_name: "",
                      extend: {}
                    },
                    model_type_meta_id: 0,
                    model_code: "",
                    model_name: "",
                    spec: {},
                    extend: {}
                  },
                  component_item: {
                    item_id: 0,
                    item_code: "",
                    item_name: "",
                    spec: {},
                    extend: {},
                    model: 0
                  },
                  quantity: 0,
                  spec: {
                    consume_items: [],
                    division: false,
                    consumptStatus: false,
                  },
                  extend: {},
                  addlocal: 0,
                  restore: false,
                }
              ]
            }
            that.detaMessageForm.resData = res.data;
            _this.detaMessageForm.rowState = 'look';
            that.returnMessage("操作成功！","success");
          }, type, options);
        }
      },
      // 修改按钮
      changeBtn(){
        this.itemCheckBox = false;
        this.detaMessageForm.rowState = 'change';
        console.log(this.detaMessageForm.resData);
        if(!this.detaMessageForm.resData.bom.item_id){
          this.detaMessageForm.resData.bom.item_id ={
            item_id: 0
          }
        }
        for(let item of this.detaMessageForm.resData.bom_item){
          if(!item.component_item){
            item.component_item = {
              item_id: 0
            }
          }
          item.restore = false;
        }
      },
      //新增按钮
      addnew(){
        let initialize = {
          bom: {
            bom_id: 0,
            bom_no: "",
            model_id: {},
            item_id: {
              item_id: 0,
            },
            version: 0,
            spec: {
              color: ""
            },
            extend: {}
          },
          bom_item: [
            {
              bom_item_id: 0,
              bom: {
                bom_id: 0,
                bom_no: "",
                model_id: 0,
                item_id: 0,
                version: 0,
                spec: {
                  color: ""
                },
                extend: {}
              },
              component_model: {
                model_id: 0,
                unit_meta: {
                  meta_id: 0,
                  meta_code: "",
                  parent_meta_code: "",
                  meta_name: "",
                  extend: {}
                },
                model_type_meta_id: 0,
                model_code: "",
                model_name: "",
                spec: {},
                extend: {}
              },
              component_item: {
                item_id: 0,
                item_code: "",
                item_name: "",
                spec: {},
                extend: {},
                model: 0
              },
              quantity: 0,
              spec: {
                consume_items: [],
                division: false,
                consumptStatus: false,
              },
              extend: {},
              addlocal: 0,
              restore: false,
            }
          ]
        };

        // 获取唯一标识
        requst.make_unique_no(this,"1",function (that,res) {
          if (res.data.code !== 0) return;
          console.log(res.data.message,'res.data.message');
          initialize.bom.bom_no = res.data.message;
        });

        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '成衣BOM - 新增',
          name: newTabName,
          closable: true,
          rowId: '',
          bom: 'bom',
          rowState: 'change',
          resData: initialize
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      //删除按钮
      deleteMethod(rowId){
        this.$confirm('此操作将永久删除, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteData = [];
          deleteData.push(rowId);
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/mat_models/boms/', {data: deleteData}, this).then((res) => {
            if (res.status == 204) {
              this.$emit('CloseTab');
              this.$message({
                showClose: true,
                message: '删除成功',
                type: 'success'
              });
            }
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      goBack(){
        var _this = this;
        this.$confirm('此操作将不会保存已填写的数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          if(!this.detaMessageForm.rowId){
            _this.$emit('CloseTab');
          }else {
            const api = this.$store.state.NEW_API;
            let url = api + '/api/mat_models/bom/?bom_id='+this.detaMessageForm.rowId;
            let listurl = api + '/api/mat_models/bom_items/?bom_id='+this.detaMessageForm.rowId;
            fetchAPI('get', url ,null, this).then((res) => {
              if (res && res.status == 200){
                this.detaMessageForm.resData.bom = res.data;
                fetchAPI('get', listurl ,null, this).then((res) => {
                  if (res && res.status == 200) {
                    console.log(res);
                    for(let item of res.data){
                      item.restore = false
                    }
                    this.detaMessageForm.resData.bom_item = res.data;
                  }
                });
                this.detaMessageForm.rowState = "look";
              }
            });
          }
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      // 保存并新增
      saveBtnAdd(){
        this.saveBtn();
        let initialize = {
          bom: {
            bom_id: 0,
            bom_no: "",
            model_id: {},
            item_id: {
              item_id: 0,
            },
            version: 0,
            spec: {
              color: ""
            },
            extend: {}
          },
          bom_item: [
            {
              bom_item_id: 0,
              bom: {
                bom_id: 0,
                bom_no: "",
                model_id: 0,
                item_id: 0,
                version: 0,
                spec: {
                  color: ""
                },
                extend: {}
              },
              component_model: {
                model_id: 0,
                unit_meta: {
                  meta_id: 0,
                  meta_code: "",
                  parent_meta_code: "",
                  meta_name: "",
                  extend: {}
                },
                model_type_meta_id: 0,
                model_code: "",
                model_name: "",
                spec: {},
                extend: {}
              },
              component_item: {
                item_id: 0,
                item_code: "",
                item_name: "",
                spec: {},
                extend: {},
                model: 0
              },
              quantity: 0,
              spec: {
                consume_items: [],
                division: false,
                consumptStatus: false,
              },
              extend: {},
              addlocal: 0,
              restore: false,
            }
          ]
        };
        // 获取唯一标识
        requst.make_unique_no(this,"1",function (that,res) {
          if (res.data.code !== 0) return;
          console.log(res.data.message,'res.data.message');
          initialize.bom.bom_no = res.data.message;
        });

        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '成衣BOM - 新增',
          name: newTabName,
          closable: true,
          rowId: '',
          rowState: 'change',
          resData: initialize
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      // 区分Item
      difItem(event,index,row){
        console.log(row,'1');
        //row.spec.consumption = this.bomItem;
        console.log(row.spec.division);
        if(row.spec.division === false){
          for(let item of this.detaMessageForm.resData.bom_item[this.clickIndex].spec.consume_items){
            item.consumption = 0
          }
        }
      },
      // 搜索功能
      getList(search,model,classify) {
        const api = this.$store.state.NEW_API;
        let getDataMassage = {
          page: this.currentPage,
          pagesize: this.pagesize,
          search: this.search,
          classify: classify
        };
        fetchAPI('get', api + '/api/mat_models/models/?page=' + getDataMassage.page + '&pagesize=' + getDataMassage.pagesize + '&search=' + this.search+ '&exclude=' + getDataMassage.classify, getDataMassage, this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount = res.data.total_number;
            if(model === "bomModel"){
              this.bomModel = res.data.data;
            }else if(model === "itemModel"){
              this.itemModel = res.data.data;
            }
          } else {
            console.log("服务器正在调试");
          }
        })
      },
      query(search,model,classify) {
        this.getList(search,model,classify);
      },
      circle_close() {
        this.search = "";
        let model = "bomModel";
        let classify = "2";
        this.getList(this.search,model,classify);
        console.log(this.search);
      },
      circle_close_Item() {
        this.search = "";
        let model = "itemModel";
        let classify = "1";
        this.getList(this.search,model,classify);
        console.log(this.search);
      },
      // 选择model模式改变
      getDialogInfo(res) {
        this.bomModel = res;
        this.detaMessageForm.resData.bom.model_id = res;
        console.log(this.bomModel);
        this.itemCheckBox = false; // 区分Item是否可选 false可选,true不可选,
        this.bomModellDialog = false;
      },
      // 选择items的Model
      getMetarilModel(res) {
        let newArr = [];
        for (let item of res.model_item) {
          newArr.push({
            bom_item_id: 0,
            bom: {
              bom_id: 0,
              bom_no: "",
              model_id: 0,
              item_id: 0,
              version: 0,
              spec: {
                color: ""
              },
              extend: {}
            },
            component_model: {
              model_id: res.model_id,
              unit_meta: res.unit_meta,
              model_type_meta_id: res.model_type_meta_id,
              model_code: res.model_code,
              model_name: res.model_name,
              spec: res.spec,
              extend: res.extend,
            },
            component_item: {
              item_id: item.item_id,
              item_code: item.item_code,
              item_name: item.item_name,
              spec: item.spec,
              extend: item.extend,
              model: item.model
            },
            quantity: 0,
            spec: {
              consume_items: [],
              division: false,
              consumptStatus: false,
            },
            extend: {},
            addlocal: 0,
            restore: false,
          });
        }
        console.log(...newArr, 'newarr1123123');
        console.log(newArr.length === 0)
        if( newArr.length === 0){
          this.itemModelDialog = false;
        }else {
          if (!this.detaMessageForm.resData.bom_item[this.clickIndex].addlocal) {
            // delete newArr[0].addlocal;
            newArr[0].bom = this.detaMessageForm.resData.bom_item[this.clickIndex].bom;
            newArr[0].bom_item_id = this.detaMessageForm.resData.bom_item[this.clickIndex].bom_item_id;
          }
          this.detaMessageForm.resData.bom_item.splice(this.clickIndex, 1, ...newArr);
          console.log(this.detaMessageForm.resData.bom_item);
          this.itemModelDialog = false;
        }
      },
      // 选择items的Item
      getMetarilItem(res) {
        let newArr = [];
        let i = 0;
        for (let item of res) {
          newArr.push({
            bom_item_id: 0,
            bom: {
              bom_id: 0,
              bom_no: "",
              model_id: 0,
              item_id: 0,
              version: 0,
              spec: {
                color: ""
              },
              extend: {}
            },
            component_model: {
              model_id: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.model_id,
              unit_meta: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.unit_meta,
              model_type_meta_id: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.model_type_meta_id,
              model_code: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.model_code,
              model_name: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.model_name,
              spec: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.spec,
              extend: this.detaMessageForm.resData.bom_item[this.clickIndex].component_model.extend,
            },
            component_item: {
              item_id: item.item_id,
              item_code: item.item_code,
              item_name: item.item_name,
              spec: item.spec,
              extend: item.extend,
              model: item.model
            },
            quantity: 0,
            spec: {
              consume_items: [],
              division: false,
              consumptStatus: false,
            },
            extend: {},
            addlocal: 0,
            restore: false,
          });
          if (this.detaMessageForm.resData.bom_item[this.clickIndex].component_item.item_id === item.item_id) {
            newArr[i] = this.detaMessageForm.resData.bom_item[this.clickIndex]
          }
          i++
        }
        console.log(...newArr)
        this.detaMessageForm.resData.bom_item.splice(this.clickIndex, 1, ...newArr);
        this.itemDialog = false;
      }
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      }
    },
    computed: {

    },
    updated() {
      let divname = '';
      if(this.bomItemDialog === false){
        divname = 'table';
        keydown(3,divname);
      }else if(this.bomItemDialog === true){
        divname = 'tableOrder';
        keydown(1,divname);
      }
    },
    mounted() {

    },
    created() {
      console.log('bomitem', this.detaMessageForm, 111);
      if (this.detaMessageForm.resData.bom.model_id.model_id && this.detaMessageForm.resData.bom.model_id.model_id !== 0) {
        this.itemCheckBox = false;
      }
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
      width:88%;
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
          .truechange {
            width: 60%;
            text-align: center;
          }
        }
      }
      .nochange {
        width: 60%;
        text-align: center;
        border-bottom: 1px solid #ccc;
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
    .click-button{
      width:9%;
      padding-top: 20px;
      position:fixed;
      right:2%;
      .extra_card{
        display: flex;
        flex-flow: column;
        align-items: center;
        .el-button{
          display:block;
          margin: 0;
        }
        .el-button:last-child{
          margin-top:10px;
        }
      }
    }
    .click-button{
      width:9%;
      padding-top: 20px;
      position:fixed;
      right:2%;
      .extra_card{
        display: flex;
        flex-flow: column;
        align-items: center;
        .el-button{
          display:block;
          margin: 0;
        }
        .el-button:nth-child(2){
          margin-top:10px;
        }
        .el-dropdown{
          width: 100%;
          height: 40px;
          line-height: 40px;
          font-size: 18px;
          text-align: center;
          color:#4db3ff;
          margin:5px 0 0 5px;
        }
      }
    }
    .extra_card{
      display: flex;
      flex-flow: column;
      align-items: center;
      .el-button{
        display:block;
        margin: 0;
      }
      .el-button:nth-child(2){
        margin-top:10px;
      }
      .el-dropdown{
        width: 100%;
        height: 40px;
        line-height: 40px;
        font-size: 18px;
        text-align: center;
        color:#4db3ff;
        margin:5px 0 0 5px;
      }
    }
  }
</style>
