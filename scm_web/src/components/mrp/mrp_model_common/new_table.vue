<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane  v-for="(item, index) in TABS"
                      :closable="item.closable"
                      :key="item.name"
                      :label="item.title"
                      :name="item.name">
          <template v-if="index === 0 && !showTableInfo">
            <tableInfo :TABS="TABS"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         :tableName="tableName"
                         :tableType="tableType"
                         :showTableColumn="showTableColumn"
                         @CloseTab="parentCloseTab"
                         @changeTabMethod="changetab"
                         @getModelInfo="getModelInfo">
            </tableInfo><br/>
          </template>
          <template v-else>
            <tableDetailed :rowId="item.rowId"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         :tableName="tableName"
                         :tableType="tableType"
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
  import tableInfo from './new_table_info.vue';
  import tableDetailed from './new_table_detaied.vue';
  import showModal from '../../../components/common/messageBox.js';
  import {fetchAPI} from '../../../utils/utils';
  export default{
    name:'new_table',
    components: {
      tableInfo,
      tableDetailed
    },
    props: {
      tableName: String,
      tableType:Number,
      showTableColumn:Boolean,
      showTableInfo:Boolean,
      model_id:Number
    },
    data () {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        TABS: [
          {
            title: this.tableName,
            name: '1',
            closable: false,
            rowId:this.model_id
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
      getModelInfo(row){
        this.$emit("getModelInfo",row);
      }
    },
    //计算属性
    computed: {
    },
    //监听数据变化
    watch: {
      TABSValue(val) {
        this.TABSValue = val;
      }
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
