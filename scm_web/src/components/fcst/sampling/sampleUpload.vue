<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane  v-for="(item, index) in TABS"
                      :closable="item.closable"
                      :key="item.name"
                      :label="item.title"
                      :name="item.name">
          <template v-if="index === 0">
            <sampleUpload_list :TABS="TABS"
                            :TABSValue="TABSValue"
                            :tabIndex="tabIndex"
                            :importType="importType"
                            @CloseTab="parentCloseTab"
                            @changeTabMethod="changetab">
            </sampleUpload_list><br/>
          </template>
          <template v-else>
            <sampleUpload_info  :rowId="item.rowId"
                                :TABSValue="TABSValue"
                                :tabIndex="tabIndex"
                                :importType="importType"
                                @CloseTab="parentCloseTab"
                                @changeTabMethod="changetab">
            </sampleUpload_info>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  //公共组件
  import sampleUpload_list from './sampleUpload_list.vue';
  import sampleUpload_info from './sampleUpload_info.vue';
  //公共文件
  import showModal from '../../common/messageBox.js';
  import {fetchAPI} from '../../../utils/utils';

  export default{
    name:'new_table',
    components: {
      sampleUpload_list,
      sampleUpload_info
    },
    props:{
      importType:{
        type:Number,
        default:2
      }
    },
    data () {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        TABS: [
          {
            title: this.importType ===2 ?"选样导入" : this.importType ===1 ? "预估导入":"实单导入",
            name: '1',
            closable: false
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
        console.log(TABS);
        this.TABS.push(TABS);
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
