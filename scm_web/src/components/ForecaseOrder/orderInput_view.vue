<template>
  <div class="order_edit_contain">
    <div class="order_edit_main">
      <el-form :model="orderData"
               class="demo-form-inline"
               label-width="80px">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              客户信息
            </h4>
          </div>
          <el-card>
            <el-form-item label="客户编码" prop="cust_code">
              <div class="edit_order_input">
                {{orderData.cust_code.cust_name}}
              </div>
            </el-form-item>
            <el-form-item label=""
                          v-if="orderData.fcst_type_meta.meta_code != '__MC_ORDER_IMPORT'">
              <div class="submit_btn edit_order_input">
                <el-button type="primary"
                           size="small"
                           @click="selectMaterialsType"
                           v-show="orderData.fcst_order_id">生成备料单
                </el-button>
              </div>
            </el-form-item>
          </el-card>
        </div>
        <div class="">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Item
              </h4>
            </div>
            <el-card>
              <el-table
                :data="modelItemData"
                class="item_table_hack"
                style="width: 100%">
                <el-table-column
                  prop="item_info.model_info.model_code"
                  width="110"
                  label="ModelCode">
                </el-table-column>
                <el-table-column
                  prop="item_info.model_info.model_name"
                  :show-overflow-tooltip="true"
                  min-width="250"
                  label="ModelName">
                </el-table-column>
                <el-table-column
                  prop="item_info.item_code"
                  :show-overflow-tooltip="true"
                  width="110"
                  label="ItemCode">
                </el-table-column>
                <el-table-column
                  prop="item_info.item_name"
                  :show-overflow-tooltip="true"
                  min-width="110"
                  label="ItemName">
                </el-table-column>
                <el-table-column
                  prop="delivery_date"
                  width="110"
                  label="日期">
                </el-table-column>
                <el-table-column
                  prop="quantity"
                  min-width="80"
                  label="数量">
                </el-table-column>
              </el-table>
              <div class="pagination clearfix">
                <!--<div class="total fl">-->
                <!--共 <b>{{item_pagedatacount}}</b> 条数据-->
                <!--</div>-->
                <div class="pagination_tool fr">
                  <el-pagination
                    layout="prev, pager, next"
                    :current-page.sync="currentPage"
                    @current-change="handleCurrentModelItemChange"
                    :page-size="pagesize"
                    :total="pagedatacount">
                  </el-pagination>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-form>
      <el-dialog
        title="已生成备料单"
        class="diff_dialog"
        :visible.sync="isShowMaterials"
        size="small">
        <div class="materials_content">
          <div>
            订单号 &nbsp;&nbsp; {{orderData.fcst_order_no}}
            <div class="group" v-if="materialsOrderData &&
               Object.keys(materialsOrderData).length">
              <div class="row_select row_select-first"
                   v-for="(item,index) in materialsOrderData">
                <div class="head">

                </div>
                <div class="body">
                  <div class="items">
                    <div class="item">
                      原料类型
                      <b>{{item.material_type_meta.meta_name
                        }}</b>
                      <span class="arrow">
                      <el-icon
                        name="d-arrow-right"></el-icon>
                      </span>
                      备料单号
                      <b class="item_contents">{{
                        item.fcst_pr_no}}</b>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              该订单无数据
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="isShowMaterials = false">确认</el-button>
      </span>
      </el-dialog>
      <el-dialog
        title="选择原料类型"
        :visible.sync="selectMaterialsTypeDialog"
        size="small">
        <el-checkbox-group
          v-model="currentMaterialsType">
          <div  v-for="item in materialsType">
            <el-checkbox
              :key="item.meta_code"
              :disabled="!!item.fcst_pr_no"
              :label="item.meta_code">
              {{item.meta_name}}
            </el-checkbox>
            {{item.fcst_pr_no ?
            '备料单号 '+item.fcst_pr_no : ''}}
          </div>
        </el-checkbox-group>
        <span slot="footer" class="dialog-footer">
          <el-button @click="selectMaterialsTypeDialog = false">取 消</el-button>
          <el-button type="primary"
                     :disabled="!currentMaterialsType.length"
                     @click="createMaterials">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default{
    name:'order-input-view',
    props:{
      order:{
        type:Object
      }
    },
    components: {

    },
    data () {
      return {
        orderData:Object.assign({},this.order),
        modelItemData:[],
        pagesize: 15,
        currentPage: 1,
        pagedatacount: 1000,
        PageCount:0,
        loading:true,
        isShowMaterials:false,
        materialsOrderData:null,
        materialsType:[],
        currentMaterialsType:[],
        selectMaterialsTypeDialog:false
      }
    },
    computed:{

    },
    created() {
      this.getOrderItem();
    },
    methods: {
      getOrderItem:function () {
        this.loading = true;
        this.modelItemData.splice(0);
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcst/fcst_order_item/?fcst_order_id='+
          this.orderData.fcst_order_id+'&page='+this.currentPage+'&pagesize='+this.pagesize,null,this).then((res) => {
            if(res && res.status == 200){
              this.pagedatacount =  Number(res.headers.pagedatacount);
              this.PageCount =
                Number(res.headers.pagecount);
              this.modelItemData =  res.data;
            }
          this.loading = false;
        });
      },
      getMaterialsType:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcstpr/fcst_order_material/?fcst_order_id='+this.orderData.fcst_order_id,null,this).then((res) => {
          if (res && res.status == 200) {
            this.materialsType.length = 0;
            this.currentMaterialsType.splice(0);
            for(let i in res.data){
              if(res.data[i].meta_value == 'NONSIZE'){
                this.materialsType.push(res.data[i]);
                if(!res.data[i].fcst_pr_no){
                  this.currentMaterialsType.push(res.data[i].meta_code);
                }
              }
            }
          }
        })
      },
      selectMaterialsType:function () {
        this.getMaterialsType();
        this.selectMaterialsTypeDialog = true;
      },
      createMaterials:function () {
        this.selectMaterialsTypeDialog = false;
        const api = this.$store.state.DEV_API;
        let data = {
          material_type_meta:this.currentMaterialsType,
          fcst_order_id:this.orderData.fcst_order_id
        }
        fetchAPI('post',api + '/api/fcstpr/estorder2pr/',data,this).then((res) => {
          if(res && res.status == 200){
            this.isShowMaterials = true;
            this.materialsOrderData = res.data;
          }
        });
      },
      handleCurrentModelItemChange:function (val) {
        this.currentPage = val;
        this.getOrderItem();
      },
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .order_edit_contain{
    height: 100%;
    padding:20px 10px 10px 10px;
    .order_edit_main{
      height: 100%;
      .head_title{
        height: 28px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 5px 12px 5px 0;
          box-sizing: border-box;
        }
      }
      .edit_order_input{
        width:300px;
      }
      .model_content{
        display: inline-block;
        width:40%;
      }
      .item_content{
        display: inline-block;
        width:50%;
      }
      .quantity_content{
        display: inline-block;
      }
    }
    .materials_content{
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
            .items{
              overflow: hidden;
              .item{
                float: left;
                margin: 9px 9px 9px 0;
                color: #000;
                width: 100%;
                .arrow{
                  margin: 0 2px;
                }
                .item_contents{
                  word-break:normal;
                  width:auto;
                  word-wrap : break-word ;
                  overflow: hidden ;
                }
              }
            }
          }
        }
      }
    }
  }
</style>
