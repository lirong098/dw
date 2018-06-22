<template>
  <div class="repository">
    <el-row class="repository-title">
      <router-link class="back" :to="{ name: 'repositories' }">
        <i class="el-icon-arrow-left">返回</i>
      </router-link>
      <h1>{{repository.namespace + ' / ' + repository.name}}</h1>
    </el-row>
    <el-row>
      <el-card class="repository-card">
        <el-col class="repository-nav" :span="2">
          <el-menu :default-active="menuActiveIndex" class="repository-menu" @select="menuSelect" :collapse="isCollapse">
            <el-menu-item index="repository_info">
              <i class="el-icon-info"></i>
              <span slot="title">信息</span>
            </el-menu-item>
            <el-menu-item index="repository_tags">
              <i class="el-icon-tickets"></i>
              <span slot="title">标签</span>
            </el-menu-item>
            <el-menu-item index="repository_setting">
              <i class="el-icon-setting"></i>
              <span slot="title">设置</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        <el-col class="repository-main" :span="22">
          <router-view></router-view>
        </el-col>
      </el-card>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'repository',
  props: {
    reData: {
      type: Object,
      default: () => ({})
    }
  },
  data () {
    return {
      repository: {
        namespace: '',
        name: ''
      },
      isCollapse: true,
      menuActiveIndex: 'repository_info'
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
      this.repository = {
        namespace: route.params.namespace,
        name: route.params.name
      }
      this.menuActiveIndex = this.$route.name
    },
    menuSelect (index, indexPath) {
      console.log('menuSelect', index, indexPath)
      this.$router.push({name: index, params: {namespace: this.repository.namespace, name: this.repository.name}})
    }
  },
  updated () {},
  watch: {}
}
</script>

<style rel="stylesheet/scss" lang="scss" scope>
.repository {
  .repository-title {
    height: 40px;
    margin: 10px;
    color: white;
    font-size: 26px;
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
  .repository-card {
    margin: 0 10px 10px 10px;
    .el-card__body {
      padding: 0;
    }
    .repository-nav {
      width: 60px;
      .el-menu {
        width: 100%;
      }
    }
    .repository-main {
      margin: 10px;
    }
  }
}
</style>
