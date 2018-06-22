<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar toolmy">
        <!--<el-col :span="11">-->
          <!--<el-form label-width="80px" style="display: inline-block;">-->
          <!--<el-col :span="12">-->
          <!--<el-input style="width:220px;"-->
          <!--placeholder="输入编码或名称"-->
          <!--v-model="search"-->
          <!--:icon="search?'circle-close':'search'"-->
          <!--@change="query(search)"-->
          <!--:on-icon-click="circle_close">-->
          <!--</el-input>-->
          <!--</el-col>-->
          <!--</el-form>-->
        <!--</el-col>-->
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
          <el-button type="danger"
                     class="handle-del mr10"
                     style="float: right; margin-right: 10px; margin-right: 50px;"
                     @click="delBtn(multipleSelection)"
                     :data="multipleSelection"
                     :disabled="delBtnStatus">批量删除
          </el-button>
          <el-button type="primary"
                     class="customer_add"
                     style="float: right; margin-right: 10px;"
                     @click="addNewaddCheckTab">新增
          </el-button>
          <el-select style="float: right; margin-right: 20px;"
                     v-model="creatDataValue"
                     @change="creatDataMethod(creatDataValue)"
                     placeholder="请选择">
            <el-option
              v-for="item in creatDataOption"
              :key="item.id"
              :label="item.label"
              :value="item.id">
            </el-option>
          </el-select>
        </el-col>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4 v-text="childTitlename">

            </h4>
          </div>
          <el-card>
            <el-table ref="multipleTable"
                      :data="listData"
                      border
                      tooltip-effect="dark"
                      style="width: 100%"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="55">
              </el-table-column>
              <el-table-column label="备料单号"
                               prop="mrp_order_no">
              </el-table-column>
              <el-table-column label="备料交期"
                               prop="delivery_date">
              </el-table-column>
              <el-table-column label="Model"
                               prop="model.model_code">
              </el-table-column>
              <el-table-column label="国别"
                               prop="spec.country">
              </el-table-column>
              <el-table-column label="操作"
                               width="150">
                <template scope="scope">
                  <el-button size="small" @click="view(scope.row)">查看
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
    components: {},
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableData: Array,
      titlename: String,
      matecode: Number // 备料类型 11: 成衣备料 , 14: 成衣实单
    },
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 1,  // 总条数
        search: '',
        childTitlename: this.titlename,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        delBtnStatus: true,
        value: '',
        childMaterialtype: this.materialtype,
        childTableData: this.tableData,
        multipleSelection: [],
        deleteData: [], // 提交删除数据
        listData: [], // 列表数据
        creatDataValue: 1,
        creatDataOption: [
          {
            label: '未生成MRP备料',
            id: 1
          },
          {
            label: '已生成MRP备料',
            id: 2
          }
        ]
      }
    },
    methods: {
      query(search) {
        fetchAPI('get', this.$store.state.NEW_API + '/api/mrp_order/mrp_orders/?page=' + this.currentPage + '&pagesize=' + this.pagesize + '&mrp_pr_type_meta_id__meta_id=' + this.matecode + '&search='+search, null, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res.data);
            this.listData = res.data.data;
            this.pagedatacount = res.data.total_number;
          }
        });
      },
      circle_close() {
        this.search = '';
        this.getList();
      },
      //获取列表
      getList() {
        fetchAPI('get', this.$store.state.NEW_API + '/api/mrp_order/mrp_orders/?page=' + this.currentPage + '&pagesize=' + this.pagesize + '&mrp_pr_type_meta_id__meta_id=' + this.matecode, null, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res.data);
            this.listData = res.data.data;
            this.pagedatacount = res.data.total_number;
          }
        });
      },
      // 勾选
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(this.multipleSelection);
      },
      // 切换是否生成MRP备料
      creatDataMethod(val) {
        console.log(val, 'creatData')
      },
      // 批量删除按钮
      delBtn(val) {
        this.$confirm('此操作将永久删除选中数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          for (let item of val) {
            this.deleteData.push(item.mrp_order_id);
          }
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/mrp_order/mrp_orders/', {data: this.deleteData}, this).then((res) => {
            if (res.status === 204) {
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
      // 分页
      handleCurrentChange: function (val) {
        this.currentPage = val;
        this.getList();
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.getList();
      },
      // 新增mrp成衣备料
      addNewaddCheckTab() {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.childTitlename + ' - 新增',
          name: newTabName,
          closable: true,
          rowId: 0,
          rowState: 'change',
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      view(row) {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.childTitlename + ' - 查看',
          name: newTabName,
          closable: true,
          rowId: row.mrp_order_id,
          rowState: 'look',
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue === "1") {
          this.pagesize = 10; // 分页条数
          this.currentPage = 1;  // 页
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
