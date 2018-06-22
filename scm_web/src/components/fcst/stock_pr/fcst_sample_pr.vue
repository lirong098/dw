<template>
  <stock fcstName="选样备料" :fcstType="6">
  </stock>
</template>
<script>
  import stock from '../common/pr_stock/stocklist.vue'
  export default{
    name:'new_product',
    components: {
      stock
    },
    data () {
      return {
      }
    }
  }
</script>
