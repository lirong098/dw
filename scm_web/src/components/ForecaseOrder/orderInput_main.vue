<template>
  <div class="order_main_contain">
    <div class="order_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-select v-model="currentOrderType"
                     @change="changeOrderType"
                     placeholder="请选择类型">
            <el-option
              v-for="item in orderTypeSelect"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
        <div class="inline_block mb3 input_length_280">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入单号或客户查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary" class="order_add"
                     @click="addOrder">新增
          </el-button>
        </div>
        <div class="inline_block mb3">
          <el-button type="danger"
                     class="handle-del mr10"
                     :disabled="!multipleSelection.length
                      || currentOrderType != 4"
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
                      ref="orderTable" v-loading.body="loading"
                      @sort-change="sortChange"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="50"></el-table-column>
              <el-table-column prop="cust_code.cust_name"
                               :show-overflow-tooltip="true"
                               sortable="custom"
                               label="客户"></el-table-column>
              <el-table-column prop="fcst_order_no"
                               :show-overflow-tooltip="true"
                               sortable="custom"
                               label="预估订单号"></el-table-column>
              <el-table-column prop="fcst_type_meta.meta_name"
                               sortable="custom"
                               label="预估订单类型"></el-table-column>
              <el-table-column prop="update_time"
                               :show-overflow-tooltip="true"
                               label="更新时间"></el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    v-show="scope.row.fcst_type_meta.meta_code ==
                           '__MC_ORDER_ESTIMATE_MANUAL'"
                    @click="editOrder(scope.$index, scope.row)">编辑</el-button>
                  <span></span>
                  <el-button
                    size="small"
                    v-show="scope.row.fcst_type_meta.meta_code !=='__MC_ORDER_ESTIMATE_MANUAL'"
                    @click="viewOrder(scope.$index,
                scope.row)">查看</el-button>
                  <span></span>
                  <el-button
                    size="small"
                    type="danger"
                    :disabled="scope.row.fcst_type_meta.meta_code !=='__MC_ORDER_ESTIMATE_MANUAL'"
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
  import {fetchAPI} from '../../utils/utils';
  export default{
    name: 'order-input-main',
    components: {},
    props: {
      editData: {
        type: Object
      },
      isFresh:{
        Boolean
      }
    },
    data () {
      return {
        selectData: '',
        searchData: '',
        orderTypeSelect: [
          {
            value: '',
            label: '所有订单'
          },
          {
            value: 1,
            label: '导入订单'
          },
          {
            value: 2,
            label: '选样订单'
          },
          {
            value: 4,
            label: '手工订单'
          }
        ],
        currentOrderType: 4,
        orderData:[],
        multipleSelection: [],
        tabIndex: 1,
        loading:false,
        pagesize: 10,
        currentPage: 1,
        pagedatacount: 1000,
        changeFlag:true,
        searchWord:'',
        sortCustomer:'',
        sortOrderNo:'',
        sortOrderType:''
      }
    },
    computed: {},
    created() {
      let type = $.cookie('orderType');
      if(type == 'null' || !type){
        this.currentOrderType = 4;
      }else{
        this.currentOrderType = 2;
        $.cookie('orderType', null);
      }
      this.getOrderData();
    },
    methods: {
      getOrderData: function () {
        this.loading = true;
        this.orderData.length = 0;
        const api = this.$store.state.DEV_API;
        let order = (this.sortCustomer + this.sortOrderNo
          + this.sortOrderType).slice(0,-1);
        let url = api +
          '/api/fcst/fcst_order/?page='+this.currentPage+'&pagesize='+this.pagesize+'&search='+this.searchWord;
        if(this.currentOrderType){
          url = url + '&order_type=' + this.currentOrderType;
        }
        fetchAPI('get',url+'&ordering='+order,null,this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount =  Number(res.headers.pagedatacount);
            this.orderData = res.data;
          }
          this.loading = false;
        })
      },
      changeOrderType:function () {
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
            cust_code:'',
            extend:null,
            tabIndex:this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs', data);
      },
      editOrder: function (index, row) {
        let rowData = Object.assign({},row);
        rowData.cust_code = rowData.cust_code.cust_code;
        let data = {
          type: 'editOrder',
          data: rowData
        };
        this.$emit('changeTabs', data);
      },
      deleteOrder: function (type,index, row) {
        const api = this.$store.state.DEV_API;
        if(type == 1){//单个
          fetchAPI('delete',api + '/api/fcst/orderupdate/?fcst_order_id='+row.fcst_order_id,null,this).then((res) => {
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
            code.push(this.multipleSelection[item].fcst_order_id);
          }
          fetchAPI('delete',api + '/api/fcst/fcst_order/',{data:code},this).then((res) => {
            if(res.status == 204){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getOrderData();
            }
          });
        }
      },
      viewOrder:function (index, row) {
        let data = {
          type: 'viewOrder',
          data: row
        };
        this.$emit('changeTabs', data);
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
        if(column.prop === "cust_code.cust_name"){
          this.sortCustomer = order +
            'cust_code__cust_name' + ',';
        }else if(column.prop === "fcst_order_no"){
          this.sortOrderNo = order + 'fcst_order_no' + ',';
        }else if(column.prop === "fcst_type_meta.meta_name"){
          this.sortOrderType = order +
            'fcst_type_meta' + ',';
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
