<template>
  <div class="mrp_preview">
    <div class="clearfix">
      <div class="card-header card-header-text">
        <h4>MRP预览</h4>
      </div>
      <div class="card_box">
        <el-table ref="multiple" border tooltip-effect="dark" show-overflow-tooltip="true" :data="fortableData"
                  @selection-change="SelectionChange">
          <el-table-column type="selection" width="55"></el-table-column>

          <el-table-column label="成衣Model" show-overflow-tooltip>
            <template scope="scope">
          <span
            v-if="scope.row.tableColumnShow">{{scope.row.clothes_model.model_code ? scope.row.clothes_model.model_code + "-" + scope.row.clothes_model.model_name + "-" + scope.row.clothes_model.spec.color : ""}}</span>
            </template>
          </el-table-column>
          <el-table-column label="备料形式" show-overflow-tooltip>
            <template scope="scope">
              <span v-if="scope.row.tableColumnShow">{{scope.row.pr_form_meta.meta_name}}</span>
            </template>
          </el-table-column>
          <el-table-column label="数量">
            <template scope="scope">
              <span v-if="scope.row.tableColumnShow">
                {{scope.row.quantity && (parseInt(scope.row.quantity) != scope.row.quantity) ? scope.row.quantity.toFixed(2) : scope.row.quantity}}
              </span>
            </template>
          </el-table-column>

          <el-table-column label="单位">
            <template scope="scope">
              <span v-if="scope.row.tableColumnShow">{{scope.row.clothes_model.unit_meta.meta_name}}</span>
            </template>
          </el-table-column>

          <el-table-column label="材料Model" show-overflow-tooltip>
            <template scope="scop">
              <span>{{scop.row.clothes_item.material_model.model_code ? scop.row.clothes_item.material_model.model_code + "-" + scop.row.clothes_item.material_model.model_name : ""}}</span>
            </template>
          </el-table-column>

          <el-table-column label="材料Item" show-overflow-tooltip>
            <template scope="scop">
          <span v-if="scop.row.clothes_item.material_item">
            {{scop.row.clothes_item.material_item.item_code ? scop.row.clothes_item.material_item.item_code + "-" + scop.row.clothes_item.material_item.item_name : ""}}
          </span>
            </template>
          </el-table-column>

          <el-table-column label="数量">
            <template scope="scop">
              <span>
                {{scop.row.clothes_item.quantity && (parseInt(scop.row.clothes_item.quantity) != scop.row.clothes_item.quantity) ? scop.row.clothes_item.quantity.toFixed(2) : scop.row.clothes_item.quantity}}
              </span>
            </template>
          </el-table-column>

          <el-table-column label="单位">
            <template scope="scop">
              <span>{{scop.row.clothes_item.material_model.unit_meta.meta_name}}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template scope="scope">
              <el-button type="text" @click="getBominfo(scope.row.bom_id,scope.row.clothes_model)">
                BOM
              </el-button>
              <!--<a href="/#/tailoring_bom_detailed?id=20" target="_blank">BOM</a>-->
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div class="click-button">
      <div class="el-card">
        <el-button type="danger" class="handle-del mr10" :data="multipleSelection" @click="againRequest">重新计算
        </el-button>
        <el-button type="success" class="handle-del mr10" :data="multipleSelection" @click="toMrpStockInfo">生成备料
        </el-button>
        <el-button type="text" class="handle-del mr10" :data="multipleSelection" @click="cancelPreview">取消</el-button>
      </div>
    </div>
  </div>
</template>
<script>
  //公共函数
  import {fetchAPI} from '../../../../utils/utils.js';
  import requst from "../../../common/vmrequst.js";

  export default {
    components: {},
    name: "mrp_preview",
    props: {
      TABSValue: String,//tag显示值
      tabIndex: Number,//tag显示值
      rowId: Number,
      fcstType: Number
    },
    data() {
      return {
        multipleSelection: [],//默认选中子表行所有数据集合
        nowModelId: 0,
        fortableData: [],
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex
      }
    },
    methods: {
      //选择后的数据用来生成备料
      SelectionChange(val) {
        this.multipleSelection = val;
      },
      //默认全选
      alltrue(fortableData) {
        this.fortableData.forEach(row => {
          this.$refs.multiple.toggleRowSelection(row);
        });
      },
      //修改数据属性
      updateItem() {
        if (this.fortableData.length === 0) return;
        let nowmodelId = 0;
        let nowMetaId = 0;
        for (let x in this.fortableData) {
          if (nowmodelId === this.fortableData[x].clothes_model.model_id && nowMetaId === this.fortableData[x].pr_form_meta.meta_id) {
            this.fortableData[x]['tableColumnShow'] = false;
          } else {
            this.fortableData[x]['tableColumnShow'] = true;
            nowmodelId = this.fortableData[x].clothes_model.model_id;
            nowMetaId = this.fortableData[x].pr_form_meta.meta_id;
          }
        }
      },
      //重新计算
      againRequest() {
        this.fortableData = [];
        this.request();
      },
      //取消预览
      cancelPreview() {
        this.$emit("CloseTab");
      },
      //生成备料
      toMrpStockInfo() {
        let mrp_pr_item = this.toMrpStockInfo_up_data(this.multipleSelection);
        let newTabName = ++this.chlidTabIndex + '';
        this.chlidTABSValue = newTabName;
        //请求唯一编号
        let mrp_pr_no = "";
        //网络请求编号
        fetchAPI("post", this.$store.state.NEW_API + "/api/mat_models/make_unique_no/", {type: "mrp"}, this).then(res => {
          if (res.data.code !== 0) return;
          mrp_pr_no = res.data.message;
          //网络请求类型
          return fetchAPI("get", this.$store.state.NEW_API + "/api/mat_models/metas/?parent_meta_code=mrp", null, this);
        }).then(res => {
          let watchChildTABS = {
            title: 'MRP备料管理',
            name: newTabName,
            closable: true,
            rowId: 0,
            rowState: 'change',
            tabName: "stockmanagement",
            resData: {
              mrp_pr: {
                mrp_pr_id: 0,
                mrp_pr_type_meta_id: {
                  meta_id: this.fcstType === 1 ? 20 : this.fcstType === 2 ? 21 : 19,
                  meta_code: "",
                  parent_meta_code: "",
                  meta_name: "",
                  extend: {}
                },
                mrp_pr_no: mrp_pr_no,
                delivery_date: "",
                spec: {},
                extend: {
                  get_metas_listdata: []
                }
              },
              mrp_pr_item: mrp_pr_item
            },
            selectData: res.data
          };
          console.log("asswssew2ewr", watchChildTABS.resData);
          this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, watchChildTABS);
        });
      },
      //生成备料 转化数据结构
      toMrpStockInfo_up_data(row) {
        let mrp_pr_item = [];
        row.forEach(rew => {
          mrp_pr_item.push({
            mrp_pr_item_id: 0,
            clothes_model: rew.clothes_model,
            material_item: {
              item_id: rew.clothes_item.material_item ? rew.clothes_item.material_item.item_id : "",
              model: rew.clothes_item.material_model,
              item_code: rew.clothes_item.material_item ? rew.clothes_item.material_item.item_code : "",
              item_name: rew.clothes_item.material_item ? rew.clothes_item.material_item.item_name : "",
              spec: rew.clothes_item.material_item ? rew.clothes_item.material_item.spec : {},
              extend: rew.clothes_item.material_item ? rew.clothes_item.material_item.extend : {}
            },
            mrp_quantity: rew.clothes_item.quantity,
            quantity: 0,
            spec: {},
            extend: {},
            mrp_pr: 0,
            deduction: 0,
            pr_form_meta: rew.pr_form_meta,
            addlocal: 0,
            restore: false,
          });
        });
        return mrp_pr_item;
      },
      //获取Bom详情
      getBominfo(id, model) {
        requst.bomdetails(id, this, model);
      },
      //网络请求预览数据
      request() {
        fetchAPI("post", this.$store.state.NEW_API + "/api/mat_models/mrp/", {fcst_pr_id: this.rowId}, this).then(res => {
          console.log("asas", res.data);
          for (let x in res.data) {
            if (res.data[x].material.length > 0) {
              for (let i in res.data[x].material) {
                this.fortableData.push({
                  clothes_model: res.data[x].clothes_model,
                  clothes_item: res.data[x].material[i],
                  pr_form_meta: res.data[x].pr_form_meta,
                  quantity: res.data[x].quantity,
                  bom_id: res.data[x].bom_id
                });
              }
            } else if (res.data[x].material.length === 0) {
              this.fortableData.push({
                clothes_model: res.data[x].clothes_model,
                clothes_item: {
                  material_item: {
                    item_code: "",
                    item_name: "",
                  },
                  material_model: {
                    model_code: "",
                    model_name: "",
                    model_id: 0,
                    spec: {color: ""},
                    unit_meta: {
                      meta_name: ""
                    }
                  },
                },
                pr_form_meta: res.data[x].pr_form_meta,
                quantity: res.data[x].quantity,
                bom_id: 0
              });
            }
          }
          this.updateItem();
          this.alltrue();
          let a = 2;
          let b = 2.30049383;
          console.log(typeof a);
          console.log(typeof b);
        });
      }
    },
    updated() {
    },
    created() {

    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      }
    },
    mounted() {
      this.request();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .mrp_preview {
    margin: 0 10px 10px 10px;
    display: flex;
    flex-flow: row;
    justify-content: space-between;
  }

  .clearfix {
    width: 87%;
    margin-top: 30px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid rgb(229, 209, 214);
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
    position: relative;
    .card_box {
      margin-top: 50px;
      margin-bottom: 30px;
      margin-left: 20px;
      margin-right: 20px;
    }
  }

  .click-button {
    width: 9%;
    position: fixed;
    right: 2%;
    margin-top: 30px;
    .el-card__body {
      padding-top: 0px;
    }
    .el-card {
      display: flex;
      flex-flow: column;
      align-items: center;
      padding: 20px;
      .el-button {
        margin: 0;
        font-size: 16px;
      }

      .el-button:nth-child(2) {
        margin-top: 10px;
        margin-bottom: 5px;
      }
      .el-button--text {
        width: 70px;
        text-align: center;
        color: #4db3ff;
        font-size: 18px;
      }
      .el-button--text:hover {
        color: #ec407a;
      }
    }
  }


</style>
