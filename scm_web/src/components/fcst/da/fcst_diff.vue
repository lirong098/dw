<template>
  <div class="forecase_sheet">
    <div class="card_box">
      <div class="card-header card-header-text">
        <h4>
          计算条件
        </h4>
      </div>
      <el-button type="danger" size="" class="button-style" style="position: absolute;right:5%;top: 8px;" @click="getList()">查询
      </el-button>
      <el-card>
        <el-form ref="form" label-width="120px">
          <el-form-item label="客户 :">
            <div class="item"
                 v-for="item in userOption"
                 :key="item.customer_id"
                 @click="changeCustomer(item.customer_id)">
              <el-tag class="eltag"
                      :type="userValue === item.customer_id ? 'success' : 'gray'">
                {{item.customer_name}}
              </el-tag>
            </div>
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
          <el-form-item label="基础版本">
            <el-select v-model="basic_fcst_order_id" placeholder="请选择基础版本" style="width:23%;">
              <el-option
                v-for="item in formData"
                :key="item.fcst_order_id"
                :label="item.fcst_order_no"
                :value="item.fcst_order_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="比较版本">
            <el-select v-model="compare_fcst_order_id" placeholder="请选择比较版本" style="width:23%;">
              <el-option
                v-for="item in compareFromData"
                :key="item.fcst_order_id"
                :label="item.fcst_order_no"
                :value="item.fcst_order_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="比较起始周">
            <el-date-picker v-model="nowWeek"
                            @change="newWeekMethod"
                            type="week"
                            firstDayOfWeek="firstDayOfWeek"
                            format="yyyy-MM-dd(WW周)"
                            disabledDate
                            placeholder="选择周"
                            style="width:23%;">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="比较结束周">
            <el-date-picker v-model="endWeek"
                            @change="endWeekMethod"
                            type="week"
                            firstDayOfWeek="firstDayOfWeek"
                            format="yyyy-MM-dd(WW周)"
                            placeholder="选择周"
                            style="width:23%;">
            </el-date-picker>
          </el-form-item>
          <el-checkbox v-model="is_diff" @change="changeIsDiff()" style="margin-left: 40px;">仅显示差异</el-checkbox>
          <!--<el-form-item label="过滤条件">-->
            <!--<el-checkbox v-model="is_diff_compare">预计预估差异</el-checkbox>-->
            <!--<el-checkbox v-model="is_diff_repeat">预计实单差异</el-checkbox>-->
          <!--</el-form-item>-->
          <!--<el-form-item label="显示角度">-->
          <!--<el-radio-group v-model="radio3">-->
          <!--<el-radio-button label="Model"></el-radio-button>-->
          <!--<el-radio-button label="周期"></el-radio-button>-->
          <!--</el-radio-group>-->
          <!--</el-form-item>-->
          <!--<el-form-item label="仅显示差异">-->
          <!--<el-checkbox v-model="form.resource"></el-checkbox>-->
          <!--</el-form-item>-->
          <!--<el-form-item label="跳转">-->
          <!--<a href="/#/sampleUpload" target="_blank">导入</a>-->
          <!--</el-form-item>-->
        </el-form>
      </el-card>
    </div>

    <div class="card_box">
      <div class="card-header card-header-text">
        <h4>
          {{radio3}}
        </h4>
      </div>
      <el-card>
        <el-table
          :data="tableData"
          v-loading="loading"
          border
          style="width: 100%">
          <el-table-column type="expand" width="70" :key="Math.random()">
            <template scope="scope">
              <el-table :data="scope.row.chirld" border style="margin-top:10px;margin-bottom:10px;width:93.5%;margin-left:6.5%;">
                <el-table-column prop="delivery_date" :key="Math.random()" label="周期"></el-table-column>
                <el-table-column
                  prop="basic_quantity"
                  :key="Math.random()"
                  label="基础版本数">
                </el-table-column>
                <el-table-column
                  prop="compare_quantity"
                  :key="Math.random()"
                  label="比较版本数">
                </el-table-column>

                <el-table-column label="预估差异" :key="Math.random()">
                  <el-table-column
                    prop="diff_compare"
                    :key="Math.random()"
                    label="差异周">
                  </el-table-column>
                  <el-table-column
                    prop="diff_compare_quantity"
                    :key="Math.random()"
                    label="数量">
                  </el-table-column>
                </el-table-column>
                <el-table-column
                  prop="repeat_quantity"
                  :key="Math.random()"
                  label="实单数">
                </el-table-column>
                <el-table-column label="实单差异" :key="Math.random()">
                  <el-table-column
                    prop="diff_repeat"
                    :key="Math.random()"
                    label="差异周">
                  </el-table-column>
                  <el-table-column
                    prop="diff_repeat_quantity"
                    :key="Math.random()"
                    label="数量">
                  </el-table-column>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column prop="date" :key="Math.random()" label="成衣Model">
            <template scope="scope">
              {{scope.row.model_info ? scope.row.model_info.model_code: ''}}
            </template>
          </el-table-column>
          <el-table-column
            prop="basic_total"
            :key="Math.random()"
            label="基础版本数">
          </el-table-column>
          <el-table-column
            prop="compare_total"
            :key="Math.random()"
            label="比较版本数">
          </el-table-column>

          <el-table-column label="预估差异" :key="Math.random()">
            <el-table-column
              prop="diff_compare"
              :key="Math.random()"
              label="差异周">
            </el-table-column>
            <el-table-column
              prop="diff_compare_quantity"
              :key="Math.random()"
              label="数量">
            </el-table-column>
          </el-table-column>
          <el-table-column
            prop="repeat_total"
            :key="Math.random()"
            label="实单数">
          </el-table-column>
          <el-table-column label="实单差异" :key="Math.random()">
            <el-table-column
              prop="diff_repeat"
              :key="Math.random()"
              label="差异周">
            </el-table-column>
            <el-table-column
              prop="diff_repeat_quantity"
              :key="Math.random()"
              label="数量">
            </el-table-column>
          </el-table-column>
        </el-table>

      </el-card>
    </div>

  </div>
</template>
<script>
  //公共组件
  //公共文件
  import showModal from '../../common/messageBox.js';
  import {fetchAPI} from '../../../utils/utils';
  import {getYearWeek} from '../../common/component.js';
  import {getweekdate} from '../../common/component.js';
  import COMMON from '../../common/common.js';

  export default {
    name: 'fcst_diff',
    components: {},
    data() {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        tableName: "预估差异",
        tableType: 1,
        TABS: [
          {
            title: "预估差异",
            name: '1',
            closable: false
          }
        ],
        radio3: "Model",
        id: 0,
        form: {},
        compareFrom: {},//比较版本
        compare_fcst_order_id: '',//比较版本id
        formData: [],//基础版本
        basic_fcst_order_id: '',//基础版本id
        compareFromData: [],
        userOption: [],  // 所有客户
        seasonData: [],  // 季节数据
        seasonInitial: '',
        nowWeek: '',
        endWeek: '',
        // 是否选中预计预估差异
        is_diff: true,
        tableData: [{
          model_info: {
            model_id: 0,
            model_name: '',
            model_code: '',
            spec: {
              color: ''
            }
          },
          basic_total: 0,
          compare_total: 0,
          diff_repeat: 0,
          diff_repeat_quantity: 0,
          diff_compare: 0,
          diff_compare_quantity: 0,
          repeat_total: 0,
          chirld: [{
            delivery_date: '',
            basic_quantity: 0,
            compare_quantity: 0,
            diff_repeat: 0,
            diff_repeat_quantity: 0,
            diff_compare: 0,
            diff_compare_quantity: 0,
            repeat_quantity: 0,
          }]
        }],
        allTableData: [],
        userValue: '',
        loading: false,
      }
    },
    methods: {
      //获取预估订单
      getFormData() {
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/newfcst/fcst_orders/?order_type=1&customer_id='+this.userValue, null, this).then((res) => {
          if (res && res.status === 200) {
            console.log('预估订单', res.data)
            this.formData = res.data.data;
            this.compareFromData = res.data.data;
          }
        })
      },
      // 当前周切换
      newWeekMethod(res) {
//        let helloArray = res.split('-')
//        let week = res.replace(res.substring(0,res.indexOf('(')),'')
//        console.log(week)
//        week = week.replace('(','')
//        week = week.replace(')','')
//        week = week.replace('周','')
//        console.log(week)
//        let nowWeek = parseInt(helloArray['0']+week)
        this.nowWeek = res;
        console.log(this.nowWeek)
      },
      endWeekMethod(res) {
        this.endWeek = res;
      },
      changeCustomer(userValue) {
        this.userValue = userValue
        this.basic_fcst_order_id = ''
        this.compare_fcst_order_id = ''

        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/newfcst/fcst_orders/?order_type=1&customer_id='+this.userValue, null, this).then((res) => {
          if (res && res.status === 200) {
            this.formData = res.data.data;
            this.compareFromData = res.data.data;

            if(this.formData.length > 0) {
              this.basic_fcst_order_id = this.formData[0].fcst_order_id
            }
            if(this.compareFromData.length > 0) {
              this.compare_fcst_order_id = this.compareFromData[0].fcst_order_id
            }
          }
        })
      },
      changeIsDiff() {
        if(this.is_diff) {
          for(let key in this.tableData) {
            if(this.tableData[key].diff_compare === 0 && this.tableData[key].diff_compare_quantity === 0
              && this.tableData[key].diff_repeat === 0 && this.tableData[key].diff_repeat_quantity === 0) {
              this.tableData.splice(key, 1)
            }
          }
        } else {
          this.tableData = JSON.parse(JSON.stringify(this.allTableData))
//          this.getFormData()
        }
      },
      // 切换季节
      seasonMethod(seasonMes) {

      },
      getList() {
        this.loading = true;
        if (!this.endWeek || !this.nowWeek) return this.loading = false;
        const api = this.$store.state.NEW_API;
        let reference = {
          basic_fcst_order_id: this.basic_fcst_order_id,
          compare_fcst_order_id: this.compare_fcst_order_id,
          start_week: this.getYW(this.nowWeek),
          end_week: this.getYW(this.endWeek),
          show_type: 1,
          customer_id: this.userValue,
          season_meta_id: this.seasonInitial
        }
        fetchAPI('put', api + '/api/newfcst/inteligent_pr/', reference, this).then((res) => {
          if (res && res.status === 200) {
            console.log(res);
            this.tableData = res.data
            this.tableData.forEach(row => {

//              row.diff_compare = 0
//              row.diff_compare_quantity = 0
//              row.diff_repeat = 0
//              row.diff_repeat_quantity = 0

              this.tableExpand(row)
            })
            this.allTableData = JSON.parse(JSON.stringify(this.tableData))
            JSON.stringify(this.tableData)
            this.changeIsDiff()
            this.loading = false;
          }
        })

      },
      getYW(res) {
        let helloArray = res.split('-')
        let week = res.replace(res.substring(0, res.indexOf('(')), '')
        week = week.replace('(', '')
        week = week.replace(')', '')
        week = week.replace('周', '')
        let val = parseInt(helloArray['0'] + week)
        return val
      },
      //展开
      tableExpand(row) {
        console.log(row)
        let reference = {
          basic_fcst_order_id: this.basic_fcst_order_id,
          compare_fcst_order_id: this.compare_fcst_order_id,
          start_week: this.getYW(this.nowWeek),
          end_week: this.getYW(this.endWeek),
          show_type: 1,
          model_id: row.model_info.model_id,
          customer_id: this.userValue,
          season_meta_id: this.seasonInitial
        }
        console.log('data', reference)
        const api = this.$store.state.NEW_API;
        fetchAPI('post', api + '/api/newfcst/get_diff_detail/', reference, this).then((res) => {
          if (res && res.status === 200) {
            console.log(res);
            row.chirld = res.data
            console.log(this.tableData)
          }
        })
      }
    },
    created() {
    },
    update() {

    },
    mounted() {
//      this.changeIsDiff()

      fetchAPI('get', this.$store.state.NEW_API + '/api/customer/customers/?all=1', null, this).then((res) => {
        if (res && res.status === 200) {
          for (let item of res.data.data) {
            this.userOption.push(item);
          }
          if (this.userOption.length > 0) {
            this.userValue = this.userOption[0].customer_id;
            this.getFormData();
          }
        }
      })

      COMMON.getMetaList(this, 43).then((res) => {
        if (res && res.status === 200) {
          if (res.data.length > 0) {
            this.seasonData = res.data;
            this.seasonInitial = this.seasonData[0].meta_id;
          } else {
            this.seasonData = [];
            this.seasonInitial = '';
          }
        }
      })
    },
    //计算属性
    computed: {},
    //监听数据变化
    watch: {}
  }
</script>
<style lang="scss" type="text/scss">
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
</style>
