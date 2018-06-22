<template>
  <el-table :data="gridData" v-if="dialogType != 1">
    <el-table-column v-for="(item,index) in gridColumn"
                     :property="item.columnProp"
                     :label="item.columnName"
                     :key="item.index">
    </el-table-column>
    <el-table-column label="操作"
                     width="120">
      <template scope="scope">
        <el-button size="small"
                   @click="getInfo(scope.$index, scope.row)">选择
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <div v-else>
      <div class="md3Button">
        <el-button type="danger"
                   class="handle-del mr10"
                   :data="multipleSelection"
                   @click="delBtn">确定
        </el-button>
      </div>
        <el-table :data="gridData" @selection-change="handleSelectionChange" >
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
  export default {
    name: 'new_dialog',
    props:{
      gridData:Array,
      dialogType:Number
    },
    data() {
      return {
        gridColumn:[ //弹窗列表
          {
            columnName: "编码",
            columnProp: "meta_code"
          }, {
            columnName: "名称",
            columnProp: "meta_name"
          }
        ],
        multipleSelection:""
      }
    },
    //addiconClick
    methods: {
      //单选
      getInfo(index,row){
        console.log("插件",row,index);
        this.$emit('getDialogInfo',row,index);
      },
      //多选
      handleSelectionChange(value) {
        this.multipleSelection = value;
      },
      //多选确认按钮
      delBtn(){
        console.log(this.multipleSelection);
        this.$emit('getDialogInfo',this.multipleSelection);
      }
    },
    mounted(){
      if(this.dialogType === 1){
        this.gridColumn =[
          {
            columnName: "编码",
            columnProp: "item_code"
          }, {
            columnName: "名称",
            columnProp: "item_name"
          }
        ];
      }
    }
  }
</script>
<style>
  .md3Button{
    float:right;
    margin-bottom:10px;
  }
</style>
