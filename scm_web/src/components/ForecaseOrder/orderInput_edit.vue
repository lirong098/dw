<template>
  <div class="order_edit_contain">
    <div class="order_edit_main">
      <el-form :model="editOrderData"
               class="demo-form-inline"
               :rules="orderRules"
               label-width="80px" ref="orderForm">
        <div class="clearfix">
          <div class="fl main-card-box">
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  客户信息
                </h4>
              </div>
              <el-card>
                <el-form-item label="订单类型">
                  <div class="edit_order_input">
                    手工订单
                  </div>
                </el-form-item>
                <el-form-item label="客户编码" prop="cust_code">
                  <div class="edit_order_input">
                    <el-select v-model="editOrderData.cust_code"
                               @change="changeCustCode"
                               :disabled="!!editOrderData.fcst_order_id"
                               placeholder="请选择客户">
                      <el-option
                        label=""
                        value="">
                        <div class="select_add">
                          <el-icon name="plus"></el-icon>
                          <span>新增</span>
                        </div>
                      </el-option>
                      <el-option
                        v-for="item in customerData"
                        :key="item.cust_code"
                        :label="item.cust_name"
                        :value="item.cust_code">
                      </el-option>
                    </el-select>
                  </div>
                </el-form-item>
              </el-card>
            </div>
          </div>
          <div class="fr opt-btn-box">
            <el-card class="extra_card">
              <el-button type="primary"
                         @click="saveEdit('orderForm')">保存
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button type="info"
                         :disabled="!editOrderData.fcst_order_id"
                         @click="addModelItem">添加Item
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button type="warning"
                         :disabled="!editOrderData.fcst_order_id"
                         @click="selectMaterialsType">生成备料单
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button type="danger"
                         @click="deleteOrder"
                         :disabled="!editOrderData.fcst_order_id">删除
              </el-button>
            </el-card>
          </div>
        </div>
        <div class="main-card-box" v-if="modelItemData
           && modelItemData.length">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Item
              </h4>
            </div>
            <el-card class="box-card">
              <el-table
                :data="modelItemData"
                class="item_table_hack"
                style="width: 100%">
                <el-table-column
                  prop="item_info.model_info.model_code"
                  width="110"
                  label="ModelCode">
                </el-table-column>
                <el-table-column
                  prop="item_info.model_info.model_name"
                  :show-overflow-tooltip="true"
                  min-width="250"
                  label="ModelName">
                </el-table-column>
                <el-table-column
                  prop="item_info.item_code"
                  :show-overflow-tooltip="true"
                  width="110"
                  label="ItemCode">
                </el-table-column>
                <el-table-column
                  prop="item_info.item_name"
                  :show-overflow-tooltip="true"
                  min-width="110"
                  label="ItemName">
                </el-table-column>
                <el-table-column
                  min-width="220"
                  label="日期">
                  <template scope="scope">
                    <el-date-picker
                      v-model="scope.row.delivery_date"
                      type="week"
                      size="small"
                      format="yyyy 第 WW 周"
                      :editable="false"
                      :clearable="false"
                      placeholder="选择周"
                      @change="changModelItem(scope.$index,'itemForm_'+scope.$index)"
                      :picker-options="pickerOptions">
                    </el-date-picker>
                  </template>
                </el-table-column>
                <el-table-column
                  min-width="150"
                  label="数量">
                  <template scope="scope">
                    <el-input-number size="small"
                                     :min="0"
                                     :controls="false"
                                     @change="changModelItem(scope.$index)"
                                     v-model="scope.row.quantity"></el-input-number>
                    <span class="icon_content"  v-show="scope.row.type == 'ok'">
                          <i class="icon icon16 icon_correct"></i>
                        </span>
                    <span class="icon_content" v-show="scope.row.type == 'no'">
                          <i class="icon icon16 icon_error"></i>
                        </span>
                  </template>
                </el-table-column>
                <el-table-column
                  width="80"
                  fixed="right"
                  label="操作">
                  <template scope="scope">
                    <el-button-group>
                      <el-button type="danger"
                                 size="small"
                                 @click="deleteModeItem(scope.$index)">删除</el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </div>
      </el-form>
    </div>
    <el-dialog
      :title="selectType == 'model' ? '点击选择model' :
      '选择item'"
      class="diff_dialog"
      :visible.sync="selectDialog"
      @close="closeDialog"
      size="small">
      <div>
        <div class="model_search_box" v-if="selectType == 'model'">
          <el-input v-model="searchModel"
                    @change="getModelData"
                    placeholder="输入model_code查询"></el-input>
        </div>
        <el-table :data="modelData"
                  v-if="selectType == 'model'"
                  v-loading.body="loading"
                  @row-click="checkModel">
          <el-table-column property="model_code"
                           label="model_code" ></el-table-column>
          <el-table-column property="model_name"
                           :show-overflow-tooltip="true"
                           label="model_name"
          ></el-table-column>
        </el-table>
        <div v-if="selectType == 'item'">
          当前Model&nbsp;&nbsp;
          <b>{{selectModuleObj.model_code}}</b>
          <el-table :data="itemData"
                    v-loading.body="loading"
                    @selection-change="handleSelectionChange">
            <el-table-column type="selection"
                             width="50"></el-table-column>
            <el-table-column property="item_code"
                             label="item_code" ></el-table-column>
            <el-table-column property="item_name"
                             :show-overflow-tooltip="true"
                             label="item_name"
            ></el-table-column>
          </el-table>
        </div>
        <div class="pagination clearfix" v-if="selectType == 'model'">
          <div class="total fl">
            共 <b>{{pagedatacount}}</b> 条数据
          </div>
          <div class="pagination_tool fr">
            <el-pagination
              layout="prev, pager, next"
              :current-page.sync="currentPage"
              @current-change="handleCurrentChange"
              :page-size="pagesize"
              :total="pagedatacount">
            </el-pagination>
          </div>
        </div>
        <div v-if="selectType == 'model'"  class="product_btn">
          <el-button type="primary"
                     @click="editProductInfo('add')"
                     size="small">添加新Model
          </el-button>
        </div>
        <div v-if="selectType == 'item'"  class="product_btn">
          <el-button type="primary"
                     @click="editProductInfo('edit')"
                     size="small">添加新Item
          </el-button>
        </div>
      </div>
      <span slot="footer" class="dialog-footer" v-if="selectType == 'item'">
        <div>
          <el-button @click="returnModel"
                     size="small">返回Model
          </el-button>
          <el-button @click="checkItem"
                     type="info"
                     size="small">确定
          </el-button>
        </div>
      </span>
    </el-dialog>
    <el-dialog
      title="已生成备料单"
      class="diff_dialog"
      :visible.sync="isShowMaterials"
      size="small">
      <div class="materials_content">
        <div>
          订单号 &nbsp;&nbsp; {{editOrderData.fcst_order_no}}
          <div class="group"
               v-if="materialsOrderData &&
               Object.keys(materialsOrderData).length">
            <div class="row_select row_select-first"
                 v-for="(item,index) in materialsOrderData">
              <div class="head">

              </div>
              <div class="body">
                <div class="items">
                  <div class="item">
                    原料类型
                    <b>{{item.material_type_meta.meta_name}}
                    </b>
                    <span class="arrow">
                      <el-icon
                        name="d-arrow-right"></el-icon>
                    </span>
                    备料单号
                    <b class="item_content">{{item.fcst_pr_no}}</b>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            该订单无数据
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="isShowMaterials = false">确认</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="选择原料类型"
      :visible.sync="selectMaterialsTypeDialog"
      size="small">
      <el-checkbox-group
        v-model="currentMaterialsType">
        <div  v-for="item in materialsType">
          <el-checkbox
            :key="item.meta_code"
            :disabled="!!item.fcst_pr_no"
            :label="item.meta_code">
            {{item.meta_name}}
          </el-checkbox>
          {{item.fcst_pr_no ?
          '备料单号 '+item.fcst_pr_no : ''}}
        </div>
      </el-checkbox-group>
      <span slot="footer" class="dialog-footer">
        <el-button @click="selectMaterialsTypeDialog = false">取 消</el-button>
        <el-button type="primary"
                   :disabled="!currentMaterialsType.length"
                   @click="createMaterials">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
  import {fetchAPI,getFirstDayOfWeek} from '../../utils/utils';
  export default{
    name:'order-input-edit',
    props:{
      editOrder:{
        type:Object
      },
      customerData:{
        type:Array
      },
      currentTab:{
          type:String
      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        editOrderData:Object.assign({},this.editOrder),
        parentCustCode:this.editOrder.cust_code
          ?this.editOrder.cust_code : this.customerData[0] && this.customerData[0].cust_code ?
            this.customerData[0].cust_code : null,
        modelItemData:[],
        modelData:[],
        itemData:[],
        selectDialog:false,
        selectModuleObj:{model_info:{}},
        selectType:'',
        loading:true,
        pickerOptions: {
//          disabledDate(time) {
//            return time.getTime() < Date.now() - 8.64e7;
//          }
        },
        tabIndex:1,
        orderRules:{
          cust_code:[
            { required: true, message: '请选择用户', trigger:   'change' }
          ],
        },
        pagesize: 15,
        currentPage: 1,
        pagedatacount: 1000,
        searchModel:'',
        isShowMaterials:false,
        materialsOrderData:null,
        multipleSelectionItem:[],
        selectMaterialsTypeDialog:false,
        currentMaterialsType:[],
        materialsType:[]
      }
    },
    computed:{

    },
    created() {
      this.getOrderItem();
      this.editOrderData.cust_code =
        this.editOrder.cust_code
        ? this.editOrder.cust_code : this.customerData[0]
        && this.customerData[0].cust_code ?
          this.customerData[0].cust_code : null;
    },
    methods: {
      getOrderItem:function () {
        const api = this.$store.state.DEV_API;
        if(this.optType == 'addOrder' ){
          return false
        }
        this.modelItemData.splice(0);
        fetchAPI('get',api +
          '/api/fcst/fcst_order_item/?fcst_order_id='+
          this.editOrderData.fcst_order_id,null,this).then((res) => {
            if(res && res.status == 200){
              this.modelItemData = res.data;
            }
        });
      },
      getModelData: function () {
        this.modelData.length = 0;
        const api = this.$store.state.DEV_API;
        let url = api +
          '/api/product/models/?page='+this.currentPage+'&pagesize='+this.pagesize+'&cust_code='+this.editOrderData.cust_code+'&search='+this.searchModel;
        fetchAPI('get',url,null,this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount =  Number(res.headers.pagedatacount);
            this.modelData = res.data;
            this.loading = false;
          }
        })
      },
      getItemData: function (model_inner_code) {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/product/items/?model_inner_code='+model_inner_code,null,this).then((res) => {
          if (res && res.status == 200) {
            this.itemData = res.data;
            this.loading = false;
          }
        })
      },
      getMaterialsType:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcstpr/fcst_order_material/?fcst_order_id='+this.editOrderData.fcst_order_id,null,this).then((res) => {
          if (res && res.status == 200){
            this.materialsType.length = 0;
            this.currentMaterialsType.splice(0);
            this.materialsType = res.data;
            for(let i in res.data){
              if(!res.data[i].fcst_pr_no){
                this.currentMaterialsType.push(res.data[i].meta_code);
              }
            }
          }
        })
      },
      handleCurrentChange:function (val) {
        this.currentPage = val;
        this.getModelData();
      },
      changeCustCode:function (cust_code) {
        if(cust_code === ''){
          this.editOrderData.cust_code = this.parentCustCode;
          let data = {
            type:'addCustomer',
            data:{
              addresses:[],
              contacts:[],
              cust_code:'',
              cust_name:'',
              extend:'',
              parent_cust_code:'',
              parent_currentTab:this.currentTab,
            }
          };
          this.$emit('changeTabs',data);
        }else{
          if(this.parentCustCode != cust_code){
            this.modelItemData.splice(0)
            this.getOrderItem();
            this.modelData.length = 0;
            this.parentCustCode = cust_code;
          }
        }
      },
      addModelItem:function () {
        this.getModelData();
        this.selectType = 'model';
        this.selectDialog = true;
        this.loading = true;
      },
      checkModel:function (row) {
        this.itemData.length = 0;
        this.loading = true;
        this.selectType = 'item';
        this.selectModuleObj = row;
        this.selectModuleObj.cust_info = row.cust_info.cust_code;
        this.selectModuleObj.model_info = {
          model_inner_code:row.model_inner_code,
          model_name:row.model_name,
          model_code:row.model_code
        },
        this.getItemData(row.model_inner_code);
      },
      checkItem:function () {
        this.selectType = '';
        this.selectDialog = false;
        this.searchModel = '';
        for(let i in this.multipleSelectionItem){
          let obj = {};
          let row = this.multipleSelectionItem[i];
          let selectModuleObj =
            JSON.parse(JSON.stringify(this.selectModuleObj));
          selectModuleObj.item_inner_code = row.item_inner_code;
          selectModuleObj.item_code = row.item_code;
          selectModuleObj.item_name = row.item_name;
          obj.item_info = selectModuleObj;
          obj.quantity = 0;
          obj.delivery_date = getFirstDayOfWeek();
          this.modelItemData.push(obj);
        }
        this.selectModuleObj = {};
      },
      handleSelectionChange:function (val) {
        this.multipleSelectionItem = val;
      },
      changModelItem:function (index,formName) {//update
        const api = this.$store.state.DEV_API;
        if(this.modelItemData[index].fcst_order_item_id){//update
          setTimeout(() => {
            let date = this.modelItemData[index].delivery_date;
            let obj = {
              item_info: this.modelItemData[index].item_info.item_inner_code,
              quantity: this.modelItemData[index].quantity,
              delivery_date: typeof date == 'string' ? date :
                date.getFullYear()  +  '-' +  (date.getMonth() + 1) + '-' + date.getDate(),
              extend: null
            };
            fetchAPI('put',api +
              '/api/fcst/orderitemupdate/?fcst_order_item_id='+this.modelItemData[index].fcst_order_item_id,obj,this).then((res) => {
              if(res && res.status == 200){
                this.$set(this.modelItemData[index],'type','ok');
              }else{
                this.$set(this.modelItemData[index],'type','no');
              }
            });
          }, 500);
        }else{//add
          if(this.editOrderData.fcst_order_id){
            setTimeout(() => {
              let data = {};
              let date = this.modelItemData[index].delivery_date;
              data.item_info =
                this.modelItemData[index].item_info.item_inner_code;
              data.quantity = this.modelItemData[index].quantity;
              data.delivery_date = date.getFullYear()  +  '-' +  (date.getMonth() + 1) + '-' + date.getDate();
              data.extend = null;
              data.fcst_order_id =  this.editOrderData.fcst_order_id;
              const api = this.$store.state.DEV_API;
              fetchAPI('post',api +
                '/api/fcst/fcst_order_item/',data,this).then((res)  => {//add item
                if(res && res.status == 201){
                  this.$set(this.modelItemData[index],'fcst_order_item_id',res.data.fcst_order_item_id);
                  this.$set(this.modelItemData[index],'type','ok');
                }else{
                  this.$set(this.modelItemData[index],'type','no');
                }
              });
            }, 500);
          }else{//无 order
            this.$message({
              message: '请先保存订单',
              type: 'warning'
            });
          }
        }
      },
      deleteModeItem:function (index) {
        if(this.modelItemData[index].fcst_order_item_id){//后台删
          this.$confirm('确认删除吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const api = this.$store.state.DEV_API;
            fetchAPI('delete',api +
              '/api/fcst/fcst_order_item/',{data:[this.modelItemData[index].fcst_order_item_id]},this).then((res) => {
              if(res && res.status == 204){
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
                this.modelItemData.splice(index,1);
              }
            })
          }).catch((err) => {
            console.log(err);
          })
        } else{
          this.modelItemData.splice(index,1);
        }
      },
      saveEdit:function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            const api = this.$store.state.DEV_API;
            if(this.editOrderData.fcst_order_id){//update
              fetchAPI('put',api +  '/api/fcst/orderupdate/?fcst_order_id=' + this.editOrderData.fcst_order_id,this.editOrderData,this).then((res) => {
                if(res && res.status == 200){
                  this.$emit('isUpdate',this.optType+'_'+this.editOrderData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                }
              });
            }else{
              fetchAPI('post',api + '/api/fcst/fcst_order/',this.editOrderData,this).then((res) => {
                if(res && res.status == 201){
                  this.$emit('isUpdate',this.optType+'_'+this.editOrderData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                  this.$set(this.editOrderData,'fcst_order_id',res.data.fcst_order_id);
                  this.editOrderData.fcst_order_no =
                    res.data.fcst_order_no;
                }
              });
            }
          } else {
            return false;
          }
        })
      },
      deleteOrder:function () {
        this.$confirm('确认删除吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const api = this.$store.state.DEV_API;
          fetchAPI('delete',api +
            '/api/fcst/orderupdate/?fcst_order_id='+this.editOrderData.fcst_order_id,null,this).then((res) => {
            if(res.status == 204){
              this.$emit('isUpdate',this.optType+'_'+this.editOrderData.tabIndex,true);
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.cancelTab();
            }
          });
        }).catch((err) => {
          console.log(err);
        });
      },
      editProductInfo:function (type) {
        this.selectType = '';
        this.selectDialog = false;
        if(type == 'add'){
          let data = {
            type:'addProduct',
            data:{
              model_code:'',
              model_name:'',
              iman_code:'',
              mpc_code:'',
              cust_info:this.editOrderData.cust_code,
              pr_method:'',
              po_duration:0,
              produce_duration:0,
              delivery_duration:0,
              safe_duration:0,
              cut_produce_duration:0,
              extend:{
                elastic_lower_ratio:{name:'下弹比率',value:0},
                elastic_higher_ratio:{name:'上弹比率',value:0},
                elastic_week_start:{name:'弹性起始周',value:''},
                elastic_week_end:{name:'弹性结束周',value:''},
                delivery_week_first:{name:'首单交期周',value:''},
                delivery_week_last:{name:'尾单交期周',value:''},
                fabric_ratio:{name:'色布比率',value:0},
                rough_ratio:{name:'毛坯比率',value:0},
                yarn_ratio:{name:'纱比率',value:0},
                pr_method:{name:'备料方式',value:''}
              },
              tabIndex:this.tabIndex,
              currentCustCode:this.editOrderData.cust_code,
              parent_currentTab:this.currentTab,
            }
          };
          this.tabIndex++;
          this.$emit('changeTabs',data);
        }else if(type == 'edit'){
          let data = {
            type:'editProduct',
            data:this.selectModuleObj
          };
          if(!this.selectModuleObj.extend){
            this.selectModuleObj.extend = {
              elastic_lower_ratio:{name:'下弹比率',value:0},
              elastic_higher_ratio:{name:'上弹比率',value:0},
              elastic_week_start:{name:'弹性起始周',value:''},
              elastic_week_end:{name:'弹性结束周',value:''},
              delivery_week_first:{name:'首单交期周',value:''},
              delivery_week_last:{name:'尾单交期周',value:''},
              fabric_ratio:{name:'色布比率',value:0},
              rough_ratio:{name:'毛坯比率',value:0},
              yarn_ratio:{name:'纱比率',value:0},
              pr_method:{name:'备料方式',value:''}
            }
          }
          this.$emit('changeTabs',data);
        }
      },
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editOrderData.tabIndex);
      },
      closeDialog:function () {
        this.searchModel = '';
      },
      returnModel:function () {
        this.selectType = 'model';
      },
      selectMaterialsType:function () {
        this.getMaterialsType();
        this.selectMaterialsTypeDialog = true;
      },
      createMaterials:function () {
        this.selectMaterialsTypeDialog = false;
        let data = {
          material_type_meta:this.currentMaterialsType,
          fcst_order_id:this.editOrderData.fcst_order_id
        }
        const api = this.$store.state.DEV_API;
        fetchAPI('post',api + '/api/fcstpr/estorder2pr/',data,this).then((res) => {
          if(res && res.status == 200){
            this.isShowMaterials = true;
            this.materialsOrderData = res.data;
          }
        });
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_edit_contain{
    height: 100%;
    padding:20px 10px 10px 10px;
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
        width:25%;
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
                .item_content{
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
