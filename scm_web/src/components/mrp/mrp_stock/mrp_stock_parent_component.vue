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
            <stockinfo :matecode=4
                       :titlename="'成衣需求'"
                       :TABS="TABS"
                       :TABSValue="TABSValue"
                       :tabIndex="tabIndex"
                       :tableData="tableData"
                       @CloseTab="parentCloseTab"
                       @changeTabMethod="changetab">
            </stockinfo>
            <br/>
          </template>
          <template v-else>
            <template v-if="!item.bom&&!item.stock">
              <stockedit :rowMessage="item.rowId"
                         :propStatus="item.rowState"
                         :titlename="'成衣需求'"
                         :materialtype=4
                         :TABS="TABS"
                         :TABSValue="TABSValue"
                         :tabIndex="tabIndex"
                         @CloseTab="parentCloseTab"
                         @changeTabMethod="changetab">
              </stockedit>
            </template>
            <template v-if="item.bom === 'bom'">
              <viewbom :rowMessage="item"
                       :materialtype=4
                       :TABS="TABS"
                       :TABSValue="TABSValue"
                       :tabIndex="tabIndex"
                       @CloseTab="parentCloseTab"
                       @changeTabMethod="changetab">
              </viewbom>
            </template>
            <template v-if="item.stock === 'stock'">
              <materialinfo :propData="item.resData"
                            :TABS="TABS"
                            :TABSValue="TABSValue"
                            :tabIndex="tabIndex"
                            :rowId=0
                            @CloseTab="parentCloseTab"
                            @changeTabMethod="changetab">
              </materialinfo>
            </template>
          </template>

          <!--<viewbom :rowMessage="item.rowMes"-->
          <!--:TABS="TABS"-->
          <!--:TABSValue="TABSValue"-->
          <!--:tabIndex="tabIndex"-->
          <!--@CloseTab="parentCloseTab"-->
          <!--@changeTabMethod="changetab">-->
          <!--</viewbom>-->
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import stockinfo from './mrp_stock_info.vue'
  import stockedit from './mrp_stock_edit.vue'
  import viewbom from '../tailoringbom/tailoring_bom_detailed.vue'
  import materialinfo from '../../mrp/common/material_stock/material_stock_info.vue'
  /*
  * materialtype 备料方式
  * matecode 备料类型
  * */
  export default {
    name: 'test-manage',
    components: {
      stockinfo,
      stockedit,
      viewbom,
      materialinfo
    },
    data() {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        // tab页数据
        TABS: [
          {
            title: '成衣需求',
            name: '1',
            closable: false
          }
        ],
        // 材料信息
        Minformation: {},
        tableData: []
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
    computed: {},
    updated() {

    },
    mounted() {
      console.log("mounted刷新一次数据")
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
