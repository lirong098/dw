<template>
  <material_stock :stockType="5"></material_stock>
</template>
<script>
  import material_stock from '../common/material_stock/material_stock.vue'
  export default{
    name:'mrp_stocktake_out',
    components: {
      material_stock
    },
    data () {
      return {
      }
    }
  }
</script>
