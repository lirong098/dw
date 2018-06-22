<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="clearfix forecase_sheet">
        <div class="card_box">
          <div class="card-header card-header-text" style="cursor: pointer;" @click="btnmethod">
            <h4>
              筛选条件
              <div style="float: right; margin-top: 5px 0px 0px 15px; height: 20px; width: 20px; padding-top: 7px">
                <div :class="btnstatus===true ? 'box':'boxright'"></div>
              </div>
            </h4>
          </div>
          <el-card :class="btnstatus === true ? 'disscaling':'scaling'">
            <el-button type="danger"
                       class="customer_add"
                       style="float: right; margin-right: 10px; position: absolute; top: 7px; left: 93%;"
                       @click="getList"
            >查询
            </el-button>
            <el-form ref="form" :label-width="'80px'">
              <el-form-item label="客户 :">
                <div class="item"
                     v-for="item in userOption"
                     :key="item.customer_id"
                     @click="changeClient(item.customer_id)">
                  <el-tag class="eltag"
                          :type="userValue === item.customer_id ? 'success' : 'gray'">
                    {{item.customer_name}}
                  </el-tag>
                </div>
              </el-form-item>
              <el-form-item label="预估版本 :">
                <el-select v-model="versionInitial" @change="versionMethod(versionInitial)" placeholder="请选择">
                  <el-option
                    v-for="item in versionData"
                    :key="item.fcst_order_id"
                    :label="item.fcst_order_no"
                    :value="item.fcst_order_id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="材料类型 :">
                <el-select v-model="typeInitial" placeholder="请选择" @change="typeMethod(typeInitial)">
                  <el-option
                    v-for="item in typeData"
                    :key="item.meta_id"
                    :label="item.meta_name"
                    :value="item.meta_id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="季节 :">
                <el-select v-model="seasonInitial" @change="seasonMethod(seasonInitial)" placeholder="请选择">
                  <el-option
                    v-for="item in seasonData"
                    :key="item.meta_id"
                    :label="item.meta_name"
                    :value="item.meta_id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="当前周 :">
                <el-date-picker v-model="nowWeek"
                                @change="newWeekMethod(nowWeek)"
                                disabledDate
                                type="week"
                                :picker-options="pickerOptions"
                                format="yyyy-MM-dd(WW周)"
                                placeholder="选择周">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="备料周期 :">
                <el-select v-model="weekValue" @change="weekChange(weekValue)" placeholder="请选择">
                  <el-option v-for="item in weekOptions"
                             :key="item.value"
                             :label="item.label"
                             :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="统计数据 :">
                <div class="body">
                  <div class="items diff_checkbox">
                    <div class="item prepare3">
                      <el-tooltip effect="dark" content="预计出货数" placement="top-start">
                        <el-checkbox v-model="diff.quantity">预计出货</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item total">
                      <el-tooltip effect="dark" content="首单实单出货数" placement="top-start">
                        <el-checkbox v-model="diff.first_quantity">首单出货</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item curr">
                      <el-tooltip effect="dark" content="翻单实单出货数" placement="top-start">
                        <el-checkbox v-model="diff.repeat_quantity">翻单出货</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item diff">
                      <el-tooltip effect="dark" content="预计上线数" placement="top-start">
                        <el-checkbox v-model="diff.arrival_quantity">预计上线</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item prepare">
                      <el-tooltip effect="dark" content="首单实单上线数" placement="top-start">
                        <el-checkbox v-model="diff.pr_on_line_quantity">首单上线</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item prepare1">
                      <el-tooltip effect="dark" content="翻单实单上线数" placement="top-start">
                        <el-checkbox v-model="diff.first_on_line_quantity">翻单上线</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item prepare2">
                      <el-tooltip effect="dark" content="预计到货数" placement="top-start">
                        <el-checkbox v-model="diff.repeat_on_line_quantity">预计到货</el-checkbox>
                      </el-tooltip>
                    </div>
                    <div class="item prepare4">
                      <el-tooltip effect="dark" content="备料剩余数" placement="top-start">
                        <el-checkbox v-model="diff.remaining_quantity">备料剩余</el-checkbox>
                      </el-tooltip>
                    </div>
                  </div>
                </div>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
      <div class="body_table">
        <div class="card_box">
          <div class="card-header card-header-text" style="z-index: 100001;">
            <h4>
              预估表
            </h4>
          </div>
          <lazy-render>
            <el-card v-loading="loading">
              <div style="position: absolute; left: 150px; width: 85%; top: 5px; height: 30px; line-height: 30px;">
                <div class="titlebox pr_quantity_color">预计出货</div>
                <div class="titlebox first_quantity_color">首单出货</div>
                <div class="titlebox repeat_quantity_color">翻单出货</div>
                <div class="titlebox arrival_quantity_color">预计上线</div>
                <div class="titlebox pr_on_line_quantity_color">首单上线</div>
                <div class="titlebox first_on_line_quantity_color">翻单上线</div>
                <div class="titlebox repeat_on_line_quantity_color">预计到货</div>
                <div class="titlebox remaining_quantity_color">备料剩余</div>
                <div class="titlebox" style="color: #c9daf8;">备料周</div>
                <div class="titlebox" style="color: #f4cccc;">出货周</div>
              </div>
              <el-table :data.lazy="dataList"
                        :height="tabHeight"
                        ref="multipleTable"
                        @selection-change="handleSelectionChange"
                        v-if="dataList.length>0"
                        border>
                <el-table-column label="操作"
                                 fixed
                                 width="80">
                  <template scope="scope">
                    <el-button type="danger"
                               fixed
                               size="small"
                               @click="creatBL(scope.row)">备料
                    </el-button>
                  </template>
                </el-table-column>
                <el-table-column type="expand" fixed>
                  <template scope="props">
                    <el-table :data="props.row.itemList"
                              border>
                      <el-table-column label="Item"
                                       fixed
                                       width="190">
                        <template scope="scope">
                          <div style="width: 100%; float: left;">
                            <div style="width: 50%; float: left;">
                              <div class="divplaceholder"
                                   v-show="diff.quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="diff.first_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="diff.repeat_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="diff.pr_on_line_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="diff.first_on_line_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="diff.repeat_on_line_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="type !== 49 && diff.arrival_quantity === true">
                              </div>
                              <div class="divplaceholder"
                                   v-show="type !== 49 && diff.remaining_quantity === true">
                              </div>
                              <div style="position: absolute; top: 45%; right: 55%;">
                                {{scope.row.item_info.item_name}}
                              </div>
                            </div>
                            <div class="pr_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'预计出货'"
                                 v-show="diff.quantity === true">
                            </div>
                            <div class="first_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'首单出货'"
                                 v-show="diff.first_quantity === true">
                            </div>
                            <div class="repeat_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'翻单出货'"
                                 v-show="diff.repeat_quantity === true">
                            </div>
                            <div class="arrival_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'预计上线'"
                                 v-show="diff.pr_on_line_quantity === true">
                            </div>
                            <div class="pr_on_line_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'首单上线'"
                                 v-show="diff.first_on_line_quantity === true">
                            </div>
                            <div class="first_on_line_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'翻单上线'"
                                 v-show="diff.repeat_on_line_quantity === true">
                            </div>
                            <div class="repeat_on_line_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'预计到货'"
                                 v-show="type !== 49 && diff.arrival_quantity === true">
                            </div>
                            <div class="remaining_quantity_color"
                                 style="width: 50%; float: right;"
                                 v-text="'备料剩余'"
                                 v-show="type !== 49 && diff.remaining_quantity === true">
                            </div>
                          </div>
                        </template>
                      </el-table-column>
                      <el-table-column :label="carry_forward_label"
                                       width="80"
                                       prop="carry_forward">
                        <template scope="scope">
                          <div class="remaining_quantity_color">
                            {{scope.row.carry_forward}}
                          </div>
                        </template>
                      </el-table-column>
                      <el-table-column v-for="(item,index) in props.row.itemList[0][props.row.itemList[0].item_id]"
                                       v-if="dataList[0].current_week<=item.delivery_date"
                                       :key="index"
                                       :label="item.delivery_date"
                                       width="80">
                        <template scope="test">
                          <div class="pr_quantity_color"
                               :class="test.row[test.row.item_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                               v-show="diff.quantity === true">
                            {{test.row[test.row.item_id][index].quantity}}
                          </div>
                          <div class="first_quantity_color"
                               :class="test.row[test.row.item_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                               v-show="diff.first_quantity === true">
                            {{test.row[test.row.item_id][index].first_quantity}}
                          </div>
                          <div class="repeat_quantity_color"
                               :class="test.row[test.row.item_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                               v-show="diff.repeat_quantity === true">
                            {{test.row[test.row.item_id][index].repeat_quantity}}
                          </div>
                          <div class="arrival_quantity_color"
                               :class="test.row[test.row.item_id][index].status ==='pr_time' ?'testcolor':''"
                               v-show="diff.pr_on_line_quantity === true">
                            {{test.row[test.row.item_id][index].pr_on_line_quantity}}
                          </div>
                          <div class="pr_on_line_quantity_color"
                               :class="test.row[test.row.item_id][index].status ==='pr_time' ?'testcolor':''"
                               v-show="diff.first_on_line_quantity === true">
                            {{test.row[test.row.item_id][index].first_on_line_quantity}}
                          </div>
                          <div class="first_on_line_quantity_color"
                               :class="test.row[test.row.item_id][index].status ==='pr_time' ?'testcolor':''"
                               v-show="diff.repeat_on_line_quantity === true">
                            {{test.row[test.row.item_id][index].repeat_on_line_quantity}}
                          </div>
                          <div class="repeat_on_line_quantity_color"
                               :class="test.row[test.row.item_id][index].status ==='pr_time' ?'testcolor':''"
                               v-show="type !== 49 && diff.arrival_quantity === true">
                            {{test.row[test.row.item_id][index].arrival_quantity}}
                          </div>
                          <div class="remaining_quantity_color"
                               :class="test.row[test.row.item_id][index].status ==='pr_time' ?'testcolor':''"
                               v-show="type !== 49 && diff.remaining_quantity === true">
                            {{test.row[test.row.item_id][index].remaining_quantity}}
                          </div>
                        </template>
                      </el-table-column>
                    </el-table>
                  </template>
                </el-table-column>
                <el-table-column label="Model"
                                 fixed
                                 sortable
                                 prop="model_info.model_code"
                                 width="190">
                  <template scope="scope">
                    <div style="width: 100%; float: left;">
                      <div style="width: 50%; float: left;">
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.first_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.repeat_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.pr_on_line_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.first_on_line_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.repeat_on_line_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             v-show="type !== 50 && diff.arrival_quantity === true">
                        </div>
                        <div class="divplaceholder"
                             style="display: inline-block"
                             v-show="diff.remaining_quantity === true">
                        </div>
                        <div :class="type === 50?'posit':'positelse'">
                          {{scope.row.model_info.model_code}}
                        </div>
                      </div>
                      <div class="pr_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'预计出货'"
                           v-show="type !== 50 && diff.quantity === true">
                      </div>
                      <div class="first_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'首单出货'"
                           v-show="type !== 50 && diff.first_quantity === true">
                      </div>
                      <div class="repeat_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'翻单出货'"
                           v-show="type !== 50 && diff.repeat_quantity === true">
                      </div>
                      <div class="arrival_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'预计上线'"
                           v-show="type !== 50 && diff.pr_on_line_quantity === true">
                      </div>
                      <div class="pr_on_line_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'首单上线'"
                           v-show="type !== 50 && diff.first_on_line_quantity === true">
                      </div>
                      <div class="first_on_line_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'翻单上线'"
                           v-show="type !== 50 && diff.repeat_on_line_quantity === true">
                      </div>
                      <div class="repeat_on_line_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'预计到货'"
                           v-show="type !== 50 && diff.arrival_quantity === true">
                      </div>
                      <div class="remaining_quantity_color"
                           style="width: 50%; float: right;"
                           v-text="'备料剩余'"
                           v-show="diff.remaining_quantity === true">
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column :label="carry_forward_label"
                                 width="80"
                                 prop="carry_forward">
                  <template scope="scope">
                    <div class="remaining_quantity_color">
                      {{scope.row.carry_forward}}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column v-for="(item,index) in dataList[0][dataList[0].model_info.model_id]"
                                 v-if="dataList[0].current_week<=item.delivery_date"
                                 :key="index"
                                 :label="item.delivery_date"
                                 style="padding: 0;"
                                 width="80">
                  <template scope="scope">
                    <div class="pr_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].shippingstatus && scope.row[scope.row.model_info.model_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                         v-if="type !== 50 && diff.quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].quantity}}
                    </div>
                    <div class="first_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].shippingstatus && scope.row[scope.row.model_info.model_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                         v-if="type !== 50 && diff.first_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].first_quantity}}
                    </div>
                    <div class="repeat_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].shippingstatus && scope.row[scope.row.model_info.model_id][index].shippingstatus ==='shipping_week'?'shoppingweek':''"
                         v-if="type !== 50 && diff.repeat_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].repeat_quantity}}
                    </div>
                    <div class="arrival_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].status && scope.row[scope.row.model_info.model_id][index].status ==='pr_time'?'testcolor':''"
                         v-if="type !== 50 && diff.pr_on_line_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].pr_on_line_quantity}}
                    </div>
                    <div class="pr_on_line_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].status && scope.row[scope.row.model_info.model_id][index].status ==='pr_time'?'testcolor':''"
                         v-if="type !== 50 && diff.first_on_line_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].first_on_line_quantity}}
                    </div>
                    <div class="first_on_line_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].status && scope.row[scope.row.model_info.model_id][index].status ==='pr_time'?'testcolor':''"
                         v-if="type !== 50 && diff.repeat_on_line_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].repeat_on_line_quantity}}
                    </div>
                    <div class="repeat_on_line_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].status && scope.row[scope.row.model_info.model_id][index].status ==='pr_time'?'testcolor':''"
                         v-if="type !== 50 && diff.arrival_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].arrival_quantity}}
                    </div>
                    <div class="remaining_quantity_color"
                         :class="scope.row[scope.row.model_info.model_id][index].status && scope.row[scope.row.model_info.model_id][index].status ==='pr_time'?'testcolor':''"
                         v-if="diff.remaining_quantity === true">
                      {{scope.row[scope.row.model_info.model_id][index].remaining_quantity}}
                    </div>
                  </template>
                </el-table-column>
              </el-table>
              <el-table v-show="dataList.length === 0" style="padding: 40px;">

              </el-table>
            </el-card>
          </lazy-render>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import {getYearWeek} from '../../common/component.js';
  import {getweekdate} from '../../common/component.js';
  import COMMON from '../../common/common.js';

  export default {
    components: {},
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableData: Array
    },
    data() {
      return {
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        userOption: [],
        userValue: 0,
        seasonData: [],
        seasonInitial: '',
        diff: {
          quantity: false,
          first_quantity: false,
          repeat_quantity: false,
          pr_on_line_quantity: true,
          first_on_line_quantity: true,
          repeat_on_line_quantity: true,
          arrival_quantity: true,
          remaining_quantity: true,
        },
        dataList: [],
        versionData: [],
        versionInitial: '',
        weekOptions: [
          {
            value: 1,
            label: '1周'
          }, {
            value: 2,
            label: '2周'
          }, {
            value: 3,
            label: '3周'
          }, {
            value: 4,
            label: '4周'
          }, {
            value: 5,
            label: '5周'
          }
        ],
        weekValue: 1,
        nowWeek: new Date(),
        carry_forward_label: '',
        itemList: [],
        multipleSelection: [],
        propData: [],
        btnstatus: true, // true展开 false缩小
        loading: true,
        typeData: [],
        typeInitial: '',
        type: '',
        pickerOptions: {
          firstDayOfWeek:1,
          showWeekNumber:true
        }
      }
    },
    methods: {
      btnmethod() {
        this.btnstatus = !this.btnstatus;
      },
      // 切换用户
      changeClient(clientCode) {
        this.userValue = clientCode;
        fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_orders/?order_type=1&all=1&customer_id=' + clientCode, null, this).then((res) => {
          if (res && res.status == 200) {
            this.versionData = res.data.data;
            if (this.versionData.length > 0) {
              this.versionInitial = this.versionData[0].fcst_order_id;
              // this.getList();
            } else {
              this.versionInitial = '';
              this.dataList = [];
            }
          }
        })
      },
      // 备料周期切换
      weekChange(week) {
        this.weekValue = week;
      },
      // 当前周切换
      newWeekMethod(nowWeek) {
        this.nowWeek = new Date(nowWeek);
      },
      typeMethod(type) {
      },
      // 切换预估版本
      versionMethod(versionMes) {

      },
      // 切换季节
      seasonMethod(seasonMes) {

      },
      // 生成备料单
      handleSelectionChange(val) {
        var _this = this;
        this.multipleSelection = [];
        let arr = [];
        let i = 0;
        if (this.type === 49) {
          this.multipleSelection.push(val);
          let weekquantity = 0;
          this.multipleSelection.forEach(function (model, index) {
            model[model.model_id].forEach(function (item, index) {
              if (item.status === 'pr_time') {
                if (item.remaining_quantity > 0) {
                  weekquantity += 0;
                } else if (item.remaining_quantity <= 0) {
                  weekquantity += item.remaining_quantity;
                }
              }
            });
            arr.push({
              fcst_pr_item_id: 0,
              item: {
                item_code: model.itemList[0].item_code,
                item_id: model.itemList[0].item_id,
                item_name: model.itemList[0].item_name,
                extend: {},
                spec: {},
                model: model.model_info
              },
              spec: {},
              extend: {},
              fcst_pr: 0,
              quantity: 0,
              disabled: false, //删除状态
              restore: false, // 恢复按钮状态
              addlocal: 0,
              fcst_order_id: _this.versionInitial,
              delivery_date: getweekdate(val.pr_week[0].pr_week),
              material_type_meta_id: _this.type,
            });
            arr[0].material_type_meta_id = _this.type;
            arr[0].quantity = Math.abs(weekquantity);
            arr[0].item.model.unit_meta = {
              meta_name: "件"
            };
          });
          fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/get_free_size/?model_id=' + val.model_id, null, this).then((res) => {
            if (res && res.status === 200) {
              arr[0].item.item_code = res.data.item_code;
              arr[0].item.item_id = res.data.item_id;
              arr[0].item.item_name = res.data.item_name;
              this.propData = arr;
              console.log('ggg', this.propData)
            }
          });
        } else if (this.type === 50) {
          this.multipleSelection.push(val);
          this.multipleSelection.forEach(function (model, index) {
            model.itemList.forEach(function (item, index) {
              arr.push({
                fcst_pr_item_id: 0,
                item: {
                  item_code: item.item_code,
                  item_id: item.item_id,
                  item_name: item.item_name,
                  extend: {},
                  spec: {},
                  model: model.model_info
                },
                spec: {},
                extend: {},
                fcst_pr: 0,
                quantity: 0,
                disabled: false, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0,
                fcst_order_id: _this.versionInitial,
                delivery_date: getweekdate(val.pr_week[0].pr_week),
                material_type_meta_id: _this.type,
              });
              let weekquantity = 0;
              item[item.item_id].forEach(function (itemlist, index) {
                if (itemlist.status === 'pr_time') {
                  if (itemlist.remaining_quantity > 0) {
                    weekquantity += 0;
                  } else if (itemlist.remaining_quantity <= 0) {
                    weekquantity += itemlist.remaining_quantity;
                  }
                }
              });
              arr[i].material_type_meta_id = _this.type;
              arr[i].quantity = Math.abs(weekquantity);
              arr[i].item.model.unit_meta = {
                meta_name: "件"
              };
              i++;
            })
          });
          for (var j = 0; j < arr.length; j++) {
            if (arr[j].quantity === 0) {
              arr.splice(j, 1);
              j--;
            }
          }
          this.propData = arr;
        }
      },
      // 创建备料
      creatBL(row) {
        var _this = this;
        this.multipleSelection = [];
        let arr = [];
        let i = 0;
        if (this.type === 49) {
          this.multipleSelection.push(row);
          let weekquantity = 0;
          this.multipleSelection.forEach(function (model, index) {
            model[model.model_id].forEach(function (item, index) {
              if (item.status === 'pr_time') {
                if (item.remaining_quantity > 0) {
                  weekquantity += 0;
                } else if (item.remaining_quantity <= 0) {
                  weekquantity += item.remaining_quantity;
                }
              }
            });
            arr.push({
              fcst_pr_item_id: 0,
              item: {
                item_code: model.itemList[0].item_code,
                item_id: model.itemList[0].item_id,
                item_name: model.itemList[0].item_name,
                extend: {},
                spec: {},
                model: model.model_info
              },
              spec: {},
              extend: {},
              fcst_pr: 0,
              quantity: 0,
              disabled: false, //删除状态
              restore: false, // 恢复按钮状态
              addlocal: 0,
              fcst_order_id: _this.versionInitial,
              delivery_date: getweekdate(row.pr_week[0].pr_week),
              material_type_meta_id: _this.type,
            });
            arr[0].material_type_meta_id = _this.type;
            arr[0].quantity = Math.abs(weekquantity);
            arr[0].item.model.unit_meta = {
              meta_name: "件"
            };
          });
          fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/get_free_size/?model_id=' + row.model_id, null, this).then((res) => {
            if (res && res.status === 200) {
              arr[0].item.item_code = res.data.item_code;
              arr[0].item.item_id = res.data.item_id;
              arr[0].item.item_name = res.data.item_name;
              this.propData = arr;
              console.log(1);
              console.log(weekquantity,'gg');
              if (weekquantity === 0) {
                this.$message({
                  message: "此Model无需备料",
                  type: 'warning'
                });
              } else if (weekquantity < 0) {
                console.log(2);
                let newTabName = ++this.chlidTabIndex + '';
                let addChildTABS = {
                  title: '预估备料 - 新增',
                  flag: 1,
                  name: newTabName,
                  closable: true,
                  propdata: this.propData,
                };
                this.chlidTABSValue = newTabName;
                this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
              }
            }
          });
        } else if (this.type === 50) {
          this.multipleSelection.push(row);
          let weekquantity = 0;
          this.multipleSelection.forEach(function (model, index) {
            model.itemList.forEach(function (item, index) {
              arr.push({
                fcst_pr_item_id: 0,
                item: {
                  item_code: item.item_code,
                  item_id: item.item_id,
                  item_name: item.item_name,
                  extend: {},
                  spec: {},
                  model: model.model_info
                },
                spec: {},
                extend: {},
                fcst_pr: 0,
                quantity: 0,
                disabled: false, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0,
                fcst_order_id: _this.versionInitial,
                delivery_date: getweekdate(row.pr_week[0].pr_week),
                material_type_meta_id: _this.type,
              });

              item[item.item_id].forEach(function (itemlist, index) {
                if (itemlist.status === 'pr_time') {
                  if (itemlist.remaining_quantity > 0) {
                    weekquantity += 0;
                  } else if (itemlist.remaining_quantity <= 0) {
                    weekquantity += itemlist.remaining_quantity;
                  }
                }
              });
              arr[i].material_type_meta_id = _this.type;
              arr[i].quantity = Math.abs(weekquantity);
              arr[i].item.model.unit_meta = {
                meta_name: "件"
              };
              i++;
            })
          });
          for (var j = 0; j < arr.length; j++) {
            if (arr[j].quantity === 0) {
              arr.splice(j, 1);
              j--;
            }
          }
          this.propData = arr;
          if (weekquantity >= 0) {
            this.$message({
              message: "此Model无需备料",
              type: 'warning'
            });
          } else if (weekquantity < 0) {
            let newTabName = ++this.chlidTabIndex + '';
            let addChildTABS = {
              title: '预估备料 - 新增',
              flag: 1,
              name: newTabName,
              closable: true,
              propdata: this.propData,
            };
            this.chlidTABSValue = newTabName;
            this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
          }
        }
//        console.log(row)
//        if (this.propData.length === 0) {
//          this.$message({
//            message: "此Model无需备料",
//            type: 'warning'
//          });
//        } else if (this.propData.length > 0) {
//          let newTabName = ++this.chlidTabIndex + '';
//          let addChildTABS = {
//            title: '预估备料 - 新增',
//            flag: 1,
//            name: newTabName,
//            closable: true,
//            propdata: this.propData,
//          };
//          this.chlidTABSValue = newTabName;
//          this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
//        }
      },
      // 获取对应Item方法
      handleChange(row, index) {
        var _this = this;
        this.type = JSON.parse(JSON.stringify(this.typeInitial));
        let current = getYearWeek(this.nowWeek);
        fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/estimate_item/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial + '&model_id=' + row.model_info.model_id + '&material_type_meta_id=' + this.typeInitial, null, this).then((res) => {
          if (res && res.status === 200) {
            let typeData = res.data.pop();
            if (this.type === 49) {
              res.data.forEach(function (item, index) {
                item.pr_week = row.pr_week;
                if (item.item_name === 'G') {
                  res.data.splice(index, 1)
                }
              })
            } else if (this.type === 50) {
//              _this.dataList[_this.dataList.model_id] = typeData;
//              console.log(_this.dataList,index)
//              console.log(index)
              res.data.forEach(function (item, index) {
                item.pr_week = row.pr_week;
              })
              this.dataList[index][this.dataList[index].model_id] = typeData;
            }
            for (let item of res.data) {
              for (let itemArr of item[item.item_id]) {
                for (let pr_week of row.pr_week) {
                  if (pr_week.pr_week === itemArr.delivery_date) {
                    itemArr.status = 'pr_time';
                  }
                  if (pr_week.shipping_week === itemArr.delivery_date) {
                    itemArr.shippingstatus = 'shipping_week'
                  }
                }
              }
            }
            console.log(_this.dataList,'_this.dataList')
            for (let model of _this.dataList) {
              for (let modelArr of model[model.model_id]) {
                for (let model_pr_week of model.pr_week) {
                  if (model_pr_week.pr_week === modelArr.delivery_date) {
                    modelArr.status = 'pr_time';
                  }
                }
              }
            }
            row.itemList = res.data;
          }
        })
      },
      getVersion(customer_id) {
        fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_orders/?order_type=1&all=1&customer_id=' + customer_id, null, this).then((res) => {
          if (res && res.status === 200) {
            this.versionData = res.data.data;
            if (this.versionData.length > 0) {
              this.versionInitial = this.versionData[0].fcst_order_id;
            } else {
              this.versionInitial = '';
              this.dataList = [];
            }
          }
        })
      },
      // 获取列表方法
      getList() {
        var _this = this;
        this.loading = true;
        if (this.seasonInitial !== '' && this.versionInitial !== '' && this.typeInitial !== '' && this.userValue !== 0) {
          let current = getYearWeek(this.nowWeek);
          fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/estimate/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial + '&material_type_meta_id=' + this.typeInitial, null, this).then((res) => {
            if (res && res.status === 200) {
              console.log(1)
              this.carry_forward_label = '< ' + res.data[0].current_week;
              for (let model of res.data) {
                for (let pr_week of model.pr_week) {
                  for (let week of model[model.model_info.model_id]) {
                    if (pr_week.pr_week === week.delivery_date) {
                      week.status = 'pr_time'
                    }
                    if (pr_week.shipping_week === week.delivery_date) {
                      week.shippingstatus = 'shipping_week'
                    }
                  }
                }
              }
//              for (let i of res.data) {
//                this.handleChange(i);
//              }
              res.data.forEach(function (item, index) {
                _this.handleChange(item, index);
              });
              this.dataList = res.data;
              this.multipleSelection = [];
              setTimeout(function () {
                _this.loading = false;
              },5000);
              // this.loading = false;
            }
          })
        } else {
          this.loading = false;
          this.$message({
            message: "缺少查询信息",
            type: 'warning'
          });
        }
      }
    },
    computed: {
      tabHeight() {
        return (this.dataList.length + 1) * 130 > 630 ? 630 : (this.dataList.length + 1) * 130;
      }
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue === "1") {
//          this.getList()
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

    },
    created() {
      var _this = this;
      fetchAPI('get', this.$store.state.NEW_API + '/api/customer/customers/?all=1', null, this).then((res) => {
        if (res && res.status === 200) {
          for (let item of res.data.data) {
            this.userOption.push(item);
          }
          if (this.userOption.length > 0) {
            this.userValue = this.userOption[0].customer_id;
          }
        }
        if (this.userOption.length > 0) {
          this.loading = false;
          fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_orders/?order_type=1&all=1&customer_id=' + this.userValue, null, this).then((res) => {
            if (res && res.status === 200) {
              this.versionData = res.data.data;
              if (this.versionData.length > 0) {
                this.versionInitial = this.versionData[0].fcst_order_id;
              } else {
                this.versionInitial = '';
                this.dataList = [];
              }
            }
            return COMMON.getMetaList(this, 43)
          }).then((res) => {
            if (res && res.status === 200) {
              if (res.data.length > 0) {
                this.seasonData = res.data;
                this.seasonInitial = this.seasonData[0].meta_id;
              } else {
                this.seasonData = [];
                this.seasonInitial = '';
              }
            }
            return COMMON.getMetaList(this, 48)
          }).then((res) => {
            if (res && res.status === 200) {
              if (res.data.length > 0) {
                this.typeData = res.data;
                this.typeInitial = this.typeData[0].meta_id;
              } else {
                this.typeData = [];
                this.typeInitial = '';
              }
              if (this.seasonInitial !== '' && this.typeInitial !== '' && this.versionInitial !== '' && this.userValue !== 0) {
                this.getList();
              }
            }
          })
        } else {
          this.loading = false;
        }
      })
    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_main_contain {
    .toolmy {
      height: 50px;
    }
    .btnright {
      width: 100%;
      height: 90px;
      float: right;
      display: inline-block;
    }
  }

  .forecase_sheet {
    padding: 20px 10px 10px 10px;
    .el-form {
      border: 1px solid #ccc;
      .el-form-item {
        /*border:1px solid red;*/
        margin: 8px 5px;
        border-bottom: 1px dashed #ccc;
        padding-bottom: 5px;
      }
      .el-form-item:last-child {
        border-bottom: none;
        padding-bottom: 0px;
      }
    }
  }

  .eltag {
    float: left;
    margin-right: 10px;
    margin-top: 6px;
    cursor: pointer;
  }

  .body {
    .items {
      overflow: hidden;
      .item {
        float: left;
        color: #000;
        /*width: 195px;*/
        margin-right: 15px;
        .arrow {
          margin: 0 15px;
        }
        .item_content {
          word-break: normal;
          width: auto;
          word-wrap: break-word;
          overflow: hidden;
        }
      }
    }
  }

  .titlebox {
    margin-right: 10px;
    float: left;
    height: 30px;
    line-height: 30px;
  }

  .pr_quantity_color {
    font-size: 14px;
    color: #eb5a46;
  }

  .first_quantity_color {
    font-size: 14px;
    color: #20a0ff;
  }

  .repeat_quantity_color {
    font-size: 14px;
    color: #13ce66;
  }

  .arrival_quantity_color {
    font-size: 14px;
    color: #ffab4a;
  }

  .pr_on_line_quantity_color {
    font-size: 14px;
    color: #1f2d3d;
  }

  .first_on_line_quantity_color {
    font-size: 14px;
    color: #c377e0;
  }

  .repeat_on_line_quantity_color {
    font-size: 14px;
    color: #00c2e0;
  }

  .remaining_quantity_color {
    font-size: 14px;
    color: #e91e63;
  }

  .el-table__expanded-cell {
    padding: 20px 0px 20px 125px;
    border-left: 0px;
  }

  .card-btn-box {
    position: absolute;
    top: 0px;
    right: 0px;
    z-index: 1;
    background: #fff;
    padding: 10px;
    box-shadow: 0 4px 20px 0px rgba(0, 0, 0, 0.14), 0 7px 10px -5px #ddd;
    border-radius: 3px;
    .select_box {
      padding-bottom: 3px;
      .title {
        color: #aaa;
        font-size: 12px;
        padding-bottom: 3px;
      }
    }

    .summit_btn {
      text-align: right;
    }
  }

  .testcolor {
    background: #c9daf8;
  }

  .scaling {
    height: 46px;
    transition: height 1s;
    -webkit-transition: height 1s; /* Safari */
  }

  .disscaling {
    height: 550px;
    transition: height 1s;
    -webkit-transition: height 1s; /* Safari */
  }

  .box {
    width: 10px;
    height: 10px;
    border-right: 2px solid #fff;
    border-bottom: 2px solid #fff;
    float: right;
    transform: rotate(45deg);
    animation: boxkey 1s;
  }

  @keyframes boxkey {
    from {
      transform: rotate(-45deg)
    }
    to {
      transform: rotate(45deg)
    }
  }

  .boxright {
    width: 10px;
    height: 10px;
    border-right: 2px solid #fff;
    border-bottom: 2px solid #fff;
    float: right;
    transform: rotate(-45deg);
    animation: boxright 1s;
  }

  @keyframes boxright {
    from {
      transform: rotate(45deg)
    }
    to {
      transform: rotate(-45deg)
    }
  }

  .divplaceholder {
    width: 60%;
    float: left;
    height: 24px;
  }

  .posit {
    position: absolute;
    top: 24%;
    right: 55%;
  }

  .positelse {
    position: absolute;
    top: 45%;
    right: 55%;
  }

  .shoppingweek {
    background: #f4cccc;
  }
</style>
