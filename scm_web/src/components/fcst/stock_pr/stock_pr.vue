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
            <stockprinfo :TABS="TABS"
                          :TABSValue="TABSValue"
                          :tabIndex="tabIndex"
                          :tableData="tableData"
                          @CloseTab="parentCloseTab"
                          @changeTabMethod="changetab">
            </stockprinfo><br/>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import stockprinfo from './stock_pr_info.vue'
  export default{
    name:'test-manage',
    components: {
      stockprinfo
    },
    data () {
      return {
        TABSValue: '1',  // tab页Value
        tabIndex: 1,  //tab页Index
        // tab页数据
        TABS:[
          {
            title: '备料库存',
            name: '1',
            closable: false
          }
        ],
        // 材料信息
        Minformation:{},
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
      }
    },
    computed: {

    },
    updated() {

    },
    mounted() {
      console.log("mounted刷新一次数据")
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
