<template>
  <div class="clearfix table_extend">
    <div class="card_box">
      <div class="card-header card-header-text">
        <h4>扩展信息</h4>
      </div>
      <el-card v-if="tableType === 1">
        <el-col class="composition">
          <el-tabs v-model="tabName" type="card">
            <el-tab-pane v-for="(item, index) in extendTabs"
                         :closable="item.closable"
                         :key="item.name"
                         :label="item.title"
                         :name="item.name">
              <template>
                <div class="extendFormDiv" v-show="item.name === 'extend' && tabName === 'extend'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="款号：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.iman_code? extendForm.iman_code.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model="extendForm.iman_code.value" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="MPC：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.mpc_code?extendForm.mpc_code.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model="extendForm.mpc_code.value" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
                <div class="extendFormDiv" v-show="item.name === 'week' && tabName === 'week'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="采购天数：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.po_duration? extendForm.po_duration.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.po_duration.value" type="number" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="生产天数：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.produce_duration?extendForm.produce_duration.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.produce_duration.value" type="number" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="交货天数：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.delivery_duration?extendForm.delivery_duration.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.delivery_duration.value" type="number" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="安全天数：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.safe_duration?extendForm.safe_duration.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.safe_duration.value" type="number" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="裁剪天数：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.cut_produce_duration?extendForm.cut_produce_duration.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.cut_produce_duration.value" type="number" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
                <div class="extendFormDiv" v-show="item.name === 'consume' && tabName === 'consume'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="备料方式：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.pr_method?extendForm.pr_method.value:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model="extendForm.pr_method.value" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="色布比率：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.fabric_ratio?extendForm.fabric_ratio.value+' %':''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.fabric_ratio.value" type="number" v-show="extendChangeStatus">
                          <img  class="png" slot="append" src="/statics/img/baifenhao.png" />
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <div style="width: 99%">
                      <el-col :span="12">
                        <el-form-item label="毛坯比率：" label-width="110px">
                          <el-input class="nochange" v-text="extendForm.rough_ratio?extendForm.rough_ratio.value+' %':''" v-show="!extendChangeStatus"></el-input>
                          <el-input class="truechange" v-model.number="extendForm.rough_ratio.value" type="number" v-show="extendChangeStatus">
                            <img  class="png" slot="append" src="/statics/img/baifenhao.png" />
                          </el-input>
                        </el-form-item>
                      </el-col>
                    </div>
                    <el-col :span="12">
                      <el-form-item label="纱线比率：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.yarn_ratio?extendForm.yarn_ratio.value+' %':''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.yarn_ratio.value" type="number" v-show="extendChangeStatus">
                          <img  class="png" slot="append" src="/statics/img/baifenhao.png" />
                        </el-input>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
                <div class="extendFormDiv" v-show="item.name === 'elastic' && tabName === 'elastic'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="上弹比率：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.elastic_higher_ratio?extendForm.elastic_higher_ratio.value+' %':''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.elastic_higher_ratio.value" type="number" v-show="extendChangeStatus">
                          <img  class="png" slot="append" src="/statics/img/baifenhao.png" />
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="下弹比率：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.elastic_lower_ratio?extendForm.elastic_lower_ratio.value+' %':''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model.number="extendForm.elastic_lower_ratio.value" type="number" v-show="extendChangeStatus">
                          <img  class="png" slot="append" src="/statics/img/baifenhao.png" />
                        </el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="上弹起始周：" label-width="110px" >
                        <el-date-picker
                          v-model="extendForm.elastic_week_start.value"
                          type="week"
                          format="yyyy-MM-dd (WW周)"
                          placeholder="选择周"
                          :disabled="!extendChangeStatus"
                          :picker-options="pickerOptions">
                        </el-date-picker>
                        <!--<dw-date-picker v-model="extendForm.elastic_week_start.value"-->
                                        <!--mode="range"-->
                                        <!--placeholder="选择周"-->
                                        <!--:disabled="!extendChangeStatus"-->
                                        <!--style="width:60%">-->
                        <!--</dw-date-picker>-->
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="上弹结束周：" label-width="110px">
                        <el-date-picker
                          v-model="extendForm.elastic_week_end.value"
                          type="week"
                          format="yyyy-MM-dd (WW周)"
                          placeholder="选择周"
                          :disabled="!extendChangeStatus"
                          :picker-options="pickerOptions">
                        </el-date-picker>
                        <!--<dw-date-picker v-model="extendForm.elastic_week_end.value"-->
                                        <!--mode="range"-->
                                        <!--placeholder="选择周"-->
                                        <!--:disabled="!extendChangeStatus"-->
                                        <!--style="width:60%">-->
                        <!--</dw-date-picker>-->
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
                <div class="extendFormDiv" v-show="item.name === 'delivery' && tabName === 'delivery'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="首单交期周：" label-width="110px">
                        <el-date-picker
                          v-model="extendForm.delivery_week_first.value"
                          type="week"
                          format="yyyy-MM-dd (WW周)"
                          placeholder="选择周"
                          :disabled="!extendChangeStatus"
                          :picker-options="pickerOptions">
                        </el-date-picker>
                        <!--<dw-date-picker v-model="extendForm.delivery_week_first.value"-->
                                        <!--mode="range"-->
                                        <!--placeholder="选择周"-->
                                        <!--:disabled="!extendChangeStatus"-->
                                        <!--style="width:60%">-->
                        <!--</dw-date-picker>-->
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="尾单交期周：" label-width="110px">
                        <el-date-picker
                          v-model="extendForm.delivery_week_last.value"
                          type="week"
                          format="yyyy-MM-dd (WW周)"
                          placeholder="选择周"
                          :disabled="!extendChangeStatus"
                          :picker-options="pickerOptions">
                        </el-date-picker>
                        <!--<dw-date-picker v-model="extendForm.delivery_week_last.value"-->
                                        <!--mode="range"-->
                                        <!--placeholder="选择周"-->
                                        <!--:disabled="!extendChangeStatus"-->
                                        <!--style="width:60%">-->
                        <!--</dw-date-picker>-->
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
              </template>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-card>
      <el-card v-if="tableType !== 1">
        <el-col class="composition">
          <el-tabs v-model="tabName" type="card">
            <el-tab-pane v-for="(item, index) in extendTabs"
                         :closable="item.closable"
                         :key="item.name"
                         :label="item.title"
                         :name="item.name">
              <template>
                <div class="extendFormDiv" v-show="item.name === 'extend' && tabName === 'extend'">
                  <el-form :model="extendForm" ref="extendForm">
                    <el-col :span="12">
                      <el-form-item label="规格：" label-width="110px">
                        <el-input class="nochange" v-text="extendForm.spec? extendForm.spec:''" v-show="!extendChangeStatus"></el-input>
                        <el-input class="truechange" v-model="extendForm.spec" v-show="extendChangeStatus"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-form>
                </div>
              </template>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-card>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'table_extend',
    props: {
      extendForm:Object,
      extendChangeStatus:Boolean,
      tableType: Number
    },
    data() {
      if(this.tableType === 1){
        return {
          extendTabs: [
            {
              title: "扩展信息",
              name: "extend",
              closable: false
            }, {
              title: "周期",
              name: "week",
              closable: false
            }, {
              title: "备料方式",
              name: "consume",
              closable: false
            }, {
              title: "弹性策略",
              name: "elastic",
              closable: false
            }, {
              title: "交期",
              name: "delivery",
              closable: false
            }
          ],
          pickerOptions: { //选择日期数据
            firstDayOfWeek:1,
            showWeekNumber:true
          },
          tabName: "extend",
        }
      }else if(this.tableType !== 1){
        return {
          extendTabs: [
            {
              title: "扩展信息",
              name: "extend",
              closable: false
            }
          ],
          tabName: "extend",
        }
      }

    },
    methods: {
    },
    mounted() {
      console.log(this.tableType)
      console.log("extend",this.extendForm);
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  /*.extendFormDiv{*/
  /*border:1px solid rgb(229, 209, 214);*/
  /*box-shadow:0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);*/
  /*}*/
  .table_extend {
    .truechange {
      width: 60%;
      text-align: center;
    }
    .el-select {
      width: 60%;
      text-align: center;
    }
    .png{
      width: 20px;
      height:20px;
    }
    .el-date-editor--week {
      width: 60%;
    }
  }

</style>
