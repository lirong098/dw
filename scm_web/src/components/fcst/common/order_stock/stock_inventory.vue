<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <el-input
            style="width:220px;"
            placeholder="输入编码或名称"
            v-model="modelName"
            :icon="iconShow ? 'search' :'circle-close'"
            @change="handleIconClick"
            :on-icon-click="iconShowFun">
          </el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="danger" v-if="listName" @click="confirmButton">确定</el-button>
          <el-button v-if="listName" @click="cancelDialog">取消</el-button>
        </div>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              {{listName ? "库存统计" : '库存抵扣列表'}}
            </h4>
          </div>
          <el-card>
            <el-table ref="multipleTable" :data="tableData" border tooltip-effect="dark" style="width: 100%"
                      :height="listName? 250:0" fit>
              <el-table-column type="index"
                               width="55">
              </el-table-column>
              <el-table-column label="成衣Model" show-overflow-tooltip>
                <template scope="scope">
                  <span>{{scope.row.clothes_model.model_id ? scope.row.clothes_model.model_code + '-' + scope.row.clothes_model.model_name + '-' + scope.row.clothes_model.spec.color : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="备料形式" show-overflow-tooltip>
                <template scope="scope">
                  <span>{{scope.row.pr_method.meta_name}}</span>
                </template>
              </el-table-column>
              <el-table-column label="材料Model" show-overflow-tooltip>
                <template scope="scope">
                  <span>{{scope.row.material_item.model.model_id ? scope.row.material_item.model.model_code + '-' + scope.row.material_item.model.model_name : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="材料Item" width="200">
                <template scope="scope">
                  <span>{{scope.row.material_item.item_id ? scope.row.material_item.item_code + '-' + scope.row.material_item.item_name : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="库存数" width="150">
                <template scope="scope">
                  <span >{{scope.row.stock}}</span>
                  <!--<span v-else>{{Math.abs(scope.row.quantity)}}</span>-->
                </template>
              </el-table-column>
              <el-table-column label="单位" width="70">
                <template scope="scope">
                  <span>{{scope.row.material_item.model.unit_meta.meta_name}}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="70" v-if="listName">
                <template scope="scope">
                  <el-button type="error" size="small" @click="addUpdatTableData(scope.row)">添加</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination clearfix" style="line-height: 32px;">
              <div class="total fl">
                共 <b>{{pagedatacount}}</b> 条数据
              </div>
              <div class="pagination_tool fr">
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                               :current-page="currentPage" :page-sizes="[10, 20, 50, 100]"
                               :page-size="pagesize" layout="total, sizes, prev, pager, next, jumper"
                               :total="pagedatacount">
                </el-pagination>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <div class="test_main_main" v-if="listName">
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              {{listName ? "库存抵扣列表" : 'List'}}
            </h4>
          </div>
          <el-card>
            <el-table ref="multipleTable" :data="updatTableData" border tooltip-effect="dark" style="width: 100%"
                      height="250">

              <el-table-column type="index"
                               width="55">
              </el-table-column>
              <el-table-column label="成衣Model" show-overflow-tooltip>
                <template scope="scope">
                  <span>{{scope.row.clothes_model.model_id ? scope.row.clothes_model.model_code + '-' + scope.row.clothes_model.model_name + '-' + scope.row.clothes_model.spec.color : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="材料Model" show-overflow-tooltip>
                <template scope="scope">
                  <span>{{scope.row.material_item.model.model_id ? scope.row.material_item.model.model_code + '-' + scope.row.material_item.model.model_name : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="材料Item" width="200">
                <template scope="scope">
                  <span>{{scope.row.material_item.item_id ? scope.row.material_item.item_code + '-' + scope.row.material_item.item_name : ''}}</span>
                </template>
              </el-table-column>
              <el-table-column label="抵扣数" width="150">
                <template scope="scope">
                  <span>{{Math.abs(scope.row.quantity)}}</span>
                </template>
              </el-table-column>
              <el-table-column label="单位" width="70">
                <template scope="scope">
                  <span>{{scope.row.material_item.model.unit_meta.meta_name}}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="70">
                <template scope="scope">
                  <el-button type="error" size="small" @click="deleteTableData(scope.$index,scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
      <el-dialog title="请填写抵扣数" :visible.sync="upQuantity" size="tiny" :modal-append-to-body="false"
                 @close="closeDialog">
        <el-button type="danger" @click="addUpData" style="float: right;margin-bottom:5px;">确定</el-button>
        <el-input :value="updateQuantity" @input="commonQty"></el-input>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../../utils/utils';
  import request from "../../../common/vmrequst.js";
  import showModal from "../../../common/messageBox.js";

  export default {
    name: 'stocklist_info',
    props: {
      tableType: Number,
      listName: {
        default: false
      },
      mrp_pr: Number,//关联mrp备料单ID
      mrp_pr_item: {
        type: Number, //关联mrp备料子项ID
        default: 64
      }
    },
    data() {
      return {
        tableData: [],//表格数据
        updatTableData: [],//抵扣表数据
        tableColumn: [],//表格列字段
        pagedatacount: 0,//数据总条数
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        modelName: "", //查询值
        nowIndex: 0, //当前行的下标
        iconShow: true,
        upQuantity: false, //填写抵扣数弹窗
        updateQuantity: 0, //抵扣数
        nowupdateQuantity: 0,//记录抵扣数
        nowRow: {} //添加的当前行
      }
    },
    methods: {
      // 分页
      handleCurrentChange: function (val) {
        this.vmRequest(this.pagesize, val);
      },
      handleSizeChange: function (val) {
        this.pagesize = val;
        this.vmRequest(val, 1);
      },
      //查询按钮
      handleIconClick() {
        if (this.modelName == "" || this.modelName == null || !this.modelName) {
          this.vmRequest(this.pagesize, this.currentPage);
          return;
        }
        this.iconShow = false;
        this.vmRequest(10, 1, this.modelName);
      },
      /*
      * 网络请求
      */
      vmRequest(qty = 10, page = 1, search = "") {
        let requestData = this.requestData(qty, page, search);
        request.requst(this, requestData.url, function (that, objRes) {
          console.log(objRes.data);
          if (that.listName) {
            that.tableData = objRes.data.stock;
            that.updatTableData = objRes.data.history;
            that.pagedatacount = objRes.data.stock.length;
          } else {
            that.tableData = objRes.data.stock;
            that.pagedatacount = objRes.data.stock.length;
          }
        });
      },
      //判断网络请求参数
      requestData(qty, page, search) {
        let requestData = {};
        if (!this.listName) {
          requestData = {
           // url: "/api/mat_models/mrp_pr_item_deductions/?page=" + page + "&pagesize=" + qty + "&search=" + search,
            url:"/api/mat_models/stock_caculate/?mrp_pr_item_id=" + this.mrp_pr_item + "&search=" + search
          };
        } else {
          console.log("mrp_pr_item_id", this.mrp_pr_item);
          requestData = {
            url: "/api/mat_models/stock_caculate/?mrp_pr_item_id=" + this.mrp_pr_item + "&search=" + search,
          };
        }
        return requestData;
      },
      //查询框icon控制
      iconShowFun() {
        if (this.iconShow) return;
        this.iconShow = true;
        this.modelName = "";
        this.vmRequest(this.pagesize, this.currentPage);
      },
      //取消按钮 关闭弹窗
      cancelDialog() {
        this.$emit("cancelDialog");
      },
      //确定按钮
      confirmButton() {
        this.$emit("confirmButton", this.updatTableData);
      },
      //添加按钮
      addUpdatTableData(res) {
        this.nowRow = res;
        this.updateQuantity = res.stock;
        this.nowupdateQuantity = res.stock;
        this.upQuantity = true;
      },
      addUpData() {
        this.updatTableData.push(
          {
            mrp_pr_item_deduction_id: 0,
            clothes_model: this.nowRow.clothes_model,
            material_item: this.nowRow.material_item,
            quantity: -parseInt(this.updateQuantity),
            spec: {},
            extend: {},
            mrp_pr: this.mrp_pr ? this.mrp_pr : 0,
            mrp_pr_item: this.mrp_pr_item ? this.mrp_pr_item : 0,
            pr_form_meta:this.nowRow.pr_method
          }
        );
        this.upQuantity = false;
      },
      closeDialog() {
        $(".v-modal").eq(0).hide();
      },
      commonQty(val) {
        if (parseInt(val) > parseInt(this.nowupdateQuantity)) {
          showModal.showMessage(this, "error", "抵扣数不能大于库存数");
          return;
        }
        this.updateQuantity = val;
      },
      //删除库存抵扣LIST
      deleteTableData(index,item){
        if(item.mrp_pr_item_deduction_id === 0){
          this.updatTableData.splice(index,1);
        }else if(item.mrp_pr_item_deduction_id > 0){
          request.requst(this, "/api/mat_models/mrp_pr_item_deductions/", function (that, objRes) {
            that.updatTableData.splice(index,1);
          },"delete",{data:[item.mrp_pr_item_deduction_id]});
        }
      }
    },
    computed: {},
    watch: {},
    created() {
    },
    updated() {
    },
    //只执行一次
    mounted() {
      this.vmRequest();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .mb3:last-child {
    float: right;
    margin-right: 50px;
    .el-select {
      float: left;
      margin-right: 10px;
    }
  }
</style>
