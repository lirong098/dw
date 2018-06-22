<template>
  <div class="card_box">
    <div class="card-header card-header-text">
      <h4>备料比率</h4>
    </div>
    <el-card>
      <el-table
        border
        :data="tableData"
        style="width: 100%">
        <el-table-column
          prop="model_name"
          label="成衣model名称">
        </el-table-column>
        <el-table-column
          prop="model_code"
          label="成衣model编码">
        </el-table-column>
        <el-table-column label="备料数" width="80">
          <template scope="scope">
            <el-input v-text="scope.row.total_quantity"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="色布" width="80">
          <template scope="scope">
            <el-input v-model="scope.row.extend.consump_item[0].quantity"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="毛坯" width="80">
          <template scope="scope">
            <el-input v-model="scope.row.extend.consump_item[1].quantity"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="纱线" width="80">
          <template scope="scope">
            <el-input v-model="scope.row.extend.consump_item[2].quantity"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="总件数" width="300">
          <template scope="scope">
            <span style="float: left;width: 100px;margin-left: 10px;margin-top: 6px" v-text="(scope.row.extend.consump_item[0].quantity-0)+(scope.row.extend.consump_item[1].quantity-0)+(scope.row.extend.consump_item[2].quantity-0)"></span>
            <span type="text" class="el-icon-information"
                  v-if="(scope.row.extend.consump_item[0].quantity-0)+(scope.row.extend.consump_item[1].quantity-0)+(scope.row.extend.consump_item[2].quantity-0) > scope.row.total_quantity"
                  style="color: #d81b60;float: left;line-height: 36px;font-size: 10px">
                总件数{{(scope.row.extend.consump_item[0].quantity-0)+(scope.row.extend.consump_item[1].quantity-0)+(scope.row.extend.consump_item[2].quantity-0)}}超过备料数{{scope.row.total_quantity}}
              </span>
            <span type="text" class="el-icon-information"
                  v-if="(scope.row.extend.consump_item[0].quantity-0)+(scope.row.extend.consump_item[1].quantity-0)+(scope.row.extend.consump_item[2].quantity-0) < scope.row.total_quantity"
                  style="color: #d81b60;float: left;line-height: 36px;font-size: 10px">
                总件数{{(scope.row.extend.consump_item[0].quantity-0)+(scope.row.extend.consump_item[1].quantity-0)+(scope.row.extend.consump_item[2].quantity-0)}}少于备料数{{scope.row.total_quantity}}
              </span>
          </template>
        </el-table-column>
      </el-table>
      <el-button size="small"  class="button-style" style="background-color: white" @click="deleteInfo()">取 消</el-button>
      <el-button size="small"  class="button-style" style="color: white" @click="confirmInfo()">确 定</el-button>
    </el-card>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../../utils/utils';
  import showModal from "../../../common/messageBox.js";

  export default {
    name: 'stock_diolag',
    props: {
      fcstPrId:Number,
      fcstType:Number
    },

    data() {
      return {
        tableData:[],
        fcst_pr_id:this.fcstPrId,
        checked:false
      }
    },
    methods: {
      getStockList(){
        console.log(this.fcst_order_id)
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/newfcst/fcst_pr_item_model/?fcst_pr_id=' + this.fcst_pr_id, null, this).then((res) => {
          if (res && res.status === 200) {
            console.log("res.data -- ", res.data);

            res.data.forEach(item => {
              if(item.extend === null || Object.keys(item.extend).length === 0) {
                item.extend = {}
                item.extend.consump_item = []
                item.extend.consump_item[0] = {}
                item.extend.consump_item[0].quantity = 0
                item.extend.consump_item[1] = {}
                item.extend.consump_item[1].quantity = 0
                item.extend.consump_item[2] = {}
                item.extend.consump_item[2].quantity = 0
              }
            })
            this.tableData = res.data;
            console.log("tableData", this.tableData)

            if(this.fcstType === 6) {
              fetchAPI('get', api + '/api/mat_models/fcst_pr_items/?fcst_pr_id=' + this.fcst_pr_id, null, this).then((resp) => {
                if (resp && resp.status === 200) {
                  this.tableData.forEach(item => {
                    resp.data.forEach(it => {
                      if(item.model_id === it.item.model.model_id) {
                        item.extend[item.model_id].pr_fabric = Math.ceil(item.total_quantity*(it.item.model.extend.consump_item[0].quantity/100))
                        item.extend[item.model_id].pr_rough = Math.ceil(item.total_quantity*(it.item.model.extend.consump_item[1].quantity/100))
                        item.extend[item.model_id].pr_yarn = Math.ceil(item.total_quantity*(it.item.model.extend.consump_item[2].quantity/100))
                      }
                    })
                  })
                }
              })
            }
          }
        })
      },
      toggleCheckbox(){
        this.checked = !this.checked;
      },
      deleteInfo(){//取消按钮触发
        this.$emit('closeDialog');
      },

      confirmInfo() {//确定按钮触发

        console.log("this.tableData", this.tableData)
        const api = this.$store.state.NEW_API;
        let requestData = {
          fcst_pr_id:this.fcst_pr_id,
          extend: {}
        }

        this.tableData.forEach(item => {
          console.log('item', item)
          requestData.extend[item.model_id] = {}
          requestData.extend[item.model_id].consump_item = []
          requestData.extend[item.model_id].consump_item.push({
            "ratio": item.extend.consump_item[0].quantity/item.total_quantity * 100,
            "meta_id": 37,
            "quantity": item.extend.consump_item[0].quantity,
            "meta_code": "pr_fabric",
            "meta_name": "备原料"
          })
          requestData.extend[item.model_id].consump_item.push({
            "ratio": item.extend.consump_item[1].quantity/item.total_quantity * 100,
            "meta_id": 38,
            "quantity": item.extend.consump_item[1].quantity,
            "meta_code": "pr_rough",
            "meta_name": "备毛坯"
          })
          requestData.extend[item.model_id].consump_item.push({
            "ratio": item.extend.consump_item[2].quantity/item.total_quantity * 100,
            "meta_id": 39,
            "quantity": item.extend.consump_item[2].quantity,
            "meta_code": "pr_yarn",
            "meta_name": "备纱线"
          })

          // requestData.extend[item.model_id] = item.extend[item.model_id]
        })

        fetchAPI('post', api + '/api/newfcst/update_fcst_pr_item_extend/', requestData, this).then((res) => {
          if (res && res.status === 200) {
            console.log(res.data);
          }
        })
        this.$emit('closeDialog');
      }
    },
    computed: {},
    watch: {},
    updated() {
    },
    //只执行一次
    mounted() {
      this.getStockList();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
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
