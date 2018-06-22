<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-input
            style="width:220px;"
            placeholder="输入订单编号"
            v-model="modelName"
            :icon="iconShow ? 'search' :'circle-close'"
            @change="handleIconClick"
            :on-icon-click="iconShowFun">
          </el-input>
        </div>
        <div class="inline_block mb3">
          <el-select v-model="customerName"
                     placeholder="请选择"
                     @change="selectChange()" @clear="clearName()">
            <el-option value="">请选择</el-option>

            <el-option v-for="item in userOption"
                       :key="item.customer_id"
                       :label="item.customer_name"
                       :value="item.customer_name">
            </el-option>
          </el-select>

          <el-button type="danger"
                     class="handle-del mr10"
                     @click="delBtnShowModal()"
                     :data="multipleSelection"
                     :disabled="multipleSelection.length <= 0">批量删除
          </el-button>
          <!--<el-button type="danger"-->
                     <!--class="handle-del mr10"-->
                     <!--@click="testDialog(1)">test-->
          <!--</el-button>-->
        </div>

      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              {{listName}}
            </h4>
          </div>
          <el-card>
            <el-table ref="multipleTable"
                      :data="tableData"
                      border
                      tooltip-effect="dark"
                      style="width: 100%"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="55">
              </el-table-column>
              <el-table-column prop="fcst_order_no"
                               label="订单单号"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column prop="customer.customer_name"
                               label="客户名称"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column label="操作" width="150" style="position: relative;border:5px solid blue;">
                <template scope="scope">
                  <el-button size="small"  @click="addCheckTab(scope.$index, scope.row)">查看</el-button>
                  <!--<el-button size="small"  @click="delCheckTab(scope.$index, scope.row)" >删除</el-button>-->
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination clearfix" style="line-height: 32px;">
              <div class="total fl">
                共 <b>{{pagedatacount}}</b> 条数据
              </div>
              <div class="pagination_tool fr">
                <el-pagination
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :current-page="currentPage"
                  :page-sizes="[10, 20, 50, 100]"
                  :page-size="pagesize"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="pagedatacount">
                </el-pagination>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <el-dialog title="库存抵扣" style="float: left" :visible.sync="moreAddBtn" size="large">
      <material-stock-dialog-box :mrpPrItemId="va" :ccc="1" :bbb="2">

      </material-stock-dialog-box>
      <!--<model-list @getDialogInfo="getDialogInfo"-->
                  <!--:onlyGetItem="onlyGetItem"-->
                  <!--:otherParameter="otherparameter"-->
                  <!--:tableName="tableName"-->
                  <!--:tableType="tableType"-->
                  <!--v-if="moreAddBtn">-->
      <!--</model-list>-->
    </el-dialog>

  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import requst from "../../common/vmrequst.js";
  import showModal from "../../common/messageBox";
  import materialStockDialogBox from "../../mrp/common/material_stock/material_stock_dialogbox";

  export default {
    name: 'sample_info',
    props: {
      TABSValue: String,
      tabIndex: Number,
      tableName: String,
      tableType: Number,
    },
    components: {
      materialStockDialogBox
    },
    data() {
      return {
        options: [],//下拉框
        tableData: [],//表格数据
        tableColumn: [],//表格列字段
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        delBtnStatus: true,
        customerName: '',
        itemValue: "",
        multipleSelection: [],
        deleteModelId: [],
        deleteData: [],
        listName: this.tableName + '列表',
        modelName: "", //查询值
        gridData: [],
        nowIndex: 0, //当前行的下标
        iconShow: true,
        userOption: [],
        userValue: '',
        va: 0,
        moreAddBtn: false
      }
    },
    methods: {
      testDialog(va) {
        this.va = va;
        this.moreAddBtn = !this.moreAddBtn;
      },
      //获取客户信息
      getCustomerInfo() {
        // 获取用户列表
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/customer/customers/?all=1', null, this).then((res) => {
          if (res && res.status === 200) {
            for (let item of res.data.data) {
              this.userOption.push(item);
            }
          }
        })
      },
      //操作更多下拉菜单触发事件
      handleCommand(command) {
        console.log(command);
      },
      // 下拉选框发送请求
      selectChange() {
        this.vmRequst(this.customerName, this.modelName);
      },
      clearName() {
        this.customerName='';
      },
      handleSelectionChange(value) {
        this.multipleSelection = value;
      },
      // 分页
      handleCurrentChange: function (val) {
        this.currentPage = val;
        this.vmRequst(this.customerName, this.modelName);
      },
      // 修改分页条数
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequst(this.customerName, this.modelName);
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        let newTabName = ++this.chlidTabIndex + '';
        let watchChildTABS = {
          title: this.tableName + '-详情',
          name: newTabName,
          closable: true,
          rowId: row.fcst_order_id
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS)
      },
      //删除确认
      delBtnShowModal(){
        showModal.showModal(this, this.delBtn, "", "确定要删除此数据！ 是否继续?", '操作提示', "是", "否");
      },
      //点击批量删除按钮
      delBtn (){
//        console.log(rows);
        let deleteArr = [];
        this.multipleSelection.forEach(item => {
          deleteArr.push(item.fcst_order_id);
        })
        const api =  this.$store.state.NEW_API;
        fetchAPI('delete', api+'/api/newfcst/fcst_orders/',{data:deleteArr} , this).then((res) => {
          if(res.status === 204){
            this.vmRequst();
            this.getCustomerInfo();
          }
        });
      },
      //查询按钮
      handleIconClick() {
        if (this.modelName === "" || this.modelName === null || !this.modelName) {
          this.vmRequst(this.customerName, this.modelName);
          return;
        }
        this.iconShow = false;
        this.vmRequst(this.customerName, this.modelName);
      },
      /*
      * 网络请求, 获取选样订单列表数据
      */
      vmRequst(customerName="", search="") {
        let url ='/api/newfcst/fcst_orders/?page=' + this.currentPage + '&pagesize=' + this.pagesize +
          '&search=' + search + "&customer__customer_name=" + customerName + '&order_type=' + this.tableType;
        requst.requst(this,url, function (that, objRes) {
          that.tableData = objRes.data.data;
          that.pagedatacount = objRes.data.total_number;
        });
      },
      //查询框icon控制
      iconShowFun() {
        if (this.iconShow) return;
        this.iconShow = true;
        this.modelName = "";
//        this.vmRequst(this.pagesize, this.currentPage);
      },

    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == '1') {
          this.vmRequst();
        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    updated() {
      if (this.multipleSelection.length > 0) {
        this.delBtnStatus = false;
      } else {
        this.delBtnStatus = true;
      }
    },
    //只执行一次
    mounted() {
      this.vmRequst();
      this.getCustomerInfo();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .mb3:last-child {
    float: right;
    margin-right: 50px;
    .el-select {
      float: left;
      margin-right: 10px;
    }
  }
  .el-dropdown{
    margin-left:5px;
    color:#4db3ff;
  }
</style>
