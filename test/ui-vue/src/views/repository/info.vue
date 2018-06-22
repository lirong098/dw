<template>
  <div class="repository-info">
    <h2 class="mb">镜像详情</h2>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="描述" name="1">
        <el-row :gutter="10">
          <el-col :span="22">
            <mavon-editor v-model="repository.description" v-bind="mavonAttr" @save="save"/>
          </el-col>
          <el-col :span="2">
            <el-tooltip effect="dark" :content="showEdit ? '编辑' : '关闭编辑'" placement="bottom-start">
              <i class="el-icon-edit-outline repository-info-edit" @click="markdownEdit" v-if="showEdit"></i>
              <i class="el-icon-close repository-info-edit" @click="close" v-else></i>
            </el-tooltip>
          </el-col>
        </el-row>
      </el-collapse-item>
      <el-collapse-item title="下载" name="2">
        <div>用下面Docker命令下载这个镜像</div>
        <el-input :value="command" style="width: 600px;">
            <div class="el-input__icon" slot="suffix" v-clipboard="command" @success="handleSuccess" @error="handleError">
              <el-tooltip effect="dark" content="复制命令到剪贴板" placement="bottom-start">
                <svg-icon icon-class="clipboard"/>
              </el-tooltip>
            </div>
        </el-input>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>
<script>
const attr = {
  toolbarsFlag: false, // 工具栏是否显示
  placeholder: '请添加镜像描述',
  defaultOpen: 'preview', // edit： 默认展示编辑区域 ， preview： 默认展示预览区域 , 其他 = edit
  subfield: false, // true： 双栏(编辑预览同屏)， false： 单栏(编辑预览分屏)
  style: {
    'min-width': '100%',
    'min-height': '100%'
  }
}
export default {
  name: 'repository-info',
  data () {
    return {
      activeNames: ['1', '2'],
      mavonAttr: attr,
      showEdit: true,
      systeminfo: {},
      repository: {}
    }
  },
  updated () {
    // console.log(this.value)
  },
  created () {
    this.initParams(this.$route.params)
    this.getRepository(this.$route.params.namespace + '/' + this.$route.params.name)
    this.getSysteminfo()
  },
  computed: {
    command () {
      return 'docker pull ' + this.systeminfo.registry_url + '/' + this.repository.namespace + '/' + this.repository.name
    }
  },
  methods: {
    initParams (params) {
      console.log('params', params)
      this.repository = params
    },
    handleChange (activeNames) {
      console.log(activeNames)
    },
    handleSuccess () {
      this.$message({
        message: '复制成功',
        type: 'success'
      })
    },
    handleError () {
      this.$message.error('复制失败')
    },
    markdownEdit () {
      console.log('fdsfs')
      this.mavonAttr = {}
      this.showEdit = false
    },
    save (value, render) {
      console.log('dsdsdsds', value)
      if (!value || value === '') return
      this.$api.project.repository(this.repository.namespace + '/' + this.repository.name, {description: value}).then(res => {
        console.log(res)
      })
    },
    close () {
      this.mavonAttr = attr
      this.showEdit = true
    },
    getRepository (name) {
      this.$api.project.getRepository(name).then(res => {
        if (res.status === 200) {
          console.log(res)
          this.repository.description = res.data.description
        }
      })
    },
    getSysteminfo () {
      this.$api.project.systeminfo().then(res => {
        if (res.status === 200) {
          this.systeminfo = res.data
        }
      })
    }
  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scope>
.repository-info {
  .repository-info-edit {
    font-size: 20px;
    color: #757575;
  }
  .repository-info-edit:hover {
    font-weight:bold;
  }
  .el-input__suffix {
    color: #757575;
  }
}
</style>
