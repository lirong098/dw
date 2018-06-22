<template>
  <stock fcstName="预估备料" :fcstType="7">
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
