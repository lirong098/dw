<template>
  <newTable :tableName="tableName"
            :tableType="tableType">
  </newTable>
</template>
<script>
  import newTable from '../mrp_model_common/new_table.vue'
  export default{
    name:'new_product',
    components: {
      newTable
    },
    data () {
      return {
        tableName: "成衣",
        tableType:1,
      }
    }
  }
</script>
