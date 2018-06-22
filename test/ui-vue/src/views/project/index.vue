<template>
  <div class="project">
    <el-row class="project-title">
      <router-link class="back" :to="{ name: 'repositories' }">
        <i class="el-icon-arrow-left">返回</i>
      </router-link>
      <h1>{{project.namespace}}</h1>
    </el-row>
    <el-row>
      <el-card class="project-card">
        <el-row>
          <el-col class="project-nav" :span="2">
            <el-menu :default-active="menuActiveIndex" class="project-menu" @select="menuSelect" :collapse="isCollapse">
              <el-menu-item index="project_repositories">
                <i class="el-icon-tickets"></i>
                <span slot="title">标签</span>
              </el-menu-item>
              <el-menu-item index="project_setting">
                <i class="el-icon-setting"></i>
                <span slot="title">设置</span>
              </el-menu-item>
            </el-menu>
          </el-col>
          <el-col class="project-main" :span="22">
            <router-view></router-view>
          </el-col>
        </el-row>
      </el-card>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'project',
  data () {
    return {
      project: {
        namespace: '',
        name: ''
      },
      isCollapse: true,
      menuActiveIndex: 'project_repositories'
    }
  },
  computed: {},
  created () {
    this.initParams(this.$route)
  },
  mounted () {},
  methods: {
    initParams (route) {
      console.log('route', route)
      this.project = {
        namespace: route.params.namespace,
        name: route.params.name
      }
      this.menuActiveIndex = route.name
    },
    menuSelect (index, indexPath) {
      console.log('menuSelect', index, indexPath)
      this.$router.push({name: index, params: {namespace: this.project.namespace}})
    }
  },
  updated () {},
  watch: {}
}
</script>

<style rel="stylesheet/scss" lang="scss" scope>
.project {
  .project-title {
    height: 40px;
    margin: 10px;
    font-size: 26px;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    .back {
      font-size: 18px;
      color: white;
      position: absolute;
      top: 0px;
      left: 0px;
    }
  }
  .project-card {
    margin: 0 10px 10px 10px;
    .el-card__body {
      padding: 0;
    }
    .project-nav {
      width: 60px;
      .el-menu {
        width: 100%;
      }
    }
    .project-main {
      margin: 10px;
    }
  }
}
</style>
