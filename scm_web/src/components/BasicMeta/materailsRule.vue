<template>
  <div class="materailsrule_contain">
    <div class="materails_main">
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
              <materailsRuleMain @changeTabs="changeTabs"
                                 :isFresh="isFresh" @cancelTab="cancelTab"></materailsRuleMain>
            </div>
            <div v-else-if="addMaterailsruleData[item.index] && item.name == 'addMaterailsrule_'+addMaterailsruleData[item.index].tabIndex">
              <materailsRuleEdit @changeTabs="changeTabs"
                                 @cancelTab="cancelTab"
                                 @isUpdate="isUpdate"
                                 :materials="materials"
                                 :editMaterailsrule="addMaterailsruleData[item.index]" :optType="item.type"></materailsRuleEdit>
            </div>
            <div v-else-if="editMaterailsruleData[item.index] && item.name == 'editMaterailsrule_'+editMaterailsruleData[item.index].tabIndex">
              <materailsRuleEdit @cancelTab="cancelTab"
                                 @changeTabs="changeTabs"
                                 @isUpdate="isUpdate"
                                 :materials="materials"
                                 :editMaterailsrule="editMaterailsruleData[item.index]" :optType="item.type"></materailsRuleEdit>
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
  import materailsRuleMain from '../../components/BasicMeta/materailsRule_main.vue';
  import materailsRuleEdit from '../../components/BasicMeta/materailsRule_edit.vue';
  import materailsTypeEdit from '../../components/BasicMeta/materailsType_edit.vue';
  import {fetchAPI} from '../../utils/utils';
  export default{
    name:'materail-Rule',
    components: {
      materailsRuleMain,
      materailsRuleEdit,
      materailsTypeEdit
    },
    data () {
      return {
        TABS:[],
        currentTab:'',
        addMaterailsruleData:{},
        editMaterailsruleData:{},
        addmaterailsTypeData:{},
        materials:[],
        isFresh:false
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
//      this.getMaterials();
    },
    methods: {
      getMaterials:function () {
        this.materials.length = 0;
        const api = this.$store.state.DEV_API;
        fetchAPI('get', api + '/api/dict/meta/materials/', null, this).then((res) => {
          if (res && res.status == 200) {
            this.materials = res.data;
          }
        });
      },
      saveAddMaterialsType:function (data) {
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
      changeTabs:function (data) {
        if(data){
          if(data.type == 'addMaterailsrule'){
            this.addMaterailsruleData[data.data.tabIndex] = Object.assign({},data.data);
            let tab = {
              title:'新增备料策略信息',
              name:data.type+'_'+data.data.tabIndex,
              index:data.data.tabIndex,
              type:data.type,
              closable:true
            };
            this.currentTab = tab.name;
            this.TABS.push(tab);
          }else if(data.type == 'editMaterailsrule'){
            let isAddTab = true;
            for(let tab in this.TABS){
              if(this.TABS[tab].index == data.data.pr_method_id){
                isAddTab = false;
                break
              }
            }
            if(isAddTab){
              data.data.tabIndex = data.data.pr_method_id;
              this.editMaterailsruleData[data.data.pr_method_id] = Object.assign({},data.data);
              let tab = {
                title:'编辑备料策略信息',
                name:data.type+'_'+data.data.pr_method_id,
                index:data.data.pr_method_id,
                type:data.type,
                closable:true
              };
              this.currentTab = tab.name;
              this.TABS.push(tab);
            }else{
              this.currentTab = data.type+'_'+data.data.pr_method_id;
            }
          }else
              if(data.type == 'addmaterailsType'){
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
      isUpdate:function (){
        this.isFresh = !this.isFresh;
      },
      cancelTab:function (tabName) {
        this.removeTab(tabName);
      },
      removeTab:function (targetName) {
        for(let tab in this.TABS){
          if(this.TABS[tab].name == targetName){
            if(targetName.indexOf('addMaterailsrule_') != -1){//关闭新增标签
              delete this.addMaterailsruleData[this.TABS[tab].index]
            }else if(targetName.indexOf('editMaterailsrule_') != -1){
              delete this.editMaterailsruleData[this.TABS[tab].index]
            }else
                if(targetName.indexOf('addmaterailsType_') != -1){
              delete this.addmaterailsTypeData[this.TABS[tab].index]
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
  .materailsrule_contain,.materails_main{
    height: 100%;
  }
</style>
