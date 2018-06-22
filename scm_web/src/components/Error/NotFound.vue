<template>
    <div class="wrapper">
       <div class="container">
         <img class="png" src="/statics/img/404.png"
              alt="404">
         <img class="png msg" src="/statics/img/404_msg.png"
              alt="404msg">
         <p>
           <a href="javascript:void(0)">
             <img src="/statics/img/404_to_index.png"
                  @click="goToIndex"
                  alt="route">
           </a>
         </p>
       </div>
      <div class="cloud"></div>
    </div>
</template>

<script>
    export default {
      name:'v-error',
      methods:{
        goToIndex:function () {
          this.$router.push('/forecasesheet');
        }
      }
    }
</script>
<style scoped scoped lang="scss" type="text/scss">
  .wrapper{
    background: url("/statics/img/error_bg.jpg") repeat-x scroll 0 0 #67ACE4;
    .container{
      margin: 0 auto;
      padding-top: 50px;
      text-align: center;
      width: 560px;
      img {
        border: medium none;
        margin-bottom: 50px;
      }
      .msg {
        margin-bottom: 65px;
      }
    }
    .cloud {
      background: url(/statics/img/error_cloud.png) repeat-x scroll 0 0
    transparent;
      bottom: 0;
      height: 170px;
      position: absolute;
      width: 100%;
    }
  }
</style>
