<template>
  <div class="repository-setting">
    <h2 class="mb">镜像设置</h2>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="删除镜像" name="1">
        <el-row class="setting-del">
          <el-col :span="1" style="text-align: center;">
            <i class="el-icon-warning setting-del-icon"></i>
          </el-col>
          <el-col :span="20">
            <span>请注意，删除镜像将无法恢复！</span>
          </el-col>
          <el-col :span="3">
            <el-button @click="delRepository" icon="el-icon-delete" type="danger">删除镜像</el-button>
          </el-col>
        </el-row>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>
<script>
export default {
  name: 'repository-setting',
  data () {
    return {
      activeNames: ['1'],
      repository: {}
    }
  },
  updated () {
    // console.log(this.value)
  },
  created () {
    this.initParams(this.$route.params)
  },
  computed: {},
  methods: {
    delRepository () {
      this.$api.project.delRepository(this.repository.namespace + '/' + this.repository.name).then(res => {
        console.log(res)
      })
    },
    initParams (params) {
      console.log('params', params)
      this.repository = params
    },
    handleChange (name) {}
  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scope>
.repository-setting {
  .setting-del {
    height: 50px;
    line-height: 50px;
    background-color: #fdf6ec;
    .setting-del-icon {
      font-size: 16px;
      color: #e6a23c;
    }
  }
}
</style>
