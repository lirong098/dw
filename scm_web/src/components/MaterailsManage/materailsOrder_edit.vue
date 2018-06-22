<template>
  <div class="order_edit_contain">
    <div class="order_edit_main">
      <el-form :model="editOrderData"
               class="demo-form-inline"
               label-width="80px" :rules="orderRule"
               ref="orderForm">
        <div class="clearfix">
          <div class="fl main-card-box">
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  备料信息
                </h4>
              </div>
              <el-card>
                <el-form-item label="下单类型" v-if="editOrderData.fcst_pr_id">
                  <div class="edit_materails_input">
                    {{editOrderData.meta_name}}
                  </div>
                </el-form-item>
                <el-form-item label="下单类型"
                              v-if="!editOrderData.fcst_pr_id">
                  <div class="edit_materails_input">
                    手工备料单
                  </div>
                </el-form-item>
                <el-form-item label="备料单号">
                  {{editOrderData.fcst_pr_no || '暂无'}}
                </el-form-item>
                <el-form-item
                  label="原料类型">
                  <el-select
                    :disabled="!!editOrderData.fcst_pr_id"
                    v-model="editOrderData.material_type_meta.meta_code"
                    @change="changeMaterialsType"
                    placeholder="请选择">
                    <el-option
                      v-for="item in materialsType"
                      :key="item.meta_code"
                      :label="item.meta_name"
                      :value="item.meta_code">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="日期">
                  <div class="edit_materails_input">
                    <el-date-picker
                      v-model="editOrderData.fcst_order_delivery_date"
                      type="week"
                      format="yyyy 第 WW 周"
                      :editable="false" :clearable="false"
                      placeholder="选择周"
                      :picker-options="pickerOptions">
                    </el-date-picker>
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
              <el-button @click="addModels" type="info"
                         v-if="editOrderData.material_type_meta.meta_value === 'NONSIZE'"
                         :disabled="!editOrderData.fcst_pr_id">
                添加Model
              </el-button>
              <el-button @click="addModelItem" type="info"
                         :disabled="!editOrderData.fcst_pr_id"
              v-else>
                添加Item
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button @click="deleteOrder"
                         :disabled="!editOrderData.fcst_pr_id"
                         type="danger">删除
              </el-button>
            </el-card>
          </div>
        </div>
        <div class="main-card-box paddingTop0"
             v-if="modelItemData
           && modelItemData.length">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Item
              </h4>
            </div>
            <el-card>
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
              <div class="pagination clearfix">
                <!--<div class="total fl">-->
                <!--共 <b>{{item_pagedatacount}}</b> 条数据-->
                <!--</div>-->
                <div class="pagination_tool fr">
                  <el-pagination
                    layout="prev, pager, next"
                    :current-page.sync="item_currentPage"
                    @current-change="handleCurrentModelItemChange"
                    :page-size="item_pagesize"
                    :total="item_pagedatacount">
                  </el-pagination>
                </div>
              </div>
              <!--<el-form-item label="Item">-->
                <!--<el-card class="box-card"-->
                         <!--&gt;-->
                  <!--<div v-for="(item,index) in-->
            <!--modelItemData"-->
                       <!--:class="{detail_item:true,model_item:true}">-->
                    <!--<el-form :inline="true" :model="item" class="demo-form-inline">-->
                      <!--<div class="">-->
                        <!--<el-form-item label="Model">-->
                          <!--{{item.item_info.model_info.model_code}}-->
                          <!--&nbsp;&nbsp;&nbsp;-->
                          <!--{{item.item_info.model_info.model_name}}-->
                        <!--</el-form-item>-->
                      <!--</div>-->
                      <!--<div class="item_content">-->
                        <!--<el-form-item label="Item">-->
                          <!--{{item.item_info.item_name}}-->
                          <!--&nbsp;&nbsp;&nbsp;-->
                          <!--{{item.item_info.item_code}}-->
                        <!--</el-form-item>-->
                      <!--</div>-->
                      <!--<div class="quantity_content">-->
                        <!--<el-form-item label="数量">-->
                          <!--<el-input-number size="small"-->
                                           <!--:min="0"-->
                                           <!--@change="changModelItem(index)"-->
                                           <!--v-model="item.quantity"></el-input-number>-->
                        <!--</el-form-item>-->
                      <!--</div>-->
                      <!--<span class="icon_content"  v-show="item.type == 'ok'">-->
                  <!--<i class="icon icon16 icon_correct"></i>-->
                <!--</span>-->
                      <!--<span class="icon_content" v-show="item.type == 'no'">-->
                  <!--<i class="icon icon16 icon_error"></i>-->
                <!--</span>-->
                      <!--<el-form-item>-->
                        <!--<el-button-group>-->
                          <!--<el-button type="info"-->
                                     <!--icon="plus" size="mini"-->
                                     <!--@click="addModelItem(index)"></el-button>-->
                          <!--<el-button type="danger"-->
                                     <!--icon="delete" size="mini"-->
                                     <!--@click="deleteModeItem(index)"></el-button>-->
                        <!--</el-button-group>-->
                      <!--</el-form-item>-->
                    <!--</el-form>-->
                  <!--</div>-->
                  <!--<div class="load_more" v-if="optType ==-->
        <!--'editOrder'">-->
                    <!--<el-button type="info" :loading="item_loading"-->
                               <!--@click="getOrderItemData"-->
                               <!--v-show="item_currentPage - 1 <-->
                         <!--item_PageCount"-->
                    <!--&gt;加载更多-->
                    <!--</el-button>-->
                  <!--</div>-->
                <!--</el-card>-->
              <!--</el-form-item>-->
            </el-card>
          </div>
        </div>
        <div class="main-card-box paddingTop0"
             v-if="modelsData
           && modelsData.length">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Model
              </h4>
            </div>
            <el-card>
              <el-table
                :data="modelsData"
                class="item_table_hack"
                style="width: 100%">
                <el-table-column
                  prop="model_info.model_code"
                  width="110"
                  label="ModelCode">
                </el-table-column>
                <el-table-column
                  prop="model_info.model_name"
                  :show-overflow-tooltip="true"
                  min-width="250"
                  label="ModelName">
                </el-table-column>
                <el-table-column
                  min-width="150"
                  label="数量">
                  <template scope="scope">
                    <el-input-number size="small"
                                     :min="0"
                                     :controls="false"
                                     @change="changModels(scope.$index)"
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
                  width="130"
                  fixed="right"
                  label="操作">
                  <template scope="scope">
                    <el-button-group>
                      <el-button type="info"
                                 size="small"
                                 @click="addModels(scope.$index)">添加</el-button>
                      <el-button type="danger"
                                 size="small"
                                 @click="deleteModes(scope.$index)">删除</el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>
              <div class="pagination clearfix">
                <!--<div class="total fl">-->
                  <!--共 <b>{{item_pagedatacount}}</b> 条数据-->
                <!--</div>-->
                <div class="pagination_tool fr">
                  <el-pagination
                    layout="prev, pager, next"
                    :current-page.sync="item_currentPage"
                    @current-change="handleCurrentModelItemChange"
                    :page-size="item_pagesize"
                    :total="item_pagedatacount">
                  </el-pagination>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-form>
    </div>
    <el-dialog
      :title="selectType == 'model' ? '点击选择model' :'选择item'"
      class="diff_dialog"
      @close="closeDialog"
      :visible.sync="selectDialog"
      size="small">
      <div>
        <div class="model_search_box" v-if="selectType == 'model'">
          <div class="inline_block width50">
            <el-select v-model="cust_code"
                       @change="changeCustomer"
                       placeholder="请选择">
              <el-option
                label=""
                value="">
                <div class="select_add">
                  <el-icon name="plus"></el-icon>
                  <span>新增</span>
                </div>
              </el-option>
              <el-option
                v-for="cust in customerData"
                :key="cust.cust_code"
                :label="cust.cust_name"
                :value="cust.cust_code">
              </el-option>
            </el-select>
          </div>
          <div class="inline_block width50">
            <el-input v-model="searchModel"
                      @change="changeModel"
                      placeholder="输入model_code查询"></el-input>
          </div>
        </div>
        <el-table :data="modelData"
                  v-if="selectType == 'model'"
                  v-loading.body="loading"
                  @row-click="checkModel">
          <el-table-column property="model_code"
                           label="model_code" ></el-table-column>
          <el-table-column property="model_name"
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
        <div v-if="selectType == 'item'" class="product_btn">
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
          <el-button @click="checkItem" size="small"
                     type="info">
            确定
          </el-button>
        </div>
      </span>
    </el-dialog>
    <el-dialog
      :title="'选择model'"
      class="diff_dialog"
      @close="closeDialog"
      :visible.sync="selectModelsDialog"
      size="small">
      <div>
        <div class="model_search_box">
          <div class="inline_block width50">
            <el-select v-model="cust_code"
                       @change="changeCustomer"
                       placeholder="请选择">
              <el-option
                label=""
                value="">
                <div class="select_add">
                  <el-icon name="plus"></el-icon>
                  <span>新增</span>
                </div>
              </el-option>
              <el-option
                v-for="cust in customerData"
                :key="cust.cust_code"
                :label="cust.cust_name"
                :value="cust.cust_code">
              </el-option>
            </el-select>
          </div>
          <div class="inline_block width50">
            <el-input v-model="searchModel"
                      @change="changeModel"
                      placeholder="输入model_code查询"></el-input>
          </div>
        </div>
        <el-table :data="modelData"
                  @selection-change="handleSelectionModelsChange"
                  v-loading.body="loading">
          <el-table-column type="selection"
                           width="50"></el-table-column>
          <el-table-column property="model_code"
                           label="model_code" ></el-table-column>
          <el-table-column property="model_name"
                           label="model_name"
          ></el-table-column>
        </el-table>
        <div class="pagination clearfix">
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
        <div class="product_btn">
          <el-button type="primary"
                     @click="editProductInfo('add')"
                     size="small">添加新Model
          </el-button>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <div>
          <el-button @click="selectModelsDialog = false"
                     size="small">取消
          </el-button>
          <el-button @click="checkModels" size="small"
                     type="info">
            确定
          </el-button>
        </div>
      </span>
    </el-dialog>
  </div>
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default{
    name:'materails-edit',
    props:{
      editOrder:{
        type:Object
      },
      customerData:{
          type:Array
      },
      materialsType:{
        type:Array
      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        materailTypeSelect: [
          {
            value: 2,
            label: '手工下单'
          },
          {
            value: 3,
            label: '实单'
          },
        ],
        editOrderData:Object.assign({},this.editOrder),
        modelItemData:[],
        tabIndex:1,
        modelData:[],
        itemData:[],
        selectDialog:false,
        selectModuleObj:{model_info:{}},
        selectType:'',
        loading:false,
        orderRule:{
          fcst_order_no:[
            { required: true, message: '请填写备料单号', trigger:
              'blur' }
          ]
        },
        pickerOptions: {
//          disabledDate(time) {
//            return time.getTime() < Date.now() - 8.64e7;
//          }
        },
        cust_code:this.customerData[0] ?
          this.customerData[0].cust_code : null,
        pagesize: 15,
        currentPage: 1,
        pagedatacount: 1000,
        item_pagesize:15,
        item_currentPage:1,
        item_pagedatacount:100,
        item_PageCount:0,
        item_loading:false,
        searchModel:'',
        changeFlag:true,
        multipleSelectionItem:[],
        selectModelsDialog:false,
        multipleSelectionModels:[],
        modelsData:[]
      }
    },
    computed:{

    },
    created() {
        this.getOrderItemData();
    },
    methods: {
      getOrderItemData:function () {
        const api = this.$store.state.DEV_API;
        if(this.optType == 'addOrder'){
          return false
        }
        this.modelsData.splice(0);
        this.modelItemData.splice(0);
        if(this.editOrderData.material_type_meta.meta_value === 'NONSIZE'){
          fetchAPI('get',api +
            '/api/fcstpr/pr_models/?fcst_pr_id='+
            this.editOrderData.fcst_pr_id+'&page='+this.item_currentPage+'&pagesize='+this.item_pagesize,null,this).then((res) => {
            if(res && res.status == 200){
              this.modelsData = res.data;
              this.item_pagedatacount =  Number(res.headers.pagedatacount);
              this.item_PageCount =
                Number(res.headers.pagecount);
            }
          });
        }else{
          fetchAPI('get',api +
            '/api/fcstpr/pr_items/?fcst_pr_id='+
            this.editOrderData.fcst_pr_id+'&page='+this.item_currentPage+'&pagesize='+this.item_pagesize,null,this).then((res) => {
            if(res && res.status == 200){
              this.modelItemData =res.data;
              this.item_pagedatacount =  Number(res.headers.pagedatacount);
              this.item_PageCount =
                Number(res.headers.pagecount);
            }
          });
        }
      },
      getModelData: function () {
        this.modelData.length = 0;
        const api = this.$store.state.DEV_API;
        let url = api +
          '/api/product/models/?page='+this.currentPage+'&pagesize='+this.pagesize+'&search='+this.searchModel;
        url = url + (this.cust_code ?
          '&cust_code=' + this.cust_code : '');
        fetchAPI('get',url,null,this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount =  Number(res.headers.pagedatacount);
            this.modelData = res.data;
          }
        })
      },
      handleCurrentChange:function (val) {
        if(this.changeFlag){
          this.currentPage = val;
          this.getModelData();
        }
      },
      handleCurrentModelItemChange:function (val) {
        if(this.changeFlag){
          this.item_currentPage = val;
          this.getOrderItemData();
        }
      },
      getItemData: function (model_inner_code) {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/product/items/?model_inner_code='+model_inner_code,null,this).then((res) => {
          if (res && res.status == 200) {
            this.itemData = res.data;
          }
        })
      },
      editProductInfo:function (type) {
        this.selectType = '';
        this.selectDialog = false;
        this.selectModelsDialog = false;
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
                pr_method:{name:'备料方式',value:''},

              },
              tabIndex:this.tabIndex,
              currentCustCode:this.editOrderData.cust_code,
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
      changeCustomer:function (val) {
        if(val){
          this.changeFlag = false;
          this.currentPage = 1;
          setTimeout(() => {this.changeFlag = true}, 1000);
          this.getModelData();
        }else{//add
          this.selectType = '';
          this.selectDialog = false;
          this.selectModelsDialog = false;
          let data = {
            type:'addCustomer',
            data:{
              addresses:[],
              contacts:[],
              cust_code:'',
              cust_name:'',
              extend:'',
              parent_cust_code:''
            }
          };
          this.$emit('changeTabs',data);
        }
      },
      changeModel:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getModelData();
      },
      checkModel:function (row) {
        this.itemData.length = 0;
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
      handleSelectionChange:function (val) {
        this.multipleSelectionItem = val;
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
          selectModuleObj.item_inner_code =  row.item_inner_code;
          selectModuleObj.item_code = row.item_code;
          selectModuleObj.item_name = row.item_name;
          obj.item_info = selectModuleObj;
          obj.quantity = 0;
          this.modelItemData.push(obj);
        }
        this.selectModuleObj = {};
      },
      checkModels:function () {
        this.searchModel = '';
        this.selectModelsDialog = false;
        for(let i in this.multipleSelectionModels){
          let row = this.multipleSelectionModels[i];
          let obj = {
            model_info:{
              model_inner_code:row.model_inner_code,
              model_name:row.model_name,
              model_code:row.model_code
            },
            quantity:0
          }
          this.modelsData.push(obj);
        }
      },
      addModelItem:function () {
        this.cust_code = this.customerData[0] ?
          this.customerData[0].cust_code : null;
        this.getModelData();
        this.selectType = 'model';
        this.selectDialog = true;
      },
      addModels:function () {
        this.cust_code = this.customerData[0] ?
          this.customerData[0].cust_code : null;
        this.getModelData();
        this.selectModelsDialog = true;
      },
      handleSelectionModelsChange:function (val) {
        this.multipleSelectionModels = val;
      },
      changModelItem:function (index) {
        const api = this.$store.state.DEV_API;
        if(this.modelItemData[index].fcst_pr_item_id){
          setTimeout(() => {
            let obj = {
              item_info: this.modelItemData[index].item_info.item_inner_code,
              quantity: this.modelItemData[index].quantity,
              fcst_pr: this.editOrderData.fcst_pr_id
            };
            fetchAPI('put',api +
              '/api/fcstpr/pr_item/?fcst_pr_item_id='+this.modelItemData[index].fcst_pr_item_id,obj,this).then((res) => {
              if(res && res.status == 200){
                this.$set(this.modelItemData[index],'type','ok');
              }else{
                this.$set(this.modelItemData[index],'type','no');
              }
            });
          }, 500);
        }else{
          if(this.editOrderData.fcst_pr_id){
            setTimeout(() => {
              let data = {};
              data.item_info =
                this.modelItemData[index].item_info.item_inner_code;
              data.quantity = this.modelItemData[index].quantity;
              data.fcst_pr =  this.editOrderData.fcst_pr_id;
              const api = this.$store.state.DEV_API;
              fetchAPI('post',api +
                '/api/fcstpr/pr_items/',data,this).then((res)  => {//add item
                if(res && res.status == 201){
                  this.$set(this.modelItemData[index],'fcst_pr_item_id',res.data.fcst_pr_item_id);
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
      changModels:function (index) {
        const api = this.$store.state.DEV_API;
        if(this.modelsData[index].fcst_pr_model_id){
          setTimeout(() => {
            let obj = {
              model_info: this.modelsData[index].model_info.model_inner_code,
              quantity: this.modelsData[index].quantity,
              fcst_pr: this.editOrderData.fcst_pr_id
            };
            fetchAPI('put',api +
              '/api/fcstpr/pr_model/?fcst_pr_model_id='+this.modelsData[index].fcst_pr_model_id,obj,this).then((res) => {
              if(res && res.status == 200){
                this.$set(this.modelsData[index],'type','ok');
              }else{
                this.$set(this.modelsData[index],'type','no');
              }
            });
          }, 500);
        }else{
          setTimeout(() => {
            let obj = {
              model_info: this.modelsData[index].model_info.model_inner_code,
              quantity: this.modelsData[index].quantity,
              fcst_pr: this.editOrderData.fcst_pr_id
            };
            fetchAPI('post',api +
              '/api/fcstpr/pr_models/',obj,this).then((res)  => {//add model
              if(res && res.status == 201){
                this.$set(this.modelsData[index],'fcst_pr_model_id',res.data.fcst_pr_model_id);
                this.$set(this.modelsData[index],'type','ok');
              }else{
                this.$set(this.modelsData[index],'type','no');
              }
            });
          }, 500);
        }
      },
      deleteModeItem:function (index) {
        if(this.modelItemData[index].fcst_pr_item_id){//后台删
          this.$confirm('确认删除吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const api = this.$store.state.DEV_API;
            fetchAPI('delete',api +
              '/api/fcstpr/pr_item/?fcst_pr_item_id='+this.modelItemData[index].fcst_pr_item_id,null,this).then((res) => {
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
      deleteModes:function (index) {
        if(this.modelsData[index].fcst_pr_model_id){//后台删
          this.$confirm('确认删除吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const api = this.$store.state.DEV_API;
            fetchAPI('delete',api +
              '/api/fcstpr/pr_model/?fcst_pr_model_id='+this.modelsData[index].fcst_pr_model_id,null,this).then((res) => {
              if(res && res.status == 204){
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
                this.modelsData.splice(index,1);
              }
            })
          }).catch((err) => {
            console.log(err);
          })
        } else{
          this.modelsData.splice(index,1);
        }
      },
      saveEdit:function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            const api = this.$store.state.DEV_API;
            let date = this.editOrderData.fcst_order_delivery_date ;
            this.editOrderData.fcst_order_delivery_date =  typeof date == 'string' ? date :
              date.getFullYear()  +  '-' +
              (date.getMonth() + 1) + '-' + date.getDate();
            let data = {
              fcst_order_no:this.editOrderData.fcst_order_no,
              fcst_order_delivery_date:this.editOrderData.fcst_order_delivery_date,
              material_type_meta:this.editOrderData.material_type_meta.meta_code,
              extend:null
            };
            if(this.editOrderData.fcst_pr_id){//update
              this.editOrderData.pr_type_meta =
                this.editOrderData.meta_code == 1 ?
                  '__MC_PR_ORDER_MANUAL' :
                  this.editOrderData.meta_code == 2 ?
                    '__MC_PR_ORDER_ESTIMATE' :
                  '__MC_PR_ORDER_PROOF';
              fetchAPI('put',api +
                '/api/fcstpr/pr_order/?fcst_pr_id='+this.editOrderData.fcst_pr_id,data,this).then((res) => {
                if(res && res.status == 200){
                  this.$emit('isUpdate',this.optType+'_'+this.editOrderData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                }
              });
            }else{//add
              fetchAPI('post',api +
                '/api/fcstpr/pr_orders/?pr_order_type='+this.editOrderData.meta_code,data,this).then((res) => {
                if(res && res.status == 201){
                  this.$emit('isUpdate',this.optType+'_'+this.editOrderData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                  this.$set(this.editOrderData,'meta_name',this.editOrderData.meta_code == 1 ? '手工备料单' :
                    this.editOrderData.meta_code == 2 ?
                      '预估备料单' :
                      this.editOrderData.meta_code == 7 ?
                        '选样备料单' : '');
                  this.$set(this.editOrderData,'fcst_pr_id',res.data.fcst_pr_id);
                  this.$set(this.editOrderData,'fcst_pr_no',res.data.fcst_pr_no);
                }
              });
            }
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
            '/api/fcstpr/pr_order/?fcst_pr_id='+this.editOrderData.fcst_pr_id,null,this).then((res) => {
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
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editOrderData.tabIndex);
      },
      closeDialog:function () {
        this.searchModel = '';
      },
      returnModel:function () {
        this.selectType = 'model';
      },
      tableRowClassNameStatus:function (row,index) {
        if(row.type == 'no'){
          return 'item_error_status'
        }else if(row.type == 'ok'){
          return 'item_ok_status'
        }
        return ''
      },
      changeMaterialsType:function (val) {
        for(let i in this.materialsType){
          if(this.materialsType[i].meta_code == val){
            this.editOrderData.material_type_meta.meta_value = this.materialsType[i].meta_value;
            break
          }
        }
      },
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_edit_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .order_edit_main{
      height: 100%;
      .edit_materails_input{
        width:250px;
      }
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
  }
</style>
