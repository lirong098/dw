<template>
  <div class="materailsrule_edit_contain">
    <div class="materailsrule_edit_main">
      <el-form :model="editMaterailsruleData"  ref="materailsForm"
               class="demo-form-inline"
               label-width="120px" :rules="materailsRules">
        <div class="clearfix">
          <div class="fl main-card-box">
            <div class="card_box">
              <div class="card-header card-header-text">
                <h4>
                  备料策略
                </h4>
              </div>
              <el-card>
                <el-form-item label="备料策略" prop="pr_method_name">
                  <div class="edit_materails_input edit_input_common">
                    <el-input size="small"
                              v-model="editMaterailsruleData.pr_method_name" placeholder="备料策略" ></el-input>
                  </div>
                </el-form-item>
              </el-card>
            </div>
          </div>
          <div class="fr opt-btn-box">
            <el-card class="extra_card">
              <el-button type="primary"
                         @click="saveEdit('materailsForm')">保存
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button @click="addmethodItem('')" type="info"
                         :disabled="!editMaterailsruleData.pr_method_id">添加Item
              </el-button>
              <div style="margin: 10px;"></div>
              <el-button @click="deleteMaterails"
                         type="danger"
                         :disabled="!editMaterailsruleData.pr_method_id">删除
              </el-button>
            </el-card>
          </div>
        </div>
        <div class="main-card-box" v-if="methoditems && methoditems.length">
          <div class="card_box">
            <div class="card-header card-header-text">
              <h4>
                Item
              </h4>
            </div>
            <el-card>
              <el-form-item label="Item 信息" >
                <el-card class="box-card extra_card">
                  <div v-for="(item,index) in methoditems"
                       :class="{detail_item:true}">
                    <el-form :inline="true" :model="item"
                             class="demo-form-inline"
                             :ref="'methodForm_'+index"
                             :rules="itemRules">
                      <el-form-item label="物料类型"
                                    prop="material_type_meta">
                        <el-select
                          v-model="item.material_type_meta"
                          @change="changeMethodItem(index,'methodForm_'+index)"
                          placeholder="请选择">
                          <el-option
                            label=""
                            value="">
                            <div class="select_add"
                                 @click="addMaterialsType">
                              <el-icon name="plus"></el-icon>
                              <span>新增</span>
                            </div>
                          </el-option>
                          <el-option
                            v-for="item in materials"
                            :key="item.meta_code"
                            :label="item.meta_name"
                            :value="item.meta_code">
                          </el-option>
                        </el-select>
                      </el-form-item>
                      <el-form-item label="百分比" prop="percent">
                        <el-input-number size="small"
                                         :min="0"
                                         :max="100"
                                         @change="changeMethodItem(index,'methodForm_'+index)"
                                         v-model="item.percent"></el-input-number>
                      </el-form-item>
                      <span class="icon_content"  v-show="item.type == 'ok'">
                  <i class="icon icon16 icon_correct"></i>
                </span>
                      <span class="icon_content" v-show="item.type == 'no'">
                  <i class="icon icon16 icon_error"></i>
                </span>
                      <el-form-item>
                        <el-button-group>
                          <el-button type="primary"
                                     icon="plus"
                                     size="mini"
                                     @click="addmethodItem(index)"></el-button>
                          <el-button type="danger" icon="delete" size="mini" @click="deletemethodItem(index)"></el-button>
                        </el-button-group>
                      </el-form-item>
                    </el-form>
                  </div>
                </el-card>
              </el-form-item>
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
    name: 'materails-rule-edit',
    props:{
      editMaterailsrule:{
        type:Object
      },
      materials:{
        type:Array
      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        editMaterailsruleData:Object.assign({},this.editMaterailsrule),
        methoditems:[],
        materailsRules:{
          pr_method_name:[
            { required: true, message: '名称必填',  trigger: 'blur' },
          ],
        },
        itemRules:{
          material_type_meta:[
            { required: true, message:
              'material_type_meta 必填',  trigger: 'blur' },
          ]
        },
        tabIndex:1
      }
    },
    computed:{

    },
    created() {
      this.getMethodItem();
    },
    methods: {
      getMethodItem:function () {
        if(this.optType == 'addMaterailsrule'){
          return false
        }
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/product/pr_items/?pr_method_id='+this.editMaterailsruleData.pr_method_id,null,this).then((res) => {
          if(res && res.status == 200){
            this.methoditems =  res.data;
          }
        })
      },
      addmethodItem:function (index) {
        let methoditem = {
          percent:0,
          material_type_meta:'',
          extend:null
        };
        if(this.methoditems && this.methoditems.length){
          if(index === ''){
            this.methoditems.push(methoditem);
          }else{
            index++;
            this.methoditems.splice(index,0,methoditem);
          }
        }else{
          let arr = [methoditem];
          this.methoditems = arr.slice();
        }
      },
      changeMethodItem:function (index,formName) {
        setTimeout(() => {
          this.$refs[formName][0].validate((valid) => {
            if (valid) {
              const api = this.$store.state.DEV_API;
              if(this.editMaterailsruleData.pr_method_id){//有策略组
                let obj = {
                  percent: this.methoditems[index].percent,
                  extend: null,
                  pr_method: this.editMaterailsruleData.pr_method_id,
                  material_type_meta:this.methoditems[index].material_type_meta
                };
                if(this.methoditems[index].pr_method_item_id){//修改
                  obj.pr_method_item_id = this.methoditems[index].pr_method_item_id;
                  fetchAPI('put',api + '/api/product/pr_item/?pr_method_item_id='+this.methoditems[index].pr_method_item_id,obj,this).then((res) => {
                    if(res && res.status == 200){
                      this.$set(this.methoditems[index], 'type','ok') ;
                    }else{
                      this.$set(this.methoditems[index],'type','no') ;
                    }
                  });
                }else{//新增
                  fetchAPI('post',api +  '/api/product/pr_items/',obj,this).then((res) => {
                    if(res && res.status == 201){
                      this.$set(this.methoditems[index],'pr_method_item_id',res.data.pr_method_item_id) ;
                      this.$set(this.methoditems[index], 'type','ok') ;
                    }else{
                      this.$set(this.methoditems[index],'type','no') ;
                    }
                  })
                }
              }else{
                this.$message({
                  message: '请先保存备料策略分组',
                  type: 'warning'
                });
              }
            } else {
              return false;
            }
          })
        }, 500);
      },
      deletemethodItem:function (index) {
        if(this.methoditems[index].pr_method_item_id){
          this.$confirm('确认删除吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const api = this.$store.state.DEV_API;
            fetchAPI('delete',api +
              '/api/product/pr_item/?pr_method_item_id='+this.methoditems[index].pr_method_item_id,null,this).then((res) => {
              if(res && res.status == 204){
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                });
                this.methoditems.splice(index,1);
              }
            })
          }).catch((err) => {
            console.log(err);
          })
        } else{
          this.methoditems.splice(index,1);
        }
      },
      saveEdit:function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            const api = this.$store.state.DEV_API;
            if(this.editMaterailsruleData.pr_method_id){//update
              fetchAPI('put',api +
                '/api/product/pr/?pr_method_id='+this.editMaterailsruleData.pr_method_id,this.editMaterailsruleData,this).then((res) => {
                if(res && res.status == 200){
                  this.$emit('isUpdate',this.optType+'_'+this.editMaterailsruleData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                }
              });
            }else{
              fetchAPI('post',api +
                '/api/product/prs/',this.editMaterailsruleData,this).then((res) => {
                if(res && res.status == 201){
                  this.$emit('isUpdate',this.optType+'_'+this.editMaterailsruleData.tabIndex,false);
                  this.$message({
                    message: '保存成功',
                    type: 'success'
                  });
                  this.$set(this.editMaterailsruleData,'pr_method_id',res.data.pr_method_id);
                }
              });
            }
          } else {
            return false;
          }
        });
      },
      deleteMaterails:function () {
        this.$confirm('确认删除吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const api = this.$store.state.DEV_API;
          fetchAPI('delete',api +
            '/api/product/pr/?pr_method_id='+this.editMaterailsruleData.pr_method_id,null,this).then((res) => {
            if(res.status == 204){
              this.$emit('isUpdate',this.optType+'_'+this.editMaterailsruleData.tabIndex,true);
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
        this.$emit('cancelTab',this.optType+'_'+this.editMaterailsruleData.tabIndex);
      },
      addMaterialsType:function () {
        let data = {
          type: 'addmaterailsType',
          data: {
            meta_code: '',
            meta_name: '',
            meta_value: '',
            tabIndex:this.tabIndex
          }
        };
        this.tabIndex++;
        this.$emit('changeTabs',data);
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .materailsrule_edit_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .materailsrule_edit_main{
      height: 100%;
      .head_title{
        height: 28px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 10px 20px 10px 5px;
          box-sizing: border-box;
        }
        margin-top: 8px;
      }
      .edit_materails_input{
        &.text{
          padding: 40px 20px 10px 10px;
        }
      }
    }
  }
</style>
