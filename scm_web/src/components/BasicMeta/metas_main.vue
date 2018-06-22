<template>
  <div class="order_main_contain">
    <div class="order_main_main">
      <div class="table_content">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              默认配置
            </h4>
          </div>
          <el-card>
            <el-table :data="metasData"
                      ref="orderTable" v-loading.body="loading"
                      @selection-change="handleSelectionChange">
              <el-table-column prop="meta_name"
                               label="数据名称"></el-table-column>
              <el-table-column prop="meta_value"
                               label="默认值"></el-table-column>
              <el-table-column label="操作" width=80>
                <template scope="scope">
                  <el-button
                    size="small"
                    type="default"
                    @click="editMetas(scope.$index,
                scope.row)">编辑</el-button>
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
  import {fetchAPI} from '../../utils/utils';
  export default{
    name: 'metas-main',
    components: {},
    props: {
      editData: {
        type: Object
      }
    },
    data () {
      return {
        currentOrderType: '',
        metasData:[],
        multipleSelection: [],
        tabIndex: 1,
        loading:false
      }
    },
    computed: {},
    created() {
      this.getMetasData();
    },
    methods: {
      getMetasData: function () {
        this.loading = true;
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api+'/api/dict/meta/default/',null,this).then((res) => {
          if (res && res.status == 200) {
            this.metasData = res.data;
          }
          this.loading = false;
        })
      },
      changeOrderType:function (type) {
        this.loading = true;
        this.currentOrderType = type;
        this.getOrderData();
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      editMetas: function (index, row) {
        let data = {
            type: 'editMetas',
            data: row
        };
        this.$emit('changeTabs', data);
      }
    },
    watch: {
      editData(data) {
        if (data) {
          if (data.type == 'editMetas') {//编辑
            const api = this.$store.state.DEV_API;
            let metasPutData = [{
              meta_code:data.data.meta_code,
              meta_value: data.data.meta_value
            }];
            fetchAPI('put',api+'/api/dict/meta/default/',metasPutData,this).then((res) => {
              if(res && res.status == 200){
                for(let metaData in this.metasData){
                  if(this.metasData[metaData].meta_code == data.data.meta_code){
                    this.metasData[metaData].meta_value = data.data.meta_value
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
  .order_main_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    .order_main_main {
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
