<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar toolmy">
        <!--<div class="head_tool toolbar toolmy">-->
          <el-col :span="11">
            <el-form label-width="80px" style="display: inline-block;">
              <el-col :span="12">
                <!--<el-form-item label="bom_no :">-->
                  <!--<el-input v-model="bom_no"-->
                            <!--placeholder="请输入bom_no">-->
                  <!--</el-input>-->
                <!--</el-form-item>-->
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
                         @click="delBtn(multipleSelection)"
                         :data="multipleSelection"
                         :disabled="delBtnStatus">删除
              </el-button>
              <el-button type="primary"
                         class="customer_add"
                         style="float: right; margin-right: 10px;"
                         @click="addNewaddCheckTab">添加
              </el-button>
              <el-select style="float: right; margin-right: 5px;" v-model="value"
                         placeholder="请选择"
                         @change="selectChange(value)">
                <el-option v-for="item in options"
                           :key="item.value"
                           :label="item.label"
                           :value="item.value">
                </el-option>
              </el-select>
            </div>
          </el-col>
        <!--</div>-->
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              BOM列表
            </h4>
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
              <el-table-column prop="bom_no"
                               label="BOM单号">
              </el-table-column>
              <el-table-column prop="model_id.model_code"
                               label="Model">
              </el-table-column>
              <el-table-column prop="model_id.model_name"
                               label="Model描述"
                               show-overflow-tooltip>
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
  import {fetchAPI} from '../../../utils/utils';

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
        pagedatacount: 0,  // 总条数
        search: '',
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        delBtnStatus: true,
        options: [
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
            value: 3,
            label: '差异订单'
          },
          {
            value: 4,
            label: '手工订单'
          }
        ],
        value: '',
        childTableData: this.tableData,
        multipleSelection: [],
        deleteData: []
      }
    },
    methods: {
      // 初始获取BOM数据列表
      getList() {
        const api = this.$store.state.NEW_API;
        let getDataMassage = {
          page: this.currentPage,
          pagesize: this.pagesize,
          search: this.search
        };
        fetchAPI('get', api + '/api/mat_models/boms/?page=' + getDataMassage.page + '&pagesize=' + getDataMassage.pagesize + '&search=' + this.search, getDataMassage, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res.data.data);
            this.pagedatacount = res.data.total_number;
            this.childTableData = res.data.data;
          } else {
            console.log("服务器正在调试");
          }
        })
      },
      // 下拉选框发送请求
      selectChange(value) {
        console.log(value)
      },
      // 删除按钮
      delBtn(val) {
        this.$confirm('此操作将永久删除选中BOM, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          for (let item of val) {
            this.deleteData.push(item.bom_id);
          }
          console.log(this.deleteData,"111");
          const api =  this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/mat_models/boms/' , {data:this.deleteData}, this).then((res) => {
            if (res.status == 204) {
              this.deleteData = [];
              this.getList();
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      // 勾选
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(val)
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
        const api = this.$store.state.NEW_API;
        let regroup = {};
        let getBomDataMassage = {
          bom_id: row.bom_id
        };
        fetchAPI('get', api + '/api/mat_models/bom/?bom_id=' + row.bom_id, getBomDataMassage, this).then((res) => {
          if (res && res.status == 200) {
            regroup.bom = res.data;
            fetchAPI('get', api + '/api/mat_models/bom_items/?bom_id=' + row.bom_id, getBomDataMassage, this).then((res) => {
              if (res && res.status == 200) {
                for (let item of res.data) {
                  item.disabled = false; //删除状态
                  item.restore = false; // 恢复按钮状态
                }
                regroup.bom_item = res.data;
                console.log(regroup,'qqq');
                let newTabName = ++this.chlidTabIndex + '';
                let watchChildTABS = {
                  title: 'BOM详细信息',
                  name: newTabName,
                  closable: true,
                  rowId: regroup.bom.bom_id,
                  resData: regroup
                };
                this.chlidTABSValue = newTabName;
                this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS);
                $(".content").scrollTop(0);
              }
            })
          }
        });
      },
      addNewaddCheckTab() {
        const api = this.$store.state.NEW_API;
        fetchAPI('post', api + '/api/mat_models/make_bom_no/', null, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res);
            let bomInitialize = {
              bom: {
                bom_no: res.data.message,
                model_id: "",
                item_id: "",
                version: 0,
                spec: {},
                extend: {}
              },
              bom_item: []
            };
            let newTabName = ++this.chlidTabIndex + '';
            let addChildTABS = {
              title: '新增BOM',
              name: newTabName,
              closable: true,
              rowId: '',
              resData: bomInitialize
            };
            this.chlidTABSValue = newTabName;
            this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
          }
        })
      },
      query(search) {
        console.log(this.search);
        this.search = search;
        this.getList(search);
      },
      circle_close() {
        this.search = '';
        this.getList();
        console.log(this.search);
      }
    },
    computed: {
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == 1) {
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
      if (this.multipleSelection.length > 0) {
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
