<template>
  <div class="repository_tags">
    <h4 style="text-align:left; margin-bottom:10px;">标签</h4>
    <dw-table :tableData="tableData" :tableColumns="tableColumns" :pagingTotal="20" :isPagination="false" @getPagingData="getPagingData"></dw-table>
    <el-dialog
      :title="'Fetch Tag:' + tagForm.name"
      :visible.sync="showDialog"
      width="70%"
      :before-close="handleClose">
      <el-row>
        <el-col :span="3">Command:</el-col>
        <el-col :span="24">
          <el-input v-model="tagForm.command"></el-input>
        </el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button v-clipboard="tagForm.command" @success="handleSuccess" @error="handleError">Copy Command</el-button>
        <el-button  @click="showDialog = false">close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import dwTable from '@/components/table/dw_table.vue'

export default {
  name: '',
  components: {
    dwTable
  },
  props: {
    parentInfo: {
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
      parentData: this.parentInfo,
      tableData: [],
      tableColumns: [],
      tagForm: {
        name: 'v1.0',
        command: '>_docker pull quay.io/hellwen/env2conf:v21'
      },
      showDialog: false,
      systeminfo: {}
    }
  },
  computed: {},
  mounted () {},
  methods: {
    initParams (params) {
      console.log('params', params)
      this.repository = {
        namespace: params.namespace,
        name: params.name
      }
    },
    getSysteminfo () {
      this.$api.project.systeminfo().then(res => {
        console.log('getSysteminfo', res)
        if (res.status === 200) {
          this.systeminfo = res.data
        }
      })
    },
    getTags () {
      let name = this.repository.namespace + '/' + this.repository.name
      this.$api.project.tags(name).then(res => {
        console.log('getTags', res)
        if (res.status === 200) {
          this.tableData = res.data
        }
      })
    },
    getPagingData (page, perPage) {
      console.log(page, perPage)
    },
    downloadTag (id) {
      console.log(id)
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
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
    pull (tagData) {
      this.tagForm.name = tagData.name
      this.tagForm.command = 'docker pull ' + this.systeminfo.registry_url + '/' + this.parentData.name + ':' + tagData.name
      this.showDialog = true
    }
  },
  updated () {},
  watch: {},
  created () {
    this.initParams(this.$route.params)
    this.getSysteminfo()
    this.getTags()
    this.tableColumns = [
      // {
      //   type: 'selection',
      //   width: '50'
      // },
      {
        prop: 'name',
        label: '标签'
      },
      // {
      //   prop: 'update_time',
      //   label: '最近修改时间'
      // },
      {
        prop: 'size',
        label: '大小'
      },
      {
        prop: 'os',
        label: '系统'
      },
      {
        cellType: 'slots',
        label: '操作',
        width: '120',
        renderCell: (props) => {
          return (
            <el-button icon="el-icon-download" on-click={() => this.pull(props.row)}></el-button>
          )
        }
      }
    ]
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scope>
</style>
