<template>
  <div class="order_main_contain">
    <div class="order_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-select v-model="currentOrderType"
                     @change="changeOrderType"
                     placeholder="请选择类型">
            <el-option
              v-for="item in materailsTypeSelect"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
        <div class="inline_block mb3 ">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入备料单号查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary" class="order_add"
                     @click="addOrder">新增
          </el-button>
        </div>
        <div class="inline_block mb3">
          <el-button type="danger"
                     class="handle-del mr10"
                     :disabled="!multipleSelection.length"
                     @click="deleteOrder(2)">批量删除
          </el-button>
        </div>
      </div>
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              订单列表
            </h4>
          </div>
          <el-card>
            <el-table :data="orderData"
                      @sort-change="sortChange"
                      ref="orderTable" v-loading.body="loading"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="50"></el-table-column>
              <el-table-column :show-overflow-tooltip="true"
                               sortable="custom"
                               prop="fcst_pr_no"
                               label="备料单号">
              </el-table-column>
              <el-table-column prop="pr_type_meta.meta_name"
                               sortable="custom"
                               :show-overflow-tooltip="true"
                               label="备料单类型"></el-table-column>
              <el-table-column prop="material_type_meta.meta_name"
                               label="原料类型"></el-table-column>
              <el-table-column prop="create_time"
                               sortable="custom"
                               :show-overflow-tooltip="true"
                               label="创建时间"></el-table-column>
              <el-table-column prop="update_time"
                               sortable="custom"
                               :show-overflow-tooltip="true"
                               label="更新时间"></el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    @click="editOrder(scope.$index, scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="deleteOrder(1,scope.$index,
                scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination clearfix">
              <div class="total fl">
                共 <b>{{pagedatacount}}</b> 条数据
              </div>
              <div class="pagination_tool fr">
                <el-pagination
                  layout="sizes,prev, pager, next"
                  :current-page.sync="currentPage"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :page-sizes="[10,15,20, 50, 100]"
                  :page-size="pagesize"
                  :total="pagedatacount">
                </el-pagination>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {fetchAPI,getFirstDayOfWeek} from '../../utils/utils';
  export default{
    name: 'materails-main',
    components: {},
    props: {
      isFresh:{
          Boolean
      }
    },
    data () {
      return {
        selectData: '',
        searchData: '',
        materailsTypeSelect: [
          {
            value: 'all',
            label: '所有备料单'
          },
          {
            value: 2,
            label: '预估备料单'
          },
          {
            value: 1,
            label: '手工备料单'
          },
          {
            value: 3,
            label: '选样备料单'
          },
          {
            value:4,
            label:'预估手工单'
          }
        ],
        currentOrderType: 'all',
        orderData:[],
        multipleSelection: [],
        tabIndex: 1,
        loading:false,
        pagesize: 10,
        currentPage: 1,
        pagedatacount: 100,
        changeFlag:true,
        searchWord:'',
        sortPrNo:'',
        sortMeta:'',
        sortCreateTime:'',
        sortUpdateTime:''
      }
    },
    computed: {},
    created() {
      this.getOrderData();
    },
    methods: {
      getOrderData: function () {
        this.loading = true;
        this.orderData.length = 0;
        const api = this.$store.state.DEV_API;
        let order = (this.sortPrNo + this.sortMeta
        + this.sortCreateTime + this.sortUpdateTime).slice(0,-1);
        let geturl =
          api+'/api/fcstpr/pr_orders/?pr_order_type='+
          this.currentOrderType+'&page=';
        fetchAPI('get',geturl+this.currentPage+'&pagesize='+this.pagesize+'&search='+this.searchWord+'&ordering='+order,null,this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount =  Number(res.headers.pagedatacount);
            this.orderData = res.data;
          }
          this.loading = false;
        })
      },
      changeOrderType:function (type) {
        this.currentOrderType = type;
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getOrderData();
      },
      handleSizeChange:function (val) {
        this.pagesize = val;
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getOrderData();
      },
      handleCurrentChange:function (val) {
        if(this.changeFlag){
          this.currentPage = val;
          this.getOrderData();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      addOrder: function () {
        let data = {
          type: 'addOrder',
          data: {
            extend:null,
            fcst_pr_no:'',
            meta_code:1,
            material_type_meta:{
              meta_code:'__MC_MATERIAL_FABRIC',
              meta_value:'NONSIZE'
            },
            nonsize_model_info:{
              model_name:'',
              model_inner_code:'',
              model_code:''
            },
            nonsize_quantity:0,
            fcst_order_delivery_date: getFirstDayOfWeek(),
            tabIndex:this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs', data);
      },
      editOrder: function (index, row) {
        row.meta_code = row.pr_type_meta.meta_code ==
        '__MC_PR_ORDER_ESTIMATE' ? 2 :
          row.pr_type_meta.meta_code ==
          '__MC_PR_ORDER_MANUAL' ? 1 :
          row.pr_type_meta.meta_code ==
          '__MC_PR_ORDER_PROOF' ? 3 : '';
        row.meta_name = row.pr_type_meta.meta_name;
        row.fcst_order_delivery_date =
          row.fcst_order_delivery_date || getFirstDayOfWeek();
        delete row.submitter;
        let data = {
          type: 'editOrder',
          data: row
        };
        this.$emit('changeTabs', data);
      },
      deleteOrder: function (type,index, row) {
        const api = this.$store.state.DEV_API;
        if(type == 1){//单个
          fetchAPI('delete',api + '/api/fcstpr/pr_order/?fcst_pr_id='+row.fcst_pr_id,null,this).then((res) => {
            if(res.status == 204){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getOrderData();
            }
          });
        }else{//多个
          let code = [];
          for(let item in this.multipleSelection){
            code.push(this.multipleSelection[item].fcst_pr_id);
          }
          fetchAPI('delete',api + '/api/fcstpr/pr_orders/',{data:code},this).then((res) => {
            if(res.status == 204){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.loading = true;
              this.orderData.length = 0;
              this.getOrderData();
            }
          });
        }
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getOrderData();
      },
      searchByWord:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getOrderData();
      },
      sortChange:function (column) {
        let order = column.order === "descending" ? '-' :
          '';
        if(column.prop === "fcst_pr_no"){
          this.sortPrNo = order +
            'fcst_pr_no' + ',';
        }else if(column.prop === "pr_type_meta.meta_name"){
          this.sortMeta = order + 'pr_type_meta' + ',';
        }else if(column.prop === "create_time"){
          this.sortCreateTime = order +
            'create_time' + ',';
        }else if(column.prop === "update_time"){
          this.sortUpdateTime = order +
            'update_time' + ',';
        }
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getOrderData();
      }
    },
    watch: {
      isFresh(){
        this.getOrderData();
      }
    },
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_main_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    .order_main_main {
      height: 100%;
      .head_tool {
        .mb3 {
          margin-bottom: 3px;
        }
        .search_input {
          width: 150px;
        }
      }
      .table_content {

      }
    }
  }
</style>
