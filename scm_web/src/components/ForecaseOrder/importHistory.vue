<template>
  <div class="customer_contain">
    <div class="customer_main">
      <lazy-render>
        <el-tabs v-model="currentTab" type="card"
                 @tab-remove="removeTab">
          <el-tab-pane
            :closable="item.closable"
            v-for="(item, index) in TABS"
            :key="item.name"
            :label="item.title"
            :name="item.name"
          >
            <div v-if="item.name == 'main'">
              <div class="import_history_contain">
                <div class="import_history_main">
                  <div class="head_tool toolbar">
                    <div class="inline_block mb3">
                      <el-input v-model="searchWord"
                                icon="close"
                                :on-icon-click="handleIconClick"
                                @keyup.enter.native="searchByWord"
                                placeholder="请输入文件名查询"></el-input>
                    </div>
                  </div>
                  <div class="table_content">
                    <div class="card_box">
                      <div class="card-header card-header-text">
                        <h4>
                          历史记录
                        </h4>
                      </div>
                      <el-card>
                        <el-table :data="historyData"
                                  v-loading.body="loading" @sort-change="sortChange">
                          <el-table-column prop="file_name"
                                           align="center"
                                           :show-overflow-tooltip="true"
                                           sortable="custom"
                                           label="文件名"></el-table-column>
                          <el-table-column prop="create_time"
                                           align="center"
                                           sortable="custom"
                                           :show-overflow-tooltip="true"
                                           label="导入时间"></el-table-column>
                          <el-table-column prop="fcst_type_meta"
                                           sortable="custom"
                                           align="center"
                                           label="文件类型">
                            <template scope="scope">
                              {{scope.row.fcst_type_meta ==
                            '__MC_ORDER_IMPORT' ? '预估订单' :
                              '选样订单'}}
                            </template>
                          </el-table-column>
                          <el-table-column prop="status"
                                           align="center"
                                           sortable="custom"
                                           label="导入结果">
                            <template scope="scope">
                              <el-tag :type="scope.row.status
                           ? 'success' : 'danger'">
                                {{scope.row.status ? '成功' :
                                '失败'}}
                              </el-tag>
                            </template>
                          </el-table-column>
                          <el-table-column label="操作" width=80>
                            <template scope="scope">
                              <el-button type="default"
                                         @click="viewHistory(scope.$index, scope.row)"
                                         size="small">查看
                              </el-button>
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
                              :page-sizes="[10,15,20, 50, 100]"
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
            </div>
            <div
              v-else-if="viewHistoryData[item.index] && item.name == 'viewHistory_'+viewHistoryData[item.index].tabIndex">
              <importHistoryView :historyDetail="viewHistoryData[item.index]"
                                 :optType="item.type"></importHistoryView>
            </div>
          </el-tab-pane>
        </el-tabs>
      </lazy-render>
    </div>
  </div>
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  import importHistoryView from
    '../../components/ForecaseOrder/importHistory_view.vue';
  export default{
    name: 'import-history',
    components: {
      importHistoryView
    },
    data () {
      return {
        TABS: [],
        optType: '',
        currentTab:'main',
        tabIndex:1,
        historyData:[],
        viewHistoryData:{},
        pagesize: 15,
        currentPage: 1,
        pagedatacount: 1000,
        changeFlag:true,
        loading:false,
        searchWord:'',
        sortFileName:'',
        sortTime:'',
        sortMeta:'',
        sortStatus:''
      }
    },
    computed: {},
    created() {
      let tab = [{
        title: this.$route.name,
        name: 'main',
        closable: false
      }];
      this.TABS = tab.slice();
      this.currentTab = 'main';
      this.getHistoryData();
    },
    methods: {
      getHistoryData:function () {
        this.historyData.length = 0;
        this.loading = true;
        const api = this.$store.state.DEV_API;
        let order = (this.sortFileName + this.sortTime
        + this.sortMeta + this.sortStatus).slice(0,-1);
        fetchAPI('get',api +
          '/api/fcst/fcst_import/?page='+this.currentPage+'&pagesize='+this.pagesize+'&search='+this.searchWord+'&ordering='+order,null,this).then((res) => {
          if(res && res.status == 200){
            this.historyData = res.data;
            this.pagedatacount =  Number(res.headers.pagedatacount);
          }
          this.loading = false;
        });
      },
      viewHistory:function (index,row) {
        let isAddTab = true;
        for (let tab in this.TABS) {
          if (this.TABS[tab].index == row.fcst_import_id) {
            isAddTab = false;
            break
          }
        }
        if(isAddTab){
          row.tabIndex = row.fcst_import_id;
          this.viewHistoryData[row.fcst_import_id] = row;
          let data = {
            title: row.fcst_type_meta ==
            '__MC_ORDER_IMPORT' ? '查看预估订单' :
              '查看选样订单',
            name: 'viewHistory_' + row.fcst_import_id,
            index: row.fcst_import_id,
            type: 'viewHistory',
            closable: true
          };
          this.currentTab = 'viewHistory_' + row.fcst_import_id;
          this.TABS.push(data);
        }else{
          this.currentTab = 'viewHistory_' + row.fcst_import_id;
        }
      },
      handleSizeChange:function (val) {
        this.pagesize = val;
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getHistoryData();
      },
      handleCurrentChange:function (val) {
        if(this.changeFlag){
          this.currentPage = val;
          this.getHistoryData();
        }
      },
      removeTab: function (targetName) {
        for (let tab in this.TABS) {
          if (this.TABS[tab].name == targetName) {
            if (targetName.indexOf('viewHistory_') != -1) {//关闭新增标签
              delete this.viewHistoryData[this.TABS[tab].index]
            }
            this.TABS.splice(tab, 1);
            this.currentTab = 'main';
            break
          }
        }
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getHistoryData();
      },
      searchByWord:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getHistoryData();
      },
      sortChange:function (column) {
        let order = column.order === "descending" ? '-' :
          '';
        if(column.prop === "file_name"){
          this.sortFileName = order +
            'file_name' + ',';
        }else if(column.prop === "create_time"){
          this.sortTime = order + 'create_time' + ',';
        }else if(column.prop === "fcst_type_meta"){
          this.sortMeta = order +
            'fcst_type_meta' + ',';
        }else if(column.prop === "status"){
          this.sortStatus = order +
            'status' + ',';
        }
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getHistoryData();
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .customer_contain, .customer_main {
    height: 100%;
    .import_history_contain{
      .import_history_main{
        padding: 0px 10px 10px 10px;
      }
    }
  }
</style>
