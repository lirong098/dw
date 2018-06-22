<template>
  <div class="matr_contain">
    <div class="matr_main">
      <lazy-render>
        <el-tabs v-model="currentTab" type="card"
                 @tab-remove="removeTab">
          <el-tab-pane
            :closable="item.closable"
            v-for="(item, index) in TABS"
            :key="item.name"
            :label="item.title"
            :name="item.name"
          >
            <div v-if="item.name == 'main'">
              <materailsOrderMain @changeTabs="changeTabs"
                                  :isFresh="isFresh"
                                  @cancelTab="cancelTab"></materailsOrderMain>
            </div>
            <div
              v-else-if="addOrderData[item.index] && item.name == 'addOrder_'+addOrderData[item.index].tabIndex">
              <materailsOrderEdit @changeTabs="changeTabs"
                                  @cancelTab="cancelTab"
                                  @isUpdate="isUpdate"
                                  :customerData="customerData"
                                  :materialsType="materialsType"
                                  :currentTab="currentTab"
                                  :editOrder="addOrderData[item.index]"
                                  :modelData="modelData"
                                  :optType="item.type"></materailsOrderEdit>
            </div>
            <div
              v-else-if="editOrderData[item.index] && item.name == 'editOrder_'+editOrderData[item.index].tabIndex">
              <materailsOrderEdit @changeTabs="changeTabs"
                                  @cancelTab="cancelTab"
                                  @isUpdate="isUpdate"
                                  :customerData="customerData"
                                  :materialsType="materialsType"
                                  :currentTab="currentTab"
                                  :editOrder="editOrderData[item.index]"
                                  :modelData="modelData"
                                  :optType="item.type"></materailsOrderEdit>
            </div>
            <div v-else-if="addCustomerData[item.index] &&
          item.name == 'addCustomer_'+addCustomerData[item.index].tabIndex">
              <customerManageEdit @saveEdit="saveEditCustomer"
                                  @cancelTab="cancelTab"
                                  :editCustomer="addCustomerData[item.index]"
                                  :optType="item.type"></customerManageEdit>
            </div>
            <div v-else-if="addProductData[item.index] && item.name == 'addProduct_'+addProductData[item.index].tabIndex">
              <productInfoEdit @cancelTab="cancelTab"
                               @changeTabs="changeTabs"
                               @isUpdate="saveEditPrductInfo"
                               :customerData="customerData"
                               :currentCust="addProductData[item.index].currentCustCode"
                               :prsData="prsData"
                               :currentTab="currentTab"
                               :editProduct="addProductData[item.index]" :optType="item.type"></productInfoEdit>
            </div>
            <div v-else-if="editProductData[item.index] && item.name == 'editProduct_'+editProductData[item.index].tabIndex">
              <productInfoEdit @cancelTab="cancelTab"
                               @changeTabs="changeTabs"
                               @isUpdate="saveEditPrductInfo"
                               :customerData="customerData"
                               :currentCust="editProductData[item.index].currentCustCode"
                               :prsData="prsData"
                               :currentTab="currentTab"
                               :editProduct="editProductData[item.index]" :optType="item.type"></productInfoEdit>
            </div>
            <div
              v-else-if="addMaterailsruleData[item.index]
            && item.name ==
            'addMaterailsrule_'+addMaterailsruleData[item.index].tabIndex">
              <materailsRuleEdit
                @isUpdate="saveEditMaterialsRule"
                @cancelTab="cancelTab"
                @changeTabs="changeTabs"
                :materials="materials"
                :editMaterailsrule="addMaterailsruleData[item.index]" :optType="item.type"></materailsRuleEdit>
            </div>
            <div
              v-else-if="addmaterailsTypeData[item.index] && item.name == 'addmaterailsType_'+addmaterailsTypeData[item.index].tabIndex">
              <materailsTypeEdit
                @saveEdit="saveAddMaterialsType"
                @changeTabs="changeTabs"
                @cancelTab="cancelTab"
                :currentTab="currentTab"
                :editmaterailsType="addmaterailsTypeData[item.index]"
                :optType="item.type"></materailsTypeEdit>
            </div>
          </el-tab-pane>
        </el-tabs>
      </lazy-render>
    </div>
  </div>
</template>
<script>
  import materailsOrderMain from '../../components/MaterailsManage/materailsOrder_main.vue';
  import materailsOrderEdit from '../../components/MaterailsManage/materailsOrder_edit.vue';
  import customerManageEdit from '../../components/BasicMeta/customerManage_edit.vue';
  import productInfoEdit from '../../components/BasicMeta/productInfo_edit.vue';
  import materailsRuleEdit from '../../components/BasicMeta/materailsRule_edit.vue';
  import {fetchAPI} from '../../utils/utils';
  import materailsTypeEdit from '../../components/BasicMeta/materailsType_edit.vue';
  export default{
    name: 'materails-manage',
    components: {
      materailsOrderMain,
      materailsOrderEdit,
      customerManageEdit,
      productInfoEdit,
      materailsRuleEdit,
      materailsTypeEdit
    },
    data () {
      return {
        TABS: [],
        currentTab: '',
        optType: '',
        addOrderData: {},
        editOrderData: {},
        addCustomerData: {},
        addProductData: {},
        editProductData: {},
        addMaterailsruleData:{},
        addmaterailsTypeData:{},
        tabIndex: 1,
        modelData: [],
        customerData: [],
        prsData: [],
        materials:[],
        materialsType:[],
        isFresh: false
      }
    },
    computed: {},
    created() {
      let tab = [{
        title: this.$route.name,
        name: 'main',
        closable: false
      }];
      this.TABS = [].concat(tab);
      this.currentTab = 'main';
      this.getCustomerData();
      this.getMaterialsType();
//      this.getPrsData();
//      this.getMaterials();
    },
    methods: {
      getCustomerData: function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get', api +
          '/api/custom/custominfolist/', null, this).then((res) => {
          if (res && res.status == 200) {
            this.customerData = res.data;
          }
        });
      },
      getMaterialsType:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api + '/api/dict/meta/materials/',null,this).then((res) => {
          if (res && res.status == 200) {
            this.materialsType = res.data;
          }
        })
      },
      getPrsData: function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get', api +
          '/api/product/prs/', null, this).then((res) => {
          if (res && res.status == 200) {
            this.prsData = res.data;
          }
        });
      },
      getMaterials:function () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get', api + '/api/dict/meta/materials/', null, this).then((res) => {
          if (res && res.status == 200) {
            this.materials = res.data;
          }
        });
      },
      changeTabs: function (data) {
        if (data) {
          if (data.type == 'addOrder') {
            this.addOrderData[data.data.tabIndex] = Object.assign({}, data.data);
            let tab = {
              title: '新增备料单',
              name: data.type + '_' + data.data.tabIndex,
              index: data.data.tabIndex,
              type: data.type,
              closable: true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          } else if (data.type == 'editOrder') {
            let isAddTab = true;
            for (let tab in this.TABS) {
              if (this.TABS[tab].index == data.data.fcst_pr_id) {
                isAddTab = false;
                break
              }
            }
            if (isAddTab) {
              data.data.tabIndex = data.data.fcst_pr_id;
              this.editOrderData[data.data.fcst_pr_id] = Object.assign({}, data.data);
              let tab = {
                title: '编辑备料单',
                name: data.type + '_' + data.data.fcst_pr_id,
                index: data.data.fcst_pr_id,
                type: data.type,
                closable: true
              };
              this.currentTab = tab.name;
              this.TABS.push(tab);
            } else {
              this.currentTab = data.type + '_' + data.data.fcst_pr_id;
            }
          } else if (data.type == 'addCustomer') {
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
          } else if (data.type == 'addProduct') {
//            this.getPrsData();
            this.addProductData[data.data.tabIndex] = Object.assign({}, data.data);
            let tab = {
              title: '新增Model',
              name: data.type + '_' + data.data.tabIndex,
              index: data.data.tabIndex,
              type: data.type,
              closable: true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          } else if (data.type == 'editProduct') {
//            this.getPrsData();
            data.data.tabIndex = this.tabIndex;
            this.editProductData[data.data.tabIndex] = Object.assign({}, data.data);
            let tab = {
              title: '编辑Model',
              name: data.type + '_' + data.data.tabIndex,
              index: data.data.tabIndex,
              type: data.type,
              closable: true
            };
            this.tabIndex++;
            this.currentTab = tab.name;
            this.TABS.push(tab);
          }else if(data.type == 'addMaterailsrule'){
            data.data.tabIndex = this.tabIndex;
            this.addMaterailsruleData[data.data.tabIndex] = Object.assign({}, data.data);
            let tab = {
              title: '新增备料策略',
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
      isUpdate: function () {
        this.isFresh = !this.isFresh;
      },
      saveEditCustomer: function (data) {
        if (data.type == 'addCustomer') {
          const api = this.$store.state.DEV_API;
          fetchAPI('post', api +
            '/api/custom/custominfolist/', data.data, this).then((res) => {
            if (res && res.status == 201) {
              this.$message({
                message: '添加成功',
                type: 'success'
              });
              this.customerData.push(data.data);
              this.removeTab(data.type + '_' + data.data.tabIndex, data.data.parent_currentTab);
            }
          })
        }
      },
      saveEditPrductInfo: function (tabName, isFresh) {
        this.$message({
          message: '添加成功',
          type: 'success'
        });
        if (isFresh) {
          this.removeTab(tabName);
        }
      },
      saveEditMaterialsRule:function (type,flag) {
        this.prsData.length = 0;
//        this.getPrsData();
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
      cancelTab: function (tabName) {
        this.removeTab(tabName);
      },
      removeTab: function (targetName, parent_currentTab){
        for (let tab in this.TABS) {
          if (this.TABS[tab].name == targetName) {
            if (targetName.indexOf('addOrder_') != -1) {//关闭新增标签
              delete this.addOrderData[this.TABS[tab].index]
            } else if (targetName.indexOf('editOrder_') != -1) {
              delete this.editOrderData[this.TABS[tab].index]
            } else if (targetName.indexOf('addCustomer_')
              != -1) {
              delete this.addCustomerData[this.TABS[tab].index]
            } else if (targetName.indexOf('addProduct_') != -1) {
              delete this.addProductData[this.TABS[tab].index]
            } else if (targetName.indexOf('editProduct_') != -1) {
              delete this.editProductData[this.TABS[tab].index]
            } else if
            (targetName.indexOf('addMaterailsrule_') != -1) {
              delete this.addMaterailsruleData[this.TABS[tab].index]
            }else if(targetName.indexOf('addmaterailsType_') != -1){
              delete this.addmaterailsTypeData[this.TABS[tab].index]
            }
            this.TABS.splice(tab, 1);
            let hasParent = false;
            if (parent_currentTab) {
              for (let tab in this.TABS) {
                if (this.TABS[tab].name == parent_currentTab) {
                  hasParent = true;
                  break
                }
              }
            }
            this.currentTab = hasParent ?
              parent_currentTab : 'main';
            break
            }
          }
        }
      }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .matr_contain, .matr_main {
    height: 100%;
  }
</style>
