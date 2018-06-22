<template>
  <div class="productinfo_edit_contain">
    <div class="productinfo_edit_main">
      <el-form :model="editProductData"
               class="demo-form-inline" label-width="110px"
               :rules="modelRules"
               ref="modelForm">
        <div class="clearfix">
          <div class="fl main-card-box">
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  Model
                </h4>
              </div>
              <el-card class="split-card">
                <el-form-item label="客户"
                              prop="cust_info">
                  <el-select
                    v-model="editProductData.cust_info"
                    placeholder="请选择" >
                    <el-option
                      label=""
                      value="">
                      <div class="select_add" @click="addCustomer">
                        <el-icon name="plus"></el-icon>
                        <span>新增</span>
                      </div>
                    </el-option>
                    <el-option
                      v-for="cust in customerData"
                      :key="cust.cust_code"
                      :label="cust.cust_name"
                      :value="cust.cust_code">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="Model Code" prop="model_code">
                  <div class="edit_produc_input">
                    <el-input
                      v-if="!editProductData.model_inner_code"
                      :maxlength="50"
                      v-model="editProductData.model_code"
                      placeholder="Model Code"></el-input>
                    <span
                      v-if="editProductData.model_inner_code">
                      <el-tag type="danger"> {{editProductData.model_code}}</el-tag>
            </span>
                  </div>
                </el-form-item>
                <el-form-item label="Model Name" prop="model_name">
                  <div class="edit_produc_input">
                    <el-input
                      v-model="editProductData.model_name"
                      placeholder="Model Name"></el-input>
                  </div>
                </el-form-item>
                <el-form-item label="Iman Code">
                  <div class="edit_produc_input">
                    <el-input
                      v-model="editProductData.iman_code"  placeholder="Iman Code"  ></el-input>
                  </div>
                </el-form-item>
                <el-form-item label="Mpc Code">
                  <div class="edit_produc_input">
                    <el-input
                      v-model="editProductData.mpc_code"
                      placeholder="Mpc Code"  ></el-input>
                  </div>
                </el-form-item>
              </el-card>
            </div>
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  周期参数
                </h4>
              </div>
              <el-card class="split-card">
                <el-form :inline="true" label-width="105px">
                  <el-form-item label="采购天数"
                                prop="po_duration">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.po_duration" :min="0"></el-input-number>
                  </el-form-item>
                  <el-form-item label="生产天数"
                                prop="produce_duration">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.produce_duration" :min="0"></el-input-number>
                  </el-form-item>
                  <el-form-item label="送货天数"
                                prop="delivery_duration">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.delivery_duration" :min="0"></el-input-number>
                  </el-form-item>
                  <el-form-item label="安全天数"
                                prop="safe_duration">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.safe_duration" :min="0"></el-input-number>
                  </el-form-item>
                  <el-form-item label="裁剪天数"
                                prop="cut_produce_duration">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.cut_produce_duration" :min="0"></el-input-number>
                  </el-form-item>
                </el-form>
              </el-card>
            </div>
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  其它
                </h4>
              </div>
              <el-card class="split-card">
                <el-form :inline="true"
                         label-width="105px"
                         class="model_info_form">
                  <el-form-item
                    :label="editProductData.extend.elastic_lower_ratio.name">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.extend.elastic_lower_ratio.value" :min="0" :max="100"></el-input-number>
                    <i
                      class="icon icon24 icon_percent"></i>
                  </el-form-item>
                  <el-form-item
                    :label="editProductData.extend.elastic_higher_ratio.name">
                    <el-input-number
                      :controls="false"
                      v-model="editProductData.extend.elastic_higher_ratio.value" :min="0" :max="100"></el-input-number>
                    <i
                      class="icon icon24 icon_percent"></i>
                  </el-form-item>
                  <el-form-item :label="editProductData.extend.elastic_week_start.name">
                    <el-date-picker
                      v-model="editProductData.extend.elastic_week_start.value"
                      type="week"
                      format="yyyy 第 WW 周"
                      :editable="false" :clearable="false"
                      placeholder="选择周">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item
                    :label="editProductData.extend.elastic_week_end.name">
                    <el-date-picker
                      v-model="editProductData.extend.elastic_week_end.value"
                      type="week"
                      format="yyyy 第 WW 周"
                      :editable="false" :clearable="false"
                      placeholder="选择周">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item
                    :label="editProductData.extend.delivery_week_first.name">
                    <el-date-picker
                      v-model="editProductData.extend.delivery_week_first.value"
                      type="week"
                      format="yyyy 第 WW 周"
                      :editable="false" :clearable="false"
                      placeholder="选择周">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item
                    :label="editProductData.extend.delivery_week_last.name">
                    <el-date-picker
                      v-model="editProductData.extend.delivery_week_last.value"
                      type="week"
                      format="yyyy 第 WW 周"
                      :editable="false" :clearable="false"
                      placeholder="选择周">
                    </el-date-picker>
                  </el-form-item>
                  <div>
                    <el-form-item
                      class="ratio_input"
                      :label="editProductData.extend.fabric_ratio.name">
                      <el-input-number
                        :controls="false"
                        v-model="editProductData.extend.fabric_ratio.value" :min="0" :max="100"></el-input-number>
                      <i
                        class="icon icon24 icon_percent"></i>
                    </el-form-item>
                    <el-form-item
                      class="ratio_input"
                      :label="editProductData.extend.rough_ratio.name">
                      <el-input-number
                        :controls="false"
                        v-model="editProductData.extend.rough_ratio.value" :min="0" :max="100">
                      </el-input-number>
                      <i
                        class="icon icon24 icon_percent"></i>
                    </el-form-item>
                    <el-form-item
                      class="ratio_input"
                      :label="editProductData.extend.yarn_ratio.name">
                      <el-input-number
                        :controls="false"
                        v-model="editProductData.extend.yarn_ratio.value" :min="0" :max="100"></el-input-number>
                      <i
                        class="icon icon24 icon_percent"></i>
                    </el-form-item>
                  </div>
                  <el-form-item
                    :label="editProductData.extend.pr_method.name">
                    <el-select
                      v-model="editProductData.extend.pr_method.value" placeholder="请选择">
                      <el-option
                        v-for="item in materialsType"
                        :key="item"
                        :label="item"
                        :value="item">
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-form>
              </el-card>
            </div>
          </div>
          <div class="fr opt-btn-box">
            <el-card class="extra_card">
              <el-button type="primary"
                         @click="saveEdit('modelForm')">保存
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button @click="addItem('')" type="info"
                         :disabled="!editProductData.model_inner_code">添加Item
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button @click="deleteModel" type="danger"
                         :disabled="!editProductData.model_inner_code">删除
              </el-button>
            </el-card>
          </div>
        </div>
        <div class="main-card-box paddingTop00" v-if="items
         &&
        items.length">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Item
              </h4>
            </div>
            <el-card>
              <el-table
                :data="items"
                class="item_table_hack"
                style="width: 100%">
                <el-table-column
                  prop="item_code"
                  label="ItemCode">
                  <template scope="scope">
                    <el-input @blur="changeItem(scope.$index,'itemForm_'+scope.$index)"
                              v-model="scope.row.item_code"
                              :maxlength="50"
                              size="small"
                              placeholder="Item Code"></el-input>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="item_name"
                  width="300px"
                  label="ItemName">
                  <template scope="scope">
                    <el-input @blur="changeItem(scope.$index,'itemForm_'+scope.$index)"
                              v-model="scope.row.item_name"
                              class="model_item_column_width"
                              :maxlength="50"
                              size="small"
                              placeholder="Item Name"></el-input>
                    <span class="icon_content"  v-show="scope.row.type == 'ok'">
                      <i class="icon icon16 icon_correct"></i>
                    </span>
                        <span class="icon_content" v-show="scope.row.type == 'no'">
                      <i class="icon icon16 icon_error"></i>
                    </span>
                  </template>
                </el-table-column>
                <el-table-column
                  width="80"
                  fixed="right"
                  label="操作">
                  <template scope="scope">
                    <el-button-group>
                      <el-button type="danger"
                                 size="small"
                                 @click="deleteItem(scope.$index)">删除</el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </div>
      </el-form>
    </div>
  </div>
</template>
<script>
  import {fetchAPI,checCode} from '../../utils/utils';
  export default{
    name: 'product-info-edit',
    props:{
      editProduct:{
        type:Object
      },
      customerData:{
        type:Array
      },
      currentTab:{
          type:String
      },
      currentCust:{

      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        editProductData:Object.assign({},this.editProduct),
        parentCustCode:this.editProduct.cust_info,
        items:[],
        itemRules:{
          item_code:[
            { required: true, message: 'Item Code必填',  trigger: 'blur' },
            {validator:checCode,trigger: 'blur'}
          ],
          item_name:[
            { required: true, message: 'Item Name必填',  trigger: 'blur' }
          ]
        },
        modelRules:{
          cust_info:[
            { required: true, message: '请选择用户', trigger:   'change' }
          ],
          model_code:[
            { required: true, message: 'Model Code必填',  trigger: 'blur' },
            {validator:checCode,trigger: 'blur'}
          ],
          model_name:[
            { required: true, message: 'Model Name必填',  trigger: 'blur' },
          ],
          po_duration_weeks:[
            { required: true, message: '采购周期必填',  trigger: 'blur' },
          ],
          produce_duration_weeks:[
            { required: true, message: '生产周期必填',  trigger: 'blur' }
          ],
        },
        materialsType:['FG AUTO/CPT CBA','FG AUTO/CPT MAX','FULL LT']
      }
    },
    computed:{

    },
    created() {
      this.getitems();
    },
    methods: {
      getitems:function () {
        if(this.optType == 'addProduct' ){
          return false
        }
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/product/items/?model_inner_code=' +
          this.editProductData.model_inner_code,null,this).then((res) => {
          if(res && res.status == 200 ){
            this.items = res.data;
          }
        })
      },
      addCustomer:function () {
        let data = {
          type:'addCustomer',
          data:{
            addresses:[],
            contacts:[],
            cust_code:'',
            cust_name:'',
            extend:'',
            parent_cust_code:'',
            parent_currentTab:this.currentTab,
          }
        };
        this.$emit('changeTabs',data);
      },
      addItem:function (index) {
        let modelitem = {
          item_code:'',
          item_name:'',
          model_info:'',
          extend:null
        };
        if(this.items && this.items.length){
          if(index === ''){
            this.items.push(modelitem);
          }else{
            index++;
            this.items.splice(index,0,modelitem);
          }
        }else{
          let arr = [modelitem];
          this.items = arr.slice();
        }
      },
      changeItem:function (index,formName) {
        const api = this.$store.state.DEV_API;
        if(this.editProductData.model_inner_code){
          let obj = {
            item_code: this.items[index].item_code,
            item_name: this.items[index].item_name,
            extend: null,
            model_info: this.editProductData.model_inner_code
          };
          if(this.items[index].item_inner_code){//修改
            obj.item_inner_code = this.items[index].item_inner_code;
            fetchAPI('put',api + '/api/product/item/?item_inner_code='+this.items[index].item_inner_code,obj,this).then((res) => {
              if(res && res.status == 200){
                this.$set(this.items[index], 'type','ok') ;
              }else{
                this.$set(this.items[index],'type','no') ;
              }
            });
          }else{//新增
            fetchAPI('post',api +  '/api/product/items/',obj,this).then((res) => {
              if(res && res.status == 201){
                this.$set(this.items[index],'item_inner_code',res.data.item_inner_code) ;
                this.$set(this.items[index], 'type','ok') ;
              }else{
                this.$set(this.items[index],'type','no') ;
              }
            })
          }
        }else{//无model
          this.$message({
            message: '请先保存Model',
            type: 'warning'
          });
        }
      },
      deleteItem:function (index) {
        if(this.items[index].item_inner_code){//后台删
          this.$confirm('确认删除吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const api = this.$store.state.DEV_API;
            fetchAPI('delete',api +
              '/api/product/item/?item_inner_code='+this.items[index].item_inner_code,null,this).then((res) => {
              if(res && res.status == 204){
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
                this.items.splice(index,1);
              }
            })
          }).catch((err) => {
            console.log(err);
          })
        } else{
          this.items.splice(index,1);
        }
      },
      saveEdit:function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let v_elastic_week_start =  this.editProductData.extend.elastic_week_start.value;
            let v_elastic_week_end =  this.editProductData.extend.elastic_week_end.value;
            let v_delivery_week_first = this.editProductData.extend.delivery_week_first.value;
            let v_delivery_week_last =  this.editProductData.extend.delivery_week_last.value;
            let fabric_ratio =  this.editProductData.extend.fabric_ratio.value;
            let rough_ratio =  this.editProductData.extend.rough_ratio.value;
            let yarn_ratio =  this.editProductData.extend.yarn_ratio.value;
            if(v_delivery_week_first && typeof  v_delivery_week_first != 'string'){
              v_delivery_week_first = v_delivery_week_first.getFullYear()  +  '-' +  (v_delivery_week_first.getMonth() + 1) + '-' + v_delivery_week_first.getDate();
            }
            if(v_delivery_week_last && typeof v_delivery_week_last != 'string'){
              v_delivery_week_last = v_delivery_week_last.getFullYear()  +  '-' +  (v_delivery_week_last.getMonth() + 1) + '-' + v_delivery_week_last.getDate();
            }
            if(v_elastic_week_start && typeof  v_elastic_week_start != 'string'){
              let mon = v_elastic_week_start.getMonth() + 1;
              mon = mon > 9 ? mon : '0' + '' + mon;
              let day = v_elastic_week_start.getDate();
              day = day > 9 ? day : '0' + '' + day;
              v_elastic_week_start =
                v_elastic_week_start.getFullYear()  +   '-' +  mon + '-' + day;
            }
            if(v_elastic_week_end && typeof v_elastic_week_end != 'string'){
              let mon = v_elastic_week_end.getMonth() + 1;
              mon = mon > 9 ? mon : '0' + '' + mon;
              let day = v_elastic_week_end.getDate();
              day = day > 9 ? day : '0' + '' + day;
              v_elastic_week_end =
                v_elastic_week_end.getFullYear()  +   '-' +  mon + '-' + day;
            }
            if(v_elastic_week_start && v_elastic_week_end){
              let start =
                v_elastic_week_start.replace(/-/g,'');
              let
                end = v_elastic_week_end.replace(/-/g,'');
              if(end - start < 0){
                this.$message({
                    message: '弹性结束周必须比起始周大',
                    type: 'error'
                  });
                return false
              }
            }
            if((fabric_ratio + rough_ratio + yarn_ratio)
              - 100 > 0){
              this.$message({
                message: '色布比率、毛坯比率、纱比率之和不能超过100',
                type: 'error'
              });
              return false
            }
            this.editProductData.extend.elastic_week_start.value = v_elastic_week_start;
            this.editProductData.extend.elastic_week_end.value = v_elastic_week_end;
            this.editProductData.extend.delivery_week_first.value = v_delivery_week_first;
            this.editProductData.extend.delivery_week_last.value = v_delivery_week_last;
            const api = this.$store.state.DEV_API;
            if(this.editProductData.model_inner_code){//update
              fetchAPI('put',api +
                '/api/product/model/?model_inner_code='+this.editProductData.model_inner_code,this.editProductData,this).then((res) => {
                if(res && res.status == 200){
                  this.$emit('isUpdate',this.optType+'_'+this.editProductData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                }
              });
            }else{
              fetchAPI('post',api +
                '/api/product/models/',this.editProductData,this).then((res) => {
                if(res && res.status == 201){
                  this.$emit('isUpdate',this.optType+'_'+this.editProductData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                  this.$set(this.editProductData,'model_inner_code',res.data.model_inner_code);
                }
              });
            }
          } else {
            return false;
          }
        });
      },
      deleteModel:function () {
        this.$confirm('确认删除吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const api = this.$store.state.DEV_API;
          fetchAPI('delete',api +
            '/api/product/model/?model_inner_code='+this.editProductData.model_inner_code,null,this).then((res) => {
            if(res.status == 204){
              this.$emit('isUpdate',this.optType+'_'+this.editProductData.tabIndex,true);
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.cancelTab();
            }
          });
        }).catch((err) => {
          console.log(err);
        });
      },
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editProductData.tabIndex);
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .productinfo_edit_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .productinfo_edit_main{
      height: 100%;
      .head_title{
        margin-top: 10px;
        height: 28px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 5px 25px 5px 12px;
          box-sizing: border-box;
        }
      }
      .edit_produc_input{
        height: 100%;
        width:60%;
        min-width: 400px;
      }
    }
  }
</style>
