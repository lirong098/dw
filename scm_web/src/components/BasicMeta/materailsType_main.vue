<template>
  <div class="materailstype_main_contain">
    <div class="materailstype_main_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3 ">
          <el-input v-model="searchWord"
                    icon="close"
                    :on-icon-click="handleIconClick"
                    @keyup.enter.native="searchByWord"
                    placeholder="请输入物料编号或名称查询"></el-input>
        </div>
        <div class="inline_block mb3">
          <el-button type="primary" class="customer_add"
                     @click="addmaterailsType">添加
          </el-button>
        </div>
      </div>
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              物料列表
            </h4>
          </div>
          <el-card>
            <el-table :data="materailsTypeData"
                      ref="orderTable" v-loading.body="loading">
              <el-table-column prop="meta_code"
                               label="物料编号"></el-table-column>
              <el-table-column prop="meta_name"
                               label="物料名称"></el-table-column>
              <el-table-column label="操作" width=150>
                <template scope="scope">
                  <el-button
                    size="small"
                    @click="editmaterailsType(scope.$index, scope.row)">编辑</el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="deletematerailsType(scope.$index, scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {fetchAPI,checCode} from '../../utils/utils';
  export default{
    name: 'materailstype-main',
    components: {},
    props: {
      editData: {
        type: Object
      }
    },
    data () {
      return {
        currentOrderType: '',
        materailsTypeData:[],
        tabIndex: 1,
        loading:false,
        searchWord:''
      }
    },
    computed: {},
    created() {
      this.getmaterailsTypeData();
    },
    methods: {
      getmaterailsTypeData: function () {
        this.loading = true;
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api+'/api/dict/meta/materials/?search='+this.searchWord,null,this).then((res) => {
          if(res && res.status == 200){
            this.materailsTypeData = res.data;
          }
          this.loading = false;
        })
      },
      addmaterailsType: function(){
        let data = {
            type: 'addmaterailsType',
            data: {
              meta_code: '',
              meta_name: '',
              tabIndex:this.tabIndex
            }
        };
        this.tabIndex++;
        this.$emit('changeTabs',data);
      },
      editmaterailsType: function (index, row) {
        let data = {
            type: 'editmaterailsType',
            data: row
        };
        this.$emit('changeTabs', data);
      },
      deletematerailsType:function (index,row) {
        const api = this.$store.state.DEV_API;
        fetchAPI('delete',api +
          '/api/dict/meta/material/?meta_code='+row.meta_code,null,this).then((res) => {
          if(res && res.status == 204){
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.materailsTypeData.splice(index,1);
          }
        });
      },
      handleIconClick:function () {
        this.searchWord = '';
        this.getmaterailsTypeData();
      },
      searchByWord:function () {
        this.getmaterailsTypeData();
      }
    },
    watch: {
      editData(data) {
        if (data) {
          if(data.type == 'addmaterailsType'){
            const api = this.$store.state.DEV_API;
            fetchAPI('post',api +
              '/api/dict/meta/materials/',data.data,this).then((res) => {
              if(res && res.status == 201){
                this.$message({
                  message: '保存成功',
                  type: 'success'
                });
                this.materailsTypeData.push(data.data);
                this.$emit('cancelTab',data.type+'_'+data.data.tabIndex);
              }
            })
          }else if (data.type == 'editmaterailsType') {//编辑
            const api = this.$store.state.DEV_API;
            let metasPutData = {
              meta_name:data.data.meta_name
            }
            fetchAPI('put',api+'/api/dict/meta/material/?meta_code='+data.data.meta_code,metasPutData,this).then((res) => {
              if(res && res.status == 200){
                for(let materailsTypeIndex in this.materailsTypeData){
                  if(this.materailsTypeData[materailsTypeIndex].meta_code == data.data.meta_code){
                    this.materailsTypeData[materailsTypeIndex].meta_name = data.data.meta_name
                  }
                }
                this.$emit('cancelTab', data.type + '_' + data.data.tabIndex);
              }
            })
          }
        }
      }
    },
  }
</script>
<style scoped lang="scss" type="text/scss">
  .materailstype_main_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    .materailstype_main_main {
      height: 100%;
      .head_tool {
        .mb3 {
          margin-bottom: 3px;
        }
        .search_input {
          width: 150px;
        }
      }
      .table_content {

      }
    }
  }
</style>
