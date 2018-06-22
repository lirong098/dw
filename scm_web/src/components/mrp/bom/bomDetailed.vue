<template>
  <div class="test_detailed_contain">
    <div class="test_detailed_main">
      <div class="head_tool toolbar">
        <div class="inline_block mb3">
          <div class="inline_block mb3"
               v-if="changeStatus === false && (detaMessageForm.rowId)">
            <el-button type="error"
                       @click="changesMethod">修改
            </el-button>
            <el-button type="danger"
                       @click="deleteMessageBtn">删除
            </el-button>
            <el-dialog title="提示"
                       :visible.sync="deleteDialogVisible"
                       size="tiny">
              <span>确认删除此条数据</span>
              <span slot="footer"
                    class="dialog-footer">
            <el-button @click="deleteFalse">取 消
            </el-button>
            <el-button type="primary"
                       @click="deleteTrue">确 定
            </el-button>
          </span>
            </el-dialog>
          </div>
          <div class="inline_block mb3"
               v-if="changeStatus !== false || !(detaMessageForm.rowId)">
            <el-button type="success"
                       @click="saveBtn">保存
            </el-button>
            <el-dialog title="提示"
                       :visible.sync="saveDialogVisible"
                       size="tiny">
              <span>确认提交信息</span>
              <span slot="footer" class="dialog-footer">
            <el-button @click="saveFalse">取 消
            </el-button>
            <el-button type="primary"
                       @click="saveTrue">确 定
            </el-button>
          </span>
            </el-dialog>
            <el-button type="error"
                       @click="closeChangesMetod">取消
            </el-button>
            <el-dialog title="提示"
                       :visible.sync="closeDialogVisible"
                       size="tiny">
              <span>取消后数据不会保存</span>
              <span slot="footer" class="dialog-footer">
            <el-button @click="closeChangesFalse">取 消</el-button>
            <el-button type="primary"
                       @click="closeChangesTrue">确 定</el-button>
          </span>
            </el-dialog>
          </div>
        </div>
      </div>

      <!--BOM信息 Start-->
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              BOM信息
            </h4>
          </div>
          <el-card>
            <el-col class="detailMessage">
              <el-form class="detaMessageForm"
                       :model="detaMessageForm.resData.bom"
                       ref="detaMessageForm.resData.bom"
                       label-width="100px">
                <!--BOM_NO-->
                <el-col :span="12">
                  <el-form-item label="BOM_NO：" prop="bom_no" v-if="(detaMessageForm.rowId)">
                    <el-input class="nochange"
                              v-text="detaMessageForm.resData.bom.bom_no"
                              v-show="changeStatus === false && (detaMessageForm.rowId)"
                              auto-complete="off">
                    </el-input>
                    <el-input class="truechange"
                              v-model="detaMessageForm.resData.bom.bom_no"
                              v-show="changeStatus !== false && (detaMessageForm.rowId)"
                              auto-complete="off">
                    </el-input>
                  </el-form-item>
                  <el-form-item label="BOM_NO：" prop="message" v-else-if="!(detaMessageForm.rowId)">
                    <el-input class="truechange"
                              :readonly="readonlyStatus"
                              v-model="detaMessageForm.resData.bom.bom_no"
                              auto-complete="off">
                    </el-input>
                  </el-form-item>
                </el-col>
                <!--BOM_NO end-->
                <!--Model_id start-->
                <el-col :span="12">
                  <el-form-item label="Model_name：" v-if="(detaMessageForm.rowId)">
                    <template scope="scope">
                    <el-input class="nochange"
                              v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="detaMessageForm.resData.bom.model_id.model_name"
                              auto-complete="off">
                    </el-input>
                    <el-input class="truechange"
                              v-show="changeStatus !== false || !(detaMessageForm.rowId)"
                              v-model="detaMessageForm.resData.bom.model_id.model_name"
                              readonly
                              icon="more"
                              :on-icon-click="event => modelIconClick(event, scope.$index, scope.row)"
                              @click="modelIdAddBtn = true">
                    </el-input>
                    </template>
                  </el-form-item>
                  <el-form-item label="Model_name：" v-else-if="!(detaMessageForm.rowId)">
                    <template scope="scope">
                      <el-input class="truechange"
                                readonly
                                auto-complete="off"
                                v-model="detaMessageForm.resData.bom.model_id.model_name"
                                icon="more"
                                :on-icon-click="event => modelIconClick(event, scope.$index, scope.row)"
                                @click="modelIdAddBtn = true">
                      </el-input>
                    </template>
                  </el-form-item>
                </el-col>
                <!--Model_id end-->
                <!-- -->
                <el-col :span="12">
                  <el-form-item label="颜色：" prop="" v-if="(detaMessageForm.rowId)">
                    <el-input class="nochange"
                              v-text="detaMessageForm.resData.bom.spec.color"
                              v-show="changeStatus === false && (detaMessageForm.rowId)"
                              auto-complete="off">
                    </el-input>
                    <el-input class="truechange"
                              v-show="changeStatus !== false || !(detaMessageForm.rowId)"
                              v-model="detaMessageForm.resData.bom.spec.color"
                              auto-complete="off">
                    </el-input>
                  </el-form-item>
                  <el-form-item label="颜色：" prop="" v-else-if="!(detaMessageForm.rowId)">
                    <el-input class="truechange"
                              :readonly="readonlyStatus"
                              v-model="detaMessageForm.resData.bom.spec.color"
                              auto-complete="off">
                    </el-input>
                  </el-form-item>
                </el-col>
                <!-- -->
                <!--item_id start-->
                <el-col :span="12">
                  <el-form-item label="item_name：" prop="" v-if="(detaMessageForm.rowId)">
                    <template scope="scope">
                      <el-input class="nochange"
                                v-text="detaMessageForm.resData.bom.item_id.item_name"
                                v-show="changeStatus === false && (detaMessageForm.rowId)"
                                auto-complete="off">
                      </el-input>
                      <el-input class="truechange"
                                v-show="changeStatus !== false || !(detaMessageForm.rowId)"
                                v-model="detaMessageForm.resData.bom.item_id.item_name"
                                auto-complete="off"
                                readonly
                                icon="more"
                                :on-icon-click="event => itemIconClick(event, scope.$index, scope.row)"
                                @click="itemIdAddBtn = true">
                      </el-input>
                    </template>
                  </el-form-item>
                  <el-form-item label="item_name：" v-else-if="!(detaMessageForm.rowId)">
                    <template scope="scope">
                      <el-input class="truechange"
                                auto-complete="off"
                                readonly
                                v-model="detaMessageForm.resData.bom.item_id.item_name"
                                icon="more"
                                :on-icon-click="event => itemIconClick(event, scope.$index, scope.row)"
                                @click="itemIdAddBtn = true">
                      </el-input>
                    </template>
                  </el-form-item>
                </el-col>
                <!--item_id end-->
              </el-form>
            </el-col>
          </el-card>
        </div>
      </div>
      <!--BOM信息 End-->
      <!--BOM_model信息 Start-->
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              BOM_item信息
            </h4>
          </div>
          <el-card>
            <el-col class="composition">
              <el-table ref="multipleTable"
                        :data="(detaMessageForm.rowId)?mlTableData:tableMlNullData"
                        border
                        tooltip-effect="dark"
                        style="width: 100%">
                <el-table-column type="index"
                                 label=" "
                                 width="50">
                </el-table-column>
                <el-table-column label="model_id"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_id">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_id">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="meta_name"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_type_meta_id.meta_name">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_type_meta_id.meta_name">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="model_code"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_code">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_code">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="model_name"
                                 :width="formLabelWidth"
                                 show-overflow-tooltip>
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_model.model_name">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-model="scope.row.component_model.model_name"
                              :readonly="true"
                              icon="more"
                              @click="bomItemModel(scope.$index, scope.row)">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="item_id"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_item.item_id">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-text="scope.row.component_item.item_id">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="item_code"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_item.item_code">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-text="scope.row.component_item.item_code">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="item_name"
                                 :width="formLabelWidth"
                                 show-overflow-tooltip>
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.component_item.item_name">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-model="scope.row.component_item.item_name"
                              :readonly="true"
                              icon="more"
                              @click="bomItemItem(scope.$index, scope.row)">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="数量"
                                 :width="formLabelWidth">
                  <template scope="scope">
                    <el-input v-show="changeStatus === false && (detaMessageForm.rowId)"
                              v-text="scope.row.quantity">
                    </el-input>
                    <el-input v-show="changeStatus === true || !(detaMessageForm.rowId)"
                              v-model="scope.row.quantity">
                    </el-input>
                  </template>
                </el-table-column>
                <el-table-column label="操作"
                                 :width="250"
                                 :max-height="400"
                                 fixed="right">
                  <template scope="scope">
                    <el-button size="small"
                               @click="addCheckTab(scope.$index, scope.row)"
                               v-show="changeStatus === false && detaMessageForm.rowId">查看
                    </el-button>
                    <!--<el-button size="small"-->
                               <!--v-show="((!detaMessageForm.rowId)||(changeStatus !== false && detaMessageForm.rowId)) && scope.row.restore === false"-->
                               <!--@click="bomItemModel(scope.$index, scope.row)">-->
                      <!--Model-->
                    <!--</el-button>-->
                    <!--<el-button size="small"-->
                               <!--v-show="((!detaMessageForm.rowId)||(changeStatus !== false && detaMessageForm.rowId)) && scope.row.restore === false"-->
                               <!--@click="bomItemItem(scope.$index, scope.row)">-->
                      <!--Item-->
                    <!--</el-button>-->
                    <el-button size="small"
                               @click="addMessage(scope.$index,scope.row)"
                               v-show="((!detaMessageForm.rowId)||(changeStatus !== false && detaMessageForm.rowId)) && scope.row.restore === false">
                      +
                    </el-button>
                    <el-button size="small"
                               @click="removeMessage(scope.$index,scope.row)"
                               v-show="((!detaMessageForm.rowId)||(changeStatus !== false && detaMessageForm.rowId)) && scope.row.restore === false">
                      -
                    </el-button>
                    <el-button size="small"
                               @click="restoreBtn(scope.$index,scope.row)"
                               v-show="((!detaMessageForm.rowId)||(changeStatus !== false && detaMessageForm.rowId)) && scope.row.restore === true">
                      恢复
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-card>
          <!--BOM详情信息查看-->
          <el-dialog title="查看Model" style="float: left" :visible.sync="bomCheck" size="large" v-if="bomCheck">
            <tableDetailed :tabIndex= '1'
                           :rowId="rowData.component_model.model_id"
                           :tableName="rowData.component_model.model_name"
                           :tableType="rowData.component_model.model_type_meta_id.meta_id">
            </tableDetailed>
          </el-dialog>
          <!--BOMModel弹窗-->
          <el-dialog title="选择Model" style="float: left" :visible.sync="modelIdAddBtn" size="large">
            <el-table border :data="model">
              <el-table-column property="model_id" label="model_id"></el-table-column>
              <el-table-column property="model_name" label="model_name"></el-table-column>
              <el-table-column property="model_code" label="model_code"></el-table-column>
              <el-table-column property="extend.size" label="size"></el-table-column>
              <el-table-column label="操作"
                               :width="180"
                               fixed="right">
                <template scope="scope">
                  <el-button size="small"
                             @click="addModeliconClick(scope.$index, scope.row)">选择
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination_tool fr">
              <el-pagination
                @size-change="modelhandleSizeChange"
                @current-change="modelhandleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="pagesize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="pagedatacount">
              </el-pagination>
            </div>
          </el-dialog>
          <!--BOMItem弹窗-->
          <el-dialog title="选择Item" style="float: left" :visible.sync="itemIdAddBtn" size="large">
            <el-table border :data="item">
              <el-table-column property="item_id" label="item_id"></el-table-column>
              <el-table-column property="item_name" label="item_name"></el-table-column>
              <el-table-column property="model" label="model"></el-table-column>
              <el-table-column property="extend.size" label="size"></el-table-column>
              <el-table-column label="操作"
                               :width="180"
                               fixed="right">
                <template scope="scope">
                  <el-button size="small"
                             @click="addItemiconClick(scope.$index, scope.row)">选择
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-dialog>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../utils/utils';
  import tableDetailed from '../../common/model/new_table_detaied.vue';

  export default {
    components: {
      tableDetailed
    },
    name: 'test-detailed',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      rowMessage: Object,
      CloseTab: Function
    },
    // disabled: false 删除状态
    // restore: false 恢复按钮状态
    // delete字段存在就提交后端删除
    // addlocal 与 delete字段同时存在,不提交给后端
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 0,  // 总条数
        modelIdAddBtn: false, // model_id弹窗
        itemIdAddBtn: false, // item_id弹窗
        changeStatus: false, // 修改状态
        closeDialogVisible: false, // 关闭修改
        compositionDialogFormVisible: true, // 组成状态弹窗
        saveDialogVisible: false, // 保存按钮弹窗
        deleteDialogVisible: false, // 删除按钮弹窗
        bomCheck: false, // bom详情查看
        readonlyStatus: false,
        iconIndex: 0,
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        formLabelWidth: '150px',
        detaMessageForm: this.rowMessage,
        // 查看BOM_model数据
        mlTableData: this.rowMessage.resData.bom_item,
        // 新增按钮BOM_model数据
        tableMlNullData: [
          {
            component_model: {
              model_id: "",
              unit_meta: {
                meta_id: "",
                meta_code: "",
                parent_meta_code: "",
                meta_name: "",
                extend: {}
              },
              model_type_meta_id: "",
              model_code: "",
              model_name: "",
              spec: {},
              extend: {}
            },
            component_item: {
              item_id: "",
              item_code: "",
              item_name: "",
              spec: {},
              extend: {},
              model: ''
            },
            quantity: 0,
            spec: {},
            extend: {},
            addlocal: 0,
            disabled: false, //删除状态
            restore: false, // 恢复按钮状态
          }
        ],
        // BOM_model选择弹窗
        model:[],
        item:[],
        rules: {},
        rowData:{}
      }
    },
    methods: {
      // 点击修改按钮
      changesMethod() {
        this.changeStatus = true;
        this.saveDialogVisible = false;
        if(this.mlTableData.length < 1){
          let addMlTableData = {
            component_model: {
              model_id: "",
              unit_meta: {
                meta_id: "",
                meta_code: "",
                parent_meta_code: "",
                meta_name: "",
                extend: {}
              },
              model_type_meta_id: "",
              model_code: "",
              model_name: "",
              spec: {},
              extend: {}
            },
            component_item: {
              item_id: "",
              item_code: "",
              item_name: "",
              spec: {},
              extend: {},
              model: ""
            },
            quantity: 0,
            spec: {},
            extend: {},
            addlocal: 0,
            disabled: false, //删除状态
            restore: false, // 恢复按钮状态
          };
          this.mlTableData.push(addMlTableData);
        }
      },
      // 关闭修改
      closeChangesMetod() {
        this.closeDialogVisible = true;
      },
      closeChangesTrue() {
        this.closeDialogVisible = false;
        this.changeStatus = false;
        this.detaMessageForm = this.rowMessage;
        this.mlTableData = this.rowMessage.resData.bom_item;
        this.$message({
          showClose: true,
          message: '操作成功',
          type: 'success'
        });
      },
      closeChangesFalse() {
        this.closeDialogVisible = false;
        console.log("取消关闭,无动作", "2222");
      },
      // 保存按钮
      saveBtn() {
        this.saveDialogVisible = true;
      },
      // 保存确认
      saveTrue() {
        this.saveDialogVisible = true;
        this.changeStatus = false;
        this.saveDialogVisible = false;
        let notNUll = false;
        let notNullmlTableData = false;
        for(let item of this.tableMlNullData){
          if(!item.component_model.model_id || !item.component_item.item_id){
            notNUll = true;
            break;
          }
        }
        for(let item of this.mlTableData){
          if(!item.component_model.model_id || !item.component_item.item_id){
            notNullmlTableData = true;
            break;
          }
        }
        if(!this.detaMessageForm.rowId && notNUll){
          this.$message({
            showClose: true,
            message: 'BOM_item未填写完整',
            type: 'error'
          });
        }else if (!this.detaMessageForm.rowId && !notNUll) {
          const api =  this.$store.state.NEW_API;
          let creatBom = {
            bom: this.detaMessageForm.resData.bom,
            bom_item: this.tableMlNullData
          };
          for(let index in creatBom.bom_item){
            if(creatBom.bom_item[index].addlocal === 0 && creatBom.bom_item[index].delete === 0){
              creatBom.bom_item.splice(creatBom.bom_item[index],1)
            }
          }
          fetchAPI('post',api+'/api/mat_models/boms/',creatBom,this).then((res) => {
            if (res && res.status == 200) {
              if(res.data.code === 1001){
                this.$message({
                  showClose: true,
                  message: 'bom_no已存在',
                  type: 'error'
                });
              }else if(res.data.code === 500){
                console.log('服务器异常')
              }else if(res.data.code === 0){
                this.detaMessageForm.rowId = res.data.bom.bom_id;
                for (let item of res.data.bom_item){
                  item.disabled = false; //删除状态
                  item.restore =  false; // 恢复按钮状态
                }
                this.detaMessageForm.resData.bom = res.data.bom;
                this.mlTableData = res.data.bom_item;
              }
            }else {
              this.$message({
                showClose: true,
                message: '请填写完整信息',
                type: 'error'
              });
            }
          })
        }else if(this.detaMessageForm.rowId && notNullmlTableData){
          this.$message({
            showClose: true,
            message: 'BOM_item未填写完整',
            type: 'error'
          });
        }else if(this.detaMessageForm.rowId && !notNullmlTableData){
          const api =  this.$store.state.NEW_API;
          let creatBom = {
            bom: this.detaMessageForm.resData.bom,
            bom_item: this.mlTableData
          };
          for(let index in creatBom.bom_item){
            if(creatBom.bom_item[index].addlocal === 0 && creatBom.bom_item[index].delete === 0){
              creatBom.bom_item.splice(creatBom.bom_item[index],1)
            }
          }
          fetchAPI("put",api+"/api/mat_models/bom/",creatBom,this).then((res) => {
            if (res && res.status == 200) {
              this.refreshData(this.detaMessageForm.rowId);
              this.$message({
                showClose: true,
                message: '保存成功',
                type: 'success'
              });
            }
          })
        }
      },
      refreshData(bomId) {
        const api =  this.$store.state.NEW_API;
        let getBomDataMassage = {
          bom_id : bomId
        };
        fetchAPI('get',api+'/api/mat_models/bom/?bom_id='+bomId,getBomDataMassage,this).then((res) => {
          if(res&& res.status == 200){
            this.detaMessageForm.resData.bom = res.data;
            fetchAPI('get',api+'/api/mat_models/bom_items/?bom_id='+bomId,getBomDataMassage,this).then((res) => {
              if(res&& res.status == 200){
                for (let item of res.data){
                  item.disabled = false; //删除状态
                  item.restore =  false; // 恢复按钮状态
                }
                this.mlTableData = res.data;
                $(".content").scrollTop(0);
              }
            })
          }
        });
      },
      saveFalse() {
        this.saveDialogVisible = false;
        console.log("取消保存,无操作")
      },
      // 删除按钮
      deleteMessageBtn() {
        this.deleteDialogVisible = true;
      },
      deleteTrue() {
        let deleteData = [];
        deleteData.push(this.detaMessageForm.resData.bom.bom_id);
        const api =  this.$store.state.NEW_API;
        fetchAPI('delete', api + '/api/mat_models/boms/' , {data:deleteData}, this).then((res) => {
          if (res.status == 204) {
            this.$emit('CloseTab');
            this.$message({
              showClose: true,
              message: '删除成功',
              type: 'success'
            });
          }
        });
      },
      deleteFalse() {
        this.deleteDialogVisible = false;
      },
      // 添加组成
      addMessage(index, row) {
        let addMlTableData = {
          component_model: {
            model_id: "",
            unit_meta: {
              meta_id: "",
              meta_code: "",
              parent_meta_code: "",
              meta_name: "",
              extend: {}
            },
            model_type_meta_id: "",
            model_code: "",
            model_name: "",
            spec: {},
            extend: {}
          },
          component_item: {
            item_id: "",
            item_code: "",
            item_name: "",
            spec: {},
            extend: {},
            model: ""
          },
          quantity: 0,
          spec: {},
          extend: {},
          addlocal: 0,
          disabled: false, //删除状态
          restore: false, // 恢复按钮状态
        };
        if (this.detaMessageForm.rowId) {
          this.mlTableData.splice(index + 1, 0, addMlTableData);
        }else if (!this.detaMessageForm.rowId){
          this.tableMlNullData.splice(index + 1, 0, addMlTableData)
        }
      },
      // 删除组成
      removeMessage(index, row) {
        if (this.detaMessageForm.rowId) {
          if (row.addlocal === 0 && !row.component_model.model_id) {
            this.mlTableData.splice(index, 1);
          } else {
            this.mlTableData = this.mlTableData.map(function (currentValue) {
              if (row.component_model.model_id === currentValue.component_model.model_id && row.component_item.item_id === currentValue.component_item.item_id) {
                currentValue.disabled = true;
                currentValue.delete = 0;
                currentValue.restore = true;
              }
              return currentValue;
            });
          }
        } else if (!this.detaMessageForm.rowId) {
          if (row.addlocal === 0 && !row.component_model.model_id) {
            if(this.tableMlNullData.length > 1){
              this.tableMlNullData.splice(index, 1)
            }
          } else {
            this.tableMlNullData = this.tableMlNullData.map(function (currentValue) {
              if (row.component_model.model_id === currentValue.component_model.model_id && currentValue.component_model.model_id) {
                currentValue.disabled = true;
                currentValue.delete = 0;
                currentValue.restore = true;
              }
              return currentValue;
            })
          }
        }
      },
      // 恢复组成
      restoreBtn(index, row) {
        if (this.detaMessageForm.rowId) {
          this.mlTableData = this.mlTableData.map(function (currentValue) {
            if (row.component_model.model_id === currentValue.component_model.model_id) {
              currentValue.disabled = false;
              delete currentValue.delete;
              currentValue.restore = false;
            }
            return currentValue;
          });
        } else if (!this.detaMessageForm.rowId) {
          this.tableMlNullData = this.tableMlNullData.map(function (currentValue) {
            if (row.component_model.model_id === currentValue.component_model.model_id) {
              currentValue.disabled = false;
              delete currentValue.delete;
              currentValue.restore = false;
            }
            return currentValue;
          });
        }
      },
      // 点击BOMModel的icon图标
      bomItemModel(index,row){
        this.pagesize = 10; // 分页条数
        this.currentPage = 1;  // 页
        this.iconIndex = index;
        this.modelIdAddBtn = true;
        this.bom_select = false;
        this.bom_item_select = true;
        this.getModelId();
      },
      // 点击BOMModelItem的icon图标
      bomItemItem(index,row){
        this.iconIndex = index;
        this.itemIdAddBtn = true;
        this.bom_select = false;
        this.bom_item_select = true;
        if(row.component_model.model_id)
        this.getItemId(row.component_model.model_id);
      },
      // 点击model_id的icon图标
      getModelId() {
        const api =  this.$store.state.NEW_API;
        let getModeIdMassage = {
          page: this.currentPage,
          pagesize: this.pagesize,
        };
        fetchAPI('get',api+'/api/mat_models/models/?page='+this.currentPage+'&pagesize='+this.pagesize,getModeIdMassage,this).then((res) => {
          if (res && res.status == 200) {
            this.pagedatacount = res.data.total_number;
            if(this.bom_select){
              this.model = res.data.data;
            }else if(this.bom_item_select){
              this.model = res.data.data;
            }
          }
        })
      },
      modelIconClick(event,index,row) {
        this.modelIdAddBtn = true;
        this.bom_item_select = false;
        this.bom_select = true;
        this.getModelId();
      },
      // 分页
      modelhandleCurrentChange:function (val) {
        this.currentPage = val;
        this.getModelId();
      },
      modelhandleSizeChange:function (val) {
        this.pagesize = val;
        this.getModelId();
      },
      addModeliconClick(index,row){
        if(!this.bom_item_select){
          this.detaMessageForm.resData.bom.model_id = row;
          this.detaMessageForm.resData.bom.item_id = {};
          this.detaMessageForm.resData.bom.item_name = "";
          this.modelIdAddBtn = false;
        }else{
          if (this.detaMessageForm.rowId) {
            this.mlTableData[this.iconIndex].component_model = row;
            this.mlTableData[this.iconIndex].component_item = {};
            this.mlTableData[this.iconIndex].quantity = 0;
            this.modelIdAddBtn = false;
          } else if (!this.detaMessageForm.rowId) {
            this.tableMlNullData[this.iconIndex].component_model = row;
            this.tableMlNullData[this.iconIndex].component_item = {};
            this.tableMlNullData[this.iconIndex].quantity = 0;
            this.modelIdAddBtn = false;
          }
        }
      },
      // 点击item_id的icon图标
      getItemId(model_id) {
        let getItemIdMassage = {
          model_id: model_id
        };
        const api =  this.$store.state.NEW_API;
        fetchAPI('get',api+'/api/mat_models/items/?model_id='+model_id,getItemIdMassage,this).then((res) => {
          if (res && res.status == 200) {
            this.item = res.data;
          }
        })
      },
      itemIconClick() {
        if(!this.bom_item_select){
          if(this.detaMessageForm.resData.bom.model_id.model_id){
            this.getItemId(this.detaMessageForm.resData.bom.model_id.model_id);
            this.itemIdAddBtn = true;
          }else{
            this.itemIdAddBtn = false;
            this.$message({
              showClose: true,
              message: '请先选择Model_id',
              type: 'error'
            });
          }
        }
      },
      addItemiconClick(index,row){
        if(!this.bom_item_select){
          this.detaMessageForm.resData.bom.item_id = row;
          this.detaMessageForm.resData.bom.item_name = row.item_name;
          this.itemIdAddBtn = false;
        }else{
          if (this.detaMessageForm.rowId) {
            this.mlTableData[this.iconIndex].component_item = row;
            this.itemIdAddBtn = false;
          } else if (!this.detaMessageForm.rowId) {
            this.tableMlNullData[this.iconIndex].component_item = row;
            this.itemIdAddBtn = false;
          }
        }
      },
      // 点击查看按钮
      addCheckTab(index, row) {
        this.rowData = row;
        this.bomCheck = true;
      }
    },
    watch: {
      TABSValue(val) {
        this.chlidTABSValue = val;
      },
      tabIndex(val) {
        this.chlidTabIndex = val;
      },
      TABS(val) {
        this.chlidTABS = val;
      }
    },
    computed: {},
    mounted() {

    },
    created() {
      console.log('bomitem', this.detaMessageForm);
    }
  }

</script>

<style scoped lang="scss" type="text/scss">
  .test_detailed_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    .test_detailed_main {
      height: 100%;
      .mb3 {
        margin-bottom: 3px;
      }
      .detailMessage {
        border: 1px solid #ccc;
        margin-bottom: 30px;
        p {
          padding: 20px 0px 0px 30px;
          font-size: 24px;
        }
        .detaMessageForm {
          padding-left: 30px;
          margin-top: 10px;
          .nochange {
            width: 60%;
            text-align: center;
            border-bottom: 1px solid #ccc;
          }
          .truechange {
            width: 60%;
            text-align: center;
          }
        }
      }
      .composition {
        border: 1px solid #ccc;
        margin-bottom: 30px;
        p {
          padding: 20px 0px 0px 30px;
          font-size: 24px;
          margin-bottom: 20px;
        }
        .el-button--small {
          margin-left: 10px;
        }
      }
    }
    .btnright {
      float: right;
    }
  }
</style>
