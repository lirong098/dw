<template>
  <div class="materails_main_contain">
    <div class="materailsrule_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3 ">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入备料策略查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary"
                     class="materailsrule_add"
                     @click="addMaterailsrule">新增
          </el-button>
        </div>
        <div class="inline_block mb3">
          <el-button  type="danger"
                      class="handle-del mr10" :disabled="!multipleSelection.length" @click="deleteMaterailsrule(2)">批量删除</el-button>
        </div>
      </div>
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              备料列表
            </h4>
          </div>
          <el-card>
            <el-table :data="materailsruleData"
                      @sort-change="sortChange"
                      ref="materailsruleTable" v-loading.body="loading" @selection-change="handleSelectionChange">
              <el-table-column type="selection"
                               width="50"></el-table-column>
              <el-table-column prop="pr_method_name" label="备料策略" :show-overflow-tooltip="true" sortable="custom"></el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    @click="editMaterailsrule(scope.$index, scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="deleteMaterailsrule(1,scope.$index, scope.row)">删除</el-button>
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
                  :page-sizes="[10,15,20,50,100]"
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
  export default {
    name: 'materatils-rule-main',
    components: {},
    props: {
      isFresh: {
        Boolean
      }
    },
    data() {
      return {
        loading:false,
        materailsruleData: [],
        multipleSelection: [],
        pagesize: 10,
        currentPage: 1,
        pagedatacount: 1000,
        changeFlag: true,
        tabIndex: 1,
        searchWord:'',
        sortMeta:''
      }
    },
    computed: {},
    created() {
      this.getMaterailsruleData();
    },
    methods: {
      getMaterailsruleData: function () {
        this.loading = true;
        this.materailsruleData.length = 0;
        const api = this.$store.state.DEV_API;
        let url =
          api + '/api/product/prs/?page=' +
          this.currentPage + '&pagesize=' + this.pagesize+'&search='+this.searchWord+'&ordering='+this.sortMeta;
        fetchAPI('get', url, null, this).then((res) => {
          if (res.status == 200) {
            this.pagedatacount = Number(res.headers.pagedatacount);
            this.materailsruleData = res.data;
          }
          this.loading = false;
        });
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {
          this.changeFlag = true
        }, 1000);
        this.getMaterailsruleData();
      },
      handleCurrentChange: function (val) {
        if (this.changeFlag) {
          this.currentPage = val;
          this.getMaterailsruleData();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      addMaterailsrule: function () {
        let data = {
          type: 'addMaterailsrule',
          data: {
            pr_method_name: '',
            extend:null,
            tabIndex: this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs', data);
      },
      editMaterailsrule: function (index, row) {
        let data = {
          type: 'editMaterailsrule',
          data: row
        };
        this.$emit('changeTabs', data);
      },
      deleteMaterailsrule: function (type, index, row) {
        const api = this.$store.state.DEV_API;
        if (type == 1) {//单个
          fetchAPI('delete', api + '/api/product/pr/?pr_method_id=' + row.pr_method_id, null, this).then((res) => {
            if (res.status == 204) {
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getMaterailsruleData();
            }
          });
        } else {//多个
          let code = [];
          for (let item in this.multipleSelection) {
            code.push(this.multipleSelection[item].pr_method_id);
          }
          fetchAPI('delete', api + '/api/product/prs/', {data: code}, this).then((res) => {
            if (res.status == 204) {
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getMaterailsruleData();
            }
          });
        }
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {
          this.changeFlag = true
        }, 1000);
        this.getMaterailsruleData();
      },
      searchByWord:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {
          this.changeFlag = true
        }, 1000);
        this.getMaterailsruleData();
      },
      sortChange:function (column) {
        let order = column.order === "descending" ? '-' :
          '';
        this.sortMeta = order + 'pr_method_name';
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {
          this.changeFlag = true
        }, 1000);
        this.getMaterailsruleData();
      }
    },
    watch: {
      isFresh() {
        this.getMaterailsruleData();
      },
    },
  }
</script>
<style scoped lang="scss" type="text/scss">
  .materails_main_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .materailsrule_main_main{
      height: 100%;
      .head_tool{
        .mb3{
          margin-bottom: 3px;
        }
        .search_input{
          width: 150px;
        }
      }
      .table_content{

      }
    }
  }
</style>
