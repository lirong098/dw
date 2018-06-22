<template>
  <div class="test_main_contain">
    <div class="test_main_main">
      <div class="head_tool toolbar toolmy">
        <el-col :span="24" style="height: 55px;">
          <el-form label-width="55px" style="height: 55px; width: 100%; display: inline-block; padding-right: 15%;">
            <!--<el-col :span="18">-->
            <!--<el-input style="width:220px;"-->
            <!--placeholder="输入编码或名称"-->
            <!--v-model="search"-->
            <!--:icon="search?'circle-close':'search'"-->
            <!--@change="query(search)"-->
            <!--:on-icon-click="circle_close">-->
            <!--</el-input>-->
            <!--</el-col>-->
            <el-form-item label="材料类型 :" style="float: left" labelWidth="90px">
              <el-select v-model="typeInitial" placeholder="请选择" @change="typeMethod(typeInitial)">
                <el-option
                  v-for="item in typeData"
                  :key="item.meta_id"
                  :label="item.meta_name"
                  :value="item.meta_id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-col>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              备料库存
            </h4>
          </div>
          <el-card>
            <el-table :data="getData"
                      v-loading="loading"
                      border
                      tooltip-effect="dark"
                      style="width: 100%">
              <el-table-column label="Model"
                               prop="customer_code">
                <template scope="scope">
                  <el-input v-text="scope.row.item.model.model_code">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="Model Name"
                               prop="customer_code">
                <template scope="scope">
                  <el-input v-text="scope.row.item.model.model_name">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="Item"
                               v-if="typeInitial !== 49"
                               prop="customer_name">
                <template scope="scope">
                  <el-input v-text="scope.row.item.item_code">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="Model Name"
                               v-if="typeInitial !== 49"
                               prop="customer_name">
                <template scope="scope">
                  <el-input v-text="scope.row.item.item_name">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="款号"
                               prop="customer_code">
                <template scope="scope">
                  <el-input v-text="scope.row.item.model.extend.iman_code?scope.row.item.model.extend.iman_code.value:''">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="客户"
                               prop="customer_code">
                <template scope="scope">
                  <el-input v-text="scope.row.item.model.customer && scope.row.item.model.customer.customer_name?scope.row.item.model.customer.customer_name:''">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="单位"
                               prop="customer_code">
                <template scope="scope">
                  <el-input v-text="scope.row.item.model.unit_meta.meta_name">
                  </el-input>
                </template>
              </el-table-column>
              <el-table-column label="件数"
                               prop="quantity">
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import {returnMessage} from '../../common/component.js';
  import COMMON from '../../common/common.js';

  export default {
    components: {},
    name: 'test-info-main',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      tableData: Array
    },
    data() {
      return {
        search: '',
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        value: '',
        childTableData: this.tableData,
        delBtnStatus: true,
        deleteData: [],
        getData: [],
        typeData: [],
        typeInitial: '',
        loading: false,
      }
    },
    methods: {
      // 初始获取BOM数据列表
      getList() {
        var _this = this;
        this.loading = true;
        fetchAPI('get', this.$store.state.NEW_API + '/api/newfcst/fcst_stock/?material_type_meta_id=' + this.typeInitial, null, this).then((res) => {
          if (res && res.status == 200) {
            console.log(res.data);
            this.getData = res.data;
            setTimeout(function () {
              _this.loading = false;
            }, 2000)
          }
        })
      },
      typeMethod(data) {
        this.typeInitial = data;
//        console.log(data,1);
        this.getList();
      },
      // 下拉选框发送请求
      selectChange(value) {
        console.log(value)
      },
      // 重组名称
      commonmethod(model) {
        if (model.model_id) {
          let keyArr = ['model_code', 'model_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          model.spec.color ? tempArr.push(model.spec.color) : '';
          return tempArr.join(' - ')
        }
        if (model.item_id) {
          let keyArr = ['item_code', 'item_name'];
          let tempArr = [];
          for (let i in keyArr) {
            if (model[keyArr[i]])
              tempArr.push(model[keyArr[i]]);
          }
          return tempArr.join(' - ');
        }
      },
      // 勾选
      handleSelectionChange(val) {
        this.deleteData = val;
      },
      // 搜索
      query(search) {
        this.search = search;
        this.getList();
      },
      circle_close() {
        this.search = '';
        this.getList();
      }
    },
    computed: {},
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
        if (this.chlidTABSValue == 1) {
          this.getList();
        }
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      },
      tableData(val) {
        this.childTableData = val;
      }
    },
    updated() {
      if (this.deleteData.length > 0) {
        this.delBtnStatus = false;
      } else {
        this.delBtnStatus = true;
      }
    },
    created() {
      COMMON.getMetaList(this, 48).then((res) => {
        if (res && res.status === 200) {
//          console.log(res.data);
          if (res.data.length > 0) {
            this.typeData = res.data;
            this.typeInitial = this.typeData[0].meta_id;
            this.getList();
          } else {
            this.typeData = [];
            this.typeInitial = '';
          }
        }
      });
    }
  }
</script>
<style lang="scss" type="text/scss">
  .test_main_contain {
    .toolmy {
      height: 50px;
    }
    .btnright {
      width: 100%;
      height: 90px;
      float: right;
      display: inline-block;
    }
  }
</style>
