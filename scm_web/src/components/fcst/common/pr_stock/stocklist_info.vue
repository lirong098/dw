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
          <el-radio-group v-model="radio3" v-if="showRadio">
            <el-radio-button label="未生成MRP备料"></el-radio-button>
            <el-radio-button label="已生成MRP备料"></el-radio-button>
          </el-radio-group>

          <!--<el-select v-model="value"-->
          <!--placeholder="请选择"-->
          <!--@change="selectChange(value)">-->
          <!--<el-option v-for="item in options"-->
          <!--:key="item.value"-->
          <!--:label="item.label"-->
          <!--:value="item.value">-->
          <!--</el-option>-->
          <!--</el-select>-->
          <el-button type="primary" class="customer_add"
                     @click="addNewaddCheckTab" v-if="fcstType ===8">新增
          </el-button>
          <el-button type="danger"
                     class="handle-del mr10"
                     :data="multipleSelection"
                     :disabled="delBtnStatus"
                     @click="delBtnShowModal()">批量删除
          </el-button>
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
              <el-table-column prop="fcst_pr_no"
                               label="备料单号"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column prop="delivery_date"
                               label="备料交期"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column label="是否发送MRP">
                <template scope="scope">
                  <span>{{scope.row.is_send_mrp ? '是':'否'}}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" style="position: relative;border:5px solid blue;">
                <template scope="scope">
                  <el-button size="small" @click="addCheckTab(scope.$index, scope.row)">查看</el-button>

                  <!--<el-dropdown @command="handleCommand">-->
                    <!--<span class="el-dropdown-link" v-show="fcstType != 6">-->
                    <!--更多<i class="el-icon-caret-bottom el-icon&#45;&#45;right"></i>-->
                    <!--</span>-->
                    <!--<el-dropdown-menu slot="dropdown">-->
                      <!--<el-dropdown-item :command="scope.row">完成</el-dropdown-item>-->
                      <!--<el-dropdown-item :command="scope.row">分派</el-dropdown-item>-->
                    <!--</el-dropdown-menu>-->
                  <!--</el-dropdown>-->

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
  import {fetchAPI} from '../../../../utils/utils';
  import showModal from "../../../common/messageBox.js";
  import requst from "../../../common/vmrequst.js";

  export default {
    name: 'stocklist_info',
    props: {
      TABSValue: String,
      tabIndex: Number,
      tableName: String,
      fcstType: Number,
    },
    data() {
      return {
        options: [],//下拉框
        tableData: [],//表格数据
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        delBtnStatus: true,
        value: '',
        itemValue: "",
        multipleSelection: [],
        deleteModelId: [],
        deleteData: [],
        listName: this.tableName + '列表',
        modelName: "", //查询值
        gridData: [],
        nowIndex: 0, //当前行的下标
        iconShow: true,
        radio3: "未生成MRP备料",
        showRadio:false //是否显示MRP备料按钮
      }
    },
    methods: {
      //操作更多下拉菜单触发事件
      handleCommand(command) {
      },
      // 下拉选框发送请求
      selectChange(value) {
      },
      //删除确认
      delBtnShowModal(){
        showModal.showModal(this, this.delBtn, "", "确定要删除此数据！ 是否继续?", '操作提示', "是", "否");
      },
      // 删除按钮
      delBtn() {
        this.multipleSelection.forEach(this.forModel);
        fetchAPI('delete', this.$store.state.NEW_API+'/api/mat_models/fcst_prs/', {data:this.deleteModelId}, this).then(res=>{
          if(res.status == 204){
            showModal.showMessage(this,"success", "删除成功");
            this.deleteModelId.forEach(row=>{
              this.tableData = this.tableData.filter(row2=>{
                return row2.fcst_pr_id !== row
              });
            })
            this.deleteModelId = [];
          }
        })
      },
      handleSelectionChange(value) {
        this.multipleSelection = value;
      },
      //获取多列数据中的fcst_pr_id
      forModel(item, index, array) {
        this.deleteModelId[index] = item.fcst_pr_id;
      },
      // 分页
      handleCurrentChange: function (val) {
        this.vmRequst(this.pagesize, val);
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequst(val, 1);
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        let newTabName = ++this.chlidTabIndex + '';
        let watchChildTABS = {
          title: this.tableName + ' - 查看',
          name: newTabName,
          closable: true,
          rowId: row.fcst_pr_id
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS)
      },
      //点击添加按钮
      addNewaddCheckTab() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.tableName + ' - 新增',
          name: newTabName,
          closable: true,
          rowId: 0
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS)
      },
      //查询按钮
      handleIconClick() {
        if (!this.modelName || this.modelName === "" || this.modelName === null ) return;
        this.iconShow = false;
        this.vmRequst();
      },
      /*
      * 网络请求
      */
      vmRequst(qty = this.pagesize, page = 1) {
        let id = this.getStockType();
        let url ='/api/mat_models/fcst_prs/?page=' + page + '&pagesize=' + qty+ '&fcst_pr_type_meta_id__meta_id=' + id;
        if(this.modelName && this.modelName !==''){
          url = url+'&search=' + this.modelName;
        }
        requst.requst(this, url, function (that, objRes) {
          that.tableData = objRes.data.data;
          that.pagedatacount = objRes.data.total_number;
        });
      },
      getStockType(){
        /*组件说明
* fcstType{1：mrp_成衣备料,2:mrp_成衣实单,3:选样实单,4:预估订单,5:预估实单,6:选样备料,7:预估备料,8:手工备料}
* meta 成衣备料{12：预估备料，13：实单翻单，14：实单首单，16：选样备料，17：盘点入库，18：盘点出库，35：直接备料}
* */
        let id= 0;
        switch (this.fcstType){
          case 1:
            id = 16;
            this.showRadio = true;
            break;
          case 2:
            id= 14;
            this.showRadio = true;
            break;
          case 3:
            id = 14;
            break;
          case 4:
            id = 12;
            break;
          case 5:
            id = 13;
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
      //查询框icon控制
      iconShowFun() {
        if (this.iconShow) return;
        this.iconShow = true;
        this.modelName = "";
        this.vmRequst(this.pagesize, this.currentPage);
      }
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
    created() {
      let options = [
        {
          value: '',
          label: '所有备料'
        },
        {
          value: 1,
          label: '选样备料'
        }
      ];
      this.options = options;
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
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .el-dropdown {
    margin-left: 5px;
    color: #4db3ff;
  }
</style>
