<template>
  <div class="add_project">
    <el-dialog
      title="新建项目"
      :visible.sync="showAddProject"
      width="40%"
      :before-close="handleClose">
      <el-form :model="addprojectData" :rules="rules" ref="addprojectData" label-width="80px">
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="addprojectData.project_name"></el-input>
        </el-form-item>
        <el-form-item label="访问级别" prop="public">
          <!-- <el-input v-model="addprojectData.public"></el-input> -->
          <el-radio v-model.number="addprojectData.public" :label="0">私有</el-radio>
          <el-tooltip placement="bottom">
            <div slot="content">当项目设为公开后，任何人都有此项目下镜像的读权限。<br/>命令行用户不需要“docker login”就可以拉取此项目下的镜像。</div>
            <el-radio v-model.number="addprojectData.public" :label="1">公开</el-radio>
          </el-tooltip>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="submitForm('addprojectData')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: 'add_project',
  components: {},
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      showAddProject: this.value,
      addprojectData: {
        public: 0
      },
      rules: {
        project_name: [{ required: true, message: '请填写项目名称', trigger: 'blur' }]
      }
    }
  },
  computed: {},
  created () {},
  mounted () {},
  methods: {
    cancel () {
      // this.showAddProject = false
      this.$emit('input', false)
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          this.cancel()
          done()
        })
        .catch(_ => {})
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$api.project.projects('post', this.addprojectData).then(res => {
            if (res.status === 201) {
              // this.showAddProject = false
              this.$message({
                message: '保存成功',
                type: 'success'
              })
              this.$emit('success')
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  },
  updated () {},
  watch: {
    value (val, old) {
      this.showAddProject = val
    }
  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scope>
</style>
