<template>
  <div class="forecase_sheet">
    <div class="card_box">
      <div class="card-header card-header-text">
        <h4>
          筛选条件
        </h4>
      </div>
      <el-card>
        <div class="header_tool">
          <div class="group">
            <div class="row_select row_select-first">
              <div class="head">品牌</div>
              <div class="body">
                <div class="items">
                  <div class="item" v-for="item in
              customerData" key="item.cust_code"
                       @click="changeCustCode(item.cust_code)">
                    <el-tag :type="currentCustCode ==
                    item.cust_code ? 'success' : 'gray'" >
                      {{item.cust_name}}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
            <div class="row_select">
              <div class="head">原料类型</div>
              <div class="body">
                <div class="items">
                  <div class="item" v-for="item in
              materialsType" key="item.meta_code"
                       @click="changeMaterialsType(item.meta_code)">
                    <el-tag :type="currentMaterialsType ==
                    item.meta_code ? 'success' : 'gray'" >
                      {{item.meta_name}}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
            <div class="row_select">
              <div class="head">周期</div>
              <div class="body">
                <div class="items">
                  <div class="item"
                       @click="changePeroid(0)">
                    <el-tag
                      :type="peroid == '' ? 'success' : 'gray'">ALL
                    </el-tag>
                  </div>
                  <div class="item"
                       @click="changePeroid(16)">
                    <el-tag :type="peroid == 16 ?
                    'success' : 'gray'">16周
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
            <div class="row_select">
              <div class="head">数量显示</div>
              <div class="body">
                <div class="items diff_checkbox">
                  <div class="item prepare3">
                    <el-checkbox
                      v-model="diff.quantity">预计出货数
                    </el-checkbox>
                  </div>
                  <div class="item total">
                    <el-checkbox
                      v-model="diff.imp_quantity">首单实单出货数
                    </el-checkbox>
                  </div>
                  <div class="item curr">
                    <el-checkbox v-model="diff.rep_quantity">翻单实单出货数
                    </el-checkbox>
                  </div>
                  <div class="item diff">
                    <el-checkbox v-model="diff.pre_quantity">预计上线数</el-checkbox>
                  </div>
                  <div class="item prepare">
                    <el-checkbox
                      v-model="diff.pre_imp_quantity">首单实单上线数
                    </el-checkbox>
                  </div>
                  <div class="item prepare1">
                    <el-checkbox
                      v-model="diff.pre_rep_quantity">翻单实单上线数
                    </el-checkbox>
                  </div>
                  <div class="item prepare2">
                    <el-checkbox
                      v-model="diff.pr_quantity">预计到货数
                    </el-checkbox>
                  </div>
                  <div class="item prepare4">
                    <el-checkbox
                      v-model="diff.remain_quantity">剩余数
                    </el-checkbox>
                  </div>
                </div>
              </div>
            </div>
            <div class="row_select">
              <div class="head">model</div>
              <div class="body">
                <div class="items">
                  <div class="item select">
                    <el-select v-model="filterModelCode"
                               filterable
                               @change="changeFilterModel"
                               clearable
                               size="samll"
                               placeholder="选择或输入model进行搜索">
                      <el-option
                        v-for="item in moduleData"
                        :key="item.vcode"
                        :label="item.vcode"
                        :value="item.vcode">
                      </el-option>
                    </el-select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    <div class="body_table">
      <div >
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              预估表
            </h4>
          </div>
          <div class="card-btn-box">
            <div class="select_box">
              <div class="title">备料周</div>
              <el-radio-group
                v-model="createMaterailsWeek"
                @change="changeCreateMaterailsWeek">
                <el-radio :label="1">1周</el-radio>
                <el-radio :label="2">2周</el-radio>
                <el-radio :label="4">4周</el-radio>
              </el-radio-group>
            </div>
            <div class="summit_btn">
              <el-button type="danger"
                         size="small"
                         :disabled="peroid == 0"
                         @click="createMaterails">生成备料单
              </el-button>
            </div>
            <!--<div class="">-->
              <!--<el-popover-->
                <!--ref="popover2"-->
                <!--placement="left"-->
                <!--title="选择备料周"-->
                <!--width="200"-->
                <!--trigger="click">-->
                <!--<div>-->
                  <!--<el-radio-group-->
                    <!--v-model="createMaterailsWeek"-->
                    <!--@change="changeCreateMaterailsWeek">-->
                    <!--<el-radio :label="1">1周</el-radio>-->
                    <!--<el-radio :label="2">2周</el-radio>-->
                    <!--<el-radio :label="4">4周</el-radio>-->
                  <!--</el-radio-group>-->
                <!--</div>-->
                <!--<div class="footer_btn">-->
                  <!--<el-button type="danger"-->
                             <!--size="small"-->
                             <!--@click="createMaterails">确定-->
                  <!--</el-button>-->
                <!--</div>-->
              <!--</el-popover>-->
              <!--<el-button type="info"-->
                         <!--v-popover:popover2-->
                         <!--:disabled="peroid == 0">生成备料单-->
              <!--</el-button>-->
            <!--</div>-->
          </div>
          <lazy-render>
            <el-card>
              <el-table  :data="filterModuleData"
                         v-loading.body="loading"
                         border
                         :default-sort="defaultSort"
                         :height="tabHeight">
                <el-table-column
                  fixed
                  width="55">
                  <template scope="scope">
                    <div v-show="scope.row.is_module">
                      <el-checkbox @change="selectModel(scope.$index, scope.row)"
                                   v-model="scope.row.select"></el-checkbox>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column width="70" fixed>
                  <template scope="scope">
                    <div class="expand_icon" v-show="scope.row.is_module" @click="handleExpand(scope.$index, scope.row)">
                      <el-icon :name="scope.row.module_expand_flag ? 'arrow-down' : 'arrow-right'"></el-icon>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="vcode" label="model"
                                 fixed min-width="150">
                  <template scope="scope">
                    <span :title="scope.row.vname">{{
                      scope.row.vcode}}</span>
                  </template>
                </el-table-column>
                <el-table-column :key="peroid"
                                 class-name="forecase_column"
                                 :label="peroid.indexOf('<') != -1 ? '<' + peroid.slice(3) : peroid.slice(2)"
                                 v-for="peroid in
                                 modulePeroid">
                  <template scope="scope">
                    <div
                      :class="scope.row.prDate.indexOf(peroid) != -1 ?
                       'remain_column' : ''"
                      v-show="scope.row[scope.row.inner_code+'_'+peroid]">
                      <div>
                        <span v-show="diff.quantity"
                              class="prepare3_color">
                        {{scope.row[scope.row.inner_code+'_'+peroid] && scope.row[scope.row.inner_code+'_'+peroid].quantity}}
                        <br>
                      </span>
                        <span v-show="diff.imp_quantity"
                              class="total_color">
                        {{scope.row[scope.row.inner_code+'_'+peroid] && scope.row[scope.row.inner_code+'_'+peroid].imp_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.rep_quantity"
                              class="curr_color">
                        {{scope.row[scope.row.inner_code+'_'+peroid] && scope.row[scope.row.inner_code+'_'+peroid].rep_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.pre_quantity"
                              class="diff_color">
                        {{scope.row[scope.row.inner_code+'_'+peroid] && scope.row[scope.row.inner_code+'_'+ peroid].pre_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.pre_imp_quantity"
                              class="prepare_color">
                        {{scope.row[scope.row.inner_code+'_'+ peroid] && scope.row[scope.row.inner_code+'_'+ peroid].pre_imp_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.pre_rep_quantity"
                              class="prepare1_color">
                        {{scope.row[scope.row.inner_code+'_'+ peroid] && scope.row[scope.row.inner_code+'_'+ peroid].pre_rep_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.pr_quantity"
                              class="prepare2_color">
                        {{scope.row[scope.row.inner_code+'_'+ peroid] && scope.row[scope.row.inner_code+'_'+ peroid].pr_quantity}}
                        <br>
                      </span>
                        <span v-show="diff.remain_quantity"
                              class="prepare4_color">
                        {{scope.row[scope.row.inner_code+'_'+ peroid] && scope.row[scope.row.inner_code+'_'+ peroid].remain_quantity}}
                      <br>
                      </span>
                      </div>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </lazy-render>
        </div>
      </div>
    </div>
    <el-dialog
      title="已生成备料单"
      class="diff_dialog"
      :visible.sync="isShowMaterials"
      size="small">
      <div class="materials_content">
        <div>
          <div class="group">
            <div class="row_select row_select-first"
                 v-for="(item,index) in materialsOrderData">
              <div class="head">

              </div>
              <div class="body">
                <div class="items">
                  <div class="item">
                    <b>{{item.vcode}}</b>
                    <span class="arrow">
                      <el-icon
                        name="d-arrow-right"></el-icon>
                    </span>
                    <span class="item_content">
                      <b>{{item.fcst_pr_no}}</b>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="isShowMaterials = false">确认</el-button>
      </span>
    </el-dialog>

  </div>
</template>
<script>
  import {fetchAPI} from '../../utils/utils';
  export default {
    data() {
      return {
        customerData:[],
        materialsType:[],
        currentCustCode:'',
        currentMaterialsType:'',
        modulePeroid:[],
        tableDatas:[],
        moduleData:[],
        filterModuleData:[],
        filterModelCode:'',
        loading:false,
        selectModels:{},
        currentTab:'main',
        TABS:[],
        tabIndex:1,
        peroid:16,
        diff:{
          quantity:false,
          imp_quantity:false,
          rep_quantity:false,
          pre_quantity:true,
          pre_imp_quantity:true,
          pre_rep_quantity:true,
          pr_quantity:true,
          remain_quantity:true,
        },
        materialsOrderData:null,
        isShowMaterials:false,
        createMaterailsWeek:1,
        defaultSort:{
          prop:'vcode',
          order:'ascending'
        }
      }
    },
    created(){
      this.getCustomerData();
    },
    computed: {
      tabHeight(){
       return (this.filterModuleData.length + 1) * 130
       >630 ? 630 : (this.filterModuleData.length +
         1) * 130 ;
      }
    },
    methods:{
      unique:function(arr){
        let res = [];
        let json = {};
        for(let i = 0; i < arr.length; i++){
          if(!json[arr[i]]){
            res.push(arr[i]);
            json[arr[i]] = 1;
          }
        }
        return res;
      },
      getCustomerData:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/custom/custominfolist/',null,this).then((res) => {
          if(res && res.status == 200){
            this.customerData = res.data;
            this.currentCustCode = res.data[0] ?
            res.data[0].cust_code : '';
            this.getMaterialsType();
          }
        })
      },
      getMaterialsType:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api + '/api/dict/meta/materials/',null,this).then((res) => {
          if (res && res.status == 200) {
            this.materialsType = res.data;
            this.currentMaterialsType = res.data[0] ?
              res.data[0].meta_code : '';
            this.getModelEst();
          }
        })
      },
      changeCustCode:function (cust_code){
        this.selectModels = {};
        this.currentCustCode = cust_code;
        this.getModelEst();
      },
      changeMaterialsType:function (meta_code) {
        this.selectModels = {};
        this.currentMaterialsType = meta_code;
        this.getModelEst();
      },
      changePeroid:function (peroid) {
        this.selectModels = {};
        this.peroid = peroid;
        this.getModelEst();
      },
      changeFilterModel:function (val) {
        if(val){
          let flag = false;
          let obj = null;
          for(let item in this.moduleData){
            if(this.moduleData[item].vcode === val){
              flag = true;
              obj = this.moduleData[item];
              break
            }
          }
          if(flag){
            this.filterModuleData = [].concat(obj);
          }else{
            this.filterModuleData.splice(0);
          }
        }else{
          this.filterModuleData = this.moduleData.slice();
        }
      },
      getModelEst:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcst/fcst_est_carry_models/?cust_code='+this.currentCustCode+'&material_type_meta='+this.currentMaterialsType,null,this).then(est => {
           if(est && est.status == 200){
             this.moduleData.length = 0;
             this.filterModuleData.length = 0;
             this.loading = true;
             const api = this.$store.state.DEV_API;
             fetchAPI('get',api +
               '/api/fcst/fcst_est_models/?cust_code='+this.currentCustCode+'&weeks='+this.peroid+'&material_type_meta='+this.currentMaterialsType,null,this).then(res => {
               if (res && res.status == 200) {
                 this.createMaterailsWeek = 1;
                 let data = res.data;
                 let moduleCode = [];
                 this.modulePeroid.length = 0;
                 for (let item of data) {
                   this.modulePeroid.push(item.delivery_date);
                   moduleCode.push(item.inner_code);
                 }
                 moduleCode = this.unique(moduleCode).slice();
                 this.modulePeroid = this.unique(this.modulePeroid).slice();
                 this.modulePeroid.sort();
                 for (let i in moduleCode) {
                   let obj = {};
                   obj.inner_code = moduleCode[i];
                   obj.module_expand_num = 0;
                   obj.module_expand_flag = false;
                   obj.is_module = true;
                   obj.select = false;
                   for (let item of data) {
                     if (item.inner_code == moduleCode[i]) {
                       obj[item.inner_code + '_' + item.delivery_date] = {};
                       obj[item.inner_code + '_' +
                       item.delivery_date]['quantity'] =
                         typeof item.quantity === 'number'?
                           item.quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['imp_quantity'] = typeof item.imp_quantity === 'number' ? item.imp_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['rep_quantity'] = typeof item.rep_quantity === 'number' ? item.rep_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['pre_quantity'] = typeof item.pre_quantity === 'number' ? item.pre_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['pre_imp_quantity'] = typeof item.pre_imp_quantity === 'number' ? item.pre_imp_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['pre_rep_quantity'] = typeof item.pre_rep_quantity === 'number' ? item.pre_rep_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['pr_quantity'] = typeof item.pr_quantity === 'number' ? item.pr_quantity : '-';
                       obj[item.inner_code + '_' +
                       item.delivery_date]['remain_quantity'] = typeof item.remain_quantity === 'number' ? item.remain_quantity : '-';
                       if (!obj.vcode) {
                         obj.vcode = item.code;
                       }
                       if (!obj.vname) {
                         obj.vname = item.name;
                       }
                       if (!obj.prDate) {
                         obj.prDate = [];
                         obj.prDate.push(item.pr_date);
                       }
                       if(est.data[obj.inner_code] && !obj[obj.inner_code + '_' +est.data[obj.inner_code].delivery_date]) {//有结转
                         obj[obj.inner_code + '_' + est.data[obj.inner_code].delivery_date] = {};
                         obj[obj.inner_code + '_' +
                         est.data[obj.inner_code].delivery_date]['pr_quantity'] = typeof est.data[obj.inner_code].pr_quantity == 'number' ? est.data[obj.inner_code].pr_quantity : '-';
                         obj[obj.inner_code + '_' +
                         est.data[obj.inner_code].delivery_date]['remain_quantity'] = typeof est.data[obj.inner_code].remain_quantity == 'number' ? est.data[obj.inner_code].remain_quantity : '-';
                       }
                     }
                   }
                   this.moduleData.push(obj);
                 }
                 let estData = Object.keys(est.data);
                 if(estData.length){
                   let inner_code = estData[0];
                   this.modulePeroid.unshift(est.data[inner_code].delivery_date);
                 }
                 this.changeFilterModel(this.filterModelCode);
//                 this.filterModuleData = this.moduleData.slice();
               }
               this.loading = false;
             })
           }
        });
      },
      getItemEst:function (inner_code,prDate) {
        const api = this.$store.state.DEV_API;
        return fetchAPI('get',api +
          '/api/fcst/fcst_est_carry_items/?model_inner_code='+inner_code+'&material_type_meta='+this.currentMaterialsType,null,this).then(est => {
          return fetchAPI('get',api  +
            '/api/fcst/fcst_est_items/?model_inner_code=' +
            inner_code+'&weeks='+this.peroid+'&cust_code='+this.currentCustCode+'&material_type_meta='+this.currentMaterialsType,null,this).then(res => {
            if(res && res.status == 200){
              let expandData = [];
              let data =  res.data;
              let itemCode = [];
              for(let item of data){
                itemCode.push(item.inner_code);
              }
              itemCode = this.unique(itemCode).slice();
              for(let i in itemCode){
                let obj = {};
                obj.inner_code = itemCode[i];
                obj.is_module = false;
                obj.select = false;
                for(let item of data){
                  if(item.inner_code == itemCode[i]){
                    obj[item.inner_code+'_'+item.delivery_date] = {};
                    obj[item.inner_code+'_'+item.delivery_date]['quantity'] = typeof item.quantity === 'number' ? item.quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['imp_quantity'] = typeof item.imp_quantity === 'number' ? item.imp_quantity: '-';
                    obj[item.inner_code+'_'+item.delivery_date]['rep_quantity'] = typeof item.rep_quantity === 'number' ? item.rep_quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['pre_quantity'] = typeof item.pre_quantity === 'number' ? item.pre_quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['pre_imp_quantity'] = typeof item.pre_imp_quantity === 'number' ? item.pre_imp_quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['pre_rep_quantity'] = typeof item.pre_rep_quantity === 'number' ? item.pre_rep_quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['pr_quantity'] = typeof item.pr_quantity === 'number' ? item.pr_quantity : '-';
                    obj[item.inner_code+'_'+item.delivery_date]['remain_quantity'] = typeof item.remain_quantity === 'number' ? item.remain_quantity : '-';
                    if(!obj.vcode){
                      obj.vcode = item.name;
                    }
                    if(!obj.vname){
                      obj.vname = item.code;
                    }
                    if(!obj.prDate){
                      obj.prDate = [].concat(prDate)
                    }
                    if(est.data[obj.inner_code] && !obj[obj.inner_code + '_' +est.data[obj.inner_code].delivery_date]) {//有结转
                      obj[obj.inner_code + '_' + est.data[obj.inner_code].delivery_date] = {};
                      obj[obj.inner_code + '_' +
                      est.data[obj.inner_code].delivery_date]['pr_quantity'] = typeof est.data[obj.inner_code].pr_quantity === 'number' ? est.data[obj.inner_code].pr_quantity : '-';
                      obj[obj.inner_code + '_' +
                      est.data[obj.inner_code].delivery_date]['remain_quantity'] = typeof est.data[obj.inner_code].remain_quantity == 'number' ? est.data[obj.inner_code].remain_quantity : '-';
                    }
                  }
                }
                expandData.push(obj);
              }
              return expandData
            }
          })
        });
      },
      getModuleList:function () {
        this.moduleData.length = 0;
        this.filterModuleData.length = 0;
        this.loading = true;
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/fcst/fcst_est_models/?cust_code='+this.currentCustCode+'&weeks='+this.peroid,null,this).then(res => {
          if(res &&res.status == 200){
            let data = res.data;
            let moduleCode = [];
            this.modulePeroid = {};
            for(let item of data){
              this.modulePeroid[item.delivery_date] = item;
              moduleCode.push(item.inner_code);
            }
            moduleCode = this.unique(moduleCode).slice();
            for(let i in moduleCode){
              let obj = {};
              obj.inner_code = moduleCode[i];
              obj.module_expand_num = 0;
              obj.module_expand_flag = false;
              obj.is_module = true;
              obj.select = false;
              for(let item of data){
                if(item.inner_code == moduleCode[i]){
                  obj[item.inner_code+'_'+item.delivery_date] = {};
                  obj[item.inner_code+'_'+item.delivery_date]['quantity'] = item.quantity ? item.quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['imp_quantity'] = item.imp_quantity ? item.imp_quantity: '0';
                  obj[item.inner_code+'_'+item.delivery_date]['rep_quantity'] = item.rep_quantity ? item.rep_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_quantity'] = item.pre_quantity ? item.pre_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_imp_quantity'] = item.pre_imp_quantity ? item.pre_imp_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_rep_quantity'] = item.pre_rep_quantity ? item.pre_rep_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pr_quantity'] = item.pr_quantity ? item.pr_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['remain_quantity'] = item.remain_quantity ? item.remain_quantity : '0';
                  if(!obj.vcode){
                    obj.vcode = item.code;
                  }
                  if(!obj.vname){
                    obj.vname = item.name;
                  }
                  if(!obj.prDate){
                    obj.prDate = [];
                    obj.prDate.push(item.pr_date);
                  }
                }
              }
              this.moduleData.push(obj);
            }
            this.filterModuleData = this.moduleData.slice();
          }
          this.loading = false;
        })
      },
      getItemList:function (inner_code,prDate) {
        const api = this.$store.state.DEV_API;
        return fetchAPI('get',api  +
          '/api/fcst/fcst_est_items/?model_inner_code=' +
          inner_code+'&weeks='+this.peroid+'&cust_code='+this.currentCustCode,null,this).then(res => {
          if(res && res.status == 200){
            let expandData = [];
            let data =  res.data;
            let itemCode = [];
            for(let item of data){
              itemCode.push(item.inner_code);
            }
            itemCode = this.unique(itemCode).slice();
            for(let i in itemCode){
              let obj = {};
              obj.inner_code = itemCode[i];
              obj.is_module = false;
              obj.select = false;
              for(let item of data){
                if(item.inner_code == itemCode[i]){
                  obj[item.inner_code+'_'+item.delivery_date] = {};
                  obj[item.inner_code+'_'+item.delivery_date]['quantity'] = item.quantity ? item.quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['imp_quantity'] = item.imp_quantity ? item.imp_quantity: '0';
                  obj[item.inner_code+'_'+item.delivery_date]['rep_quantity'] = item.rep_quantity ? item.rep_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_quantity'] = item.pre_quantity ? item.pre_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_imp_quantity'] = item.pre_imp_quantity ? item.pre_imp_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pre_rep_quantity'] = item.pre_rep_quantity ? item.pre_rep_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['pr_quantity'] = item.pr_quantity ? item.pr_quantity : '0';
                  obj[item.inner_code+'_'+item.delivery_date]['remain_quantity'] = item.remain_quantity ? item.remain_quantity : '0';
                  if(!obj.vcode){
                    obj.vcode = item.name;
                  }
                  if(!obj.vname){
                    obj.vname = item.code;
                  }
                  if(!obj.prDate){
                    obj.prDate = [].concat(prDate)
                  }
                }
              }
              expandData.push(obj);
            }
            return expandData
          }
        })
      },
      handleExpand:function (index,row) {
        let flag = this.filterModuleData[index].module_expand_flag;
        if(this.filterModuleData[index].module_expand_flag){//要折叠
          this.filterModuleData.splice(index+1,this.filterModuleData[index].module_expand_num);
        }else{//要展开
          this.getItemEst(row.inner_code,row.prDate).then((expandData) => {
            this.filterModuleData[index].module_expand_num = expandData.length;
            this.filterModuleData.splice(index+1,0,...expandData);
          });
        }
        this.filterModuleData[index].module_expand_flag = !flag;
      },
      selectModel:function (index,row) {
        if(row.select){
            this.selectModels[row.inner_code] = row;
        }else{
            delete this.selectModels[row.inner_code];
        }
      },
      createMaterails:function () {
        if(Object.keys(this.selectModels).length){
          const api = this.$store.state.DEV_API;
          let data = {};
          let obj = [];
          for(let item in this.selectModels) {//inner_code
            obj.push(this.selectModels[item].inner_code);
          }
          data.cust_code = this.currentCustCode;
          data.model_inner_code = obj;
          data.weeks = this.createMaterailsWeek;
          data.material_type_meta = this.currentMaterialsType;
          fetchAPI('post',api + '/api/fcstpr/est2pr/',data,this).then((res) => {
            if(res && res.status == 200){
              this.materialsOrderData = {};
              for(let i in this.selectModels){
                let inner_code = this.selectModels[i].inner_code;
                this.materialsOrderData[inner_code] = {};
                let vcode = this.selectModels[i].vcode;
                if(res.data[inner_code]){//生成
                  res.data[inner_code].vcode = vcode;
                  this.materialsOrderData[inner_code] = res.data[inner_code];
                }else{//已备足
                  let obj = {};
                  obj.fcst_pr_no = '已备足';
                  obj.vcode = vcode;
                  this.materialsOrderData[inner_code] = obj;
                }
              }
              this.selectModels = {};
              this.getModelEst();
//              this.filterModelCode = '';
              this.isShowMaterials = true;
            }
          });
        }else{
          this.$message({
            message: '请选择Model',
            type: 'warning'
          });
        }
      },
      changeCreateMaterailsWeek:function (val) {
        for(let i in this.filterModuleData){
          this.filterModuleData[i].prDate.splice(1);
          let num =
            Number(this.filterModuleData[i].prDate[0]);
          if(val == 2){
            this.filterModuleData[i].prDate.push(num +
              1 + '');
          }else if(val == 4){
            this.filterModuleData[i].prDate.push(num + 1
              + '');
            this.filterModuleData[i].prDate.push(num + 2
              + '');
            this.filterModuleData[i].prDate.push(num + 3
              + '');
          }
        }
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .footer_btn{
    text-align: right;
    margin-top: 5px;
  }
  .card-btn-box{
    position: absolute;
    top:-52px;
    right:0px;
    z-index: 1;
    background: #fff;
    padding: 10px;
    box-shadow: 0 4px 20px 0px rgba(0, 0, 0, 0.14), 0 7px
    10px -5px #ddd;
    border-radius: 3px;
    .select_box{
      padding-bottom: 3px;
      .title{
        color:#aaa;
        font-size: 12px;
        padding-bottom: 3px;
      }
    }
    .summit_btn{
      text-align: right;
    }
  }
  .forecase_sheet{
    padding:20px 10px 10px 10px;
    .header_tool{
      margin-bottom: 10px;
      .title{
        color: #999;
        margin-bottom: 2px;
      }
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
            padding:0 100px 0 112px;
            .items{
              min-height: 36px;
              overflow: hidden;
              .item{
                float: left;
                margin: 9px 10px 9px 0;
                height: 18px;
                color: #000;
                cursor: pointer;
                &.select{
                  margin: 0;
                }
              }
            }
          }
        }
      }
    }
    .body_table{
      .opt_btn{
        padding-bottom: 2px;
        margin: 20px 0;
      }
      .expand_icon{
        width: 100%;
        height:100%;
        cursor: pointer;
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
                  margin: 0 15px;
                }
                .item_content{
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
