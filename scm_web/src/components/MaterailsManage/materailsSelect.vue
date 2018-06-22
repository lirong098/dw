<template>
  <div class="materails_select_content">
    <div class="materails_select_main">
      <div class="card_box">
        <div class="card-header card-header-text">
          <h4>
            筛选条件
          </h4>
        </div>
        <el-card>
          <div class="header_tool">
            <div class="group">
              <div class="row_select row_select-first">
                <div class="head">品牌</div>
                <div class="body">
                  <div class="items">
                    <div class="item" v-for="item in
              customerList" key="item.cust_code"
                         @click="changCus(item.cust_code)">
                      <el-tag :type="cus ==
                    item.cust_code ? 'success' : 'gray'" >
                        {{item.cust_name}}
                      </el-tag>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row_select">
                <div class="head">原料类型</div>
                <div class="body">
                  <div class="items">
                    <div class="item" v-for="item in
              materialsType" key="item.meta_code"
                         @click="changType(item.meta_code)">
                      <el-tag :type="currentMaterialsType ==
                    item.meta_code ? 'success' : 'gray'" >
                        {{item.meta_name}}
                      </el-tag>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      <div class="body_table">
        <div>
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                备料统计
              </h4>
            </div>
            <el-card>
              <lazy-render>
                <el-table  :data="ModelList"  fit>
                  <el-table-column width="70" fixed>
                    <template scope="scope">
                      <div class="expand_icon" v-show="scope.row.is_model" @click="handleExpand(scope.$index, scope.row)">
                        <el-icon :name="scope.row.module_expand_flag ? 'arrow-down' : 'arrow-right'"></el-icon>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="code" label="Code"
                                   :show-overflow-tooltip="true"
                                   min-width="150">
                    <template scope="scope">
          <span :title="scope.row.code">{{
            scope.row.code}}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="name" label="Name"
                                   :show-overflow-tooltip="true"
                                   min-width="150">
                    <template scope="scope">
          <span :title="scope.row.name">{{
            scope.row.name}}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="quantity" label="数量"
                                   min-width="150">
                    <template scope="scope">
          <span :title="scope.row.quantity">{{
            scope.row.quantity}}</span>
                    </template>
                  </el-table-column>
                </el-table>
              </lazy-render>
            </el-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI,checCode} from '../../utils/utils';
  export default {
    data(){
      return {
        customerList:[],
        ModelList:[],
        cus:'',
        model:'',
        itemList:[],
        materialsType:[],
        currentMaterialsType:''
      }
    },
    created() {
      this.getCusList()
    },
    methods:{
      getCusList:function(){
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api+'/api/custom/custominfolist/',null,this).then((res) => {
          if(res && res.status == 200){
            this.customerList = res.data;
            if(res.data.length){
              this.cus = res.data[0].cust_code;
              this.getMaterialsType();
            }
          }
        })
      },
      getMaterialsType:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api + '/api/dict/meta/materials/',null,this).then((res) => {
          if (res && res.status == 200) {
            this.materialsType = res.data;
            this.currentMaterialsType = res.data[0] ?
              res.data[0].meta_code : '';
            this.getModelList();
          }
        })
      },
      getModelList:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api+'/api/fcstpr/pr_stock_model/?cust_code='+this.cus+'&material_type_meta='+this.currentMaterialsType,null,this).then((res) => {
          if(res && res.status == 200){
            this.ModelList = res.data
            for(let modelindex in this.ModelList){
              this.ModelList[modelindex]['is_model'] = true
              this.ModelList[modelindex]['module_expand_flag'] = false
              this.ModelList[modelindex]['module_expand_num'] = 0
            }
          }
        })
      },
      getItemList:function(model_inn_code){
        const api = this.$store.state.DEV_API;
        return fetchAPI('get',api+'/api/fcstpr/pr_stock_item/?model_inner_code='+model_inn_code+'&material_type_meta='+this.currentMaterialsType,null,this).then((res) => {
          if(res && res.status == 200){
            this.itemList = res.data
            for(let itemindex in this.itemList){
              this.itemList[itemindex]['is_model'] = false
            }
            return this.itemList
          }
        })
      },
      changCus:function(cust_code){
        this.ModelList.length = 0;
        this.cus = cust_code;
        this.getModelList();
      },
      changType:function (meta_code) {
        this.ModelList.length = 0;
        this.currentMaterialsType = meta_code;
        this.getModelList();
      },
      handleExpand:function (index,row) {
        let flag = this.ModelList[index].module_expand_flag;
        if(this.ModelList[index].module_expand_flag){//要折叠
          this.ModelList.splice(index+1,this.ModelList[index].module_expand_num);
        }else{//要展开
          this.getItemList(row.inner_code).then((res) => {
            this.ModelList[index].module_expand_num = res.length;
            this.ModelList.splice(index+1,0,...res);
          });
        }
        this.ModelList[index].module_expand_flag = !flag;
      },
      tableRowClassName:function(row,index){
        if(row.is_model === true){
          return 'info-row'
        }else{
          return ''
        }
      }
    }
  }
</script>

<style scoped lang="scss" type="text/scss">
  .materails_select_content{
    height: 100%;
    .materails_select_main{
      padding:20px 10px 10px 10px;
      .body_table{
        margin-top: 30px;
        .create_btn{
          text-align: right;
          padding-bottom: 2px;
        }
        .expand_icon{
          width: 100%;
          height:100%;
          cursor: pointer;
        }
      }
      .header_tool{
        margin-bottom: 10px;
        .title{
          color: #999;
          margin-bottom: 2px;
        }
        .group{
          border:1px solid #e8e8e8;
          position: relative;
          .row_select-first, .row_select:first-child{
            border-top:none;
          }
          .row_select{
            position: relative;
            border-top: 1px dashed #dedede;
            margin: 0 8px;
            .head{
              position: absolute;
              left: 11px;
              top: 9px;
              color: #999;
            }
            .body{
              padding:0 100px 0 112px;
              .items{
                min-height: 36px;
                overflow: hidden;
                .item{
                  float: left;
                  margin: 9px 10px 9px 0;
                  height: 18px;
                  color: #000;
                  cursor: pointer;
                  &.select{
                    margin: 0;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
</style>

