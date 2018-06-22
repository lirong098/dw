<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane v-for="(item, index) in TABS"
                     :closable="item.closable"
                     :key="item.name"
                     :label="item.title"
                     :name="item.name">
          <template v-if="index === 0">
            <stocklist_info :TABS="TABS"
                            :TABSValue="TABSValue"
                            :tabIndex="tabIndex"
                            :tableName="tableName"
                            :fcstType="fcstType"
                            @CloseTab="parentCloseTab"
                            @changeTabMethod="changetab">
            </stocklist_info>
            <br/>
          </template>
          <template v-else-if="item.tabName">
            <mrp_preview v-if="item.tabName =='preview'"
                         :rowId="item.rowId"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         :fcstType="fcstType"
                         @CloseTab="parentCloseTab" @changeTabMethod="changetab"></mrp_preview>
            <bom_detailed v-if="item.tabName == 'bominfo'" :rowMessage="item" :TABSValue="TABSValue"
                          :tabIndex="tabIndex" @CloseTab="parentCloseTab" @changeTabMethod="changetab"></bom_detailed>
            <stock_detailed v-if="item.tabName == 'stockmanagement'"
                            :propData="item.resData"
                            :materialtype="fcstType === 1 ? 20:fcstType ===2 ? 21:19"
                            :titlename="fcstType === 1 ? 'MRP备料':fcstType ===2 ? 'MRP实单':''"
                            :TABS="TABS" :TABSValue="TABSValue" :tabIndex="tabIndex" @CloseTab="parentCloseTab"
                            @changeTabMethod="changetab"></stock_detailed>
          </template>
          <template v-else>
            <stocklist_edit :rowId="item.rowId" :TABSValue="TABSValue" :tabIndex="tabIndex" :fcstName="tableName"
                            :fcstType="fcstType" @CloseTab="parentCloseTab" @changeTabMethod="changetab">
            </stocklist_edit>
          </template>

        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  //公共组件
  import stocklist_info from './stocklist_info.vue';
  import stocklist_edit from './stocklist_edit.vue';
  import stock_detailed from "../../common/material_stock/material_stock_info.vue";
  import bom_detailed from '../../tailoringbom/tailoring_bom_detailed.vue';
  import mrp_preview from "./mrp_preview.vue";
  //公共文件
  import showModal from '../../../common/messageBox.js';
  import {fetchAPI} from '../../../../utils/utils';
  /*组件说明
  * fcstType{1：mrp_成衣备料,2:mrp_成衣实单,3:选样实单,4:预估订单,5:预估实单,6:选样备料,7:预估备料,8:手工备料}
  * */
  export default {
    name: 'new_table',
    components: {
      stocklist_info,
      stocklist_edit,
      stock_detailed,
      bom_detailed,
      mrp_preview
    },
    props: {
      fcstName: {
        type: String,
        default: "成衣备料"
      },//tag显示值
      fcstType: {
        type: Number,
        default: 1
      }
    },
    data() {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        tableName: this.fcstName,
        tableType: 1,
        TABS: [
          {
            title: this.fcstName,
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
    },
    created() {
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
