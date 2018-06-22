<template>
  <div class="customer_edit_contain">
    <div class="customer_edit_main">
      <div class="card_box">
        <div class="card-header card-header-text">
          <h4>
            客户信息
          </h4>
        </div>
        <el-card>
          <div class="head_title" v-if="optType == 'editCustomer'">
            <span>客户编码</span> {{editCustomerData.cust_code}}
          </div>
          <el-form :model="editCustomerData"
                   class="demo-form-inline"
                   label-width="80px" :rules="custRule"
                   ref="custForm">
            <el-form-item label="客户编码" v-if="optType ==
        'addCustomer'" prop="cust_code">
              <div class="edit_input_common">
                <el-input :maxlength="50"
                          v-model="editCustomerData.cust_code" placeholder="客户编码"></el-input>
              </div>
            </el-form-item>
            <el-form-item label="客户名称" prop="cust_name">
              <div class="edit_input_common">
                <el-input v-model="editCustomerData.cust_name" placeholder="客户名称"></el-input>
              </div>
            </el-form-item>
            <el-form-item label="联系人">
              <el-card class="box-card extra_card"
                       v-if="editCustomerData.contacts && editCustomerData.contacts.length">
                <div v-for="(item,index) in editCustomerData.contacts" class="text item">
                  <el-form :inline="true" :model="item"
                           class="demo-form-inline"
                           label-width="70px">
                    <el-form-item label="姓名">
                      <el-input v-model="item.contact_name" placeholder="姓名"></el-input>
                    </el-form-item>
                    <el-form-item label="电话">
                      <el-input v-model="item.contact_tel" placeholder="电话"></el-input>
                    </el-form-item>
                    <el-form-item>
                      <el-button-group>
                        <el-button type="primary" icon="plus" size="mini" @click="addContact(index)"></el-button>
                        <el-button type="danger" icon="delete" size="mini" @click="deleteContact(index)"></el-button>
                      </el-button-group>
                    </el-form-item>
                  </el-form>
                </div>
              </el-card>
              <div v-else>
                暂无客户联系方式,点击添加
                <el-button @click="addContact('')" :plain="true" type="info" size="mini">添加</el-button>
              </div>
            </el-form-item>
            <el-form-item label="客户地址" >
              <el-card class="box-card extra_card"
                       v-if="editCustomerData.addresses && editCustomerData.addresses.length">
                <div v-for="(item,index) in editCustomerData.addresses" class="text item">
                  <el-form :inline="true" :model="item"
                           class="demo-form-inline"
                           label-width="70px">
                    <el-form-item label="所属省份">
                      <el-input v-model="item.contact_province" placeholder="所属省份"></el-input>
                    </el-form-item>
                    <el-form-item label="详细地址">
                      <el-input v-model="item.contact_addre" placeholder="详细地址"></el-input>
                    </el-form-item>
                    <el-form-item>
                      <el-button-group>
                        <el-button type="primary" icon="plus" size="mini"  @click="addAddress(index)"></el-button>
                        <el-button type="danger" icon="delete" size="mini" @click="deleteAddress(index)"></el-button>
                      </el-button-group>
                    </el-form-item>
                  </el-form>
                </div>
              </el-card>
              <div v-else>
                暂无客户地址,点击添加
                <el-button @click="addAddress('')" :plain="true" type="info" size="mini">添加</el-button>
              </div>
            </el-form-item>
            <el-form-item>
              <div class="submit_btn">
                <el-button type="primary" @click="saveEdit" >保存
                </el-button>
                <el-button @click="cancelTab" >取消</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script>
  import {checCode} from '../../utils/utils';
  export default{
    name:'customer-manage-edit',
    props:{
      editCustomer:{
        type:Object
      },
      optType:{
        type:String
      }
    },
    components: {

    },
    data () {
      return {
        editCustomerData:Object.assign({},this.editCustomer),
        custRule:{
          cust_code:[
            { required: true, message: '客户编码必填',  trigger: 'blur' },
            {validator:checCode,trigger: 'blur'}
          ],
          cust_name:[
            { required: true, message: '客户名称必填',  trigger:'blur' },
          ]
        }
      }
    },
    computed:{

    },
    created() {

    },
    methods: {
      addContact:function (index) {
        let contact = {
          contact_name:'',
          contact_tel:''
        };
        if(this.editCustomerData.contacts && this.editCustomerData.contacts.length){
          if(index === ''){
            this.editCustomerData.contacts.push(contact);
          }else{
            index++;
            this.editCustomerData.contacts.splice(index,0,contact);
          }
        }else{
          let arr = [contact];
          this.editCustomerData.contacts = arr.slice();
        }
      },
      deleteContact:function (index) {
        this.editCustomerData.contacts.splice(index,1);
      },
      addAddress:function (index) {
        let addresses = {
          contact_province:'',
          contact_addre:''
        };
        if(this.editCustomerData.addresses && this.editCustomerData.addresses.length){
          if(index === ''){
            this.editCustomerData.addresses.push(addresses);
          }else{
            index++;
            this.editCustomerData.addresses.splice(index,0,addresses);
          }
        }else{
          let arr = [addresses];
          this.editCustomerData.addresses = arr.slice();
        }
      },
      deleteAddress:function (index) {
        this.editCustomerData.addresses.splice(index,1);
      },
      saveEdit:function () {
        let data = {
          type:this.optType,
          data:this.editCustomerData
        };
        this.$emit('saveEdit',data);
      },
      cancelTab:function () {
        this.$emit('cancelTab',this.optType+'_'+this.editCustomerData.tabIndex);
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .customer_edit_contain{
    height: 100%;
    padding:20px 10px 10px 10px;
    .customer_edit_main{
      height: 100%;
      .head_title{
        height: 28px;
        margin-top: 5px;
        span{
          font-size: 14px;
          color: rgb(72, 106, 106);
          line-height: 1;
          padding: 5px 10px 5px 12px;
          box-sizing: border-box;
        }
      }
      .edit_cust_input{

      }
    }
  }
</style>
