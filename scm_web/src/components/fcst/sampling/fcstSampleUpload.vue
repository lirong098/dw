<template>
  <div>
    <sampleUpload :importType="4"></sampleUpload>
  </div>
</template>
<script>
  import sampleUpload from './sampleUpload.vue'
  export default{
    name:'fcstSampleUpload',
    components: {
      sampleUpload
    }
  }
</script>
