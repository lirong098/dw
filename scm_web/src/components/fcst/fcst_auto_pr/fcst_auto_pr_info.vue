<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="clearfix forecase_sheet">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              筛选条件
            </h4>
          </div>
          <el-card>
            <el-button type="danger"
                       class="customer_add"
                       style="float: right; margin-right: 10px; position: absolute; top: 7px; left: 93%;"
                       @click="getList"
            >查询
            </el-button>
            <el-form ref="form" label-width="120px">
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
                <el-select v-model="versionInitial" @change="versionInitial !== ''?getList:''" placeholder="请选择">
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
              <el-form-item label="仅显示需备料 :" label-width="120px">
                <el-checkbox v-model="checked" @change="checkedmethod"></el-checkbox>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              智能备料
            </h4>
          </div>
          <el-card>
            <el-table :data="checked === true?listNotNull:listAll"
                      v-loading="loading"
                      v-show="listAll.length>0"
                      ref="multipleTable"
                      border
                      :summary-method="getSummaries"
                      show-summary
                      @selection-change="handleSelectionChange"
                      style="width: 100%; margin-top: 20px; height: 100%">
              <el-table-column prop="model" label="成衣Model">
                <template scope="scope">
                  <el-input v-text="commonmethod(scope.row.model)"></el-input>
                </template>
              </el-table-column>
              <el-table-column prop="total_needs" label="总需求数" width="150">
              </el-table-column>
              <el-table-column prop="pred_quantity" label="已备料数" width="150">
              </el-table-column>
              <el-table-column prop="remaining_quantity" label="需备料数" width="150">
              </el-table-column>
              <el-table-column label="操作／分析详情" width="200">
                <template scope="scope">
                  <el-button size="small" class="marginstyle" @click="creatBL(scope.row)">备料
                  </el-button>
                  <el-button size="small" class="marginstyle" @click="detail(scope.row)">查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-table v-show="listNotNull.length === 0 && listAll.length === 0" v-loading="loading">

            </el-table>
          </el-card>
        </div>
      </div>
      <el-dialog :title="'智能备料详情'" style="float: left; z-index: 10001;" :visible.sync="detailStatus" size="large">
        <div style="position: absolute; left: 165px; top: 22px; font-weight: 900;">{{detailList.name}}</div>
        <el-table border
                  v-loading="lodingview"
                  v-if="JSON.stringify(detailList) !== '{}'"
                  :data="detailList[detailList.model.model_id]"
                  style="width: 100%;">
          <el-table-column prop="delivery_date" label="周期">
          </el-table-column>
          <el-table-column prop="quantity" label="预估出货数">
            <template scope="scope">
              <div :class="scope.row.delivery_date === detailList.shipping_weeks[0].shipping_week?'quantity':''"
                   v-text="scope.row.quantity">
              </div>
            </template>
          </el-table-column>
          <el-table-column label="实单出货数">
            <el-table-column prop="first_quantity" label="首单">
            </el-table-column>
            <el-table-column prop="repeat_quantity" label="翻单">
            </el-table-column>
          </el-table-column>
          <el-table-column label="实单上线数">
            <el-table-column label="预估上线数">
              <template scope="scope">
                <div :class="scope.row.delivery_date === detailList.pr_weeks[0].pr_week?'pr_on_line_quantity':''"
                     v-text="scope.row.pr_on_line_quantity">
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="first_on_line_quantity" label="首单">
              <template scope="scope">
                <div :class="scope.row.delivery_date === detailList.pr_weeks[0].pr_week?'pr_on_line_quantity':''"
                     v-text="scope.row.first_on_line_quantity">
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="repeat_on_line_quantity" label="翻单">
              <template scope="scope">
                <div :class="scope.row.delivery_date === detailList.pr_weeks[0].pr_week?'pr_on_line_quantity':''"
                     v-text="scope.row.repeat_on_line_quantity">
                </div>
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column label="预计到货数">
            <template scope="scope">
              <div :class="scope.row.delivery_date === detailList.pr_weeks[0].pr_week?'arrival_quantity':''"
                   v-text="scope.row.arrival_quantity">
              </div>
            </template>
          </el-table-column>
          <el-table-column label="剩余数">
            <template scope="scope">
              <div :class="scope.row.delivery_date === detailList.pr_weeks[0].pr_week?'remaining_quantity':''"
                   v-text="scope.row.remaining_quantity">
              </div>
            </template>
          </el-table-column>
        </el-table>

        <el-table border
                  v-loading="lodingview"
                  v-if="JSON.stringify(detailList) === '{}'"
                  style="width: 100%;">
          <el-table-column label="周期">
          </el-table-column>
          <el-table-column label="预估出货数">

          </el-table-column>
          <el-table-column label="实单出货数">
            <el-table-column label="首单">
            </el-table-column>
            <el-table-column label="翻单">
            </el-table-column>
          </el-table-column>
          <el-table-column label="实单上线数">
            <el-table-column label="预估上线数">

            </el-table-column>
            <el-table-column label="首单">

            </el-table-column>
            <el-table-column label="翻单">

            </el-table-column>
          </el-table-column>
          <el-table-column label="预计到货数">

          </el-table-column>
          <el-table-column label="剩余数">

          </el-table-column>
        </el-table>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import {returnMessage} from '../../common/component.js';
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
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 1,  // 总条数
        search: '',
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        childTableData: this.tableData,
        nowWeek: new Date(),
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
        checked: true,
        userOption: [],
        userValue: 0,
        seasonData: [],
        seasonInitial: '',
        firstDayOfWeek: 1,
        listAll: [],
        listNotNull: [],
        detailStatus: false,
        detailList: {},
        selected: [],
        arrAll: [],
        versionData: [],
        versionInitial: '',
        postBlData: [],
        loading: true,
        typeData: [],
        typeInitial: '',
        typevalue: 0,
        lodingview: false,
        pickerOptions: {
          firstDayOfWeek:1,
          showWeekNumber:true
        }
      }
    },
    methods: {
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
          return tempArr.join(' - ');
        }
      },
      // 获取列表方法
      getList() {
        this.loading = true;
        if (this.userValue !== 0 && this.versionInitial !== '' && this.seasonInitial !== '') {
          let current = getYearWeek(this.nowWeek);
          this.typevalue = JSON.parse(JSON.stringify(this.typeInitial));
          fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial + '&material_type_meta_id=' + this.typevalue, null, this).then((res) => {
            if (res && res.status == 200) {
              this.listAll = res.data;
              let newArr = JSON.parse(JSON.stringify(res.data));
              for (var i = 0; i < newArr.length; i++) {
                if (newArr[i].remaining_quantity === 0) {
                  newArr.splice(i, 1);
                  i--;
                }
              }
              this.listNotNull = newArr;
              this.loading = false;
            }
          })
        } else {
          this.$message({
            message: "缺少查询信息",
            type: 'warning'
          });
          this.loading = false;
        }
      },
      getVersion(customer_id) {
        fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_orders/?order_type=1&all=1&customer_id=' + customer_id, null, this).then((res) => {
          if (res && res.status == 200) {
            this.versionData = res.data.data;
            if (this.versionData.length > 0) {
              this.versionInitial = this.versionData[0].fcst_order_id;
//              if (this.versionInitial !== '') {
//                this.getList();
//              }
            } else {
              this.versionInitial = '';
              this.listAll = [];
              this.listNotNull = [];
            }
          }
        })
      },
      // 切换季节
      seasonMethod(seasonMes) {

      },
      // 切换用户
      changeClient(clientCode) {
        this.userValue = clientCode;
        this.getVersion(clientCode);
      },
      // 当前周切换
      newWeekMethod(nowWeek) {
        this.nowWeek = new Date(nowWeek);
      },
      // 切换材料类型
      typeMethod(type) {

      },
      // 备料周期切换
      weekChange(week) {
        this.weekValue = week;
      },
      checkedmethod() {
        console.log(this.checked, 'gg');
        console.log(this.listAll, 1);
        console.log(this.listNotNull, 2);
        if (this.checked === false) {
//          this.arrAll = [];
//          for (let x in this.listAll) {
//            this.arrAll.push(this.listAll[x])
//          }
//          this.toggleSelection(this.arrAll);
        } else if (this.checked === true) {
//          this.arrAll = [];
//          for (let x in this.listNotNull) {
//            this.arrAll.push(this.listNotNull[x])
//          }
//          this.toggleSelection(this.arrAll);
        }
      },
      // 备料
      creatBL(row) {
        var _this = this;
        let current = getYearWeek(this.nowWeek);
        if (this.typevalue === 49) {
          fetchAPI('get', this.$store.state.NEW_API + '/api/mat_models/get_free_size/?model_id=' + row.model.model_id, null, this).then((res) => {
            if (res && res.status === 200) {
              console.log(res.data);
              let arr = [];
              arr.push({
                fcst_pr_item_id: 0,
                item: {
                  item_code: res.data.item_code,
                  item_id: res.data.item_id,
                  item_name: res.data.item_name,
                  extend: {},
                  spec: {},
                  model: row.model,
                },
                spec: {},
                extend: {},
                fcst_pr: 0,
                quantity: row.remaining_quantity,
                disabled: false, //删除状态
                restore: false, // 恢复按钮状态
                addlocal: 0,
                fcst_order_id: _this.versionInitial,
                delivery_date: getweekdate(row.pr_week),
                material_type_meta_id: _this.typevalue,
              });
              arr[0].item.model.unit_meta = row.model.unit_meta;
              _this.postBlData = arr;
              if (_this.postBlData[0].quantity === 0) {
                this.$message({
                  message: "此model无需备料",
                  type: 'warning'
                });
                return;
              } else {
                let newTabName = ++this.chlidTabIndex + '';
                let addChildTABS = {
                  title: '预估备料 - 新增',
                  flag: 1,
                  name: newTabName,
                  closable: true,
                  propdata: _this.postBlData,
                };
                this.chlidTABSValue = newTabName;
                this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
              }
            }
          })
        } else if (this.typevalue === 50) {
          fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/inteligent_item/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial + '&model_id=' + row.model.model_id + '&material_type_meta_id=' + this.typevalue, null, this).then((res) => {
            if (res && res.status === 200) {
              let arr = [];
              let i = 0;
              res.data.forEach(function (item, index) {
                arr.push({
                  fcst_pr_item_id: 0,
                  item: {
                    item_code: item.item.item_code,
                    item_id: item.item.item_id,
                    item_name: item.item.item_name,
                    extend: {},
                    spec: {},
                    model: row.model,
                  },
                  spec: {},
                  extend: {},
                  fcst_pr: 0,
                  quantity: item.remaining_quantity,
                  disabled: false, //删除状态
                  restore: false, // 恢复按钮状态
                  addlocal: 0,
                  fcst_order_id: _this.versionInitial,
                  delivery_date: getweekdate(row.pr_week),
                  material_type_meta_id: _this.typevalue,
                });
                arr[i].item.model.unit_meta = {
                  meta_name: "件"
                };
                _this.postBlData = arr;
                i++;
              });
              for (var j = 0; j < arr.length; j++) {
                if (arr[j].quantity === 0) {
                  arr.splice(j, 1);
                  j--;
                }
              }
            }
            let newTabName = ++this.chlidTabIndex + '';
            let addChildTABS = {
              title: '预估备料 - 新增',
              flag: 1,
              name: newTabName,
              closable: true,
              propdata: _this.postBlData,
            };
            this.chlidTABSValue = newTabName;
            this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
          })
        }
      },
      // 智能备料详情
      detail(row) {
        console.log(row, 11);
        this.lodingview = true;
        this.detailStatus = true;
        let current = getYearWeek(this.nowWeek);
        this.detailList = {};
        let postData = {
          customer_id: this.userValue,
          current: current,
          season_meta_id: this.seasonInitial,
          fcst_order_id: this.versionInitial,
          pr_time: this.weekValue,
          model_id: row.model.model_id,
          material_type_meta_id: this.typeInitial
        };
        fetchAPI('post', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/', postData, this).then((res) => {
          if (res && res.status == 200) {
            this.lodingview = true;
            for (var i = 0; i < res.data[res.data.model.model_id].length; i++) {
              if (res.data[res.data.model.model_id][i].delivery_date < res.data.current_week || res.data[res.data.model.model_id][i].delivery_date > res.data.shipping_weeks[0].shipping_week) {
                res.data[res.data.model.model_id].splice(i, 1);
                i--;
              }
            }
            this.detailList = res.data;
            this.detailList.name = this.commonmethod(row.model);
            this.lodingview = false;
          }
        })
      },
      handleSelectionChange(val) {
        this.selected = val;
      },
      toggleSelection(rows) {
        setTimeout(() => {
          if (rows) {
            rows.forEach(row => {
              this.$refs.multipleTable.toggleRowSelection(row);
            });
          } else {
            this.$refs.multipleTable.clearSelection();
          }
        }, 10)
      },
      getSummaries(param) {
        const {columns, data} = param;
        const sums = [];
        columns.forEach((column, index) => {
          if (index === 0) {
            sums[index] = '汇总';
            return;
          }
          const values = data.map(item => Number(item[column.property]));
          if (!values.every(value => isNaN(value))) {
            sums[index] = values.reduce((prev, curr) => {
              const value = Number(curr);
              if (!isNaN(value)) {
                return prev + curr;
              } else {
                return prev;
              }
            }, 0);
          } else {
            sums[index] = '';
          }
        });
        return sums;
      },
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue === "1") {
//          this.getList();
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
    mounted() {

    },
    created() {
      // 获取用户列表
      fetchAPI('get', this.$store.state.NEW_API + '/api/customer/customers/?all=1', null, this).then((res) => {
        if (res && res.status == 200) {
          for (let item of res.data.data) {
            this.userOption.push(item)
          }
          if (this.userOption.length > 0) {
            this.userValue = this.userOption[0].customer_id;
          } else {
            this.loading = false;
          }
          return fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_orders/?order_type=1&all=1&customer_id=' + this.userValue, null, this)
        }
      }).then((res) => {
        if (res && res.status == 200) {
          this.versionData = res.data.data;
          if (this.versionData.length > 0) {
            this.versionInitial = this.versionData[0].fcst_order_id;
          } else {
            this.versionInitial = '';
            this.listAll = [];
            this.listNotNull = [];
            this.loading = false;
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
            this.loading = false;
          }
          return COMMON.getMetaList(this, 48)
        }
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
    }
//        if (this.userValue !== 0 && this.versionInitial !== '' && this.seasonInitial !== '') {
//          fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial, null, this).then((res) => {
//            if (res && res.status == 200) {
//              this.listAll = res.data;
//              let newArr = JSON.parse(JSON.stringify(res.data));
//              for (var i = 0; i < newArr.length; i++) {
//                if (newArr[i].remaining_quantity === 0) {
//                  newArr.splice(i, 1);
//                  i--;
//                }
//              }
//              this.listNotNull = newArr;
//              let current = getYearWeek(this.nowWeek);
//              let postData = {
//                customer_id: this.userValue,
//                current: current,
//                season_meta_id: this.seasonInitial,
//                fcst_order_id: this.versionInitial,
//                pr_time: this.weekValue,
//                model_id: res.data[0].model.model_id
//              };
//              return fetchAPI('post', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/', postData, this)
//            }
//          }).then((res) => {
//            if (res && res.status == 200) {
//              this.detailList = res.data;
//              this.detailList.name = this.commonmethod(this.listAll[0].model);
//            }
//          })
//        }
//        let current = getYearWeek(this.nowWeek);
//        return fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/?customer_id=' + this.userValue + '&current=' + current + '&pr_time=' + this.weekValue + '&season_meta_id=' + this.seasonInitial + '&fcst_order_id=' + this.versionInitial, null, this)
//      }).then((res) => {
//        if (res && res.status == 200) {
//          this.listAll = res.data;
//          let newArr = JSON.parse(JSON.stringify(res.data));
//          for (var i = 0; i < newArr.length; i++) {
//            if (newArr[i].remaining_quantity === 0) {
//              newArr.splice(i, 1);
//              i--;
//            }
//          }
//          this.listNotNull = newArr;
//          let current = getYearWeek(this.nowWeek);
//          let postData = {
//            customer_id: this.userValue,
//            current: current,
//            season_meta_id: this.seasonInitial,
//            fcst_order_id: this.versionInitial,
//            pr_time: this.weekValue,
//            model_id: res.data[0].model.model_id
//          };
//          return fetchAPI('post', this.$store.state.NEW_API + '/api/newfcst/inteligent_pr/', postData, this)
//        }
//      }).then((res) => {
//        if (res && res.status == 200) {
//          this.detailList = res.data;
//          this.detailList.name = this.commonmethod(this.listAll[0].model);
//        }
//      })
//    }
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

  .clearfix {
    margin-top: 20px;
  }

  .truechange {
    width: 25%;
    text-align: center;
  }

  .el-date-editor.el-input {
    width: 25%;
  }

  .el-select > .el-input {
    width: 100%;
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

  .el-table .cell {
    padding: 0;
    .quantity {
      background: #c9daf8;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .pr_on_line_quantity {
      background: #d9ead3;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .remaining_quantity {
      background: #f4cccc;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
    .arrival_quantity {
      background: #ffd966;
      height: 40px;
      line-height: 40px;
      width: 100%;
    }
  }

  .el-table .cell {
    padding: 0px !important;
  }

  marginstyle {
    margin-bottom: 5px;
  }

  .el-dialog .el-dialog--large {
    min-height: 800px !important;
  }

</style>
