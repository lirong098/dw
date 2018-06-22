<template>
  <div class="customer_main_contain">
    <div class="customer_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3 ">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入客户编码或名称查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary" class="customer_add"
                     @click="addCustomer">新增
          </el-button>
        </div>
        <div class="inline_block mb3">
          <el-button  type="danger"
                      class="handle-del mr10" :disabled="!multipleSelection.length" @click="deleteMultiple">批量删除</el-button>
        </div>
      </div>
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              客户列表
            </h4>
          </div>
          <el-card>
            <el-table :data="customerData"
                      ref="customerTable"
                      @selection-change="handleSelectionChange" @sort-change="sortChange">
              <el-table-column type="selection"
                               width="50"></el-table-column>
              <el-table-column prop="cust_code" label="客户编码"  sortable="custom"></el-table-column>
              <el-table-column prop="cust_name" label="客户名称" sortable="custom"></el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    @click="editCustomer(scope.$index, scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="deleteCustomer(scope.$index, scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {fetchAPI,checCode} from '../../utils/utils';
  export default{
    name:'customer-manage-main',
    components: {

    },
    props:{
      editData:{
        type:Object
      }
    },
    data () {
      return {
        selectData:'',
        searchData:'',
        customerData:[],
        multipleSelection:[],
        tabIndex:1,
        searchWord:'',
        sortCode:'',
        sortName:''
      }
    },
    computed:{

    },
    created() {
      this.getCustomerData();
    },
    methods: {
      getCustomerData:function () {
        const api = this.$store.state.DEV_API;
        let order = (this.sortCode + this.sortName).slice(0,-1);
        fetchAPI('get',api +
        '/api/custom/custominfolist/?search='+this.searchWord+'&ordering='+order,null,this).then((res) => {
          if(res && res.status == 200){
            this.customerData = res.data;
          }
        })
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      addCustomer:function () {
        let data = {
          type:'addCustomer',
          data:{
            addresses:[],
            contacts:[],
            cust_code:'',
            cust_name:'',
            extend:'',
            parent_cust_code:'',
            tabIndex:this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs',data);
      },
      editCustomer:function (index,row) {
        let data = {
          type:'editCustomer',
          data:row
        };
        this.$emit('changeTabs',data);
      },
      deleteCustomer:function (index,row) {
        const api = this.$store.state.DEV_API;
        fetchAPI('delete',api
          +'/api/custom/custominfo/?pk='+row.cust_code,null,this).then((res) => {
          if(res && res.status == 204){
            this.customerData.splice(index,1);
          }
        });
      },
      deleteMultiple:function () {
        let code = [];
        let deleteIndex = [];
        for(let item in this.multipleSelection){
          code.push(this.multipleSelection[item].cust_code);
          for(let index in this.customerData){
            if(this.customerData[index].cust_code == this.multipleSelection[item].cust_code){
              deleteIndex.push(index);
              break
            }
          }
        }
        deleteIndex.sort();
        const api = this.$store.state.DEV_API;
        let data = {
          customs:code
        };
        fetchAPI('post',api
          +'/api/custom/custmultidelete/',data,this).then((res) => {
          if(res && res.status == 204){
            for(let index = deleteIndex.length - 1;index >= 0; index--){
              this.customerData.splice(index,1);
            }
            this.$refs.customerTable.clearSelection();
          }
        })
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.getCustomerData();
      },
      searchByWord:function () {
        this.getCustomerData();
      },
      sortChange:function (column) {
        let order = column.order === "descending" ? '-' :
          '';
        if(column.prop === "cust_code"){
          this.sortCode = order +
            'cust_code' + ',';
        }else if(column.prop === "cust_name"){
          this.sortName = order + 'cust_name' + ',';
        }
        this.getCustomerData();
      }
    },
    watch: {
      editData(data) {
        if(data){
          if(data.type == 'editCustomer'){//编辑
            const api = this.$store.state.DEV_API;
            fetchAPI('put',api +
              '/api/custom/custominfo/?pk='+data.data.cust_code,data.data,this).then((res) => {
              if(res && res.status == 200){
                this.$message({
                  message: '保存成功',
                  type: 'success'
                });
                for(let item in this.customerData){
                  if(this.customerData[item].cust_code === data.data.cust_code){
                    this.customerData[item] = data.data;
                    this.$set(this.customerData,item,data.data);
                    this.$emit('cancelTab',data.type+'_'+data.data.tabIndex);
                    break
                  }
                }
                this.$emit('cancelTab',data.type+'_'+data.data.tabIndex);
              }
            })
          }else if(data.type == 'addCustomer'){//新增
            const api = this.$store.state.DEV_API;
            fetchAPI('post',api +
              '/api/custom/custominfolist/',data.data,this).then((res) => {
              if(res && res.status == 201){
                this.$message({
                  message: '保存成功',
                  type: 'success'
                });
                this.customerData.push(data.data);
                this.$emit('cancelTab',data.type+'_'+data.data.tabIndex);
              }
            })
          }
        }
      }
    },
  }
</script>
<style scoped lang="scss" type="text/scss">
  .customer_main_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .customer_main_main{
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
