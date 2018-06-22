<template>
  <div>
    <div class="mrp-data">
      <div class="required-number">
        <el-table :data="stockList">
          <el-table-column prop="item.material_item.material_item.model.model_name" label="材料model名称">
          </el-table-column>
          <el-table-column prop="item.material_item.material_item.model.model_code" label="材料model编号">
          </el-table-column>
          <el-table-column prop="item.material_item.material_item.model.spec.bar_code" label="坯布代号">
          </el-table-column>
          <el-table-column prop="item.clothes_model.model_name" label="成衣model">
          </el-table-column>
          <el-table-column prop="item.delivery_date" label="备料交期" >
          </el-table-column>
          <el-table-column prop="item.mrp_quantity" label="需求数" >
          </el-table-column>
        </el-table>
      </div>
      <div class="filter-conditions">
        <div class="filter-header">
          <h5>过滤条件</h5>
        </div>
        <div class="filter-checkbox">

          <el-radio-group v-model="radio" @change="getStockCaculate()">
            <el-radio class="radio"  label="1">坯布代号</el-radio>
            <el-radio class="radio"  label="2">成衣model</el-radio>
            <el-radio class="radio"  label="3">材料</el-radio>
          </el-radio-group>
        </div>
      </div>
    </div>
    <div class="card_box">
        <div class="card-header card-header-text">
          <h4>备料信息</h4>
        </div>
      <div class="tableOrder">
        <el-card>
          <el-table :data="stockCaculateList" border>
            <el-table-column prop="pr_form_meta.meta_name" label="备料形式">
            </el-table-column>
            <el-table-column prop="material_item.model.model_code" label="材料model编号">
            </el-table-column>
            <el-table-column prop="material_item.model.model_name" label="材料model名称">
            </el-table-column>
            <el-table-column prop="material_item.item_name" label="item名称">
            </el-table-column>
            <el-table-column prop="material_item.item_code" label="item编号">
            </el-table-column>
            <el-table-column prop="delivery_date" label="备料交期" >
            </el-table-column>
            <el-table-column prop="quantity" label="库存数">
            </el-table-column>
            <el-table-column label="抵扣数" width="150">
              <template scope="scope">
                <el-input v-model.number="scope.row.deductible"></el-input>
              </template>
            </el-table-column>
          </el-table>
          <!--<div class="pagination clearfix" style="line-height: 32px;">-->
          <!--<div class="total fl">-->
          <!--共 <b>{{pagedatacount}}</b> 条数据-->
          <!--</div>-->
          <!--<div class="pagination_tool fr">-->
          <!--<el-pagination-->
          <!--@size-change="handleSizeChange"-->
          <!--@current-change="handleCurrentChange"-->
          <!--:current-page="currentPage"-->
          <!--:page-sizes="[10, 20, 50, 100]"-->
          <!--:page-size="pagesize"-->
          <!--layout="total, sizes, prev, pager, next, jumper"-->
          <!--:total="pagedatacount">-->
          <!--</el-pagination>-->
          <!--</div>-->
          <!--</div>-->
          <el-button size="small" @click="closeBtn()" class="button-style" style="background-color: white">取 消</el-button>
          <el-button size="small" @click="confirmBtn()" class="button-style" style="color: white">确 定</el-button>
        </el-card>
      </div>
    </div>

  </div>
</template>
<script>
  import {fetchAPI} from '../../../../utils/utils';
  import showModal from "../../../common/messageBox";
  export default {
    name: '',
    components: {
    },
    props: {
      caculate:Object,
    },
    data() {
      return {
        isCode: false,
        isModel: false,
        isMaterial: false,
        stockCaculateList: [],
        stockList:[{item:this.caculate}],
        updateList: [],//抵扣数选中的数组
        pagedatacount: 0,
        pagesize:10,
        currentPage:1,
        radio: '1'
      }
    },
    methods: {
      getStockCaculate(){
        let data= {
          mrp_pr_item_id:this.caculate.material_item.mrp_pr_item_id,
          pr_form_meta_id:this.caculate.pr_form_meta_id
        }

        const api = this.$store.state.NEW_API
        let url = api + '/api/mat_models/stock_caculate/?pr_form_meta_id='+data.pr_form_meta_id
          + '&mrp_pr_item_id=' + data.mrp_pr_item_id

//        '&clothes_model=' + data.search + '&material_item=' + data.search+
        if(this.radio === '1') {
          url = url + '&bar_code=' + this.caculate.material_item.material_item.model.spec.bar_code
        }
        if(this.radio === '2') {
          url = url + '&clothes_model=' + this.caculate.clothes_model.model_id
        }
        if(this.radio === '3') {
          url = url + '&material_model=' + this.caculate.material_item.material_item.model.model_id + '&material_item=' + this.caculate.material_item.material_item.item_id


        }


        fetchAPI('get', url, null, this).then((res) => {
          if (res && res.status === 200) {
            this.stockCaculateList = res.data
            console.log(res.data)
          }
        })
      },
      confirmBtn() {
        this.stockCaculateList.forEach(item => {
          if(item.deductible !== null && item.deductible !== undefined) {
            this.updateList.push(item)
          }
          console.log(this.updateList);
        })
        //处理抵扣数选中的数组
        this.$emit('confirmInfo',this.updateList)
      },
      closeBtn() {
        this.$emit('closeInfo')
      },
      // 修改分页条数
      handleSizeChange (val) {

      },
      // 分页
      handleCurrentChange () {

      }


    },
    computed: {},
    updated() {
//      let divname = 'tableOrder';
//      this.keydown(1,divname);
    },
    mounted() {
      this.getStockCaculate();
    }
  }
</script>

<style lang="scss" type="text/scss">
  .mrp-data{
    height: 100px;
    margin-bottom: 30px;
    clear: both;
    .required-number{
      border: 1px solid rgb(229, 209, 214);
      float: left;
      width: 65%;
      margin-bottom: 20px;
    }
    .filter-conditions{
      height: 80px;
      width: 30%;
      min-width: 300px;
      float: right;
      position: relative;
      border: 1px solid rgb(229, 209, 214);
      border-radius: 4px;
      background-color: #fff;
      box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
      margin-bottom: 20px;
      font-size: 18px;
      .filter-header{
        position: absolute;
        top: 0;
        left: 0;
        background: linear-gradient(60deg, #ec407a, #d81b60);
        box-shadow: 0 4px 20px 0px rgba(0, 0, 0, 0.14), 0 7px 10px -5px rgba(233, 30, 99, 0.4);
        padding: 15px;
        border-radius: 3px;
        margin: -20px 15px 0;
        display: inline-block;
        line-height: 1;
        z-index: 1;
        min-width: 60px;
        text-align: center;
        color: #ffffff;
      }
      .filter-checkbox{
        line-height: 100px;
        margin-left: 5%;
      }
    }
  }
  .button-style{
    float: right;
    width: 60px;
    background-color: #ec407a;
    margin: 20px;
    font-size: 14px;
    box-shadow: 0 4px 20px 0px rgba(0, 0, 0, 0.14), 0 7px 10px -5px rgba(233, 30, 99, 0.4);
    margin-right: 10px;
  }
 .el-dialog__title{
   position: absolute;
   top: 0;
   left: 24px;
   background: linear-gradient(60deg, #ec407a, #d81b60);
   box-shadow: 0 4px 20px 0px rgba(0, 0, 0, 0.14), 0 7px 10px -5px rgba(233, 30, 99, 0.4);
   padding: 15px;
   border-radius: 3px;
   margin: -20px 15px 0;
   display: inline-block;
   line-height: 1;
   z-index: 1;
   min-width: 60px;
   text-align: center;
   color: white;
   font-size: 18px;
   line-height: 27px;
 }
</style>
