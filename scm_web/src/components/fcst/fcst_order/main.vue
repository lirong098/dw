<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane v-for="(item, index) in TABS"
                     :closable="item.closable"
                     :key="item.name"
                     :label="item.title"
                     :name="item.name">
          <template v-if="item.name  === '1'">
            <sample-info :TABS="TABS"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         :tableName="tableName"
                         :tableType="tableType"
                         @CloseTab="parentCloseTab"
                         @changeTabMethod="changetab">
            </sample-info>
            <br/>
          </template>
          <template v-if="item.name > 1 && item.name < 100">
            <sample-edit :rowId="rowId"
                         :TABS="TABS"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         :tableName="tableName"
                         :tableType="tableType"
                         :fcstType="fcstTypeNum"
                         @CloseTab="parentCloseTab"
                         @changeTabMethod="changetab">
            </sample-edit>
          </template>

          <template v-if="item.name > 200">
            <stock-list-edit :propData="item.resData"
                             :rowId="item.rowId"
                             :TABSValue="TABSValue"
                             :tabIndex="tabIndex"
                             :tableName="tableName"
                             :fcstType="item.fcstType"
                             @CloseTab="parentCloseTab" @changeTabMethod="changetab">
            </stock-list-edit>
          </template>

        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  //公共组件
  import sampleInfo from './list.vue';
  import sampleEdit from './view.vue';

  import stockListEdit from '../common/pr_stock/stocklist_edit.vue';

  //公共文件
  import showModal from '../../common/messageBox.js';
  import {fetchAPI} from '../../../utils/utils';

  export default {
    name: 'new_table',
    components: {
      sampleInfo,
      sampleEdit,
      stockListEdit,
    },
    props: {
      //tag显示值
      tagName: {
        type: String,
        default: "选样实单"
      },
      // 订单类型
      fcstType: {
        type: Number,
        default: 6  // 5 预估实单，6 选样实单
      }
    },
    data() {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        tableName: this.tagName,
        tableType: this.fcstType,
        fcstTypeNum: this.fcstType,
        rowId: 1,
        TABS: [
          {
            title: this.tagName,
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
      parentCloseTab() {
        if (this.TABSValue > 1) {
          this.removeTab(this.TABSValue)
        }
      },
      // 子组件更新父组件
      changetab(tabIndex, TABSValue, TABS) {
        this.TABSValue = TABSValue;
        this.tabIndex = tabIndex;
        this.rowId = TABS.rowId;
        this.TABS.push(TABS);
      }
    },
    //计算属性
    computed: {},
    //监听数据变化
    watch: {
      TABSValue(val) {
        this.TABSValue = val;
      }
    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_contain .test_main {
    height: 100%;
    .el-table {
      text-align: center;
      th > .cell {
        text-align: center;
      }
    }
  }
</style>
