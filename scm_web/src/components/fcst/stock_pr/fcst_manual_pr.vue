<template>
  <stock fcstName="手工备料" :fcstType="8">
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
