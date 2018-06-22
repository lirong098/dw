<template>
  <div class="test_detailed_contain">
    <div class="fl test_detailed_main main-card-box">
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4 v-text="stockInfo.stock_name">
            </h4>
          </div>
          <el-card class="divCard">
            <el-col class="detailMessage">
              <el-form v-model="tableData"
                       label-width="150px">
                <el-col :span="12">
                  <el-form-item label="备料单号：">
                    <el-input class="nochange"
                              v-show="!changeShow"
                              v-text="tableData.mrp_pr.mrp_pr_no">
                    </el-input>
                    <el-input class="truechange"
                              v-show="changeShow"
                              v-model="tableData.mrp_pr.mrp_pr_no"
                              :disabled='true'>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="国　　别 :"
                                labelWidth="150px">
                    <el-input class="nochange"
                              style="width: 80%"
                              v-text="tableData.mrp_pr.spec.country"
                              :disabled="true">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="成衣Model编号：">
                    <el-input class="nochange"
                              v-show="!changeShow"
                              v-text="tableData.mrp_pr.model.model_code">
                    </el-input>
                    <el-input class="truechange"
                              v-show="changeShow"
                              v-model="tableData.mrp_pr.model.model_code"
                              icon="more"
                              :on-icon-click="()=>getCModelData()">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="成衣Model名称：">
                    <el-input class="nochange"
                              v-show="!changeShow"
                              v-text="tableData.mrp_pr.model.model_name">
                    </el-input>
                    <el-input class="truechange"
                              v-show="changeShow"
                              v-model="tableData.mrp_pr.model.model_name">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="备料交期：">
                    <el-input class="nochange"
                              v-show="!changeShow"
                              v-text="tableData.mrp_pr.delivery_date">
                    </el-input>
                    <el-date-picker v-model="tableData.mrp_pr.delivery_date"
                                    type="date"
                                    style="width: 80%;"
                                    v-show="changeShow"
                                    placeholder="选择日期"
                                    :picker-options="pickerOptions"
                                    @change="changeDate">
                    </el-date-picker>
                    <!--<dw-date-picker v-model="tableData.mrp_pr.delivery_date"-->
                    <!--v-show="changeShow"-->
                    <!--mode="single"-->
                    <!--placeholder="选择日期"-->
                    <!--@change="changeDate"-->
                    <!--style="width:100%">-->
                    <!--</dw-date-picker>-->
                  </el-form-item>
                </el-col>
              </el-form>
            </el-col>
          </el-card>
        </div>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4 v-text="'详细信息'"></h4>
          </div>
          <div class="table">
            <el-card>
              <div class="card_list card_list_title">
                <span class="card_title" >备料形式</span>
                <span class="card_title" >材料Model编号</span>
                <span class="card_title" >材料Model名称</span>
                <span class="card_title" >材料Item名称</span>
                <span class="card_list_span_qty card_title">需求数</span>
                <span class="card_title">操作</span>
              </div>
              <div :class="{'card_div':true,'restoreCardDiv':item.restore}" v-for="(item,index) in tableData.mrp_pr_item" :key="index">
                <div class="card_list card_list_title">
                <span>
                  <div v-show="!changeShow">{{item.pr_form_meta.meta_name}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-select v-model="item.spec.pr_form_meta_id" placeholder="请选择" :disabled="item.restore">
                      <el-option v-for="(item,index) in prFormMeta" :label="item.meta_name" :value="item.meta_id"
                                 :key="index"></el-option>
                    </el-select>
                  </div>
                </span>
                  <span>
                  <div v-show="!changeShow">{{item.material_item.model.model_code}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-input v-model="item.material_item.model.model_code"
                              icon="more"
                              :on-icon-click="()=>getMModelData(index,item)"
                              :disabled="item.restore"></el-input>
                  </div>
                </span>
                  <span>
                  <div v-show="!changeShow">{{item.material_item.model.model_name}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-input v-model="item.material_item.model.model_name" disabled></el-input>
                  </div>
                </span>
                  <span>
                  <div v-show="!changeShow">{{item.material_item.item_name}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-input v-model="item.material_item.item_name"
                              icon="more"
                              :disabled="item.restore"
                              :on-icon-click="()=>getMModelItemData(index,item)">
                    </el-input>
                  </div>
                </span>
                  <span class="card_list_span_qty">
                  <div v-show="!changeShow">{{item.mrp_quantity}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-input v-model="item.mrp_quantity" :disabled="item.restore"></el-input>
                  </div>
                </span>
                  <span class="card_list_span_qty">
                  <el-button type="error" size="small" @click="addTableItem" v-show="changeShow && !item.restore">+</el-button>
                  <el-button type="error" size="small" @click="deleteTableItem(item,index)" v-show="changeShow && !item.restore">-</el-button>
                  <el-button type="error" size="small" @click="upTableItem(item,index)" v-show="changeShow && item.restore">恢复</el-button>
                </span>
                </div>
                <div class="card_list_title_small" v-if="tableItemShow">
                  <span class="card_list_title_small_span--info ">详情</span>
                  <span class="card_list_title_small_span--qty ">库存数</span>
                  <span class="card_list_title_small_span--qty ">总库存数</span>
                  <span class="card_list_title_small_span--qty ">计算比率</span>
                  <span class="card_list_title_small_span--qty ">抵扣数</span>
                  <span class="card_list_title_small_span--button"></span>
                </div>
                <div class="card_list_info" v-if="tableItemShow" v-for="(row,key) in item.mrp_pr_item_deductions"
                     :key="'info'+key">
                <span class="card_list_info_span--info">
                  <div class="card_list_info_span--info_text" v-for="(scope,scopeKey) in row.deductionsInfo"
                       :key="'scope'+scopeKey">
                    <p class="card_list_info_span--info_text_name">
                      <el-button type="text" icon="circle-close" @click="deleteCaculate(index,scope,scopeKey,key)" style="color: rgb(217, 191, 197);"></el-button>
                      <span>{{scope.delivery_data+'   '+scope.deduction_mrp_pr_item.material_item.model.model_code+
                      '   '+scope.deduction_mrp_pr_item.material_item.model.model_name+
                      '   '+scope.deduction_mrp_pr_item.material_item.item_name+
                      '   '+scope.deduction_mrp_pr_item.material_item.model.spec.bar_code}}</span>
                    </p>
                    <p class="card_list_info_span--info_text_qty">{{scope.quantity}}</p>
                  </div>
                </span>
                  <span class="card_list_info_span--qty">{{row.sumQuantity}}</span>
                  <span class="card_list_info_span--qty">{{row.Ratio}}</span>
                  <span class="card_list_info_span--qty">{{row.deMrpQuantity}}</span>
                  <span class="card_list_info_span--button">
                  <el-button type="primary" size="small"
                             @click="stockCaculate(row.pr_meta_id,item,index,key,row.Ratio)">抵扣</el-button>
                </span>
                  <div class="card_list_info_posi_title">
                    <span>{{row.pr_meta_name }}</span>
                  </div>
                </div>
                <div class="card_list_info card_list_info_last">
                <span class="card_list_info_span--qty" style="border:none;width:15%;">
                  <span>备料数：</span>
                </span>
                  <span class="card_list_info_span--qty" style="margin-right:7%; width: 16%;border:none;">
                  <div v-show="!changeShow">{{item.quantity}}</div>
                  <div v-show="changeShow" class="card_list_info_change">
                    <el-input v-model="item.quantity"></el-input>
                  </div>
                </span>
                </div>
              </div>
            </el-card>
          </div>

        </div>
      </div>
    </div>
    <!--操作按钮-->
    <div class=" click-button">
      <el-card class="extra_card" v-show="!changeShow">
        <!--<el-button type="danger"-->
                   <!--size="large"-->
                   <!--@click="addNewaddCheckTab">新增-->
        <!--</el-button>-->
        <el-button type="primary"
                   size="large"
                   @click="upChangeShow">修改
        </el-button>
        <el-button type="error"
                   size="large"
                   @click="deleteMethod(rowId)"
                   style="border: 0; color: #4db3ff;">删除
        </el-button>
      </el-card>
      <el-card class="extra_card" v-show="changeShow">
        <el-button type="primary"
                   size="large"
                   class="customer_add"
                   @click="saveBtn">保存
        </el-button>
        <el-button type="danger"
                   size="large">保存<br/>新增
        </el-button>
        <el-button type="error"
                   size="large"
                   @click="closeChangesMetod"
                   style="border: 0; color: #4db3ff;">取消
        </el-button>
      </el-card>
    </div>
    <el-dialog title="选择材料Model" style="float: left" :visible.sync="moreAddBtn" size="large" @close="closeDialog">
      <modellist @getDialogInfo="getDialogInfo"
                 :model_id="modelDiaLog.model_id"
                 :onlyGetItem="modelDiaLog.onlyGetItem"
                 :tableName="modelDiaLog.tableName"
                 :tableType="modelDiaLog.tableType"
                 :exclude="modelDiaLog.exclude"
                 :noGetItem="modelDiaLog.noGetItem"
                 v-if="moreAddBtn">
      </modellist>
    </el-dialog>
    <el-dialog title="库存统计" style="float: left" :visible.sync="stockCaculateShow" size="large" @close="closeInfo">
      <material_stock_dialogbox v-if="stockCaculateShow"
                                :caculate="caculate"
                                @confirmInfo="createDeDuc"
                                @closeInfo="closeInfo">
      </material_stock_dialogbox>
    </el-dialog>
  </div>
</template>

<script>
  //公共组件
  import modellist from "../../../common/model_dialog/dialog_model.vue";
  import material_stock_dialogbox from "./material_stock_dialogbox.vue";
  //公共函数
  import {fetchAPI} from '../../../../utils/utils';
  import COMMON from '../../../common/common.js';
  import showModal from '../../../common/messageBox.js';

  export default {
    components: {
      modellist,
      material_stock_dialogbox
    },
    name: 'test-detailed',
    props: {
      stockInfo: {
        type:Object,
        default: () => {
          return {
            stock_name : 'MRP备料',
            stock_id :20
          }
        }
      },
      TABSValue: String,
      TABSIndex: Number,
      rowId: {
        type:Number,
        default:0
      },
      propData: {
        type: Object,
        default: () => {
          return {}
        }
      }
    },
    data() {
      return {
        changeShow: false,//默认view状态 true：修改状态
        moreAddBtn: false,//ModelList弹窗
        modelDiaLog: {},//model弹窗参数
        stockCaculateShow: false,//库存统计弹窗
        caculate: {},//库存统计参数
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.TABSIndex,
        tableItemShow: false,
        iconIndex: 0,//选择model当前行
        caculateIconIndex:0,//点击抵扣记录当前行
        caculateIconKey:0,//记录当前备料类型
        tableData: {
          mrp_pr: {
            mrp_pr_id: this.rowId,
            model: {
              model_id: 0,
              model_code: '',
              model_name: '',
            },
            mrp_pr_type_meta_id: {
              meta_id: this.stockInfo.stock_id,
            },
            mrp_pr_no: '',
            delivery_date: COMMON.formatDate(),
            deal_date: COMMON.formatDate(),
            spec: {},
            extend: {},
          },
          mrp_pr_item: [this.basicTableItem()]
        },
        value: '',
        prFormMeta: [],//备料形式
        pickerOptions: { //选择日期数据
          firstDayOfWeek:1,
        },
      }
    },
    methods: {
//      // 删除按钮
//      delBtn(val) {
//        showModal.showModal(this, this.delBtnConfirm, "", "此操作将永久删除选中数据, 是否继续?", '操作提示', "是", "否");
//      },
//      //删除确认执行函数
//      delBtnConfirm() {
//        this.multipleSelection.forEach(res => {
//          this.deleteDataId.push(res.mrp_pr_id);
//        })
//        const url = this.$store.state.NEW_API + '/api/mat_models/mrp_prs/';
//        console.log('deleteId',this.deleteDataId);
//        fetchAPI('delete', url, {data: this.deleteDataId}, this).then((res) => {
//          this.deleteDataId = [];
//          this.getList();
//          showModal.showMessage(this,'success', '删除成功!')
//        });
//      },
      deleteMethod(rowId){
        this.$confirm('此操作将永久删除, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteData = [];
          deleteData.push(rowId);
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/mat_models/mrp_prs/', {data: deleteData}, this).then((res) => {
            if (res.status == 204) {
              this.$emit('CloseTab');
              this.$message({
                showClose: true,
                message: '删除成功',
                type: 'success'
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
      //表体初始化结构
      basicTableItem(res = false, modelRes = false) {
        return {
          mrp_pr: 0,
          mrp_pr_item_id: 0,
          material_item: {
            item_id: res ? res.item_id : 0,
            item_code: res ? res.item_code : '',
            item_name: res ? res.item_name : '',
            model: {
              model_id: modelRes ? modelRes.model_id : 0,
              model_code: modelRes ? modelRes.model_code : '',
              model_name: modelRes ? modelRes.model_name : '',
            },
          },
          mrp_quantity: 0,
          quantity: 0,
          spec: {
            pr_form_meta_id: ''
          },
          extend: {
            material_consume_quantity: 1
          },
          pr_form_meta: {
            meta_id: '',
            meta_code: '',
            meta_name: '',
          },
          addlocal: 0,
          restore:false
        }
      },
      //计算比率
      getItemRatio(data) {
        let len = data.length
        let i = 0
        data.forEach(row => {
          let meta_code = row.pr_form_meta.meta_code
          let modelExtend = row.material_item.model.extend.consume_pr_form
          let url = this.$store.state.NEW_API + '/api/mat_models/mrp_pr_item_deductions/?mrp_pr_item__mrp_pr_item_id='
          let Ratio = 1
          row['mrp_pr_item_deductions'] = []
          fetchAPI('get', url + row.mrp_pr_item_id, null, this).then(objRes => {
            if (objRes.status === 200) {
              if(modelExtend){
                this.prFormMeta.forEach(res => {
                  Ratio = COMMON.fomatFloat(modelExtend[res.meta_code] / modelExtend[meta_code], 1)
                  let deductionItem = []
                  objRes.data.data.forEach(objRow => {
                    if (objRow.deduction_mrp_pr_item.spec.pr_form_meta_id === res.meta_id) {
                      deductionItem.push(objRow)
                    }
                  })
                  row.mrp_pr_item_deductions.push(this.getItemRatio_deductions(res, Ratio, deductionItem))
                })
              }
              i = i + 1
              if (len === i) {
                this.tableData.mrp_pr_item = data
                this.tableItemShow = true
                console.log('tableData.mrp_pr_item', this.tableData.mrp_pr_item)
                console.log('tableData', this.tableData)
              }
            }
          })
        })
      },
      //getItemRatio_deductions
      getItemRatio_deductions(res, Ratio, deductionItem) {
        let sumQuantity = this.forAdd(deductionItem)
        return {
          pr_meta_id: res.meta_id,
          pr_meta_name: res.meta_name,
          deductionsInfo: deductionItem,
          sumQuantity: sumQuantity,//总库存数
          Ratio: Ratio,//计算比率
          deMrpQuantity:Math.round(sumQuantity / Ratio) //抵扣数
        }
      },
      //循环相加
      forAdd(data){
        let sumQuantity = 0;
        data.forEach(row => {
          sumQuantity = sumQuantity + parseFloat(row.quantity)
        })
        return sumQuantity
      },
      //计算单条item的备料数
      getQuantity(data){
        let qty = 0
        data.mrp_pr_item_deductions.forEach(row=>{
          qty = qty + parseFloat(row.deMrpQuantity)
        })
        data.quantity = parseFloat(data.mrp_quantity)-qty
      },
      upQuantity(index,key,qty){
        this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].sumQuantity = this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].sumQuantity - qty
        this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].deMrpQuantity = Math.round(this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].sumQuantity/this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].Ratio)
        this.getQuantity(this.tableData.mrp_pr_item[index])
      },
      //抵扣创建成功后 计算备料数
      confirmInfo() {
        let qty = this.forAdd(this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_deductions[this.caculateIconKey].deductionsInfo)
        this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_deductions[this.caculateIconKey].sumQuantity = qty
        let ratio = this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_deductions[this.caculateIconKey].Ratio
        this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_deductions[this.caculateIconKey].deMrpQuantity =Math.round(qty/ratio)
        this.getQuantity(this.tableData.mrp_pr_item[this.caculateIconIndex])
        this.stockCaculateShow = false
        this.up_tab_item_quantity(this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_id,this.tableData.mrp_pr_item[this.caculateIconIndex].quantity)
      },
      //计算完之后将备料数提交给数据库
      up_tab_item_quantity(id,qty){
        console.log('up_tab_item_quantity')
        let url = this.$store.state.NEW_API+'/api/mat_models/mrp_pr_item/'
        fetchAPI('put',url,[{mrp_pr_item_id:id,quantity:qty}],this).then(res=>{
          console.log(res)
        })
      },
      //删除抵扣信息
      deleteCaculate(index,scope,scopeKey,key){
        if(scope.mrp_pr_item_deduction_id && scope.mrp_pr_item_deduction_id > 0){
          let url = this.$store.state.NEW_API+'/api/mat_models/mrp_pr_item_deductions/'
          fetchAPI('delete',url,{data:[scope.mrp_pr_item_deduction_id]},this).then(res=>{
            if(res.status == 204) {
              showModal.showMessage(this, "success", "删除成功");
              this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].deductionsInfo.splice(scopeKey,1)
              this.upQuantity(index,key,scope.quantity)
            }
          })
        }else if(scope.mrp_pr_item_deduction_id === 0){
          this.tableData.mrp_pr_item[index].mrp_pr_item_deductions[key].deductionsInfo.splice(scopeKey,1)
          this.upQuantity(index,key,scope.quantity)
        }
      },
      //创建库存抵扣记录 //抵扣回调函数
      createDeDuc(data){
        if(!data.length ===0) return
        let deDucdata =[]
        data.forEach(row=>{
          deDucdata.push({
            mrp_pr_item_deduction_id: 0,//抵扣记录ID
            deduction_mrp_pr_item: {
              mrp_pr_item_id:row.mrp_pr_item_id
            },//抵扣mrp_pr_item数据
            quantity: row.deductible,//抵扣数量
            spec:{},
            extend:{},
            mrp_pr: this.tableData.mrp_pr.mrp_pr_id,//被抵扣mrp备料单表头ID
            mrp_pr_item: this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_id, //被抵扣mrp备料单子项ID
          })
        })
        let url = this.$store.state.NEW_API+'/api/mat_models/mrp_pr_item_deduction/'
        fetchAPI('put',url,deDucdata,this).then(res=>{
          if(res.status ===200){
            if(res.data.data.length >0 && res.data.data){
              res.data.data.forEach(row=>{
                console.log('wewqewqewq',row)
                this.tableData.mrp_pr_item[this.caculateIconIndex].mrp_pr_item_deductions[this.caculateIconKey].deductionsInfo.push(row)
              })
            }
            this.confirmInfo()
            showModal.showMessage(this, "success", "创建成功");
          }
        })
      },
      //备料日期
      changeDate(val) {
        this.tableData.mrp_pr.delivery_date = val
      },
      // 关闭弹窗
      closeDialog() {
        this.moreAddBtn = false
      },
      //
      closeInfo(){
        this.stockCaculateShow = false
      },
      //打开弹窗
      openDialog() {
        this.moreAddBtn = true
      },
      //修改按钮
      upChangeShow() {
        this.changeShow = !this.changeShow;
      },
      //网络获取item信息的时候进行状态赋值
      updateItem(resData) {
        if (resData.length === 0) return;
        for (let x in resData) {
          resData[x]['disabled'] = false;
          resData[x]['restore'] = false;
        }
        this.tableData.mrp_pr_item = resData;
      },
      //新增时执行
      add() {
        this.upChangeShow();
        // 请求唯一编号
        COMMON.make_unique_no(this, "mrp").then(res => {
          if (res.data.code !== 0) return;
          this.tableData.mrp_pr.mrp_pr_no = res.data.message;
        })
        if (this.propData.length > 0) {
          this.updateItem(this.propData)
        }
      },
      //网络请求表头信息
      getMrpPr() {
        let url = this.$store.state.NEW_API + '/api/mat_models/mrp_pr/?mrp_pr_id=' + this.tableData.mrp_pr.mrp_pr_id
        fetchAPI('get', url, null, this).then(res => {
          this.tableData.mrp_pr = res.data
        })
      },
      //请求表体信息
      getMrpPrItem() {
        let url = this.$store.state.NEW_API + '/api/mat_models/mrp_pr_items/?mrp_pr_id=' + this.tableData.mrp_pr.mrp_pr_id
        fetchAPI('get', url, null, this).then(res => {
          res.data.forEach(row=>{
            row['restore'] = false
          })
          this.getItemRatio(res.data)
        })
      },
      //选择材料Model
      getMModelData(index, res) {
        this.updateModelDiaLog(0, false, '面料', 2, 1, false)
        this.iconIndex = index
        this.openDialog()
      },
      //选择成衣Model
      getCModelData() {
        this.updateModelDiaLog()
        this.openDialog()
      },
      //选择Item
      getMModelItemData(index, res) {
        if (res.material_item.model.model_id && res.material_item.model.model_id > 0) {
          this.updateModelDiaLog(res.material_item.model.model_id, true, '面料', 2, 1, false)
        } else {
          this.updateModelDiaLog(0, false, '面料', 2, 1, false)
        }
        this.iconIndex = index
        this.openDialog()
      },
      //modelList参数
      updateModelDiaLog(model_id = 0, onlyGetItem = false, tableName = '成衣', tableType = 1, exclude = 2, noGetItem = true) {
        this.modelDiaLog = {
          model_id: model_id,
          onlyGetItem: onlyGetItem,
          tableName: tableName,
          tableType: tableType,
          exclude: exclude,
          noGetItem: noGetItem
        }
      },
      //model弹窗回调函数
      getDialogInfo(res) {
        if (this.modelDiaLog.exclude === 1 && !this.modelDiaLog.onlyGetItem) {
          this.setTableItem(res)
        } else if (this.modelDiaLog.exclude === 1 && this.modelDiaLog.onlyGetItem) {
          this.setTableModelItem(res)
        } else if (this.modelDiaLog.exclude === 2) {
          this.tableData.mrp_pr.model.model_id = res.model_id
          this.tableData.mrp_pr.model.model_name = res.model_name
          this.tableData.mrp_pr.model.model_code = res.model_code
          this.closeDialog()
        }
      },
      //非成衣ModelItem
      setTableModelItem(res) {
        if (!res || res.length === 0) return
        this.forItem(res, this.tableData.mrp_pr_item[this.iconIndex].material_item.model)
        this.closeDialog()
      },
      //表体新增数据
      addTableItem() {
        this.tableData.mrp_pr_item.push(this.basicTableItem())
      },
      //删除表体数据
      deleteTableItem(item,index){
        if(item.mrp_pr_item_id ===0){
          if(this.tableData.mrp_pr_item.length ===1) return
          this.tableData.mrp_pr_item.splice(index,1)
        }else if(item.mrp_pr_item_id && item.mrp_pr_item_id >0){
          console.log('item',item)
          console.log('index',index)
          this.tableData.mrp_pr_item[index]['delete'] =0
          this.tableData.mrp_pr_item[index].restore = true
          //this.$set(this.$data, 'tableData', this.tableData);
          console.log('tableData',this.tableData)
        }
      },
      //恢复按钮
      upTableItem(item,index){
        this.tableData.mrp_pr_item[index].delete =2
        this.tableData.mrp_pr_item[index].restore = false
      },
      //循环表体数据
      setTableItem(res) {
        if (!res) return
        if (res.model_item === '' || !res.model_item) {
          this.setMaterialItem(false, res)
        } else if (res.model_item.length > 0) {
          this.forItem(res.model_item, res)
        }
        this.closeDialog()
      },
      //循环过程
      forItem(data, modeldata) {
        data.forEach((row, key) => {
          if (key === 0) {
            this.setMaterialItem(row, modeldata)
          } else {
            this.tableData.mrp_pr_item.splice(this.iconIndex + 1, 0, this.basicTableItem(row, modeldata))
          }
        })
      },
      //更改当前行材料item
      setMaterialItem(res = false, modelRes = false) {
        this.tableData.mrp_pr_item[this.iconIndex].material_item = {
          item_id: res ? res.item_id : 0,
          item_code: res ? res.item_code : '',
          item_name: res ? res.item_name : '',
          model: {
            model_id: modelRes ? modelRes.model_id : 0,
            model_code: modelRes ? modelRes.model_code : '',
            model_name: modelRes ? modelRes.model_name : '',
          },
        }
      },
      //点击新增按钮
      addNewaddCheckTab() {
        this.addTab(0);
      },
      //添加tab函数
      addTab(id) {
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: this.stockInfo.stock_name,
          name: newTabName,
          closable: true,
          rowId: id
        }
        this.$emit('changeTabMethod', this.chlidTabIndex, newTabName, addChildTABS);
      },
      // 取消按钮
      closeChangesMetod() {
        showModal.showModal(this, this.closeChangesMetodConfirm, "", "此操作将不保存数据, 是否继续?", '操作提示', "是", "否");
      },
      //取消确定按钮执行函数
      closeChangesMetodConfirm() {
        this.changeShow = false;
        if (this.tableData.mrp_pr.mrp_pr_id > 0) {
          this.getMrpPr();
          this.getMrpPrItem();
        } else {
          this.$emit('CloseTab');
        }
        showModal.showMessage(this, "success", "取消成功");
      },
      //保存按钮
      saveBtn(addFun) {
        let url = "/api/mat_models/mrp_prs/";
        let text = "保存成功";
        let type = "post";
        if (this.tableData.mrp_pr.mrp_pr_id > 0) {
          url = "/api/mat_models/mrp_pr/";
          text = "修改成功";
          type = 'put';
        }
        let a = true
        this.tableData.mrp_pr_item.forEach(row => {
          if (row.spec.pr_form_meta_id === '' || !row.spec.pr_form_meta_id) {
            a = false
          }
        })
        if (!a) {
          showModal.showModal(this, '', '', "请选择备料类型", '错误提示');
          return
        }
        console.log('shuju',this.tableData)
        fetchAPI(type, this.$store.state.NEW_API + url, this.tableData, this).then(res => {
          if (res && res.status === 200 && !res.data.code) {
            res.data.mrp_pr_item.forEach(row=>{
              row['restore'] = false
            })
            console.log('row',res.data)
            this.tableData = res.data
            showModal.showMessage(this, "success", text);
            this.changeShow = false
            this.tableItemShow = false
            this.getItemRatio(this.tableData.mrp_pr_item)
            if (typeof addFun === "function") { //保存新增时执行新增的事件
              this.$emit("CloseTab");
              addFun();
            }
          }
        }).catch(err => {
        })
      },
      //抵扣函数
      /*
      prMeta:备料形式id,item:表体一条信息,index:表体一条信息的下标,key:当前备料形式下标,ratio:当前备料形式的比率
      */
      stockCaculate(prMeta, item, index,key,ratio) {
        if(!item || item.restore) return
        let xuqiushu = Math.round(item.quantity*ratio)
        this.caculate = {
          material_item: item,//备料子项信息
          delivery_date: this.tableData.mrp_pr.delivery_date,//备料交期
          pr_form_meta_id: prMeta,//备料形式id
          clothes_model: this.tableData.mrp_pr.model, //成衣Model
          mrp_quantity:xuqiushu
        }
        this.caculateIconIndex =index
        this.caculateIconKey = key
        this.stockCaculateShow = true
      }
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      TABSIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    computed: {},
    created() {
      let divname = 'table';
      this.keydown(6,divname);
    },
    mounted() {
      console.log('propData',this.propData)
      // 请求备料方式
      COMMON.getMetaList(this, 36).then(res => {
        this.prFormMeta = res.data;
      })
      if (this.tableData.mrp_pr.mrp_pr_id === 0 || !this.tableData.mrp_pr.mrp_pr_id) {
        if(this.propData.mrp_pr){
          this.tableData = this.propData
        }
        this.add()
        return
      }
      this.getMrpPr();
      this.getMrpPrItem();
    }
  }
</script>

<style scoped lang="scss" type="text/scss">
  .test_detailed_contain {
    .test_detailed_main {
      width: 87%;
      .nochange {
        width: 100%;
        height: 36px;
      }
      .card_title {
        color: rgb(61, 31, 38);
        font-size: 14px;
        font-weight: bold;
        line-height: 25px;
      }

      .card_div {
        display: flex;
        flex-flow: column;
        justify-content: flex-end;
        align-items: flex-start;
        margin-top: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-radius: 4px;
        border: 1px solid rgb(229, 209, 214);
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
      }
      .restoreCardDiv{
        background-color: #f4f4f4;
      }
      .card_list {
        display: flex;
        flex-flow: row;
        height: 40px;
        line-height: 40px;
      }
      .card_list_title {
        justify-content: space-between;
        align-items: flex-start;
        width: 98%;
        margin-left: 1%;
        span {
          text-align: center;
          height: 100%;
          .card_list_info_change {
            padding-right: 5px;
            padding-left: 5px;
            border-right: 1px solid rgb(246, 238, 239);
            border-top: 1px solid rgb(246, 238, 239);
            border-bottom: 1px solid rgb(246, 238, 239);
          }
          .card_list_info_change:nth-child(1) {
            border-left: 1px solid rgb(246, 238, 239);
            margin-left: 8px;
          }
        }
        span:nth-child(1) {
          flex: 1;
        }
        span:nth-child(2) {
          flex: 1.5;
        }
        span:nth-child(4) {
          flex: 1;
        }
        span:nth-child(6) {
          flex: 1;
        }
        span:nth-child(3) {
          flex: 3;
        }
        .card_list_span_qty {
          width: 120px;
        }
      }
      .card_list_title_small {
        display: flex;
        flex-flow: row;
        justify-content: flex-end;
        align-items: flex-end;
        width: 70%;
        margin-left: 22.5%;
        margin-top: 10px;
        background-color: rgb(246, 238, 239);
        color: #b2b2b2;
        font-size: 14px;
        line-height: 30px;
        /*border:1px solid blue;*/
        span {
          text-align: center;
          /*border:1px solid black;*/
        }
        .card_list_title_small_span--info {
          flex: 1;
        }
        .card_list_title_small_span--ratio {
          width: 9%;
        }
        .card_list_title_small_span--qty {
          width: 10%;
        }
        .card_list_title_small_span--button {
          width: 10%;
        }
      }
      .card_list_info {
        display: flex;
        flex-flow: row;
        justify-content: flex-end;
        align-items: center;
        width: 70%;
        margin-left: 22.5%;
        margin-top: 15px;
        padding-bottom: 10px;
        padding-top: 10px;
        border-radius: 4px;
        border: 1px solid rgb(229, 209, 214);
        position: relative;
        span {
          text-align: center;
          /*border:1px solid red;*/
        }
        .card_list_info_posi_title {
          position: absolute;
          left: -21px;
          top: -10px;
          background-color: white;
        }
        .card_list_info_span--info {
          flex: 1;
          display: flex;
          flex-flow: column;
          border-right: 1px solid rgb(246, 238, 239);
          .card_list_info_span--info_text {
            display: flex;
            flex-flow: row;
            justify-content: space-between;
            align-items: flex-start;
            height: 25px;
            line-height: 25px;
            font-size: 12px;
            .card_list_info_span--info_text_name {
              flex: 1;
              overflow: hidden;
              height: 100%;
              display: flex;
              flex-flow: row;
              justify-content: flex-start;
              align-items: center;
              margin-left: 1%;
              /*border:1px solid black;*/
              span {
                margin-left: 8px;
                overflow: hidden;
                height: 100%;
              }
            }
            .card_list_info_span--info_text_qty {
              width: 18%;
              /*border:1px solid black;*/
            }
          }
        }
        .card_list_info_span--ratio {
          width: 19%;
          border-right: 1px solid rgb(246, 238, 239);
        }
        .card_list_info_span--qty {
          width: 10%;
          border-right: 1px solid rgb(246, 238, 239);
        }
        .card_list_info_span--button {
          width: 10%;
          border-right: 1px solid rgb(246, 238, 239);
        }
      }
      .card_list_info_last {
        border: none;
        margin-top: 0px;
      }
    }
    .click-button {
      width: 9%;
      position: fixed;
      right: 2%;
      margin-top: 20px;
      .el-card__body {
        padding-top: 0px;
      }
      .el-card {
        display: flex;
        flex-flow: column;
        align-items: center;
        padding: 20px;
        .el-button {
          margin: 0;
          font-size: 16px;
        }

        .el-button:nth-child(2) {
          margin-top: 10px;
          margin-bottom: 5px;
        }
        .el-button--text {
          width: 70px;
          text-align: center;
          color: #4db3ff;
          font-size: 18px;
        }
        .el-button--text:hover {
          color: #ec407a;
        }
      }
    }
  }
</style>
