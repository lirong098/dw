<template>
  <div class="product_contain">
    <div class="product_main">
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
              <productInfoMain @changeTabs="changeTabs"
                               :customerData="customerData"
                               :isFresh="isFresh"
                               @cancelTab="cancelTab"></productInfoMain>
            </div>
            <div v-else-if="addProductData[item.index] && item.name == 'addProduct_'+addProductData[item.index].tabIndex">
              <productInfoEdit @cancelTab="cancelTab"
                               @changeTabs="changeTabs"
                               @isUpdate="isUpdate"
                               :customerData="customerData"
                               :prsData="prsData"
                               :currentTab="currentTab"
                               :editProduct="addProductData[item.index]" :optType="item.type"></productInfoEdit>
            </div>
            <div v-else-if="editProductData[item.index] && item.name == 'editProduct_'+editProductData[item.index].tabIndex">
              <productInfoEdit  @cancelTab="cancelTab"
                                @changeTabs="changeTabs"
                                @isUpdate="isUpdate"
                                :customerData="customerData"
                                :prsData="prsData"
                                :currentTab="currentTab"
                                :editProduct="editProductData[item.index]" :optType="item.type"></productInfoEdit>
            </div>
            <div v-else-if="addCustomerData[item.index] &&
          item.name == 'addCustomer_'+addCustomerData[item.index].tabIndex">
              <customerManageEdit @saveEdit="saveEditCustomer"
                                  @cancelTab="cancelTab"
                                  :editCustomer="addCustomerData[item.index]"
                                  :optType="item.type"></customerManageEdit>
            </div>
            <!--<div-->
              <!--v-else-if="addmaterailsTypeData[item.index] && item.name == 'addmaterailsType_'+addmaterailsTypeData[item.index].tabIndex">-->
              <!--<materailsTypeEdit-->
                <!--@saveEdit="saveAddMaterialsType"-->
                <!--@changeTabs="changeTabs"-->
                <!--@cancelTab="cancelTab"-->
                <!--:currentTab="currentTab"-->
                <!--:editmaterailsType="addmaterailsTypeData[item.index]"-->
                <!--:optType="item.type"></materailsTypeEdit>-->
            <!--</div>-->
          </el-tab-pane>
        </el-tabs>
      </lazy-render>
    </div>
  </div>
</template>
<script>
  import productInfoMain from '../../components/BasicMeta/productInfo_main.vue';
  import productInfoEdit from '../../components/BasicMeta/productInfo_edit.vue';
  import customerManageEdit from '../../components/BasicMeta/customerManage_edit.vue';
  import {fetchAPI} from '../../utils/utils';
  import materailsTypeEdit from '../../components/BasicMeta/materailsType_edit.vue';
  export default{
    name:'product-info',
    components: {
      productInfoMain,
      productInfoEdit,
      customerManageEdit,
      materailsTypeEdit
    },
    data () {
      return {
        TABS:[],
        currentTab:'',
        addProductData:{},
        editProductData:{},
        editData:{},
        customerData:[],
        prsData:[],
        materials:[],
        addCustomerData:{},
        addmaterailsTypeData:{},
        isFresh:false,
        tabIndex:1
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
      this.getCustomerData();
//      this.getPrsData();
//      this.getMaterials();
    },
    methods: {
      getCustomerData: function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/custom/custominfolist/',null,this).then((res)  => {
          if (res && res.status == 200) {
            this.customerData = res.data;
          }
        });
      },
      getPrsData:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/product/prs/',null,this).then((res)  => {
          if (res && res.status == 200) {
            this.prsData = res.data;
          }
        });
      },
      getMaterials:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api +
          '/api/dict/meta/materials/',null,this).then((res)  => {
          if (res && res.status == 200) {
            this.materials = res.data;
          }
        });
      },
      changeTabs:function (data) {
        if(data){
          if(data.type == 'addProduct'){
            this.addProductData[data.data.tabIndex] = Object.assign({},data.data);
            let tab = {
              title:'新增Model',
              name:data.type+'_'+data.data.tabIndex,
              index:data.data.tabIndex,
              type:data.type,
              closable:true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          }else if(data.type == 'editProduct'){
            let isAddTab = true;
            for(let tab in this.TABS){
              if(this.TABS[tab].index == data.data.model_code){
                isAddTab = false;
                break
              }
            }
            if(isAddTab){
              data.data.tabIndex = data.data.model_code;
              this.editProductData[data.data.model_code] = Object.assign({},data.data);
              let tab = {
                title:'编辑Model',
                name:data.type+'_'+data.data.model_code,
                index:data.data.model_code,
                type:data.type,
                closable:true
              };
              this.currentTab = tab.name;
              this.TABS.push(tab);
            }else{
              this.currentTab = data.type+'_'+data.data.model_code;
            }
          }else if(data.type == 'addCustomer'){
            data.data.tabIndex = this.tabIndex;
            this.addCustomerData[data.data.tabIndex] = Object.assign({}, data.data);
            let tab = {
              title: '新增客户信息',
              name: data.type + '_' + data.data.tabIndex,
              index: data.data.tabIndex,
              type: data.type,
              closable: true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
            this.tabIndex++;
          }else if(data.type == 'addmaterailsType'){
            this.addmaterailsTypeData[data.data.tabIndex] = Object.assign({},data.data);
            let tab = {
              title:'新增物料类型',
              name:data.type+'_'+data.data.tabIndex,
              index:data.data.tabIndex,
              type:data.type,
              closable:true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          }
        }
      },
      saveEditCustomer:function (data) {
        if(data.type == 'addCustomer'){
          const api = this.$store.state.DEV_API;
          fetchAPI('post',api +
            '/api/custom/custominfolist/',data.data,this).then((res) => {
            if(res && res.status == 201){
              this.customerData.push(data.data);
              this.removeTab(data.type+'_'+data.data.tabIndex,data.data.parent_currentTab);
            }
          })
        }
      },
      saveEditMaterialsRule:function (type,flag) {
        this.materials.length = 0;
//        this.getMaterials();
      },
      saveAddMaterialsType:function (data){
        const api = this.$store.state.DEV_API;
        fetchAPI('post',api +
          '/api/dict/meta/materials/',data.data,this).then((res) => {
          if(res && res.status == 201){
            this.$message({
              message: '保存成功',
              type: 'success'
            });
            this.materials.push(data.data);
            this.removeTab(data.type+'_'+data.data.tabIndex);
          }
        })
      },
      isUpdate:function () {
        this.isFresh = !this.isFresh;
      },
      cancelTab:function (tabName) {
        this.removeTab(tabName);
      },
      removeTab:function(targetName,parent_currentTab) {
        for(let tab in this.TABS){
          if(this.TABS[tab].name == targetName){
            if(targetName.indexOf('addProduct_') != -1){//关闭新增标签
              delete this.addProductData[this.TABS[tab].index]
            }else if(targetName.indexOf('editProduct_') != -1){
              delete this.editProductData[this.TABS[tab].index]
            }else if (targetName.indexOf('addCustomer_') != -1) {
              delete this.addCustomerData[this.TABS[tab].index]
            }else if(targetName.indexOf('addmaterailsType_') != -1){
              delete this.addmaterailsTypeData[this.TABS[tab].index]
            }
            this.TABS.splice(tab,1);
            let hasParent = false;
            if(parent_currentTab){
              for(let tab in this.TABS){
                if(this.TABS[tab].name == parent_currentTab){
                  hasParent = true;
                  break
                }
              }
            }
            this.currentTab = hasParent ? parent_currentTab : 'main';
            break
          }
        }
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .product_contain,.product_main{
    height: 100%;
  }
</style>
