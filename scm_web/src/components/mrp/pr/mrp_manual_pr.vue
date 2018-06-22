<template>
  <material_stock :stockType="3"></material_stock>
</template>
<script>
  import material_stock from '../common/material_stock/material_stock.vue'
  export default{
    name:'mrp_manual_pr',
    components: {
      material_stock
    },
    data () {
      return {
      }
    }
  }
</script>
