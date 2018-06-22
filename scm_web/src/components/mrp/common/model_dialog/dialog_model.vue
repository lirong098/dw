<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane  v-for="(item, index) in TABS"
                      :closable="item.closable"
                      :key="item.name"
                      :label="item.title"
                      :name="item.name">
          <template v-if="item.tabName === 'modelList' && !onlyGetItem">
            <tableInfo :TABS="TABS"
                       :TABSValue="TABSValue"
                       :tabIndex="tabIndex"
                       :tableName="tableName"
                       :exclude="exclude"
                       :noGetItem="noGetItem"
                       :otherParameter="otherParameter"
                       @CloseTab="parentCloseTab"
                       @changeTabMethod="changetab"
                       @getDialogInfo="getDialogInfo">
            </tableInfo><br/>
          </template>
          <template v-if="item.tabName === 'item'">
            <new-dialog
              :modelData="item.data"
              :model_id="item.rowId"
              :onlyGetItem="onlyGetItem"
              @CloseTab="parentCloseTab"
              @changeTabMethod="changetab"
              @getDialogInfo="getDialogInfo">
            </new-dialog>
          </template>
          <template v-if="item.tabName === 'modelInfo' && !onlyGetItem">
            <tableDetailed :rowId="item.rowId"
                           :TABSValue="TABSValue"
                           :tabIndex="tabIndex"
                           :tableName="item.tableName"
                           :tableType="item.tableType"
                           @CloseTab="parentCloseTab"
                           @changeTabMethod="changetab">
            </tableDetailed>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import tableInfo from './dialog_model_list.vue';
  import tableDetailed from '../model/new_table_detaied.vue';
  import newDialog from "./dialog_model_item.vue";
  export default{
    name:'new_table',
    components: {
      tableInfo,
      tableDetailed,
      newDialog
    },
    props: {
      tableName: { //查看Model详情时需要
        type:String,
        default:"Model"
      },
      tableType: { //查看Model详情时 需要
        type:Number,
        default:1
      },
      exclude: { // 2成衣 1（面料 辅料）
        type:Number,
        default:2
      },
      noGetItem:{ //true 获取model 不获取Item
        type:Boolean,
        default:false
      },
      onlyGetItem:{ //true 只获取Item
        type:Boolean,
        default:false
      },
      model_id:{ //只获取Item和查看Model详情时 必须要有
        type:Number,
        default:0
      },
      otherParameter:{ //过滤参数 包括 客户ID 季节id
        type:Object,
        default:()=>{ return {
          otherCustomerId:'',
          otherSeasonId:''
        }}
      }
    },
    data () {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        TABS: [
          {
            title: this.model_id === 0 ?"Model列表" :this.onlyGetItem ? "选择tem" :"Model详情",
            name: '1',
            closable: false,
            rowId:this.model_id,
            tabName:this.model_id === 0 ?"modelList" : this.onlyGetItem ? "item" :"modelInfo",
            tableType:this.tableType,
            tableName:this.tableName
          }
        ]
      }
    },
    methods: {
      removeTab(targetName) {
        let tabs = this.TABS;
        let activeName = this.TABSValue;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
            }
          });
        }
        this.TABSValue = activeName;
        this.TABS = tabs.filter(tab => tab.name !== targetName);
      },
      parentCloseTab(){
        if( this.TABSValue > 1){
          this.removeTab(this.TABSValue)
        }
      },
      // 子组件更新父组件
      changetab(tabIndex,TABSValue,TABS){
        this.TABSValue = TABSValue;
        this.tabIndex = tabIndex;
        this.TABS.push(TABS);
      },
      getDialogInfo(row,model_id){
        this.$emit("getDialogInfo",row,model_id);
      },
    },
    //监听数据变化
    watch: {
      TABSValue(val) {
        this.TABSValue = val;
      }
    },
    mounted(){
      console.log("tableName",this.tableName);
      console.log("tableType",this.tableType);
      console.log("exclude",this.exclude);
      console.log("noGetItem",this.noGetItem);
      console.log("onlyGetItem",this.onlyGetItem);
      console.log("model_id",this.model_id);
    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_contain .test_main{
    height: 100%;
    .el-table {
      text-align: center;
      th>.cell {
        text-align: center;
      }
    }
  }
</style>
