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
          <el-button type="primary" class="customer_add"
                     @click="addNewaddCheckTab">新增
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
              <el-table-column v-for="(item,index) in tableColumn"
                               :prop="item.columnProp"
                               :label="item.columnName"
                               :key="index"
                               :width="item.columnWidth ===0 ?'':item.columnWidth"
                               show-overflow-tooltip>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template scope="scope">
                  <el-button size="small"
                             @click="addCheckTab(scope.$index, scope.row)">查看
                  </el-button>
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
  import newDialog from "./new_dialog.vue";
  import showModal from "../messageBox.js";
  export default {
    name: 'test-info-main',
    components: {
      newDialog
    },
    props: {
      TABSValue: String,
      tabIndex: Number,
      tableName: String,
      tableType: Number,
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
        delBtnStatus: true,
        value: '',
        itemValue: "",
        multipleSelection: [],
        deleteModelId:[],
        deleteData: [],
        listName: this.tableName + '列表',
        modelName: "", //查询值
        nowIndex:0, //当前行的下标
        iconShow:true,
        checkList:[], //
    }
    },
    methods: {
      //删除确认
      delBtnShowModal(){
        showModal.showModal(this, this.delBtn, "", "确定要删除此数据！ 是否继续?", '操作提示', "是", "否");
      },
      // 删除按钮
      delBtn() {
        this.multipleSelection.forEach(this.forModel);
        let url = this.vmRequstApi("","",4);
        fetchAPI('delete', url, {data:this.deleteModelId}, this).then((res) => {
          if(res.status == 204){
            showModal.showMessage(this,"success", "删除成功");
            this.deleteModelId.forEach(row=>{
              this.tableData = this.tableData.filter(row2=>{
                console.log(row2.model_id,row);
                return row2.model_id !== row
              });
            })
            this.deleteModelId = [];
          }
        });
      },
      handleSelectionChange(value) {
        this.multipleSelection = value;
      },
      //获取多列数据中的model_id
      forModel(item,index,array){
        this.deleteModelId[index] = item.model_id;
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
          title: this.tableName + '-查看',
          name: newTabName,
          closable: true,
          rowId: row.model_id
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS)
      },
      addNewaddCheckTab() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.tableName + '-新增',
          name: newTabName,
          closable: true,
          rowId: 0
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS)
      },
      //查询按钮
      handleIconClick() {
        if (this.modelName == "" || this.modelName == null || !this.modelName) {
          this.vmRequst(this.pagesize, this.currentPage, 1);
          return;
        }
        this.iconShow = false;
        this.vmRequst();
      },
      /*
      * 网络请求
      * status 1 请求列表 2模糊查询(code) 4 delete*/
      vmRequst(qty = this.pagesize, page = 1, status = 1) {
        let url = this.vmRequstApi(qty, page, status);
        fetchAPI('get', url, null, this).then((res) => {
          this.tableData = res.data.data;
          this.pagedatacount = res.data.total_number;
        })
      },
      //请求api判断
      vmRequstApi(qty, page, type) {
        const api = this.$store.state.NEW_API;
        let url = '';
        if (type === 1) {
          url = api + '/api/mat_models/models/?page=' + page + '&pagesize=' + qty + '&model_type_meta_id=' + this.tableType;
          if(this.modelName && this.modelName != ''){
            url = url + '&search=' + this.modelName;
          }
        }else if(type === 4){
          url = api + '/api/mat_models/models/';
        }
        return url;
      },
      //查询框icon控制
      iconShowFun(){
        if(this.iconShow) return;
        this.iconShow = true;
        this.modelName ='';
        this.vmRequst(this.pagesize, this.currentPage, 1);
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
      },
      tableData(val) {
        this.tableData = val;
      }
    },
    created() {
      let tableColumn = [
        {
          columnName: "编码",
          columnProp: "model_code",
          columnWidth:0
        }, {
          columnName: "名称",
          columnProp: "model_name",
          columnWidth:0
        },{
          columnName: "客户",
          columnProp: "customer.customer_name",
          columnWidth:0
        },{
          columnName: "季节",
          columnProp: "season.meta_name",
          columnWidth:120
        }
      ];
      this.tableColumn = tableColumn;
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
<style  scoped lang="scss" type="text/scss">
  .mb3:last-child {
    float: right;
    margin-right: 50px;
    .el-select {
      float: left;
      margin-right: 10px;
    }
  }
</style>
