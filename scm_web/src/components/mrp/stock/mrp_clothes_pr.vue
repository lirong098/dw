<template>
  <stock fcstName="成衣备料" :fcstType="1">
  </stock>
</template>
<script>
  import stock from '../mrp_stock/clothes_stock/stocklist.vue'
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
