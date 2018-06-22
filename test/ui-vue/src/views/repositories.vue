<template>
  <div class="repositories">
    <el-row class="repositories-title">
      <h1>镜像列表</h1>
    </el-row>
    <el-row>
      <el-col :span="17">
        <el-card class="repositories-card">
          <dw-table
            class="repositories-table"
            :tableData="tableData"
            :tableColumns="tableColumns"
            :pagingTotal="pagingTotal"
            @getPagingData="getPagingData"
            :tableAttrs="tableAttrs">
            <template slot="search">
              <el-input
                class="mr"
                placeholder="search"
                v-model="q"
                @keyup.enter.native="searchQ">
                <i slot="suffix" class="el-input__icon el-icon-search" @click="searchQ"></i>
              </el-input>
            </template>
          </dw-table>
        </el-card>
      </el-col>
      <el-col :span="7">
        <projects></projects>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import dwTable from '@/components/table/dw_table.vue'
import projects from '@/views/projects.vue'
import { formatDate } from '@/global/means.js'

export default {
  name: 'repositories',
  components: {
    dwTable,
    projects
  },
  props: {},
  data () {
    return {
      pagingTotal: 20,
      page: 1,
      perPage: 20,
      tableData: [],
      tableColumns: [],
      tableAttrs: {},
      q: ''
    }
  },
  computed: {},
  mounted () {},
  methods: {
    searchQ () {
      if (!this.q && this.q !== '') return
      this.getRepositories({q: this.q})
    },
    getPagingData (page, perPage) {
      console.log(page, perPage, 'getPagingData')
      this.page = page
      this.perPage = perPage
      this.getRepositories()
    },
    getRepositories (search = {}) {
      search.page = this.page
      search.page_size = this.perPage
      this.$api.project.repositories(search).then(res => {
        console.log('getRepositories', res)
        if (res.status === 200) {
          this.pagingTotal = parseInt(res.headers['x-total-count'])
          this.tableData = res.data
        }
      })
    }
  },
  updated () {},
  watch: {},
  created () {
    this.getRepositories()
    this.tableColumns = [{
      cellType: 'slots',
      label: '镜像名称',
      renderCell: (props) => {
        return (
          <router-link to={{name: 'repository_info', params: {namespace: props.row.namespace, name: props.row.name}}}>{ props.row.namespace + ' / ' + props.row.name}</router-link>
        )
      }
    }, {
      cellType: 'slots',
      label: '最近修改时间',
      renderCell: (props) => {
        return (formatDate(props.row.update_time))
      }
    }, {
      prop: 'pull_count',
      label: '下载次数'
    }]
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scope>
.repositories {
  .repositories-title {
    height: 40px;
    margin: 10px;
    color: white;
    font-size: 26px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .repositories-card {
    margin: 0 10px 10px 10px;
    max-height: calc(99% - 90px);
    overflow-y: auto;
  }
}
</style>
