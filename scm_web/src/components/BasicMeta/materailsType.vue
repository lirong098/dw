<template>
  <div class="materailstype_contain">
    <div class="materailstype_main">
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
            <materailsTypeMain @changeTabs="changeTabs"
                            :editData="editData"
                            @cancelTab="cancelTab"></materailsTypeMain>
          </div>
          <div
            v-else-if="addmaterailsTypeData[item.index] && item.name == 'addmaterailsType_'+addmaterailsTypeData[item.index].tabIndex">
            <materailsTypeEdit @saveEdit="saveEdit"
                            @changeTabs="changeTabs"
                            @cancelTab="cancelTab"
                            :currentTab="currentTab"
                            :editmaterailsType="addmaterailsTypeData[item.index]"
                            :optType="item.type"></materailsTypeEdit>
          </div>
          <div
            v-else-if="editmaterailsTypeData[item.index] && item.name == 'editmaterailsType_'+editmaterailsTypeData[item.index].tabIndex">
            <materailsTypeEdit @saveEdit="saveEdit"
                            @changeTabs="changeTabs"
                            @cancelTab="cancelTab"
                            :currentTab="currentTab"
                            :editmaterailsType="editmaterailsTypeData[item.index]"
                            :optType="item.type"></materailsTypeEdit>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import materailsTypeMain from '../../components/BasicMeta/materailsType_main.vue';
  import materailsTypeEdit from '../../components/BasicMeta/materailsType_edit.vue';
  export default{
    name: 'materailstype-manage',
    components: {
      materailsTypeMain,
      materailsTypeEdit
    },
    data () {
      return {
        TABS: [],
        currentTab: '',
        optType: '',
        addmaterailsTypeData:{},
        editmaterailsTypeData: {},
        editData: {},
        tabIndex:1
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
    },
    methods: {
      changeTabs: function (data) {
        if (data) {
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
          }else if (data.type == 'editmaterailsType') {
            let isAddTab = true;
            for (let tab in this.TABS) {
              if (this.TABS[tab].index == data.data.meta_code) {
                isAddTab = false;
                break
              }
            }
            if (isAddTab) {
              data.data.tabIndex = data.data.meta_code;
              this.editmaterailsTypeData[data.data.meta_code] = Object.assign({}, data.data);
              let tab = {
                title: '编辑物料类型',
                name: data.type + '_' + data.data.meta_code,
                index: data.data.meta_code,
                type: data.type,
                closable: true
              };
              this.currentTab = tab.name;
              this.TABS.push(tab);
            } else {
              this.currentTab = data.type + '_' + data.data.meta_code;
            }
          }
        }
      },
      saveEdit: function (data) {
        this.editData = data;
      },
      cancelTab: function (tabName) {
        this.removeTab(tabName);
      },
      removeTab: function (targetName,parent_currentTab) {
        for (let tab in this.TABS) {
          if (this.TABS[tab].name == targetName) {
            if (targetName.indexOf('addmaterailsTypeEdit_') != -1) {//关闭新增标签
              delete this.addmaterailsTypeData[this.TABS[tab].index]
            } else if (targetName.indexOf('editmaterailsTypeEdit_') != -1) {
              delete this.editmaterailsTypeData[this.TABS[tab].index]
            }
            this.TABS.splice(tab, 1);
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
  .materailstype_contain, .materailstype_main {
    height: 100%;
  }
</style>
