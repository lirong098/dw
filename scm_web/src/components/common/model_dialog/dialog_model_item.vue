<template>
  <div id="dialog_model_item">
    <div class="md3Button">
      <el-button type="error"
                 class="handle-del mr10"
                 @click="getClick">
        {{getAll ? '添加所有Item' :'取消所有Item'}}
      </el-button>
      <el-button type="danger"
                 class="handle-del mr10"
                 :data="multipleSelection"
                 @click="confirmButtton"
                 :disabled="onlyGetItem && multipleSelection.length === 0 ? true : false">确定
      </el-button>
    </div>
    <el-table ref="ItemList" :data="gridData" @selection-change="handleSelectionChange" border>
      <el-table-column type="selection"
                       width="55">
      </el-table-column>>
      <el-table-column v-for="(item,index) in gridColumn"
                       :property="item.columnProp"
                       :label="item.columnName"
                       :key="item.index">
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
  import {fetchAPI} from '../../../utils/utils';
  export default {
    name: 'dialog_model_item',
    props:{
      model_id:{
        type:Number,
        default:0
      },
      modelData:{
        default:null
      },
      onlyGetItem:{ //true 只获取Item
        type:Boolean,
        default:false
      },
    },
    data() {
      return {
        gridColumn:[ //弹窗列表
          {
            columnName: "编码",
            columnProp: "item_code"
          }, {
            columnName: "名称",
            columnProp: "item_name"
          }
        ],
        multipleSelection:[],//勾选的值
        gridData:[], //item数据
        getAll:true //true时：显示添加所有Item false时：显示取消所有Item
      }
    },
    methods: {
      //getClick
      getClick(){
        this.getAll ? this.getAllButtton() : this.noGetAllButton();
      },
      //添加所有Item
      getAllButtton(){
        this.gridData.forEach(row=>{
          this.$refs.ItemList.toggleRowSelection(row);
        })
        this.getAll = false;
      },
      //取消所有Item
      noGetAllButton(){
        this.$refs.ItemList.clearSelection();
        this.getAll = true;
      },
      //多选
      handleSelectionChange(value) {
        this.multipleSelection = value;
      },
      //多选确认按钮
      confirmButtton(){
        if(this.modelData != null && !this.onlyGetItem){
          this.modelData.model_item = this.multipleSelection;
          this.$emit('getDialogInfo',this.modelData);
        }else if(this.onlyGetItem){
          this.$emit('getDialogInfo',this.multipleSelection,this.model_id);
        }
      }
    },
    mounted(){
      let url = this.$store.state.NEW_API+"/api/mat_models/items/?model_id="+this.model_id;
      fetchAPI('get', url, null, this).then((res) => {
        if (res && res.status == 200) {
          this.gridData = res.data;
        }
      })
    }
  }
</script>
<style>
  .md3Button{
    float:right;
    margin-bottom:10px;
  }
</style>
