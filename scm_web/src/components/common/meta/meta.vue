<template>
  <div class="mrp_meta">
    <div class="clearfix">
      <div class="card-header card-header-text">
        <h4>Meta</h4>
      </div>
      <div class="card_box">
        <el-input
          placeholder="输入关键字进行过滤"
          v-model="filterText">
        </el-input>
        <el-tree
          class="filter-tree"
          :data="treeData"
          :props="defaultProps"
          node-key="meta_id"
          :filter-node-method="filterNode"
          :expand-on-click-node="true"
          :render-content="renderContent"
          @node-click="nodeClickFun"
          :default-expanded-keys="[99999]"
          ref="tree2">
        </el-tree>
      </div>
    </div>
    <div class="right_box">
      <el-form ref="form" :model="metaData" label-width="140px">
        <el-form-item label="编号">
          <el-input v-show="!showChange" class="nochange" v-text="metaData.meta_code"></el-input>
          <el-input v-show="showChange" class="truechange" v-model="metaData.meta_code"></el-input>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-show="!showChange" class="nochange" v-text="metaData.meta_name"></el-input>
          <el-input v-show="showChange" class="truechange" v-model="metaData.meta_name"></el-input>
        </el-form-item>
        <el-form-item label="是否可以修改">
          <el-radio class="radio" v-model="metaData.extend.allow_edit" :label="1" :disabled="!showChange">是</el-radio>
          <el-radio class="radio" v-model="metaData.extend.allow_edit" :label="0" :disabled="!showChange">否</el-radio>
        </el-form-item>
        <el-form-item label="是否可以新增下级">
          <el-radio class="radio" v-model="metaData.extend.allow_add_children" :label="1" :disabled="!showChange">是</el-radio>
          <el-radio class="radio" v-model="metaData.extend.allow_add_children" :label="0" :disabled="!showChange">否</el-radio>
        </el-form-item>
      </el-form>
    </div>
    <div class="click-button">
      <div class="el-card" v-show="!showChange && metaData.extend.allow_edit ===1">
        <el-button type="success" class="handle-del mr10" @click="revise">修改
        </el-button>
      </div>
      <div class="el-card" v-show="showChange">
        <el-button type="danger"  class="handle-del mr10" @click="save">保存
        </el-button>
      </div>
    </div>
  </div>
</template>
<script>
  //公共函数
  import {fetchAPI} from "../../../utils/utils.js";
  import showModal from '../messageBox.js';
  let comMetaId = 10000;
  export default {
    components: {},
    name: "mrp_meta",
    props: {
    },
    data() {
      return {
        treeData: [],//树形结构数据
        defaultProps: { //props 数据
          children: 'children',
          label: 'meta_name'
        },
        filterText:'',//搜索数据
        metaData: { //meta详情数据
          meta_id:comMetaId,
          meta_code: "",
          meta_name: "",
          parent_meta_code:{
            meta_id:0
          },
          extend:{
            allow_edit:1,
            allow_add_children:1
          },
          children:[]
        },
        showChange:false
      }
    },
    methods: {
      //对树节点进行筛选时执行的方法
      filterNode(value, data) {
        if (!value) return true;
        return data.meta_name.indexOf(value) !== -1;
      },
      //树节点的内容区的渲染
      renderContent(h, { node, data, store }) {
        if(data.extend && data.extend.allow_edit ===1){
          return (
            <span>
            <span>
            <span>{node.label}</span>
          </span>
          <span style="float: right; margin-right: 20px">
            <el-button size="mini" style="width:23px;" on-click={ (event) => this.append(store, data,event)}>+</el-button>
          <el-button size="mini" style="width:23px;" on-click={ (event) => this.remove(store, data,event)}>-</el-button>
          </span>
          </span>)
        }else{
          return (
            <span>
            <span>
            <span>{node.label}</span>
          </span>
          <span style="float: right; margin-right: 20px">
            <el-button size="mini" style="width:23px;" on-click={ (event) => this.append(store, data,event)}>+</el-button>
          </span>
          </span>)
        }
      },
      //点击+号执行事件
      append(store, data,event) {
        let addData ={
          meta_id:comMetaId++,
          meta_code:"",
          meta_name: "新增",
          parent_meta_code:{
            meta_id:data.meta_id
          },
          extend:{
            allow_edit:1,
            allow_add_children:0
          },
          children: [],
          addLocal:1
        };
        store.append(addData, data);
        this.nodeClickFun(addData);
        event.stopPropagation();
      },
      //移除事件
      remove(store, data,event) {
        showModal.showModal(this, function (that) {
          fetchAPI("delete",that.$store.state.NEW_API+'/api/mat_models/metas/',{data:[data.meta_id]},that).then(res=>{
            store.remove(data);
            showModal.showMessage(that,'success', '删除成功');
          });
          that.metaData = that.treeData['0'].children['0'];
        }, "", "确定要删除此数据？", "操作提示");
        event.stopPropagation();
      },
      //节点被点击时的回调
      nodeClickFun(data){
        if(data.meta_id === 99999) return;
        if(!data.extend){
          data.extend={
            allow_edit:1,
            allow_add_children:1
          };
        }
        console.log('meta',data);
        this.metaData = data;
        this.showChange = !data.addLocal ? false:true;
      },
      //点击修改按钮
      revise(){
        this.showChange = true;
      },
      //网络请求meta数据
      vmRequest(code){
        let url = this.$store.state.NEW_API+"/api/mat_models/metas/?all=1";
        let data =[];
        fetchAPI("get",url,null,this).then(res=>{
          console.log('data', res.data)
          if(res.data.length ===0) return;
          res.data.forEach((row,key)=>{
            //console.log('row', row)
            if(row.parent_meta_code === null ||!row.parent_meta_code){
              data.push(row);
              row['delete'] = 1;
            }
          });
          res.data = res.data.filter(val=>{return !val.delete});
          data.forEach(row=>{
            row["children"] = [];
            res.data.forEach((row2,key2)=>{
              //console.log('row2', row2)
              if(row.meta_id === row2.parent_meta_code.meta_id){
                row.children.push(row2);
                row2['delete'] = 1;
              }
            })
          });
          res.data = res.data.filter(val=>{return !val.delete});
          // console.log('12', res.data)
          if(res.data.length === 0){
            this.treeData= [{
              meta_id:99999,
              meta_code: 0,
              meta_name: "字典项",
              children:data
            }];
            this.nodeClickFun(data['0']);
            return;
          }
          data.forEach(row=>{
            row.children.forEach((row2,key2)=>{
              row2["children"] = [];
              res.data.forEach((row3,key3)=>{
                if(row2.meta_id === row3.parent_meta_code.meta_id){
                  row2.children.push(row3);
                  row3['delete'] = 1;
                }
              });
            })
          });
          res.data = res.data.filter(val=>{return !val.delete});
          if(res.data.length === 0){
            this.treeData= [{
              meta_id:99999,
              meta_code: 0,
              meta_name: "字典项",
              children:data
            }];
            this.nodeClickFun(data['0']);
            return;
          }
          console.log('s', res.data)
          data.forEach(row=>{
            row.children.forEach((row2,key2)=>{
              row2.children.forEach((row3,key3)=>{
                row3["children"] = [];
                res.data.forEach((row4,key4)=>{
                  //console.log('row4',row4)
                  if(row3.meta_id === row4.parent_meta_code.meta_id){
                    row3.children.push(row4);
                    row4['delete'] = 1;
                  }
                });
              });
            })
          });
          res.data = res.data.filter(val=>{return !val.delete});
          if(res.data.length === 0){
            this.treeData= [{
              meta_id:99999,
              meta_code: 0,
              meta_name: "字典项",
              children:data
            }];
            this.nodeClickFun(data['0']);
            return;
          }
          // console.log('14',res.data)
          data.forEach(row=>{
            row.children.forEach((row2,key2)=>{
              row2.children.forEach((row3,key3)=>{
                row3.children.forEach((row4,key4)=>{
                  // console.log('row4', row4)
                  // console.log('res.data', res.data)
                  row4["children"] = [];
                  res.data.forEach((row5,key5)=>{
                    if(row4.meta_id === row5.parent_meta_code.meta_id){
                      row4.children.push(row5);
                      row5['delete'] = 1;
                    }
                  });
                })
              });
            })
          });
          res.data = res.data.filter(val=>{return !val.delete});
          if(res.data.length === 0){
            this.treeData= [{
              meta_id:99999,
              meta_code: 0,
              meta_name: "字典项",
              children:data
            }];
            this.nodeClickFun(data['0']);
            return;
          }
          data.forEach(row=>{
            row.children.forEach((row2,key2)=>{
              row2.children.forEach((row3,key3)=>{
                row3.children.forEach((row4,key4)=>{
                  row4.children.forEach((row5,key5)=>{
                    row5['children'] = []
                    res.data.forEach((row6,key6)=>{
                      if(row5.meta_id === row6.parent_meta_code.meta_id){
                        row5.children.push(row6);
                        row6['delete'] = 1;
                      }
                    });
                  })
                })
              });
            })
          });
          this.treeData= [{
            meta_id:99999,
            meta_code: 0,
            meta_name: "字典项",
            children:data
          }];
          this.nodeClickFun(data['0']);
        })
      },
      //点击保存按钮
      save(){
        let url ="/api/mat_models/metas/";
        let type = "post";
        if(!this.metaData.addLocal){
          url ="/api/mat_models/meta/";
          type = "put";
        }
        if(!this.metaData.parent_meta_code){
          this.metaData.parent_meta_code={
            meta_id:0
          }
        }
        if(this.metaData.meta_id >= 10000){
          this.metaData.meta_id = 0;
        }
        if(this.metaData.parent_meta_code.meta_id === 99999){
          this.metaData.parent_meta_code.meta_id = 0;
        }
        fetchAPI(type,this.$store.state.NEW_API+url,this.metaData,this).then(res=>{
          this.metaData = res.data;
          this.showChange = false;
        });
      }
    },
    computed:{
    },
    updated() {
    },
    created() {
    },
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      }
    },
    mounted() {
      this.vmRequest();
    }
  }
</script>
<style scoped lang="scss" type="text/scss">
  .mrp_meta {
    margin: 30px 10px 10px 10px;
    display: flex;
    flex-flow: row;
    position: relative;
    .clearfix {
      width: 35%;
      background-color: white;
      border-radius: 4px;
      border: 1px solid rgb(229, 209, 214);
      box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
      .card_box {
        margin-top: 60px;
        margin-bottom: 30px;
        margin-left: 20px;
        margin-right: 20px;
        width:90%;
        .filter-tree{
          .el-button--mini{
            width:20px;
          }
        }

      }
    }
    .right_box{
      background-color: white;
      border-radius: 4px;
      border: 1px solid rgb(229, 209, 214);
      box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
      width: 41%;
      float: left;
      margin-left: 10px;
      position: fixed;
      right:12%;
      .el-form{
        border:1px solid rgb(229, 209, 214);
        width: 80%;
        margin:8%;
        padding: 2%;
        .truechange{
          width: 60%;
        }
        .el-select{
          width:60%;
        }
      }
    }
    .click-button {
      width: 9%;
      position: fixed;
      right: 2%;
      .el-card__body {
        padding-top: 0px;
      }
      .el-card {
        display: flex;
        flex-flow: column;
        align-items: center;
        padding: 20px;
        .el-button {
          margin: 0;
          font-size: 16px;
          p:nth-child(2) {
            margin-top:8px;
          }
        }

        .el-button:nth-child(2) {
          margin-top: 10px;
          margin-bottom: 5px;
        }
        .el-button--text {
          width: 70px;
          text-align: center;
          color: #4db3ff;
          font-size: 18px;
        }
        .el-button--text:hover {
          color: #ec407a;
        }
      }
    }
  }


</style>
