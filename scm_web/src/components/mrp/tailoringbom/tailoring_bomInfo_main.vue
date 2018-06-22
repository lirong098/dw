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
                       @click="delBtn(multipleSelection)"
                       :data="multipleSelection"
                       :disabled="delBtnStatus">删除
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
              成衣BOM
            </h4>
          </div>
          <el-card style="overflow: inherit">
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
              <el-table-column label="Model">
                <template scope="scope">
                  {{commonmethod(scope.row.model_id)}}
                </template>
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
  //公共文件
  import requst from "../../common/vmrequst.js";
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
        fetchAPI('get', api + '/api/mat_models/boms/?page=' + getDataMassage.page + '&pagesize=' + getDataMassage.pagesize + '&search=' + this.search + '&filter=1', getDataMassage, this).then((res) => {
          if (res && res.status == 200) {
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
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/mat_models/boms/', {data: this.deleteData}, this).then((res) => {
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
                console.log(res.data,'123');
                for(let item of res.data){
                  if(!item.component_item){
                    item.component_item = {
                      item_id : 0
                    };
                  }
                  item.restore = false;
                }
                if(res.data.length === 0){
                  res.data = [
                    {
                      bom_item_id: 0,
                      bom: {
                        bom_id: 0,
                        bom_no: "",
                        model_id: 0,
                        item_id: 0,
                        version: 0,
                        spec: {
                          color: ""
                        },
                        extend: {}
                      },
                      component_model: {
                        model_id: 0,
                        unit_meta: {
                          meta_id: 0,
                          meta_code: "",
                          parent_meta_code: "",
                          meta_name: "",
                          extend: {}
                        },
                        model_type_meta_id: 0,
                        model_code: "",
                        model_name: "",
                        spec: {},
                        extend: {}
                      },
                      component_item: {
                        item_id: 0,
                        item_code: "",
                        item_name: "",
                        spec: {},
                        extend: {},
                        model: 0
                      },
                      quantity: 0,
                      spec: {
                        consume_items: [],
                        division: false,
                        consumptStatus: false,
                      },
                      extend: {},
                      addlocal: 0,
                      restore: false,
                    }
                  ]
                }
                regroup.bom_item = res.data;
                let newTabName = ++this.chlidTabIndex + '';
                let watchChildTABS = {
                  title: '成衣BOM - 查看',
                  name: newTabName,
                  closable: true,
                  rowState: 'look',
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
        let initialize = {
          bom: {
            bom_id: 0,
            bom_no: "",
            model_id: {},
            item_id: {
              item_id: 0,
            },
            version: 0,
            spec: {
              color: ""
            },
            extend: {}
          },
          bom_item: [
            {
              bom_item_id: 0,
              bom: {
                bom_id: 0,
                bom_no: "",
                model_id: 0,
                item_id: 0,
                version: 0,
                spec: {
                  color: ""
                },
                extend: {}
              },
              component_model: {
                model_id: 0,
                unit_meta: {
                  meta_id: 0,
                  meta_code: "",
                  parent_meta_code: "",
                  meta_name: "",
                  extend: {}
                },
                model_type_meta_id: 0,
                model_code: "",
                model_name: "",
                spec: {},
                extend: {}
              },
              component_item: {
                item_id: 0,
                item_code: "",
                item_name: "",
                spec: {},
                extend: {},
                model: 0
              },
              quantity: 0,
              spec: {
                consume_items: [],
                division: false,
                consumptStatus: false,
              },
              extend: {},
              addlocal: 0,
              restore: false,
            }
          ]
        };

        // 获取唯一标识
        requst.make_unique_no(this,"1",function (that,res) {
          if (res.data.code !== 0) return;
          console.log(res.data.message,'res.data.message');
          initialize.bom.bom_no = res.data.message;
        });

        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '成衣BOM - 新增',
          name: newTabName,
          closable: true,
          rowId: '',
          rowState: 'change',
          resData: initialize
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
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
      },
      commonmethod(model){
        if(model.model_id){
          let keyArr = ['model_code','model_name'];
          let tempArr = [];
          for(let i in keyArr){
            if(model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          model.spec.color?tempArr.push(model.spec.color):'';
          return tempArr.join(' - ')
        }
        if(model.item_id){
          let keyArr = ['item_code','item_name'];
          let tempArr = [];
          for(let i in keyArr)
          {
            if(model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          return tempArr.join(' - ');
        }
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
      height: 35px;
    }
    .btnright {
      width: 100%;
      height: 90px;
      float: right;
      display: inline-block;
    }
  }
</style>
