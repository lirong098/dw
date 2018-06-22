<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar toolmy">
        <!--<div class="head_tool toolbar toolmy">-->
        <el-col :span="11">
          <el-form label-width="80px" style="display: inline-block;">
            <el-col :span="12">
              <el-input style="width:220px;"
                        placeholder="输入编码或名称"
                        v-model="search"
                        :icon="search?'circle-close':'search'"
                        @change="query(search)"
                        :on-icon-click="circle_close">
              </el-input>
            </el-col>
          </el-form>
        </el-col>
        <el-col :span="12" style="float: right;">
          <div class="inline_block mb3 btnright">
            <el-button type="danger"
                       class="handle-del mr10"
                       style="float: right; margin-right: 10px;"
                       @click="delBtn(deleteData)"
                       :data="deleteData"
                       :disabled="delBtnStatus">批量删除
            </el-button>
            <el-button type="primary"
                       class="customer_add"
                       style="float: right; margin-right: 10px;"
                       @click="addNewaddCheckTab">添加
            </el-button>
            <!--<el-select style="float: right; margin-right: 5px;" v-model="value"-->
                       <!--placeholder="请选择"-->
                       <!--@change="selectChange(value)">-->
              <!--<el-option v-for="item in options"-->
                         <!--:key="item.value"-->
                         <!--:label="item.label"-->
                         <!--:value="item.value">-->
              <!--</el-option>-->
            <!--</el-select>-->
          </div>
        </el-col>
        <!--</div>-->
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              客户列表
            </h4>
          </div>
          <el-card>
            <el-table ref="childTableData"
                      :data="childTableData"
                      border
                      tooltip-effect="dark"
                      style="width: 100%"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="55">
              </el-table-column>
              <el-table-column label="客户编码"
                               prop="customer_code">
              </el-table-column>
              <el-table-column label="客户名称"
                               prop="customer_name">

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
  import {returnMessage} from '../../../common/component.js';
  export default {
    components: {

    },
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableData: Array
    },
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 1,  // 总条数
        search: '',
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        delBtnStatus: true,
        value: '',
        childTableData: this.tableData,
        delBtnStatus: true,
        deleteData: []
      }
    },
    methods: {
      // 初始获取BOM数据列表
      getList() {
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/customer/customers/?page=' + this.currentPage + '&pagesize=' + this.pagesize + '&search=' + this.search, null, this).then((res) => {
        if (res && res.status == 200) {
          this.childTableData = res.data.data;
          this.pagedatacount = res.data.total_number;
        }
       })
      },
      // 下拉选框发送请求
      selectChange(value) {
        console.log(value)
      },
      // 删除按钮
      delBtn(val) {
        this.$confirm('此操作将永久删除选中数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteArr = [];
          for (let item of val) {
            deleteArr.push(item.customer_id);
          }
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/customer/customers/', {data: deleteArr}, this).then((res) => {
            if (res.status == 204) {
              this.deleteData = [];
              this.getList();
              returnMessage("删除成功","success",this);
            }
          });
        }).catch(() => {
          returnMessage("已取消操作","info",this);
        });
      },
      // 勾选
      handleSelectionChange(val) {
        this.deleteData = val;
      },
      // 分页
      handleCurrentChange: function (val) {
        this.currentPage = val;
        this.getList();
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.getList();
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        let newTabName = ++this.chlidTabIndex + '';
        let watchChildTABS = {
          title: '客户 - 查看',
          name: newTabName,
          closable: true,
          rowId: row.customer_id,
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS);
        $(".content").scrollTop(0);
      },
      addNewaddCheckTab() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '客户 - 新增',
          name: newTabName,
          closable: true,
          rowId: 0,
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      query(search) {
        this.search = search;
        this.getList();
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
        if (this.chlidTABSValue == 1) {
          this.pagesize= 10; // 分页条数
          this.currentPage= 1;  // 页
          this.getList();
        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      },
      tableData(val) {
        this.childTableData = val;
      }
    },
    updated() {
      if (this.deleteData.length > 0) {
        this.delBtnStatus = false;
      } else {
        this.delBtnStatus = true;
      }
    },
    created() {
      this.getList();
    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_main_contain {
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
