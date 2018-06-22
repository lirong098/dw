<template>
  <newTable :tableName="tableName"
            :tableType="tableType">
  </newTable>
</template>
<script>
  import newTable from '../mrp_model_common/new_table.vue'
  export default{
    name:'new_fabric',
    components: {
      newTable
    },
    data () {
      return {
        tableName: "辅料",
        tableType:3,
      }
    }
  }
</script>
