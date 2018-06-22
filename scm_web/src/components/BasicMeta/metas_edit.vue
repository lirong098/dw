<template>
  <div class="metas_edit_contain">
    <div class="metas_edit_main">
      <div class="edit-card-box">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              编辑默认值
            </h4>
          </div>
          <el-card class="">
            <el-form :model="editMetasData" class="demo-form-inline" label-width="68px">
              <el-form-item label="数据名称">
                <div class="edit_metas_input">
                  {{editMetasData.meta_name}}
                </div>
              </el-form-item>
              <el-form-item label="默认值">
                <div class="edit_metas_input">
                  <el-input-number :min="0"
                                   :controls="false"
                                   v-model="editMetasData.meta_value"></el-input-number>
                </div>
              </el-form-item>
              <el-form-item >
                <div class="edit_metas_input">
                  <div class="submit_btn">
                    <el-button type="danger"
                               @click="saveEdit">保存
                    </el-button>
                    <el-button @click="cancelTab">取消</el-button>
                  </div>
                </div>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default{
    name:'materails-edit',
    props:{
      editMetas:{
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
        editMetasData:Object.assign({},this.editMetas),
        tabIndex:1,
        loading:true,
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() < Date.now() - 8.64e7;
          }
        },
      }
    },
    computed:{

    },
    created() {
    },
    methods: {
      saveEdit:function () {
        let data = {
          type:this.optType,
          data:this.editMetasData,
        };
        this.$emit('saveEdit',data);
      },
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editMetasData.tabIndex);
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .metas_edit_contain{
    height: 100%;
    padding:0 10px 10px 10px;
    .metas_edit_main{
      height: 100%;
      .edit_metas_input{
        width:250px;
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
