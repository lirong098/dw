<template>
  <div class="metas_contain">
    <div class="metas_main">
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
            <el-card>
              <div v-if="item.name == 'main'">
                <metasMain @changeTabs="changeTabs"
                           :editData="editData"
                           @cancelTab="cancelTab"></metasMain>
              </div>
              <div
                v-else-if="editMetasData[item.index] && item.name == 'editMetas_'+editMetasData[item.index].tabIndex">
                <metasEdit @saveEdit="saveEdit"
                           @changeTabs="changeTabs"
                           @cancelTab="cancelTab"
                           :currentTab="currentTab"
                           :editMetas="editMetasData[item.index]"
                           :optType="item.type"></metasEdit>
              </div>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </lazy-render>
    </div>
  </div>
</template>
<script>
  import metasMain from '../../components/BasicMeta/metas_main.vue';
  import metasEdit from '../../components/BasicMeta/metas_edit.vue';
  export default{
    name: 'metas-manage',
    components: {
      metasMain,
      metasEdit
    },
    data () {
      return {
        TABS: [],
        currentTab: '',
        optType: '',
        editMetasData: {},
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
          if (data.type == 'editMetas') {
            let isAddTab = true;
            for (let tab in this.TABS) {
              if (this.TABS[tab].index == data.data.meta_code) {
                isAddTab = false;
                break
              }
            }
            if (isAddTab) {
              data.data.tabIndex = data.data.meta_code;
              this.editMetasData[data.data.meta_code] = Object.assign({}, data.data);
              let tab = {
                title: '编辑默认值',
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
            if (targetName.indexOf('addMetas_') != -1) {//关闭新增标签
              delete this.addMetasData[this.TABS[tab].index]
            } else if (targetName.indexOf('editMetas_') != -1) {
              delete this.editMetasData[this.TABS[tab].index]
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
  .metas_contain, .metas_main {
    height: 100%;
  }
</style>
