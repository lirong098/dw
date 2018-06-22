<template>
  <div class="customer_contain">
    <div class="customer_main">
      <lazy-render>
        <el-tabs v-model="currentTab" type="card" @tab-remove="removeTab">
          <el-tab-pane
            :closable="item.closable"
            v-for="(item, index) in TABS"
            :key="item.name"
            :label="item.title"
            :name="item.name"
          >
            <div v-if="item.name == 'main'">
              <customerManageMain @changeTabs="changeTabs"  :editData="editData" @cancelTab="cancelTab"></customerManageMain>
            </div>
            <div v-else-if="addCustomerData[item.index] && item.name == 'addCustomer_'+addCustomerData[item.index].tabIndex">
              <customerManageEdit @saveEdit="saveEdit"
                                  @cancelTab="cancelTab"
                                  :editCustomer="addCustomerData[item.index]" :optType="item.type"></customerManageEdit>
            </div>
            <div v-else-if="editCustomerData[item.index] && item.name == 'editCustomer_'+editCustomerData[item.index].tabIndex">
              <customerManageEdit @saveEdit="saveEdit"
                                  @cancelTab="cancelTab"
                                  :editCustomer="editCustomerData[item.index]" :optType="item.type"></customerManageEdit>
            </div>
          </el-tab-pane>
        </el-tabs>
      </lazy-render>
    </div>
  </div>
</template>
<script>
  import customerManageMain from '../../components/BasicMeta/customerManage_main.vue';
  import customerManageEdit from '../../components/BasicMeta/customerManage_edit.vue';
  export default{
    name:'customer-manage',
    components: {
      customerManageMain,
      customerManageEdit
    },
    data () {
      return {
        TABS:[],
        currentTab:'',
        addCustomerData:{},
        editCustomerData:{},
        editData:{}
      }
    },
    computed:{

    },
    created() {
      let tab = [{
        title:this.$route.name,
        name:'main',
        closable:false
      }];
      this.TABS = tab.slice();
      this.currentTab = 'main';
    },
    methods: {
      changeTabs:function (data) {
        if(data){
          if(data.type == 'addCustomer'){
            this.addCustomerData[data.data.tabIndex] = Object.assign({},data.data);
            let tab = {
              title:'新增客户信息',
              name:data.type+'_'+data.data.tabIndex,
              index:data.data.tabIndex,
              type:data.type,
              closable:true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          }else if(data.type == 'editCustomer'){
            let isAddTab = true;
            for(let tab in this.TABS){
              if(this.TABS[tab].index == data.data.cust_code){
                isAddTab = false;
                break
              }
            }
            if(isAddTab){
              data.data.tabIndex = data.data.cust_code;
              this.editCustomerData[data.data.cust_code] = Object.assign({},data.data);
              let tab = {
                title:'编辑客户信息',
                name:data.type+'_'+data.data.cust_code,
                index:data.data.cust_code,
                type:data.type,
                closable:true
              };
              this.currentTab = tab.name;
              this.TABS.push(tab);
            }else{
              this.currentTab = data.type+'_'+data.data.cust_code;
            }
          }
        }
      },
      saveEdit:function (data) {
        this.editData = data;
      },
      cancelTab:function (tabName) {
        this.removeTab(tabName);
      },
      removeTab:function (targetName) {
        for(let tab in this.TABS){
          if(this.TABS[tab].name == targetName){
            if(targetName.indexOf('addCustomer_') != -1){//关闭新增标签
              delete this.addCustomerData[this.TABS[tab].index]
            }else if(targetName.indexOf('editCustomer_') != -1){
              delete this.editCustomerData[this.TABS[tab].index]
            }
            this.TABS.splice(tab,1);
            this.currentTab = 'main';
            break
          }
        }
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .customer_contain,.customer_main{
    height: 100%;
  }
</style>
