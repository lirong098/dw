<template>
  <div class="productinfo_main_contain">
    <div class="productinfo_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-select v-model="selectCustCode"
                     @change="changeCustCode"
                     placeholder="请选择">
            <el-option
              v-for="cust in customerData"
              :key="cust.cust_code"
              :label="cust.cust_name"
              :value="cust.cust_code">
            </el-option>
          </el-select>
        </div>
        <div class="inline_block mb3 input_length_375">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入Model Code、Model Name或Mpc Code查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary" class="product_add"
                     @click="addProduct">新增
          </el-button>
        </div>
        <div class="inline_block mb3">
          <el-button  type="danger"
                      class="handle-del mr10"
                      :disabled="!multipleSelection.length" @click="deleteProduct(2)">批量删除</el-button>
        </div>
      </div>
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              Model
            </h4>
          </div>
          <el-card>
            <el-table :data="productData" v-loading.body="loading"
                      ref="productTable"
                      @sort-change="sortChange"
                      @selection-change="handleSelectionChange">
              <el-table-column type="selection" width="40"></el-table-column>
              <el-table-column prop="model_code"
                               :show-overflow-tooltip="true"
                               sortable="custom"
                               label="Model Code"></el-table-column>
              <el-table-column prop="model_name" label="Model Name"
                               sortable="custom"
                               :show-overflow-tooltip="true"
              ></el-table-column>
              <el-table-column prop="mpc_code"
                               :show-overflow-tooltip="true"
                               label="Mpc Code">
              </el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    @click="editProduct(scope.$index, scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="deleteProduct(1,scope.$index, scope.row)">删除</el-button>
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
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default{
    name:'product-info-main',
    components: {

    },
    props:{
      editData:{
        type:Object
      },
      customerData:{
        type:Array
      },
      isFresh:{
          Boolean
      }
    },
    data () {
      return {
        selectCustCode:this.customerData.length ? this.customerData[0].cust_code : '',
        productData:[],
        multipleSelection:[],
        tabIndex:1,
        loading:false,
        pagesize: 15,
        currentPage: 1,
        pagedatacount: 1000,
        changeFlag:true,
        searchWord:'',
        sortCode:'',
        sortName:''
      }
    },
    computed:{

    },
    created() {
      this.getProductData();
    },
    methods: {
      getProductData:function () {
        this.loading = true;
        this.productData.length = 0;
        const api = this.$store.state.DEV_API;
        let order = (this.sortCode + this.sortName).slice(0,-1);
        let url =
          api +  '/api/product/models/?page='+this.currentPage+'&pagesize='+this.pagesize;
        url = this.selectCustCode ?
          url+'&cust_code='+this.selectCustCode : url;
        fetchAPI('get',url+'&ordering='+order+'&search='+this.searchWord,null,this).then((res) => {
          if(res && res.status == 200){
            this.pagedatacount =  Number(res.headers.pagedatacount);
            this.productData = res.data;
          }
          this.loading = false;
        });
      },
      changeCustCode:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getProductData();
      },
      handleSizeChange:function (val) {
        this.pagesize = val;
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getProductData();
      },
      handleCurrentChange:function (val) {
        if(this.changeFlag){
          this.currentPage = val;
          this.getProductData();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      addProduct:function () {
        let data = {
          type:'addProduct',
          data:{
            model_code:'',
            model_name:'',
            iman_code:'',
            mpc_code:'',
            cust_info:this.selectCustCode,
            pr_method:'',
            po_duration:0,
            produce_duration:0,
            delivery_duration:0,
            safe_duration:0,
            cut_produce_duration:0,
            extend:{
              elastic_lower_ratio:{name:'下弹比率',value:0},
              elastic_higher_ratio:{name:'上弹比率',value:0},
              elastic_week_start:{name:'弹性起始周',value:''},
              elastic_week_end:{name:'弹性结束周',value:''},
              delivery_week_first:{name:'首单交期周',value:''},
              delivery_week_last:{name:'尾单交期周',value:''},
              fabric_ratio:{name:'色布比率',value:0},
              rough_ratio:{name:'毛坯比率',value:0},
              yarn_ratio:{name:'纱比率',value:0},
              pr_method:{name:'备料方式',value:''}
            },
            tabIndex:this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs',data);
      },
      editProduct:function (index,row) {
        row.cust_info = row.cust_info.cust_code;
        row.pr_method = row.pr_method ?
          row.pr_method.pr_method_id : null;
        if(!row.extend){
          row.extend = {
            elastic_lower_ratio:{name:'下弹比率',value:0},
            elastic_higher_ratio:{name:'上弹比率',value:0},
            elastic_week_start:{name:'弹性起始周',value:''},
            elastic_week_end:{name:'弹性结束周',value:''},
            delivery_week_first:{name:'首单交期周',value:''},
            delivery_week_last:{name:'尾单交期周',value:''},
            fabric_ratio:{name:'色布比率',value:0},
            rough_ratio:{name:'毛坯比率',value:0},
            yarn_ratio:{name:'纱比率',value:0},
            pr_method:{name:'备料方式',value:''}
          }
        }
        let data = {
          type:'editProduct',
          data:row
        };
        this.$emit('changeTabs',data);
      },
      deleteProduct:function (type,index,row) {
        const api = this.$store.state.DEV_API;
        if(type == 1){//单个
          fetchAPI('delete',api + '/api/product/model/?model_inner_code='+row.model_inner_code,null,this).then((res) => {
            if(res.status == 204){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getProductData();
            }
          });
        }else{//多个
          let code = [];
          for(let item in this.multipleSelection){
            code.push(this.multipleSelection[item].model_inner_code);
          }
          fetchAPI('delete',api + '/api/product/models/',{data:code},this).then((res) => {
            if(res.status == 204){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getProductData();
            }
          });
        }
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getProductData();
      },
      searchByWord:function () {
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getProductData();
      },
      sortChange:function (column) {
        let order = column.order === "descending" ? '-' :
          '';
        if(column.prop === "model_code"){
          this.sortCode = order +
            'model_code' + ',';
        }else if(column.prop === "model_name"){
          this.sortName = order + 'model_name' + ',';
        }
        this.changeFlag = false;
        this.currentPage = 1;
        setTimeout(() => {this.changeFlag = true}, 1000);
        this.getProductData();
      }
    },
    watch: {
      customerData(data){
        this.selectCustCode = data.length ? data[0].cust_code : ''
      },
      isFresh(){
        this.getProductData();
      }
    },
  }
</script>
<style scoped lang="scss" type="text/scss">
  .productinfo_main_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .productinfo_main_main{
      height: 100%;
      .head_tool{
        .mb3{
          margin-bottom: 3px;
        }
        .search_input{
          width: 150px;
        }
      }
    }
  }
</style>
