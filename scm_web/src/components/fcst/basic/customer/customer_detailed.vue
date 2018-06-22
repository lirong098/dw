<template>
  <div class="test_detailed_contain">
    <div class="fl test_detailed_main main-card-box">
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              客户信息
            </h4>
          </div>
          <el-card class="divCard">
            <el-col class="detailMessage">
              <el-form class="detaMessageForm"
                       :model="submitData"
                       ref="submitData">
                <el-col :span="12">
                  <el-form-item label="客户编码 :">
                    <el-input class="nochange"
                              v-show="checkstatus === 'look'"
                              v-text="submitData.customer_code">
                    </el-input>
                    <el-input class="nochange"
                              v-show="checkstatus === 'change' && detaMessageForm!==0"
                              v-text="submitData.customer_code">
                    </el-input>
                    <el-input class="truechange"
                              v-show="checkstatus === 'change' && detaMessageForm===0"
                              v-model="submitData.customer_code">
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="客户名称 :">
                    <el-input class="nochange"
                              v-show="checkstatus === 'look'"
                              v-text="submitData.customer_name">
                    </el-input>
                    <el-input class="truechange"
                              v-show="checkstatus === 'change'"
                              v-model="submitData.customer_name">
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-form>
            </el-col>
          </el-card>
        </div>
      </div>
      <div class="clearfix">
        <div class="card_box">
          <div class="card-header card-header-text">
            <h4>
              联系人信息
            </h4>
          </div>
          <div class="table">
            <el-card>
              <el-col class="composition">
                <el-table ref="submitData.extend.contacts"
                          :data="submitData.extend.contacts"
                          style="width: 100%;"
                          border
                          tooltip-effect="dark">
                  <el-table-column type="index"
                                   label="序号"
                                   width="70">
                  </el-table-column>
                  <el-table-column label="联系人"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="checkstatus === 'look'"
                                style="width: 100%;"
                                v-text="scope.row.contactor">
                      </el-input>
                      <el-input class="truechange"
                                style="width: 100%;"
                                v-show="checkstatus === 'change'"
                                :disabled="scope.row.removeStatus"
                                v-model="scope.row.contactor">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="电话"
                                   show-overflow-tooltip>
                    <template scope="scope">
                      <el-input v-show="checkstatus === 'look'"
                                style="width: 100%;"
                                v-text="scope.row.phone">
                      </el-input>
                      <el-input class="truechange"
                                v-show="checkstatus === 'change'"
                                style="width: 100%;"
                                :disabled="scope.row.removeStatus"
                                v-model="scope.row.phone">
                      </el-input>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作"
                                   v-if="checkstatus === 'change'"
                                   :width="150">
                    <template scope="scope">
                      <el-button size="small"
                                 @click="addrow(scope.$index,scope.row)"
                                 v-show="!scope.row.removeStatus && checkstatus === 'change'">
                        +
                      </el-button>
                      <el-button size="small"
                                 style="margin-right: 8px;"
                                 @click="remove(scope.$index,scope.row)"
                                 v-show="!scope.row.removeStatus && checkstatus === 'change'">
                        -
                      </el-button>
                      <el-button size="small"
                                 v-show="scope.row.removeStatus && checkstatus === 'change'"
                                 @click="changeremove(scope.$index,scope.row)">
                        恢复
                      </el-button>
                      <el-button size="small"
                                 @click="addrow(scope.$index,scope.row)"
                                 v-show="scope.row.removeStatus && checkstatus === 'change'">
                        +
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-card>
          </div>
          <!--<el-card>-->
            <!--<el-col class="composition">-->
              <!--<el-table ref="submitData.extend.contacts"-->
                        <!--:data="submitData.extend.contacts"-->
                        <!--style="width: 100%;"-->
                        <!--border-->
                        <!--tooltip-effect="dark">-->
                <!--<el-table-column type="index"-->
                                 <!--label="序号"-->
                                 <!--width="70">-->
                <!--</el-table-column>-->
                <!--<el-table-column label="联系人"-->
                                 <!--show-overflow-tooltip>-->
                  <!--<template scope="scope">-->
                    <!--<el-input v-show="checkstatus === 'look'"-->
                              <!--style="width: 100%;"-->
                              <!--v-text="scope.row.contactor">-->
                    <!--</el-input>-->
                    <!--<el-input class="truechange"-->
                              <!--style="width: 100%;"-->
                              <!--v-show="checkstatus === 'change'"-->
                              <!--:disabled="scope.row.removeStatus"-->
                              <!--v-model="scope.row.contactor">-->
                    <!--</el-input>-->
                  <!--</template>-->
                <!--</el-table-column>-->
                <!--<el-table-column label="电话"-->
                                 <!--show-overflow-tooltip>-->
                  <!--<template scope="scope">-->
                    <!--<el-input v-show="checkstatus === 'look'"-->
                              <!--style="width: 100%;"-->
                              <!--v-text="scope.row.phone">-->
                    <!--</el-input>-->
                    <!--<el-input class="truechange"-->
                              <!--v-show="checkstatus === 'change'"-->
                              <!--style="width: 100%;"-->
                              <!--:disabled="scope.row.removeStatus"-->
                              <!--v-model="scope.row.phone">-->
                    <!--</el-input>-->
                  <!--</template>-->
                <!--</el-table-column>-->
                <!--<el-table-column label="操作"-->
                                 <!--v-if="checkstatus === 'change'"-->
                                 <!--:width="150">-->
                  <!--<template scope="scope">-->
                    <!--<el-button size="small"-->
                               <!--@click="addrow(scope.$index,scope.row)"-->
                               <!--v-show="!scope.row.removeStatus && checkstatus === 'change'">-->
                      <!--+-->
                    <!--</el-button>-->
                    <!--<el-button size="small"-->
                               <!--style="margin-right: 8px;"-->
                               <!--@click="remove(scope.$index,scope.row)"-->
                               <!--v-show="!scope.row.removeStatus && checkstatus === 'change'">-->
                         <!-- - -->
                    <!--</el-button>-->
                    <!--<el-button size="small"-->
                               <!--v-show="scope.row.removeStatus && checkstatus === 'change'"-->
                               <!--@click="changeremove(scope.$index,scope.row)">-->
                      <!--恢复-->
                    <!--</el-button>-->
                    <!--<el-button size="small"-->
                               <!--@click="addrow(scope.$index,scope.row)"-->
                               <!--v-show="scope.row.removeStatus && checkstatus === 'change'">-->
                      <!--+-->
                    <!--</el-button>-->
                  <!--</template>-->
                <!--</el-table-column>-->
              <!--</el-table>-->
            <!--</el-col>-->
          <!--</el-card>-->
        </div>
      </div>
    </div>
    <!--操作按钮-->
    <div class=" click-button">
      <el-card class="extra_card" v-show="checkstatus === 'look'">
        <el-button type="danger"
                   size="large"
                   @click="addtab">新增
        </el-button>
        <el-button type="primary"
                   size="large"
                   @click="changeBtn">修改
        </el-button>
        <el-button type="error"
                   size="large"
                   style="border: 0; color: #4db3ff;"
                   @click="deleteMethod(detaMessageForm)">删除
        </el-button>
      </el-card>
      <el-card class="extra_card" v-show="checkstatus === 'change'">
        <el-button type="primary"
                   size="large"
                   @click="saveBtn">保存
        </el-button>
        <el-button type="danger"
                   size="large"
                   @click="saveBtnAdd">保存<br />新增
        </el-button>
        <el-button type="error"
                   size="large"
                   style="border: 0; color: #4db3ff;"
                   @click="goBack">取消
        </el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../../../utils/utils';
  import {returnMessage} from '../../../common/component.js';
//  import {keydown} from "../../../../components/common/component.js";
  export default {
    components: {

    },
    name: 'test-detailed',
    props: {
      TABS: Array,
      TABSValue: String,
      tabIndex: Number,
      rowMessage: Number,
      CloseTab: Function
    },
    data() {
      return {
        pagesize: 10, // 分页条数
        currentPage: 1,  // 页
        pagedatacount: 0,  // 总条数
        modelIndex: 0, // 点击当前行的下标
        chlidTABSValue: this.TABSValue,
        chlidTabIndex: this.tabIndex,
        chlidTABS: this.TABS,
        detaMessageForm: this.rowMessage,
        checkstatus: "", // 编辑状态: change, 查看状态: look
        // 初始化数据
        submitData: {
          customer_id: 0,
          customer_code: "",
          parent_customer: null,
          customer_name: "",
          spec: { },
          extend: {
            contacts: [
              {
                contactor: "",
                phone: "",
                removeStatus: false
              }
            ]
          }
        }
      }
    },
    methods: {
      addtab(){
        let newTabName = ++this.chlidTabIndex + '';
        let addChildTABS = {
          title: '客户 - 新增',
          name: newTabName,
          closable: true,
          rowId: 0,
        };
        this.chlidTABSValue = newTabName;
        this.$emit('changeTabMethod', this.chlidTabIndex, this.chlidTABSValue, addChildTABS);
      },
      addrow(index,row){
        let newrow = {
          contactor: "",
          phone: "",
          removeStatus: false,
        };
        this.submitData.extend.contacts.splice(index+1,0,newrow)
      },
      remove(index,row){
        this.modelIndex = index;
        console.log(this.submitData.extend.contacts);
        if(row.contactor === "" && row.phone === ""){
          if(this.submitData.extend.contacts.length>1) {
            this.submitData.extend.contacts.splice(index, 1);
          }
        } else {
          row.removeStatus = true;
        }
      },
      changeremove(index,row){
        row.removeStatus = false;
      },
      saveBtn(){
        console.log(this.submitData);
        const api = this.$store.state.NEW_API;
        if(this.submitData.customer_code === "" || this.submitData.customer_name === ""){
          returnMessage("请填写完整客户信息","error",this);
          return;
        }
        for(let x in this.submitData.extend.contacts){
          if((this.submitData.extend.contacts[x].contactor === "" || this.submitData.extend.contacts[x].phone === "")&&this.submitData.extend.contacts[x].removeStatus === false){
            returnMessage("请填写完整联系人信息","error",this);
            return;
          }
          if(this.submitData.extend.contacts[x].removeStatus === true){
            this.submitData.extend.contacts.splice(x, 1);
          }
        }
        for(let item of this.submitData.extend.contacts){
          delete item.removeStatus
        }
        if(this.detaMessageForm === 0){
          fetchAPI('post', api + '/api/customer/customers/', this.submitData , this).then((res) => {
            if (res && res.status == 200) {
              if(res.data.code === 1001){
                returnMessage("客户编码重复","error",this);
              }else{
                for(let item of res.data.extend.contacts){
                  item.removeStatus = false;
                }
                this.submitData = res.data;
                this.detaMessageForm = res.data.customer_id;
                this.checkstatus = "look";
              }
            }
          })
        }else {
          fetchAPI('put', api + '/api/customer/customer/', this.submitData , this).then((res) => {
            if (res && res.status == 200) {
              for(let item of res.data.extend.contacts){
                item.removeStatus = false;
              }
              this.submitData = res.data;
              this.detaMessageForm = res.data.customer_id;
              this.checkstatus = "look";
            }
          })
        }
      },
      goBack(){
        this.$confirm('此操作将不会保存已填写的数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          if(!this.detaMessageForm){
            this.$emit('CloseTab');
          }else {
            // 获取网络请求数据
            this.checkstatus = "look";
            const api = this.$store.state.NEW_API;
            fetchAPI('get', api + '/api/customer/customer/?customer_id='+this.detaMessageForm, null, this).then((res) => {
              if (res.status == 200) {
                console.log(res.data);
                if(!res.data.extend){
                  res.data.extend = {
                    contacts: [
                      {
                        contactor: "",
                        phone: "",
                        removeStatus: false
                      }
                    ]
                  }
                }
                for(let item of res.data.extend.contacts){
                  item.removeStatus = false;
                }
                this.submitData = res.data;
              }
            })
          }
        }).catch(()=> {
          returnMessage("已取消操作","info",this);
        });
      },
      saveBtnAdd(){
        const api = this.$store.state.NEW_API;
        if(this.submitData.customer_code === "" && this.submitData.customer_name === ""){
          returnMessage("请填写完整客户信息","error",this);
          return;
        }
        for(let x in this.submitData.extend.contacts){
          if(this.submitData.extend.contacts[x].contactor === "" || this.submitData.extend.contacts[x].phone === ""){
            returnMessage("请填写完整联系人信息","error",this);
            return;
          }
          if(this.submitData.extend.contacts[x].removeStatus === true){
            this.submitData.extend.contacts.splice(index, 1);
          }
        }
        for(let item of this.submitData.extend.contacts){
          delete item.removeStatus
        }
        if(this.detaMessageForm === 0){
          fetchAPI('post', api + '/api/customer/customers/', this.submitData , this).then((res) => {
            if (res && res.status == 200) {
              for(let item of res.data.extend.contacts){
                item.removeStatus = false;
              }
              this.submitData = res.data;
              this.detaMessageForm = res.data.customer_id;
              this.checkstatus = "look";
            }
          })
        }else {
          fetchAPI('put', api + '/api/customer/customer/', this.submitData , this).then((res) => {
            if (res && res.status == 200) {
              for(let item of res.data.extend.contacts){
                item.removeStatus = false;
              }
              this.submitData = res.data;
              this.detaMessageForm = res.data.customer_id;
              this.checkstatus = "look";
            }
          })
        }
        this.$emit('CloseTab');
        this.addtab()
      },
      changeBtn(){
        this.checkstatus = "change";
      },
      deleteMethod(id){
        this.$confirm('此操作将永久删除, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteArr = [];
          deleteArr.push(id);
          const api = this.$store.state.NEW_API;
          fetchAPI('delete', api + '/api/customer/customers/', {data: deleteArr}, this).then((res) => {
            if (res.status == 204) {
              returnMessage("删除成功","success",this);
              this.$emit('CloseTab');
            }
          });
        }).catch(() => {
          returnMessage("已取消操作","info",this);
        })
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
    updated() {
      let divname = 'table';
      this.keydown(2,divname);
    },
    computed: {

    },
    mounted() {
      if(this.detaMessageForm !== 0){
        this.checkstatus = "look";
        const api = this.$store.state.NEW_API;
        fetchAPI('get', api + '/api/customer/customer/?customer_id='+this.detaMessageForm, null, this).then((res) => {
          if (res&&res.status == 200) {
            console.log(res.data);
            if(!res.data.extend || JSON.stringify(res.data.extend) === '{}'){
              res.data.extend = {};
              res.data.extend.contacts = [
                {
                  contactor: "",
                  phone: "",
                  removeStatus: false
                }
              ]
            }
            this.submitData = res.data;
          }
        })
      }else {
        this.checkstatus = "change"
      }
    },
    created() {

    }
  }

</script>

<style scoped lang="scss" type="text/scss">
  .test_detailed_contain {
    height: 100%;
    padding: 0 10px 10px 10px;
    position: relative;
    .test_detailed_main {
      height: 100%;
      width:88%;
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
          .truechange {
            width: 60%;
            text-align: center;
          }
        }
      }
      .nochange {
        width: 60%;
        text-align: center;
        border-bottom: 1px solid #ccc;
      }
      .composition {
        border: 1px solid #ccc;
        margin-bottom: 40px;
        p {
          padding: 20px 0px 0px 30px;
          font-size: 24px;
          margin-bottom: 20px;
        }
        overflow: hidden;
      }
      overflow: hidden;
    }
    .click-button{
      width:9%;
      padding-top: 20px;
      position:fixed;
      right:2%;
      .extra_card{
        display: flex;
        flex-flow: column;
        align-items: center;
        .el-button{
          display:block;
          margin: 0;
        }
        .el-button:last-child{
          margin-top:10px;
        }
      }
    }
    .click-button{
      width:9%;
      padding-top: 20px;
      position:fixed;
      right:2%;
      .extra_card{
        display: flex;
        flex-flow: column;
        align-items: center;
        .el-button{
          display:block;
          margin: 0;
        }
        .el-button:nth-child(2){
          margin-top:10px;
        }
        .el-dropdown{
          width: 100%;
          height: 40px;
          line-height: 40px;
          font-size: 18px;
          text-align: center;
          color:#4db3ff;
          margin:5px 0 0 5px;
        }
      }
    }
    .extra_card{
      display: flex;
      flex-flow: column;
      align-items: center;
      .el-button{
        display:block;
        margin: 0;
      }
      .el-button:nth-child(2){
        margin-top:10px;
      }
      .el-dropdown{
        width: 100%;
        height: 40px;
        line-height: 40px;
        font-size: 18px;
        text-align: center;
        color:#4db3ff;
        margin:5px 0 0 5px;
      }
    }
  }
</style>
