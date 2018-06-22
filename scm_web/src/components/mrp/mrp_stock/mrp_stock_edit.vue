<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="clearfix" style="width: 90%">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4 v-text="active === 2?'MRP预览':childTitlename">

            </h4>
          </div>
          <el-card>
            <div style="margin: 0px 200px; width: 60%">
              <el-steps :space="100" :active="active" finish-status="success">

                <el-step align-center title="基本信息录入" style="width: 48.2%;">

                </el-step>
                <el-step align-center title="比率录入" style="width: 48.2%;">

                </el-step>
                <el-step align-center title="MRP预览" style="width: 48.2%;">

                </el-step>

              </el-steps>
            </div>
            <div class="table">
              <!--tabOne START-->
              <el-card class="tab" v-show="active===0">
                <el-col class="detailMessage">
                  <el-form class="detaMessageForm">
                    <el-col :span="12">
                      <el-form-item label="需求单号 :"
                                    labelWidth="80px">
                        <el-input class="nochange hidden-input"
                                  :title="detaMessageForm.mrp_order.mrp_order_no"
                                  v-text="detaMessageForm.mrp_order.mrp_order_no"
                                  :disabled="true">
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Model :"
                                    labelWidth="80px">
                        <el-input class="nochange hidden-input"
                                  v-show="status === 'look' && childRowId !== 0"
                                  :title="commonmethod(detaMessageForm.mrp_order.model)"
                                  v-text="commonmethod(detaMessageForm.mrp_order.model)">
                        </el-input>
                        <el-input class="truechange"
                                  v-show="status === 'change'"
                                  :value="commonmethod(detaMessageForm.mrp_order.model)"
                                  readonly
                                  :icon="childRowId !== 0?'':'more'"
                                  :on-icon-click="showModel">
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <div style="width: 99%">
                      <el-col :span="12">
                        <el-form-item label="国　　别 :"
                                      labelWidth="80px">
                          <el-input class="nochange"
                                    v-if="childRowId !== 0"
                                    v-text="detaMessageForm.mrp_order.spec.country"
                                    :disabled="true">
                          </el-input>
                          <el-select v-model="countryInitial"
                                     v-if="childRowId === 0"
                                     style="width: 79%"
                                     @change="countryMethod(countryInitial)" placeholder="请选择">
                            <el-option
                              v-for="item in countryData"
                              :key="item.meta_id"
                              :label="item.meta_code"
                              :value="item.meta_code">
                            </el-option>
                          </el-select>
                        </el-form-item>
                      </el-col>
                    </div>
                    <el-col :span="12">
                      <el-form-item label="需求交期 :"
                                    labelWidth="80px">
                        <el-input class="nochange"
                                  v-show="status === 'look'"
                                  v-text="detaMessageForm.mrp_order.delivery_date+'( '+week+'周 )'">
                        </el-input>
                        <el-date-picker v-model="nowWeek"
                                        v-show="status === 'change'"
                                        @change="newWeekMethod"
                                        type="week"
                                        :picker-options="pickerOptions"
                                        format="yyyy-MM-dd(WW周)"
                                        placeholder="选择周">
                        </el-date-picker>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="单据日期 :"
                                    labelWidth="80px">
                        <el-input class="nochange"
                                  v-show="status === 'look'"
                                  v-text="detaMessageForm.mrp_order.deal_date">
                        </el-input>
                        <el-date-picker v-model="nowDate"
                                        type="date"
                                        v-show="status === 'change'"
                                        @change="changeNowDate"
                                        placeholder="选择日期"
                                        :picker-options="pickerOptions">
                        </el-date-picker>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </el-col>
              </el-card>
              <el-card class="tab tableclass" v-show="active===0">
                <template v-if="active===0">
                  <el-table border
                            :data="detaMessageForm.mrp_order_item"
                            style="width: 100%">
                    <el-table-column type="index"
                                     width="50">
                    </el-table-column>
                    <el-table-column label="Item" width="400">
                      <template scope="scope">
                        <el-input class="view"
                                  v-show="status === 'look' && childRowId !== 0"
                                  v-text="commonmethod(scope.row.item)">
                        </el-input>
                        <el-input class="truechange"
                                  :value="commonmethod(scope.row.item)"
                                  v-show="status === 'change'"
                                  readonly
                                  :disabled="scope.row.restore===false?false:true"
                                  :icon="scope.row.restore===false?'more':''"
                                  :on-icon-click="showItem">
                        </el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="数量">
                      <template scope="scope">
                        <el-input class="view"
                                  v-show="status === 'look'"
                                  v-text="scope.row.quantity">
                        </el-input>
                        <el-input v-model.number="scope.row.quantity"
                                  v-show="status === 'change'"
                                  :disabled="scope.row.restore===false?false:true"
                                  class="truechange">
                        </el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="单位">
                      <template scope="scope">
                        <el-input v-text="detaMessageForm.mrp_order.model.unit_meta.meta_name">

                        </el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="110" v-if="status === 'change'">
                      <template scope="scope">
                        <el-button size="small"
                                   @click="addrow(scope.$index)"
                                   v-show="scope.row.restore === false">
                          +
                        </el-button>
                        <el-button size="small"
                                   style="margin-right: 8px;"
                                   @click="removerow(scope.$index,scope.row)"
                                   v-show="scope.row.restore === false">
                          -
                        </el-button>
                        <el-button size="small"
                                   @click="recoverrow(scope.$index,scope.row)"
                                   v-show="scope.row.restore === true">
                          恢复
                        </el-button>
                        <el-button size="small"
                                   @click="addrow(scope.$index,scope.row)"
                                   v-show="scope.row.restore === true">
                          +
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </template>
                <!--Model弹窗-->
                <el-dialog title="Model" style="float: left" :visible.sync="modelDialog" size="large">
                  <modellist @getDialogInfo="getlModel"
                             :noGetItem="false"
                             :exclude="2"
                             v-if="modelDialog">
                  </modellist>
                </el-dialog>
                <!--Item弹窗-->
                <el-dialog title="Model" style="float: left" :visible.sync="itemDialog" size="large">
                  <modellist @getDialogInfo="getlItem"
                             :onlyGetItem="true"
                             :model_id="detaMessageForm.mrp_order.model.model_id"
                             v-if="itemDialog">
                  </modellist>
                </el-dialog>
              </el-card>
              <!--tabOne END-->
              <!--tabTwo START-->
              <el-card class="tab tableclass" v-show="active===1">
                <div style="height: 20px; margin-left: 10%; font-weight: 900;">
                  Model : {{commonmethod(detaMessageForm.mrp_order.model)}}
                </div>
                <div style="height: 20px; margin-left: 10%; font-weight: 900;">总数 : {{quantityall}}</div>
                <template>
                  <el-table border
                            class="ratio"
                            :data="BLarr"
                            style="width: 80%; margin-left: 10%;">
                    <el-table-column label="备料类型" :width="250">
                      <!--v-model="detaMessageForm.fcst_pr_item[scope.$index].quantity"-->
                      <template scope="scope">
                        <el-input v-text="scope.row.meta_name">

                        </el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="比率" :width="250">
                      <template scope="scope">
                        <el-input class="view"
                                  style="width: 24%"
                                  v-show="status === 'look' && childRowId !== 0"
                                  v-text="scope.row.ratio">
                        </el-input>
                        <el-input v-model.number="scope.row.ratio"
                                  v-show="status === 'change'"
                                  class="twotable"
                                  @change="quantity(scope.row,scope.$index)">

                        </el-input>
                        %
                      </template>
                    </el-table-column>
                    <el-table-column label="件数" :width="250">
                      <template scope="scope">
                        <el-input class="view"
                                  v-show="status === 'look' && childRowId !== 0"
                                  v-text="scope.row.quantity">
                        </el-input>
                        <el-input v-model.number="scope.row.quantity"
                                  v-show="status === 'change'"
                                  class="twotable"
                                  @change="ratio(scope.row)">
                        </el-input>
                      </template>
                    </el-table-column>
                  </el-table>
                </template>
              </el-card>
              <!--tabTwo END-->
              <!--tabThree START-->
              <el-card class="tab tableclass" v-show="active===2">
                <el-col class="detailMessage">
                  <el-form class="detaMessageForm">
                    <el-col :span="12">
                      <el-form-item label="Model :"
                                    labelWidth="80px">
                        <el-input class="nochange"
                                  v-text="commonmethod(detaMessageForm.mrp_order.model)"
                                  :disabled="true">
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="单位 :"
                                    labelWidth="80px">
                        <el-input class="nochange"
                                  v-text="detaMessageForm.mrp_order.model.unit_meta.meta_name?detaMessageForm.mrp_order.model.unit_meta.meta_name:'件'">
                          <!--v-text="detaMessageForm.mrp_order.model.unit_meta.meta_name"-->
                          <!--{{'米'}}-->
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="数量 :"
                                    labelWidth="80px">
                        <el-input class="nochange"
                                  v-text="quantityall"
                                  :disabled="true">
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-button style="margin-bottom: 12px; float: right; margin-right: 17%;"
                                 type="primary"
                                 class="customer_add"
                                 @click="viewBom">BOM
                      </el-button>
                    </el-col>
                  </el-form>
                </el-col>
              </el-card>
              <el-card class="tab" v-show="active===2">
                <div style="width: 100%">
                  <div style="float: left; margin-right: 10px; margin-bottom: 10px;" v-for="item in BLarr">
                    {{item.meta_name}} : {{item.ratio}}%
                  </div>
                </div>
                <el-col class="detailMessage">
                  <el-form class="detaMessageForm">
                    <template v-if="active===2 && code !==0">
                      <el-table border
                                @selection-change="handleSelectionChange"
                                :data="bomData"
                                style="width: 100%; margin-bottom: 20px;">
                        <el-table-column type="selection"
                                         width="55">
                        </el-table-column>
                        <el-table-column label="备料形式">
                          <template scope="scope">
                            <el-input class="view"
                                      v-text="scope.row.pr_form_meta.meta_name">
                            </el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="Model" width="150">
                          <template scope="scope">
                            <div class="view jump"
                                 @click.stop="lookModelBtn(scope.$index, scope.row)"
                                 v-text="commonmethod(scope.row.material_item.model)">
                            </div>
                          </template>
                        </el-table-column>
                        <el-table-column label="Item" width="150">
                          <template scope="scope">
                            <el-input class="view"
                                      v-text="commonmethod(scope.row.material_item)">
                            </el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="纱线损耗">
                          <template scope="scope">
                            {{scope.row.material_item.extend.consume_pr_form.pr_yarn}}
                          </template>
                        </el-table-column>
                        <el-table-column label="毛坯损耗">
                          <template scope="scope">
                            {{scope.row.material_item.extend.consume_pr_form.pr_rough}}
                          </template>
                        </el-table-column>
                        <el-table-column label="色布损耗">
                          <template scope="scope">
                            {{scope.row.material_item.extend.consume_pr_form.pr_fabric}}
                          </template>
                        </el-table-column>
                        <el-table-column label="件数">
                          <template scope="scope">
                            <el-input class="view" v-text="classifQuantity(scope.row)">
                            </el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="需求数">
                          <template scope="scope">
                            <el-input style="width: 80%;"
                                      v-model="scope.row.quantity">
                            </el-input>
                          </template>
                        </el-table-column>
                      </el-table>
                    </template>
                  </el-form>
                </el-col>
              </el-card>
            </div>
          </el-card>
        </div>
      </div>
    </div>
    <div class=" click-button">
      <el-card class="extra_card" v-if="status === 'look'">
        <el-button type="danger"
                   style="margin-bottom: 12px; width: 100%;"
                   v-show="status === 'look' && active!==2"
                   @click="statusMethod">修改
        </el-button>
        <el-button style="margin-bottom: 12px; width: 100%;"
                   v-show="active>0?true:false"
                   @click="up">上一步
        </el-button>
        <el-button style="margin-bottom: 12px; width: 100%;"
                   v-show="active<2?true:false"
                   @click="next">下一步
        </el-button>
        <el-button type="danger"
                   style="margin-bottom: 12px; width: 100%;"
                   v-show="active===2?true:false"
                   @click="refresh">刷新数据
        </el-button>
        <el-button type="success"
                   style="margin-bottom: 12px; width: 100%;"
                   v-if="status === 'look'"
                   v-show="active===2?true:false" @click="makePr">生成备料
        </el-button>
      </el-card>
      <el-card class="extra_card" v-if="status === 'change'">
        <el-button style="margin-bottom: 12px; width: 100%;"
                   v-show="active>0?true:false"
                   @click="up">上一步
        </el-button>
        <el-button style="margin-bottom: 12px; width: 100%;"
                   v-show="active<2?true:false"
                   @click="next">下一步
        </el-button>
        <el-button type="danger"
                   style="margin-bottom: 12px; width: 100%;"
                   v-show="active===2?true:false"
                   @click="refresh">刷新数据
        </el-button>
        <el-button type="success"
                   style="margin-bottom: 12px; width: 100%;"
                   v-if="status === 'change'"
                   v-show="active===2?true:false" @click="makePr">生成备料
        </el-button>
      </el-card>
    </div>
    <el-dialog title="查看Model" style="float: left" :visible.sync="lookModelDialog" size="large" v-if="lookModelDialog">
      <tableDetailed :tabIndex='1'
                     :rowId="lookModel.clothes_model.model_id"
                     :tableName="lookModel.clothes_model.model_name"
                     :tableType="lookModel.clothes_model.model_type_meta_id.meta_id">
      </tableDetailed>
    </el-dialog>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import {getweekdate} from '../../common/component.js';
  import {getYearWeek} from '../../common/component.js';
  import common from '../../../components/common/common.js'
  import modellist from "../common/model_dialog/dialog_model.vue";
  import requst from "../../common/vmrequst.js";
  import COMMON from '../../common/common.js';
  import tableDetailed from '../../common/model/new_table_detaied.vue';

  export default {
    components: {
      modellist,
      tableDetailed
    },
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      titlename: String,
      rowMessage: Number,
      materialtype: Number, // 备料方式 21: MRP备料
      propStatus: String,
    },
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 1,  // 总条数
        search: '',
        chlidTABS: this.TABS,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        childTitlename: this.titlename,
        childRowId: this.rowMessage,
        childMaterialtype: this.materialtype,
        status: this.propStatus,
        active: 0,
        nowWeek: new Date(),
        nowDate: new Date(),
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          },
          firstDayOfWeek:1,
          showWeekNumber:true
        },
        detaMessageForm: {
          mrp_order: {
            mrp_order_id: 0,
            mrp_order_type_meta: {
              meta_code: '',
              meta_id: this.materialtype,  // 备料类型(MRP备料,MRP实单)
              meta_name: '',
              parent_meta_code: '',
              extend: {}
            },
            model: {
              model_id: 0,
              model_code: '',
              model_name: '',
              unit_meta: {
                meta_name: ''
              },
              spec: {},
              extend: {},
            },
            mrp_order_no: '',
            delivery_date: this.nowDate, //备料交期
            deal_date: this.nowDate,  // 单据日期
            spec: {},
            extend: {},
          },
          mrp_order_item: [
            {
              mrp_order_item_id: 0,
              mrp_order: 0,
              item: {
                item_code: "",
                item_id: 0,
                item_name: "",
                spec: {},
                extend: {},
                model: {
                  model_id: 0,
                  model_code: '',
                  model_name: '',
                  unit_meta: {
                    meta_name: ''
                  }
                }
              },
              delivery_date: "",
              quantity: 0,
              restore: false, // 恢复按钮状态
              addlocal: 0
            }
          ]
        },
        modelDialog: false, // model弹窗状态
        itemDialog: false, //Item弹窗状态
        clickindex: 0, // 记录点击第几个
        quantityall: 0, // 总数
        BLarr: [],
        week: '',
        code: 0,
        bomData: [],
        multipleSelection: [],
        metaList: [],
        lookModelDialog: false, // model详情弹窗控制
        lookModel: {}, // model数据
        countryInitial: '',
        countryData: []
      }
    },
    methods: {
      countryMethod(data){
        console.log(data,'data')
        this.detaMessageForm.mrp_order.spec.country = data;
      },
      // 查看model详情
      lookModelBtn(index, row) {
        this.lookModel = row;
        this.lookModelDialog = true;
        console.log(this.lookModel, 111)
      },
      // 生成备料方法
      makePr() {
        if (this.multipleSelection.length === 0) {
          this.$message({
            type: 'info',
            message: '请选择备料信息'
          });
          return;
        }
        let initialize = {
          mrp_pr: {
            mrp_pr_id: 0,
            model: this.detaMessageForm.mrp_order.model,
            mrp_pr_type_meta_id: {
              meta_id: 20,
            },
            mrp_pr_no: '',
            delivery_date: COMMON.formatDate(),
            deal_date: COMMON.formatDate(),
            spec: this.detaMessageForm.mrp_order.spec,
            extend: {},
          },
          mrp_pr_item: []
        };
        for (let item of this.multipleSelection) {
          initialize.mrp_pr_item.push({
            mrp_pr: 0,
            mrp_pr_item_id: 0,
            material_item: item.material_item,
            mrp_quantity: item.quantity,
            quantity: item.quantity,
            spec: {
              pr_form_meta_id: item.pr_form_meta.meta_id
            },
            extend: {
              material_consume_quantity: 1
            },
            pr_form_meta: item.pr_form_meta,
            addlocal: 0,
            restore: false,
          })
        }
        console.log(initialize);
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '生成备料',
          name: newTabName,
          closable: true,
          stock: 'stock',
          resData: initialize
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      statusMethod() {
        this.status = 'change';
        if (this.detaMessageForm.mrp_order_item.length === 0) {
          this.detaMessageForm.mrp_order_item.push({
            mrp_order_item_id: 0,
            item: {
              item_code: "",
              item_id: 0,
              item_name: "",
              extend: {},
              spec: {},
              model: {
                model_id: 0,
                model_code: '',
                model_name: '',
                unit_meta: {
                  meta_name: ''
                }
              }
            },
            quantity: 0,
            spec: {},
            extend: {},
            pr_form_meta: {
              meta_code: '',
              meta_id: this.materialtype,
              meta_name: '',
              parent_meta_code: '',
              extend: {}
            },
            restore: false, // 恢复按钮状态
            addlocal: 0
          })
        }
      },
      // 重组名称
      commonmethod(model) {
        if (model.model_id) {
          let keyArr = ['model_code', 'model_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          model.spec.color ? tempArr.push(model.spec.color) : '';
          return tempArr.join(' - ')
        }
        if (model.item_id) {
          let keyArr = ['item_code', 'item_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          return tempArr.join(' - ')
        }
      },
      // 比率
      quantity(row, index) {
        row.quantity = Math.ceil(this.quantityall * row.ratio / 100); // 计算比例
//        if (index === (this.BLarr.length - 1)) {
//          row.quantity = this.quantityall * row.ratio / 100; // 计算比例
//          return;
//        }
//        let sum = 0;
//        // 循环比率所在的数组
//        for (let i = 0; i < this.BLarr.length - 1; i++) {
//          // 循环判断除最后一项的数组中比率值是否存在0,存在0不计算
//          if (this.BLarr[i].ratio === 0) {
//            return
//          } else {
//            // 累加比率值
//            sum += Number(this.BLarr[i].ratio);
//          }
//        }
//        // 判断累加值是否大于100
//        if (sum < 100) {
//          // 计算最后一项比率值
//          this.BLarr[this.BLarr.length - 1].ratio = 100 - sum;
//          // 计算最后一项件数
//          this.BLarr[this.BLarr.length - 1].quantity = this.quantityall * this.BLarr[this.BLarr.length - 1].ratio / 100;
//        }
//        this.$forceUpdate();
      },
      ratio(row) {
        row.ratio = Math.round(((row.quantity / this.quantityall) * 100) * 100000) / 100000;
      },
      // 下一步
      next() {
        if (this.active === 0) {
          console.log(this.detaMessageForm.mrp_order_item, 1);
          for (let i = 0; i < this.detaMessageForm.mrp_order_item.length; i++) {
            if (this.detaMessageForm.mrp_order_item[i].quantity === 0) {
              this.detaMessageForm.mrp_order_item.splice(i, 1);
              i--;
            }
          }
          if (this.detaMessageForm.mrp_order_item.length === 0) {
            this.detaMessageForm.mrp_order_item.push({
              mrp_order_item_id: 0,
              item: {
                item_code: "",
                item_id: 0,
                item_name: "",
                extend: {},
                spec: {},
                model: {
                  model_id: 0,
                  model_code: '',
                  model_name: '',
                  unit_meta: {
                    meta_name: ''
                  }
                }
              },
              quantity: 0,
              spec: {},
              extend: {},
              pr_form_meta: {
                meta_code: '',
                meta_id: this.materialtype,
                meta_name: '',
                parent_meta_code: '',
                extend: {}
              },
              restore: false, // 恢复按钮状态
              addlocal: 0
            })
          }
          let flag = true;
          for (let item of this.detaMessageForm.mrp_order_item) {
            if (item.item.item_id === 0 || item.item.item_id === '') {
              flag = false;
              break
            }
          }
          if (this.detaMessageForm.mrp_order_item.length === 0) {
            this.$message({
              type: 'info',
              message: '请输入正确Item信息'
            });
            return
          }
          console.log(this.detaMessageForm.mrp_order_item, 11);
          if (flag === false) {
            this.$message({
              type: 'info',
              message: 'Item信息不能为空'
            });
          } else {
            this.quantityall = 0;
            let i = 0;
            for (let item of this.detaMessageForm.mrp_order_item) {
              i += Number(item.quantity);
            }
            this.quantityall = i;
            if (this.childRowId === 0) {
              fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/metas/?parent_meta_code=36', null, this).then((res) => {
                if (res && res.status === 200) {
                  this.BLarr = [];
                  for (let item of res.data) {
                    this.BLarr.push({
                      meta_code: item.meta_code,
                      meta_id: item.meta_id,
                      meta_name: item.meta_name,
                      ratio: 0,
                      quantity: 0,
                    });
                    this.BLarr[0].ratio = 100;
                    this.quantity(this.BLarr[0]);
                  }

                  this.detaMessageForm.mrp_order.extend.consump_item = this.BLarr;
                  this.detaMessageForm.mrp_order.delivery_date = common.formatDate(this.nowWeek);
                  this.detaMessageForm.mrp_order.deal_date = common.formatDate(this.nowDate);
                  let postData = {
                    mrp_order: this.detaMessageForm.mrp_order,
                    mrp_order_item: this.detaMessageForm.mrp_order_item
                  };
                  return fetchAPI('post', this.$store.state.NEW_API + '/api/mrp_order/mrp_orders/', postData, this)
                }
              }).then((res) => {
                if (res && res.status === 200) {
                  for (let item of res.data.mrp_order_item) {
                    item.restore = false; // 恢复按钮状态
                  }
                  this.childRowId = res.data.mrp_order.mrp_order_id;
                  this.detaMessageForm = res.data;
                  this.$message({
                    type: 'success',
                    message: '基础数据保存成功'
                  });
                  this.active += 1;
                }
              });
            } else {
              if (JSON.stringify(this.detaMessageForm.mrp_order.extend) === '{}') {
                this.quantityall = 0;
                let i = 0;
                for (let item of this.detaMessageForm.mrp_order_item) {
                  i += Number(item.quantity);
                }
                this.quantityall = i;
                fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/metas/?parent_meta_code=36', null, this).then((res) => {
                  if (res && res.status === 200) {
                    this.BLarr = [];
                    for (let item of res.data) {
                      this.BLarr.push({
                        meta_code: item.meta_code,
                        meta_id: item.meta_id,
                        meta_name: item.meta_name,
                        ratio: 0,
                        quantity: 0,
                      });
                      this.BLarr[0].ratio = 100;
                      this.quantity(this.BLarr[0]);
                    }
                  }
                });
              } else {
                this.BLarr = this.detaMessageForm.mrp_order.extend.consump_item;
              }
              for (let item of this.BLarr) {
                this.quantity(item);
              }

              if (this.status === 'change') {
//                alert(1)
                this.detaMessageForm.mrp_order.extend.consump_item = this.BLarr;
                this.detaMessageForm.mrp_order.delivery_date = common.formatDate(this.nowWeek);
                this.detaMessageForm.mrp_order.deal_date = common.formatDate(this.nowDate);
                let postData = {
                  mrp_order: this.detaMessageForm.mrp_order,
                  mrp_order_item: this.detaMessageForm.mrp_order_item
                };
                fetchAPI('put', this.$store.state.NEW_API + '/api/mrp_order/mrp_order/', postData, this).then((res) => {
                  if (res && res.status === 200) {
                    console.log(res.data, 333);
                    for (let item of res.data.mrp_order_item) {
                      item.restore = false; // 恢复按钮状态
                    }
                    this.childRowId = res.data.mrp_order.mrp_order_id;
                    this.detaMessageForm = res.data;
                    this.$message({
                      type: 'success',
                      message: '基础数据保存成功'
                    });
                    this.active += 1;
                  }
                })
              } else if (this.status === 'look') {
                this.active += 1;
              }
            }
          }
        } else if (this.active === 1) {
          let sum = 0;
          for (let item of this.BLarr) {
            sum += Number(item.quantity);
          }
          if (sum > Number(this.quantityall)) {
            this.$message({
              type: 'info',
              message: '件数总数量超出,请核对'
            });
            return;
          }
          // 创建mrp_order
          if (this.childRowId === 0) {
            this.getmeta();
            this.detaMessageForm.mrp_order.extend.consump_item = this.BLarr;
            this.detaMessageForm.mrp_order.delivery_date = common.formatDate(this.nowWeek);
            this.detaMessageForm.mrp_order.deal_date = common.formatDate(this.nowDate);
            let postData = {
              mrp_order: this.detaMessageForm.mrp_order,
              mrp_order_item: this.detaMessageForm.mrp_order_item
            };
            fetchAPI('post', this.$store.state.NEW_API + '/api/mrp_order/mrp_orders/', postData, this).then((res) => {
              if (res && res.status === 200) {
                for (let item of res.data.mrp_order_item) {
                  item.restore = false; // 恢复按钮状态
                }
                this.childRowId = res.data.mrp_order.mrp_order_id;
                this.detaMessageForm = res.data;
              }
              let postData = {
                mrp_order_id: this.detaMessageForm.mrp_order.mrp_order_id
              };
              return fetchAPI('post', this.$store.state.NEW_API + '/api/mat_models/mrp/', postData, this)
            }).then((res) => {
              if (res && res.status === 200) {
                this.code = res.data[0].bom_id;
                this.$message({
                  type: 'success',
                  message: '基础数据保存成功'
                });
                this.active += 1;
              }
            });
          } else if (this.childRowId !== 0) {
            this.getmeta();
            // 修改mrp_order
            this.detaMessageForm.mrp_order.extend.consump_item = this.BLarr;
            this.detaMessageForm.mrp_order.delivery_date = common.formatDate(this.nowWeek);
            this.detaMessageForm.mrp_order.deal_date = common.formatDate(this.nowDate);
            let postData = {
              mrp_order: this.detaMessageForm.mrp_order,
              mrp_order_item: this.detaMessageForm.mrp_order_item
            };
            fetchAPI('put', this.$store.state.NEW_API + '/api/mrp_order/mrp_order/', postData, this).then((res) => {
              if (res && res.status === 200) {
                for (let item of res.data.mrp_order_item) {
                  item.restore = false; // 恢复按钮状态
                }
                this.childRowId = res.data.mrp_order.mrp_order_id;
                this.detaMessageForm = res.data;
              }
              let postData = {
                mrp_order_id: this.detaMessageForm.mrp_order.mrp_order_id
              };
              return fetchAPI('post', this.$store.state.NEW_API + '/api/mat_models/mrp/', postData, this)
            }).then((res) => {
              if (res && res.status === 200) {
                this.code = res.data[0].bom_id;
                for (let i = 0; i < res.data.length; i++) {
                  if(res.data[i].bom_id === 0){
                    return this.active += 1;
                  }
                  if (!res.data[i].material_item.extend.consume_pr_form) {
                    res.data[i].material_item.extend.consume_pr_form = {
                      pr_yarn: 1,
                      pr_rough: 1,
                      pr_fabric: 1
                    }
                  }
                  for (let j = 0; j < this.BLarr.length; j++) {
                    if (this.BLarr[j].meta_id === res.data[i].pr_form_meta.meta_id) {
                      res.data[i].pr_form_meta.quantity = this.BLarr[j].quantity;
                    }
                  }
                  if (res.data[i].pr_form_meta.quantity === 0) {
                    res.data.splice(i, 1);
                    i--;
                  }
                }
                this.bomData = res.data;
                if (this.status === 'look') {
                  return this.active += 1;
                } else if (this.status === 'change') {
                  this.$message({
                    type: 'success',
                    message: '基础数据保存成功'
                  });
                  this.active += 1;
                }
              }
            });
          }
        } else if (this.active > 2) {
          this.active = 2;
        }
      },
      // 上一步
      up() {
        if (this.active === 2) {
          this.active -= 1;
        } else if (this.active === 1) {
          this.active -= 1;
        } else if (this.active === 0) {
          this.active = 0;
        }
      },
      // 查看BOM
      viewBom() {
        console.log(this.code, 'code');
        if (this.code === 0) {
          let initialize = {
            bom: {
              bom_id: 0,
              bom_no: "",
              model_id: this.detaMessageForm.mrp_order.model,
              item_id: {
                item_id: 0,
              },
              version: 0,
              spec: {
                color: ""
              },
              extend: {}
            },
            bom_item: [
              {
                bom_item_id: 0,
                bom: {
                  bom_id: 0,
                  bom_no: "",
                  model_id: 0,
                  item_id: 0,
                  version: 0,
                  spec: {
                    color: ""
                  },
                  extend: {}
                },
                component_model: {
                  model_id: 0,
                  unit_meta: {
                    meta_id: 0,
                    meta_code: "",
                    parent_meta_code: "",
                    meta_name: "",
                    extend: {}
                  },
                  model_type_meta_id: 0,
                  model_code: "",
                  model_name: "",
                  spec: {},
                  extend: {}
                },
                component_item: {
                  item_id: 0,
                  item_code: "",
                  item_name: "",
                  spec: {},
                  extend: {},
                  model: 0
                },
                quantity: 0,
                spec: {
                  consume_items: [],
                  division: false,
                  consumptStatus: false,
                },
                extend: {},
                addlocal: 0,
                restore: false,
              }
            ]
          };
          // 获取唯一标识
          requst.make_unique_no(this, "1", function (that, res) {
            if (res.data.code !== 0) return;
            console.log(res.data.message, 'res.data.message');
            initialize.bom.bom_no = res.data.message;
          });
          let newTabName = ++this.chlidTabIndex + '';
          let addChildTABS = {
            title: '成衣BOM - 新增',
            name: newTabName,
            closable: true,
            rowId: '',
            bom: 'bom',
            rowState: 'change',
            resData: initialize
          };
          this.chlidTABSValue = newTabName;
          this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
        } else {
          let regroup = {};
          let getBomDataMassage = {
            bom_id: this.code
          };
          fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/bom/?bom_id=' + this.code, getBomDataMassage, this).then((res) => {
            if (res && res.status == 200) {
              regroup.bom = res.data;
              fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/bom_items/?bom_id=' + this.code, getBomDataMassage, this).then((res) => {
                if (res && res.status == 200) {
                  for (let item of res.data) {
                    if (!item.component_item) {
                      item.component_item = {
                        item_id: 0
                      };
                    }
                    item.restore = false;
                  }
                  if (res.data.length === 0) {
                    res.data = [
                      {
                        bom_item_id: 0,
                        bom: {
                          bom_id: 0,
                          bom_no: "",
                          model_id: 0,
                          item_id: 0,
                          version: 0,
                          spec: {
                            color: ""
                          },
                          extend: {}
                        },
                        component_model: {
                          model_id: 0,
                          unit_meta: {
                            meta_id: 0,
                            meta_code: "",
                            parent_meta_code: "",
                            meta_name: "",
                            extend: {}
                          },
                          model_type_meta_id: 0,
                          model_code: "",
                          model_name: "",
                          spec: {},
                          extend: {}
                        },
                        component_item: {
                          item_id: 0,
                          item_code: "",
                          item_name: "",
                          spec: {},
                          extend: {},
                          model: 0
                        },
                        quantity: 0,
                        spec: {
                          consume_items: [],
                          division: false,
                          consumptStatus: false,
                        },
                        extend: {},
                        addlocal: 0,
                        restore: false,
                      }
                    ]
                  }
                  regroup.bom_item = res.data;
                  let newTabName = ++this.chlidTabIndex + '';
                  let watchChildTABS = {
                    title: '成衣BOM - 查看',
                    name: newTabName,
                    closable: true,
                    rowState: 'look',
                    bom: 'bom',
                    rowId: regroup.bom.bom_id,
                    resData: regroup
                  };
                  this.chlidTABSValue = newTabName;
                  this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS);
                  $(".content").scrollTop(0);
                }
              })
            }
          });
        }
      },
      newWeekMethod(res) {
        console.log(res)
      },
      // 改变单据日期
      changeNowDate(res) {

      },
      // model弹窗
      showModel() {
        this.modelDialog = true;
      },
      // model弹窗选择按钮
      getlModel(res) {
        console.log(res);
        let arr = [];
        this.detaMessageForm.mrp_order.model = res;
        for (let i = 0; i < res.model_item.length; i++) {
          arr.push(
            {
              mrp_order_item_id: 0,
              mrp_order: 0,
              item: {
                item_code: res.model_item[i].item_code,
                item_id: res.model_item[i].item_id,
                item_name: res.model_item[i].item_name,
                extend: {},
                spec: {},
                model: {
                  model_id: res.model_id,
                  model_code: res.model_code,
                  model_name: res.model_name,
                  unit_meta: res.unit_meta
                }
              },
              delivery_date: this.nowWeek !== '' ? common.formatDate(this.nowWeek) : '', //备料交期
              spec: {},
              extend: {},
              quantity: 0,
              restore: false, // 恢复按钮状态
              addlocal: 0
            }
          )
        }
        this.detaMessageForm.mrp_order_item = arr;
        this.modelDialog = false;
      },
      // Item弹窗
      showItem() {
        if (this.detaMessageForm.mrp_order.model.model_id === 0) {
          this.$message({
            type: 'info',
            message: '请选择model'
          });
        } else {
          this.itemDialog = true;
        }
      },
      // Item弹窗选择按钮
      getlItem(res) {
        // 容器数组
        let arr = [];
        // 将有信息的数据存入容器数组
        for (let x of this.detaMessageForm.mrp_order_item) {
          if (x.item.item_id !== 0 && x.item.item_code !== '' && x.item.item_name !== '') {
            arr.push(x);
          }
        }
        console.log(arr, 1);
        // 容器数组长度为0 则push所有数据
        if (arr.length === 0) {
          for (let y = 0; y < res.length; y++)
            arr.push(
              {
                mrp_order_item_id: 0,
                mrp_order: 0,
                item: {
                  item_code: res[y].item_code,
                  item_id: res[y].item_id,
                  item_name: res[y].item_name,
                  extend: {},
                  spec: {},
                  model: {
                    model_id: this.detaMessageForm.mrp_order.model.model_id,
                    model_code: this.detaMessageForm.mrp_order.model.model_code,
                    model_name: this.detaMessageForm.mrp_order.model.model_name,
                    unit_meta: this.detaMessageForm.mrp_order.model.unit_meta
                  }
                },
                delivery_date: this.nowWeek !== '' ? common.formatDate(this.nowWeek) : '', //备料交期
                quantity: 0,
                spec: {},
                extend: {},
                pr_form_meta: {
                  meta_code: '',
                  meta_id: this.materialtype,
                  meta_name: '',
                  parent_meta_code: '',
                  extend: {}
                },
                delete: 0, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0
              }
            )
        } else {
          // 循环res数组
          console.log(res);
          for (let i = 0; i < res.length; i++) {
            let flag = true;
            // 去重
            for (let j = 0; j < arr.length; j++) {
              if (res[i].item_id === arr[j].item.item_id) {
                flag = false;
                break;
              }
            }
            if (flag === true) {
              arr.push(
                {
                  mrp_order_item_id: 0,
                  mrp_order: 0,
                  item: {
                    item_code: res[i].item_code,
                    item_id: res[i].item_id,
                    item_name: res[i].item_name,
                    extend: {},
                    spec: {},
                    model: {
                      model_id: this.detaMessageForm.mrp_order.model.model_id,
                      model_code: this.detaMessageForm.mrp_order.model.model_code,
                      model_name: this.detaMessageForm.mrp_order.model.model_name,
                      unit_meta: this.detaMessageForm.mrp_order.model.unit_meta
                    }
                  },
                  delivery_date: this.nowWeek !== '' ? common.formatDate(this.nowWeek) : '', //备料交期
                  quantity: 0,
                  spec: {},
                  extend: {},
                  pr_form_meta: {
                    meta_code: '',
                    meta_id: this.materialtype,
                    meta_name: '',
                    parent_meta_code: '',
                    extend: {}
                  },
                  restore: false, // 恢复按钮状态
                  addlocal: 0
                }
              )
            }
          }
        }
        this.detaMessageForm.mrp_order_item = arr;
        this.itemDialog = false;
      },
      // 增加行数
      addrow(index) {
        let addrow = {
          mrp_order_item_id: 0,
          item: {
            item_code: "",
            item_id: 0,
            item_name: "",
            extend: {},
            spec: {},
            model: {
              model_id: 0,
              model_code: '',
              model_name: '',
              unit_meta: {
                meta_name: ''
              }
            }
          },
          quantity: 0,
          spec: {},
          extend: {},
          pr_form_meta: {
            meta_code: '',
            meta_id: this.materialtype,
            meta_name: '',
            parent_meta_code: '',
            extend: {}
          },
          restore: false, // 恢复按钮状态
          addlocal: 0
        };
        this.detaMessageForm.mrp_order_item.splice(index + 1, 0, addrow)
      },
      // 移除按钮
      removerow(index, row) {
        console.log(row);
        if (row.item.item_id === 0 && index !== 0) {
          this.detaMessageForm.mrp_order_item.splice(index, 1);
        } else if (row.item.item_id !== 0) {
          row.delete = 0;
          row.restore = true;
        }
      },
      // 恢复按钮
      recoverrow(index, row) {
        console.log(row);
        row.restore = false;
      },
      // 勾选
      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log(val)
      },
      // MRP数显示方法
      classifQuantity(row) {
        for (let item of this.BLarr) {
          if (item.meta_id === row.pr_form_meta.meta_id) {
            if (row.quantity === 0) {
              row.quantity = item.quantity;
            }
            return item.quantity
          }
        }
      },
      // 刷新按钮
      refresh() {
        let postData = {
          mrp_order_id: this.detaMessageForm.mrp_order.mrp_order_id
        };
        fetchAPI('post', this.$store.state.NEW_API + '/api/mat_models/mrp/', postData, this).then((res) => {
          if (res && res.status === 200) {
//            this.code = res.data[0].bom_id;
//            this.bomData = res.data;
//            console.log(this.bomData);
            this.code = res.data[0].bom_id;
            for (let i = 0; i < res.data.length; i++) {
              if (!res.data[i].material_item.extend.consume_pr_form) {
                res.data[i].material_item.extend.consume_pr_form = {};
                res.data[i].material_item.extend.consume_pr_form.pr_yarn = 1;
                res.data[i].material_item.extend.consume_pr_form.pr_rough = 1;
                res.data[i].material_item.extend.consume_pr_form.pr_fabric = 1;
              }
              for (let j = 0; j < this.BLarr.length; j++) {
                if (this.BLarr[j].meta_id === res.data[i].pr_form_meta.meta_id) {
                  res.data[i].pr_form_meta.quantity = this.BLarr[j].quantity;
                }
              }
              if (res.data[i].pr_form_meta.quantity === 0) {
                res.data.splice(i, 1);
                i--;
              }
            }
            this.bomData = res.data;
            this.$message({
              type: 'success',
              message: '刷新成功'
            });
          }
        });
      },
      // 获取元数据方法
      getmeta() {
        fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/metas/?parent_meta_code=36', null, this).then((res) => {
          if (res && res.status === 200) {
            this.metaData = res.data;
            console.log(this.metaData)
          }
        });
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == 1) {

        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      },
      tableData(val) {
        this.childTableData = val;
      }
    },
    updated() {
      var _this = this;
      document.onkeydown = function(e) {
        var e = window.event || e;
        var ele;
        var len;
        var lenShow = 0;
        var eleShow = []; //存显示出来input的数组
        var keyCode = e.keyCode;
        if(keyCode !== 40 && keyCode !== 39 && keyCode !== 38 && keyCode !== 37) return;
        ele = document.querySelectorAll('.table input[type=text]');
        len = ele.length;
        for(var i = 0; i < len; i++) {
          /*过滤掉display为none的元素*/
          if(ele[i].style.display !== 'none' && ele[i].placeholder !== '选择周' && ele[i].placeholder!== '选择日期') {
            eleShow.push(ele[i]);
          }
        }
        eleShow.splice(0,1);
        lenShow = eleShow.length;
        for(var i = 0; i < lenShow; i++) {
          if(document.activeElement === eleShow[i] && _this.active !== 2) {
//            if(e.keyCode === 37 && e.ctrlKey){
//              eleShow[(i - 1) % lenShow].focus();
//              break;
//            }
//            if(e.keyCode === 37 && e.ctrlKey){
//              eleShow[(i - 1) % lenShow].focus();
//              break;
//            }
            switch(keyCode) {
              case 40:
                e.preventDefault();
                eleShow[(i + 2) % lenShow].focus();
                break;
//              case 39:
//                e.preventDefault();
//                eleShow[(i + 1) % lenShow].focus();
//                break;
              case 38:
                e.preventDefault();
                eleShow[(i + (lenShow - 2)) % lenShow].focus();
                break;
//              case 37:
//                e.preventDefault();
//                eleShow[(i - 1) % lenShow].focus();
//                break;
            }
            //取余从第一个开始
            break;
          }else if(document.activeElement === eleShow[i] && _this.active === 2){
            switch(keyCode) {
              case 40:
                e.preventDefault();
                eleShow[(i + 1) % lenShow].focus();
                break;
              case 38:
                e.preventDefault();
                eleShow[(i + (lenShow - 1)) % lenShow].focus();
                break;
            }
            break;
          }
        }
      }
    },
    mounted() {
    },
    created() {
      var _this = this;
      if (this.childRowId === 0) {
        fetchAPI('get', this.$store.state.NEW_API + '/api/mrp_order/make_mrp_order_no/', null, this).then((res) => {
          if (res && res.status === 200) {
            this.detaMessageForm = {
              mrp_order: {
                mrp_order_id: 0,
                mrp_order_type_meta: {
                  meta_code: '',
                  meta_id: this.materialtype,  // 备料类型(MRP备料,MRP实单)
                  meta_name: '',
                  parent_meta_code: '',
                  extend: {}
                },
                model: {
                  model_id: 0,
                  model_code: '',
                  model_name: '',
                  unit_meta: {
                    meta_name: ''
                  },
                  spec: {},
                  extend: {},
                },
                mrp_order_no: res.data.message,
                delivery_date: common.formatDate(this.nowWeek), //备料交期
                deal_date: common.formatDate(this.nowDate),  // 单据日期
                spec: {},
                extend: {},
              },
              mrp_order_item: [
                {
                  mrp_order_item_id: 0,
                  mrp_order: 0,
                  item: {
                    item_code: "",
                    item_id: 0,
                    item_name: "",
                    spec: {},
                    extend: {},
                    model: {
                      model_id: 0,
                      model_code: '',
                      model_name: '',
                      unit_meta: {
                        meta_name: ''
                      }
                    }
                  },
                  delivery_date: this.nowWeek !== '' ? common.formatDate(this.nowWeek) : '',
                  spec: {},
                  extend: {},
                  quantity: 0,
                  restore: false, // 恢复按钮状态
                  addlocal: 0
                }
              ]
            }
          }
          return fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/metas/?parent_meta_code=54', null, this)
        }).then((res) => {
          if (res && res.status === 200) {
            this.countryInitial = res.data[0].meta_code;
            this.countryData = res.data;
            console.log(res.data,'aaaaaa')
          }
        });
        console.log(this.detaMessageForm)
      } else if (this.childRowId !== 0) {
        fetchAPI('get', this.$store.state.NEW_API + '/api/mrp_order/mrp_order/?mrp_order_id=' + this.childRowId, null, this).then((res) => {
          if (res && res.status === 200) {
            this.nowWeek = new Date(res.data.delivery_date); // 备料交期
            this.nowDate = new Date(res.data.deal_date); // 单据日期
            this.detaMessageForm.mrp_order = res.data;
            this.week = getYearWeek(new Date(this.detaMessageForm.mrp_order.delivery_date));
            fetchAPI('get', this.$store.state.NEW_API + '/api/mrp_order/mrp_order_items/?mrp_order_id=' + this.childRowId, null, this).then((res) => {
              if (res && res.status === 200) {
                for (let item of res.data) {
                  item.restore = false; // 恢复按钮状态
                }
                this.detaMessageForm.mrp_order_item = res.data;
                console.log(res.data, '222222');
              }
            })
          }
        });
      }
    }
  }
</script>
<style lang="scss" type="text/scss">
  .clearfix {
    margin-top: 20px;
  }

  .tab {
    margin-bottom: 20px;
  }

  .tab > .el-card__body {
    padding-top: 30px;
  }

  .truechange {
    width: 80%;
  }

  .el-date-editor.el-input {
    width: 80%;
  }

  .nochange {
    float: left;
    height: 36px;
    width: 80%;
  }

  .view {
    line-height: 36px;
    height: 36px;
    margin: 5px 5px;
  }

  .twotable {
    width: 40%;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .click-button {
    width: 8%;
    padding-top: 20px;
    position: fixed;
    right: 1%;
    top: 35%;
    .extra_card {
      display: flex;
      flex-flow: column;
      align-items: center;
      .el-button {
        display: block;
        margin: 0;
      }
      .el-button:nth-child(2) {
        margin-top: 10px;
      }
      .el-dropdown {
        width: 100%;
        height: 40px;
        line-height: 40px;
        font-size: 18px;
        text-align: center;
        color: #4db3ff;
        margin: 5px 0 0 5px;
      }
    }
  }

  .jump {
    color: blue;
    cursor: pointer;
  }

  .ratio>.el-table__body-wrapper{
    overflow-x: hidden !important;
  }
  .hidden-input {
    display: inline-block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
  }
</style>
