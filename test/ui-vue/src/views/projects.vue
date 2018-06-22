<template>
  <div class="projects">
    <el-card class="projects-card">
      <el-row class="projects-title">
        <h2>项目</h2>
      </el-row>
      <el-row class="projects-row" v-for="(item, key) in projects" :key="key">
        <el-col :span="3">
        </el-col>
        <el-col :span="21">
          <router-link :to="{name: 'project_repositories', params: {namespace: item.name}}">{{ item.name }}</router-link>
        </el-col>
      </el-row>
      <el-row class="projects-add" style="border-top:1px solid #D8d8d8;">
        <el-col :span="24">
          <el-button type="text" icon="el-icon-plus" style="width:100%;height:100%;font-size:16px;" @click="showDialog = true">创建项目</el-button>
        </el-col>
      </el-row>
    </el-card>
    <project-add v-model="showDialog" @success="successDialog"></project-add>
  </div>
</template>

<script>
import projectAdd from '@/views/project_add.vue'

export default {
  name: 'projects',
  components: {
    projectAdd
  },
  props: {},
  data () {
    return {
      projects: [],
      showDialog: false,
      q: ''
    }
  },
  computed: {},
  mounted () {},
  methods: {
    // 创建项目成功回调
    successDialog () {
      this.getProjects()
      this.showDialog = false
    },
    getProjects () {
      this.$api.project.projects().then(res => {
        console.log('projects', res)
        if (res.status === 200) {
          this.projects = res.data
        }
      })
    }
  },
  updated () {},
  watch: {},
  created () {
    this.getProjects()
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scope>
.projects {
  .projects-card {
    margin: 0 10px 10px 0;
    max-height: calc(99% - 90px);
    overflow-y: auto;
  }
  .projects-title {
    height: 40px;
    margin-top: 10px;
  }
  .projects-row {
    max-height: calc(99% - 90px);
    overflow-y: auto;
    text-align: left;
  }
  .projects-add {
    text-align: left;
  }
}
</style>
