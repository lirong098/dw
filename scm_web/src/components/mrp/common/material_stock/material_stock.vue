<template>
  <div class="test_contain">
    <div class="test_main">
      <el-tabs v-model="TABSValue" type="card" @tab-remove="removeTab">
        <el-tab-pane v-for="(item, index) in TABS"
                     :closable="item.closable"
                     :key="item.name"
                     :label="item.title"
                     :name="item.name">
          <template v-if="item.name === '1'">
            <stock_list :stockInfo="stockInfo"
                        :TABSValue="TABSValue"
                        :TABSIndex="TABSIndex"
                        @CloseTab="parentCloseTab"
                        @changeTabMethod="changetab">
            </stock_list>
            <br/>
          </template>
          <template v-else>
            <stock_info :stockInfo="stockInfo"
                        :TABSValue="TABSValue"
                        :TABSIndex="TABSIndex"
                        :rowId="item.rowId"
                        @CloseTab="parentCloseTab"
                        @changeTabMethod="changetab">
            </stock_info>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import stock_list from './material_stock_list.vue'
  import stock_info from './material_stock_info.vue'

  export default {
    name: 'test-manage',
    components: {
      stock_list,
      stock_info
    },
    props: {
      stockType: {
        type: Number,
        default: 1
      }
    },
    data() {
      return {
        TABSValue: '1',  // tab页Value
        TABSIndex:1,
        // tab页数据
        stockInfo:this.getBasicValue(),
        TABS: [
          {
            title: this.getBasicValue().stock_name,
            name: '1',
            closable: false,
            rowId:0
          }
        ],
      }
    },
    methods: {
      //根据类型获取基础值
      /*
  * stockType:{1:MRP备料，2：MRP实单，3：手工备料，4：盘点入库，5：盘点出库}
  */
      getBasicValue(type = this.stockType) {
        let stockInfo = {
          stock_name:'',
          stock_id:0
        }
        switch (type) {
          case 1:
            stockInfo.stock_name = 'MRP备料';
            stockInfo.stock_id = 20;
            break;
          case 2:
            stockInfo.stock_name = 'MRP实单';
            stockInfo.stock_id = 21;
            break;
          case 3:
            stockInfo.stock_name = '手工备料';
            stockInfo.stock_id = 19;
            break;
          case 4:
            stockInfo.stock_name = '盘点入库';
            stockInfo.stock_id = 17;
            break;
          case 5:
            stockInfo.stock_name = '盘点出库';
            stockInfo.stock_id = 18;
            break;
        }
        return stockInfo;
      },
      //
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
      changetab(TABSIndex,TABSValue, TABS) {
        this.TABS.push(TABS);
        this.TABSValue = TABSValue;
        this.TABSIndex = TABSIndex;
      }
    },
    computed: {},
    updated() {

    },
    mounted() {
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
