<template>
  <div class="profile-wrap">
    <!--<div class="ms-title">个人信息</div>-->
    <!--<div class="ms-profile">-->
      <!--<el-form :label-position="labelPosition" label-width="80px" :model="Profile">-->
        <!--<el-form-item label="昵称">-->
          <!--<el-input v-model="Profile.username"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="姓名">-->
          <!--<el-input v-model="Profile.last_name"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="电话">-->
          <!--<el-input v-model="Profile.tel"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item label="Email">-->
          <!--<el-input v-model="Profile.email"></el-input>-->
        <!--</el-form-item>-->
        <!--<div class="editpwd-btn">-->
            <!--<el-button @click="submitForm">提交</el-button>-->
            <!--<el-button @click="resetForm">重置</el-button>-->
        <!--</div>-->
      <!--</el-form>-->
      <!--<div class="back"><a @click="back"-->
                           <!--href="javascript:void(0)"><i-->
        <!--class="el-icon-d-arrow-left"></i>回到首页</a></div>-->
    <!--</div>-->
    <div class="editprofile_main">
      <div class="card_box">
        <div class="card-header card-header-text">
          <h4>
            个人信息修改
          </h4>
        </div>
        <el-card>
          <el-form :model="Profile" ref="ruleForm2"
                   :rules="rules"
                   label-width="100px" class="demo-ruleForm">
            <el-form-item label="昵称" prop="username">
              <div class="edit_input_common">
                <el-input  v-model="Profile.username" auto-complete="off"></el-input>
              </div>
            </el-form-item>
            <el-form-item label="姓名" prop="last_name">
              <div class="edit_input_common">
                <el-input  v-model="Profile.last_name" auto-complete="off"></el-input>
              </div>
            </el-form-item>
            <el-form-item label="电话" prop="tel">
              <div class="edit_input_common">
                <el-input v-model.number="Profile.tel"></el-input>
              </div>
            </el-form-item>
            <el-form-item label="Email" prop="email">
              <div class="edit_input_common">
                <el-input v-model.number="Profile.email"></el-input>
              </div>
            </el-form-item>
            <el-form-item>
              <el-button type="danger"
                         @click="submitForm('ruleForm2')">提交
              </el-button>
              <el-button @click="resetForm()">重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
  import {fetchAPI} from '../../utils/utils';
  export default {
    data () {
      return {
        labelPosition: 'right',
        Profile: {
          username: '',
          last_name: '',
          tel: '',
          email: ''
        },
        rules: {
          username: [
            { required: true, message: '请输入昵称', trigger:
              'blur' }
          ]
        }
      }
    },
    methods: {
      getProfile () {
        const api = this.$store.state.DEV_API;
        fetchAPI('get',api + '/api/user/profile/',null,this).then(res => {
          if(res && res.status == 200){
            this.Profile.username = res.data.username;
            this.Profile.last_name = res.data.last_name;
            this.Profile.tel = res.data.tel;
            this.Profile.email = res.data.email;
          }
        })
      },
      submitForm () {
        const api = this.$store.state.DEV_API
        fetchAPI('put',api + '/api/user/profile/',this.Profile,this).then((res) => {
          if(res && res.status == 200){
            this.$cookie.set('profile', this.Profile.username,1);
            this.$store.commit('SET_USER_NAME',this.Profile.username)
            this.$message({
              message: '修改成功',
              type: 'success'
            });
          }
        })
      },
      back () {
        this.$router.push('/forecasesheet')
      },
      resetForm:function(){
        this.getProfile()
      }
    },
    created () {
      this.getProfile()
    }
  }
</script>

<style scoped>
    .profile-wrap{
        position: relative;
        width:100%;
        height:100%;
    }
    .editprofile_main{
      padding: 20px 0px 0 10px;
    }
    .ms-title{
        position: absolute;
        top:50%;
        width:100%;
        margin-top: -230px;
        text-align: center;
        font-size:30px;
        color: #3fa88f;

    }
    .ms-profile{
        position: absolute;
        left:50%;
        top:50%;
        width:400px;
        height:300px;
        margin:-150px 0 0 -250px;
        padding:40px;
        border-radius: 5px;
        background: #6ebcaa;
    }
    .editpwd-btn{
        text-align: right;
    }
    .editpwd-btn button{
        width:20%;
        height:36px;
    }
    .back{
      text-align: left;
      font-size: 12px;
      color: #ffffff;
    }
  .back a{
    color: #ffffff;
  }
</style>
