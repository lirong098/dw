<template>
  <div class="materailstype_edit_contain">
    <div class="materailstype_edit_main">
      <div class="card_box">
        <div class="card-header card-header-text">
          <h4>
            物料信息
          </h4>
        </div>
        <el-card>
          <el-form :model="editmaterailsTypeData"
                   class="demo-form-inline"
                   ref="typeForm"
                   label-width="80px" :rules="typeRules">
            <el-form-item label="物料编号" prop="meta_code">
              <div class="edit_materailstype_input edit_input_common"
                   v-if="optType == 'addmaterailsType'">
                <el-input v-model="editmaterailsTypeData.meta_code" placeholder="物料编号"></el-input>
              </div>
              <div class="edit_materailstype_input edit_input_common"
                   v-if="optType == 'editmaterailsType'">
                {{editmaterailsTypeData.meta_code}}
              </div>
            </el-form-item>
            <el-form-item label="物料名称" prop="meta_name">
              <div class="edit_materailstype_input edit_input_common">
                <el-input
                  v-model="editmaterailsTypeData.meta_name"
                  placeholder="物料名称"></el-input>
              </div>
            </el-form-item>
            <el-form-item>
              <div class="submit_btn">
                <el-button type="primary"
                           @click="saveEdit('typeForm')">保存
                </el-button>
                <el-button @click="cancelTab" >取消</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script>
  export default{
    name:'materailstype-edit',
    props:{
      editmaterailsType:{
        type:Object
      },
      currentTab:{
          type:String
      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        editmaterailsTypeData:Object.assign({},this.editmaterailsType),
        tabIndex:1,
        loading:true,
        typeRules:{
          meta_code:[
            { required: true, message: '物料编号必填',
              trigger:
                'blur' },
          ],
          meta_name:[
            { required: true, message: '物料名称必填',
              trigger:
              'blur' },
          ],
        }
      }
    },
    computed:{

    },
    created() {

    },
    methods: {
      saveEdit:function (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let data = {
              type:this.optType,
              data:this.editmaterailsTypeData,
            };
            this.$emit('saveEdit',data);
          }
        })
      },
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editmaterailsTypeData.tabIndex);
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .materailstype_edit_contain{
    height: 100%;
    padding:20px 10px 10px 10px;
    .materailstype_edit_main{
      height: 100%;
      .edit_materailstype_input{

      }
      .head_title{
        height: 28px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 5px 12px 5px 0;
          box-sizing: border-box;
        }
      }
      .edit_order_input{
        width:300px;
      }
      .model_content{
        display: inline-block;
        width:40%;
      }
      .item_content{
        display: inline-block;
        width:25%;
      }
      .quantity_content{
        display: inline-block;
      }
    }
  }
</style>
