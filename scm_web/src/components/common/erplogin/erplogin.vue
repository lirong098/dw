<template>
  <!--<div>-->
    <!--<dw-date-picker v-model="date" :showWeek="false" mode="single"></dw-date-picker>-->
  <!--</div>-->
</template>
<script>
  //公共函数
  import {fetchAPI} from "../../../utils/utils.js";
  import showModal from '../messageBox.js';
  export default {
    components: {},
    name: "mrp_meta",
    props: {},
    data() {
      return {
        date:''
      }
    },
    methods: {
      tokenLogin(token, url) {
        fetchAPI('post', this.$store.state.NEW_API + '/api/user/tokenlogin/', {token: token}, this).then(
          res => {
            console.log('token请求', res)
            if (res.status === 200) {
              if(res.data.code ===0){
                this.$cookie.set('profile', res.data.user, 1);
                this.$cookie.set('orderType', 1212, 1);
                this.$store.commit('SET_USER_NAME', res.data.user);
                this.$router.push('/' + url);
              }else{
                this.login();
              }
            } else {
               this.login();
            }
          }
        )
      },
      login(){
        this.$router.push('/login');
      }
    },
    computed: {},
    updated() {
    },
    created() {
    },
    watch: {},
    mounted() {
      $.cookie('profile','admin',1)
      if(this.$route.query.token && this.$route.query.url) {
        this.tokenLogin(this.$route.query.token, this.$route.query.url)
      }else{
        this.login();
      }
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
</style>
