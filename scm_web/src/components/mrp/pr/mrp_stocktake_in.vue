<template>
  <material_stock :stockType="4"></material_stock>
</template>
<script>
  import material_stock from '../common/material_stock/material_stock.vue'
  export default{
    name:'mrp_stocktake_in',
    components: {
      material_stock
    },
    data () {
      return {
      }
    }
  }
</script>
