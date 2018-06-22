<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-input
            style="width:220px;"
            placeholder="输入编码或名称"
            v-model="modelName"
            :icon="iconShow ? 'search' :'circle-close'"
            @change="handleIconClick"
            :on-icon-click="iconShowFun">
          </el-input>

        </div>
        <div class="inline_block mb3">
          <el-select v-if="exclude ===2" v-model="customerValue" placeholder="请选择客户" @change="selectCustomer"
                     :disabled="otherParameter.otherCustomerId >0 ? true:false">
            <el-option
              v-for="item in customerData"
              :key="item.customer_id"
              :label="item.customer_name"
              :value="item.customer_id">
            </el-option>
          </el-select>
          <el-select v-if="exclude ===2" v-model="seasonValue" placeholder="请选择季节" @change="selectSeason"
                     :disabled="otherParameter.otherSeasonId >0 ? true:false">
            <el-option
              v-for="item in seasonData"
              :key="item.meta_id"
              :label="item.meta_name"
              :value="item.meta_id">
            </el-option>
          </el-select>
          <el-dropdown type="primary" class="customer_add" @command="addNewaddCheckTab">
            <el-button type="primary">
              新增<i class="el-icon-caret-bottom el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="product">成衣</el-dropdown-item>
              <el-dropdown-item command="fabric">面料</el-dropdown-item>
              <el-dropdown-item command="accessories">辅料</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
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
                      style="width: 100%">
              <el-table-column label="编码" show-overflow-tooltip>
                <template scope="scope">
                  <a href="javascript:void(0);"
                     @click="addCheckTab(scope.$index, scope.row)">{{scope.row.model_code}}</a>
                </template>
              </el-table-column>
              <el-table-column v-for="(item,index) in tableColumn"
                               :prop="item.columnProp"
                               :label="item.columnName"
                               :key="index"
                               :width="item.columnWidth ===0 ?'':item.columnWidth"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template scope="scope">
                  <el-button size="small" @click="getItemInfo(scope.row,scope.row.model_id)">选择</el-button>
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
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import showModal from "../messageBox.js";
  import COMMON from "../common.js";

  export default {
    name: 'test-info-main',
    components: {},
    props: {
      TABSValue: String,
      tabIndex: Number,
      tableName: String, //页面显示的名字
      exclude: {
        type: Number,
        default: 2
      }, // 成衣 面料 辅料
      noGetItem: {
        type: Boolean,
        default: false
      },
      otherParameter: Object
    },
    data() {
      return {
        tableData: [],//表格数据
        tableColumn: [],//表格列字段
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        listName: this.tableName + '列表',
        modelName: "", //查询值
        iconShow: true,
        customerValue: this.otherParameter.otherCustomerId,//选中的客户值
        customerData: [],//客户数据
        seasonValue: this.otherParameter.otherSeasonId,//选中的季节值
        seasonData: [],//季节数据
      }
    },
    methods: {
      // 分页
      handleCurrentChange: function (val) {
        this.vmRequst(this.pagesize, val, 1, this.customerValue, this.seasonValue);
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequst(val, 1, 1, this.customerValue, this.seasonValue);
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        this.setTabs(row.model_type_meta_id.meta_name, row.model_type_meta_id.meta_id, "modelInfo", "", "详情", row.model_id);
      },
      addNewaddCheckTab(command) {
        let type = 1;
        let tableName = "成衣";
        if (command === "fabric") {
          type = 2;
          tableName = "面料";
        } else if (command === "accessories") {
          type = 3;
          tableName = "辅料";
        }
        this.setTabs(tableName, type, "modelInfo");
      },
      //进入详情页的TABS
      setTabs(tableName, tableType, tabName, data = "", viewOrEdit = "新增", rowId = 0) {
        let newTabName = ++this.chlidTabIndex + '';
        this.chlidTABSValue = newTabName;
        let addChildTABS = {
          title: tableName + viewOrEdit,
          name: newTabName,
          closable: true,
          rowId: rowId,
          tabName: tabName,
          tableType: tableType,
          tableName: tableName,
          data: data
        };
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      //查询按钮
      handleIconClick() {
        if (this.modelName == "" || this.modelName == null || !this.modelName) {
          this.vmRequst(this.pagesize, this.currentPage, 1, this.customerValue, this.seasonValue);
          return;
        }
        this.iconShow = false;
        this.vmRequst(10, 1, 1, this.customerValue, this.seasonValue);
      },
      /*
      * 网络请求
      * status 1 请求列表 2模糊查询(code) 4 delete*/
      vmRequst(qty = this.pagesize, page = 1, status = 1, customer_id = 0, season_meta_id = 0) {
        let url = this.vmRequstApi(qty, page, status, customer_id, season_meta_id);
        fetchAPI('get', url, null, this).then((res) => {
          this.tableData = res.data.data;
          this.pagedatacount = res.data.total_number;
        })
      },
      //请求api判断
      vmRequstApi(qty, page, type, customer_id, season_meta_id) {
        const api = this.$store.state.NEW_API;
        let url = "";
        if (this.modelName && this.modelName != '') {
          url = api + '/api/mat_models/models/?search=' + this.modelName + '&exclude=' + this.exclude;
        } else {
          url = api + '/api/mat_models/models/?page=' + page + '&pagesize=' + qty + '&exclude=' + this.exclude;
        }
        if (customer_id > 0 && customer_id) {
          url = url + '&spec__customer_id=' + customer_id
        }
        if (season_meta_id > 0 && season_meta_id) {
          url = url + '&spec__season_meta_id=' + season_meta_id
        }
        return url;
      },
      //点击选择按钮   根据model获取item信息
      getItemInfo(row, model_id) {
        if (this.noGetItem) {
          //点击选择按钮   不选择Item信息
          this.$emit("getDialogInfo", row);
          return;
        }
        this.setTabs("选择Item", 1, "item", row, " ", model_id);
      },
      //查询框icon控制
      iconShowFun() {
        if (this.iconShow) return;
        this.iconShow = true;
        this.modelName = "";
        this.vmRequst(this.pagesize, this.currentPage, 1, this.customerValue, this.seasonValue);
      },
      //选择客户过滤请求
      selectCustomer(val) {
        this.vmRequst(this.pagesize, this.currentPage, 1, val, this.seasonValue);
      },
      //选择季节过滤请求
      selectSeason(val) {
        this.vmRequst(this.pagesize, this.currentPage, 1, this.customerValue, val);
      },

    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == '1') {
          this.vmRequst(10, 1, 1, this.customerValue, this.seasonValue);
        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    created() {
      let tableColumn = [
        {
          columnName: "名称",
          columnProp: "model_name",
          columnWidth: 0
        }, {
          columnName: "客户",
          columnProp: "customer.customer_name",
          columnWidth: 0
        }, {
          columnName: "季节",
          columnProp: "season.meta_name",
          columnWidth: 120
        }
      ];
      this.tableColumn = tableColumn;
    },
    updated() {
    },
    //只执行一次
    mounted() {
      COMMON.getCustomerList(this).then(res => {
        this.customerData = res.data.data;
      })
      COMMON.getMetaList(this, 43).then(res => {
        this.seasonData = res.data;
      })
      this.vmRequst(10, 1, 1, this.otherParameter.otherCustomerId, this.otherParameter.otherSeasonId);
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
</style>
