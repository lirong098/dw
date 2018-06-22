<template>
  <div class="material_stock_list">
    <div class="test_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-input style="width:220px;"
                    placeholder="输入编码或名称"
                    v-model="search"
                    :icon="search?'circle-close':'search'"
                    @change="getList"
                    :on-icon-click="circle_close">
          </el-input>
        </div>
        <div class="inline_block mb3">
          <el-button v-if="stockInfo.stock_id !== 20 && stockInfo.stock_id !== 21" type="primary" class="customer_add"
                     @click="addNewaddCheckTab">新增
          </el-button>
          <el-button type="danger"
                     class="handle-del mr10"
                     :data="multipleSelection"
                     :disabled="delBtnStatus"
                     @click="delBtn">批量删除
          </el-button>
        </div>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4 v-text="stockInfo.stock_name"></h4>
          </div>
          <el-card>
            <el-table ref="multipleTable"
                      :data="childTableData"
                      border
                      tooltip-effect="dark"
                      style="width: 100%"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="55">
              </el-table-column>
              <el-table-column label="备料单号"
                               prop="mrp_pr_no">
              </el-table-column>
              <el-table-column label="备料交期"
                               prop="delivery_date">
              </el-table-column>
              <el-table-column label="国别"
                               prop="spec.country">
              </el-table-column>
              <el-table-column label="成衣Model编号"
                               prop="model.model_code">
              </el-table-column>
              <el-table-column label="操作"
                               width="120">
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
  import {fetchAPI} from '../../../../utils/utils';
  //公共文件
  import requst from "../../../common/vmrequst.js";
  import COMMON from "../../../common/common.js";
  import showModal from "../../../common/messageBox.js";

  export default {
    components: {},
    name: 'material_stock_list',
    props: {
      TABSValue: String,
      TABSIndex: Number,
      stockInfo: Object,
      stockType: Number
    },
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 0,  // 总条数
        search: '',
        childTitlename: this.titlename,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.TABSIndex,
        delBtnStatus: true,//删除按钮状态
        childTableData: [],
        multipleSelection: [],
        deleteDataId: []
      }
    },
    methods: {
      /*
      * 网络请求
      */
      getList(search, page = 1, qty = this.pagesize) {
        let url = this.$store.state.NEW_API + '/api/mat_models/mrp_prs/?page=' + page + '&pagesize=' + qty + '&mrp_pr_type_meta_id__meta_id=' + this.stockInfo.stock_id
        if (this.search && this.search !== '') {
          url = url + '&search=' + this.search
        }
        fetchAPI('get', url, null, this).then((res) => {
          this.childTableData = res.data.data;
          this.pagedatacount = res.data.total_number;
        })
      },
      // 删除按钮
      delBtn(val) {
        showModal.showModal(this, this.delBtnConfirm, "", "此操作将永久删除选中数据, 是否继续?", '操作提示', "是", "否");
      },
      //删除确认执行函数
      delBtnConfirm() {
        this.multipleSelection.forEach(res => {
          this.deleteDataId.push(res.mrp_pr_id);
        })
        const url = this.$store.state.NEW_API + '/api/mat_models/mrp_prs/';
        console.log('deleteId',this.deleteDataId);
        fetchAPI('delete', url, {data: this.deleteDataId}, this).then((res) => {
          this.deleteDataId = [];
          this.getList();
          showModal.showMessage(this,'success', '删除成功!')
        });
      },
      // 勾选
      handleSelectionChange(val) {
        this.multipleSelection = val
      },
      // 分页
      handleCurrentChange: function (val) {
        this.currentPage = val
        this.getList('', val, this.pagesize)
      },
      handleSizeChange: function (val) {
        this.pagesize = val
        this.getList('', this.currentPage, val)
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        if(!row.mrp_pr_id){
          showModal.showMessage(this,'error', '数据异常')
          return
        }
        this.addTab(row.mrp_pr_id);
      },
      //点击新增按钮
      addNewaddCheckTab() {
        this.addTab(0);
      },
      //添加tab函数
      addTab(id){
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.stockInfo.stock_name,
          name: newTabName,
          closable: true,
          rowId:id
        }
        this.$emit('changeTabMethod', this.chlidTabIndex,newTabName, addChildTABS);
      },
      circle_close() {
        this.search = '';
        this.getList();
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        console.log('value',val);
        if (this.chlidTABSValue ==='1') {
          this.pagesize = 10; // 分页条数
          this.currentPage = 1;  // 页
          this.getList();
        }
      },
      TABSIndex(val){
        console.log('index',val);
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
    mounted() {
      this.getList();
      console.log(this.stockInfo);
    }
  }
</script>
<style lang="scss" type="text/scss">
  .material_stock_list {
    .toolmy {
      height: 50px;
    }
    .btnright {
      width: 100%;
      height: 90px;
      float: right;
      display: inline-block;
    }
  }
</style>
