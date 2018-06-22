from public.models import Meta,Customer
import json

def create_parent_meta():
    parent_metas = ['成衣Model', '面料Model', '辅料Model', '单位', '币种', '成衣备料类型'
        , 'MRP备料类型', '备料形式类型', '备料方式','销售订单类型','采购订单类型','季节']
    for i in range(len(parent_metas)):
        meta = Meta()
        meta.meta_name = parent_metas[i]
        meta.meta_code = 'MC00' + str(i)
        meta.save()


def create_child_meta(parent_meta_id, child_metas, meta_code):
    for i in range(len(child_metas)):
        meta = Meta()
        meta.meta_name = child_metas[i]
        meta.parent_meta_id = parent_meta_id
        meta.meta_code = meta_code + '0' + str(i)
        meta.save()


units = ['件', '米']
currency = ['人民币', '美元']
clothes_models = ['选样备料', '预估备料', '盘点入库', '盘点出库', '实单首单', '实单翻单']
mrp_type = ['手工备料', '自动计算', '实单抵充', '盘点入库', '盘点出库']
material_type = ['备原料', '备毛坯', '备纱线']
material_method = ['FG AUTO/CPT CBA', 'FG AUTO/CPT MAX ', 'FULL LT']
so_type=['销售type1','销售type2','销售type3']
po_type=['采购type1','采购type2','采购type3']
season=['春','夏','秋','冬']


def start_meta():
    create_child_meta(4, units, 'UNI')
    create_child_meta(5, currency, 'CUR')
    create_child_meta(6, clothes_models, 'CLO')
    create_child_meta(7, mrp_type, 'MRP')
    create_child_meta(8, material_type, 'MATT')
    create_child_meta(9, material_method, 'MATM')
    create_child_meta(10, so_type, 'SOT')
    create_child_meta(11, po_type, 'POT')
    create_child_meta(12, season, 'SEA')



