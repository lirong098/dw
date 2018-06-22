import {fetchAPI} from '../../utils/utils';
let requst ={
  /*
      * 网络请求数据
      * self,//作用的当前实例对象
      * type,//请求类型 get,post....
      * url,//路径
      * options,//post时数据*/
  requst(self,url, successfun, type = 'get', options = 'null') {
    const api = self.$store.state.NEW_API;
    let apiUrl = api + url;
    fetchAPI(type, apiUrl, options, self).then((res) => {
      if ((res && res.status == 200) || (type == "delete" && res && res.status == 204)) {
        typeof successfun == "function" && successfun(self, res);
      }
    })
  },
  /*网络请求 生成内部唯一编码标识
  * self,作用的当前实例对象
  * type,{成衣：1，面料：2，辅料：3，bom：bom，item:item，备料：fcst}*/
  make_unique_no(self,type,successfun){
    this.requst(self,"/api/mat_models/make_unique_no/",successfun,"post",{type:type});
  },
  /*网络请求 元数据list
    * self,作用的当前实例对象
    * type,{单位：unit10，model：unit09，备料：unit11}*/
  get_metas_list(self,type,successfun){
    this.requst(self,"/api/mat_models/metas/?parent_meta_code="+type,successfun);
  },
  /*
  * BOM详情*/
  bomdetails(bomId,self,model){
    if(bomId == 0){
      let initialize = {
        bom: {
          bom_id: 0,
          bom_no: "",
          model_id: model,
          item_id: {
            item_id: 0,
          },
          version: 0,
          spec: {
            color: ""
          },
          extend: {}
        },
        bom_item: [
          {
            bom_item_id: 0,
            bom: {
              bom_id: 0,
              bom_no: "",
              model_id: 0,
              item_id: 0,
              version: 0,
              spec: {
                color: ""
              },
              extend: {}
            },
            component_model: {
              model_id: 0,
              unit_meta: {
                meta_id: 0,
                meta_code: "",
                parent_meta_code: "",
                meta_name: "",
                extend: {}
              },
              model_type_meta_id: 0,
              model_code: "",
              model_name: "",
              spec: {},
              extend: {}
            },
            component_item: {
              item_id: 0,
              item_code: "",
              item_name: "",
              spec: {},
              extend: {},
              model: 0
            },
            quantity: 0,
            spec: {
              consume_items: [],
              division: false,
              consumptStatus: false,
            },
            extend: {},
            addlocal: 0,
            restore: false,
          }
        ]
      };
      // 获取唯一标识
      this.make_unique_no(self,"1",function (that,res) {
        if (res.data.code !== 0) return;
        initialize.bom.bom_no = res.data.message;
      });
      let newTabName = ++self.chlidTabIndex + '';
      self.chlidTABSValue = newTabName;
      let bomInfo = {
        title: 'BOM详细信息',
        name: newTabName,
        closable: true,
        rowState: 'change',
        rowId:"",
        resData: initialize,
        tabName:"bominfo"
      };
      self.$emit('changeTabMethod', self.chlidTabIndex, self.chlidTABSValue, bomInfo);
    };
    const api = self.$store.state.NEW_API;
    let regroup = {};
    let getBomDataMassage = {
      bom_id: bomId
    };
    fetchAPI('get', api + '/api/mat_models/bom/?bom_id=' + bomId, getBomDataMassage, self).then((res) => {
      if (res && res.status == 200) {
        regroup.bom = res.data;
        return fetchAPI('get', api + '/api/mat_models/bom_items/?bom_id=' + bomId, getBomDataMassage, self);
      }
    }).then((res) => {
      if (res && res.status == 200) {
        for(let item of res.data){
          if(!item.component_item){
            item.component_item = {
              item_id : 0
            };
          }
          item.restore = false;
        }
        regroup.bom_item = res.data;
        let newTabName = ++self.chlidTabIndex + '';
        self.chlidTABSValue = newTabName;
        let bomInfo = {
          title: 'BOM详细信息',
          name: newTabName,
          closable: true,
          rowState: 'look',
          rowId: regroup.bom.bom_id,
          resData: regroup,
          tabName:"bominfo"
        };
        self.$emit('changeTabMethod', self.chlidTabIndex, self.chlidTABSValue, bomInfo);
      }
    });
  },
};
module.exports = requst;
