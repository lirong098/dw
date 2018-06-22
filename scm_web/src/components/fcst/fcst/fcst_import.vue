<template>
  <div id="fcst_import">
    <sampleUpload :importType="1"></sampleUpload>
  </div>
</template>
<script>
  import sampleUpload from '../sampling/sampleUpload.vue'
  export default{
    name:'fcst_import',
    components: {
      sampleUpload
    }
  }
</script>
