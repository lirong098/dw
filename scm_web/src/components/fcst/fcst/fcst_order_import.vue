<template>
  <div id="fcst_import">
    <sampleUpload :importType="3"></sampleUpload>
  </div>
</template>
<script>
  import sampleUpload from '../sampling/sampleUpload.vue'
  export default{
    name:'fcst_order_import',
    components: {
      sampleUpload
    }
  }
</script>
