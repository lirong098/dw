import time
import random
from so.serializer import *
from po.serializer import *
from .messages import *


def make_unique_code(type=None):
    localtime = time.localtime(int(time.time()))
    localtime = time.strftime('%y%m%d%H%M%S', localtime)

    if type == '1':
        unique_no = 'O' + str(localtime)
    elif type == '2':
        unique_no = 'M' + str(localtime)
    elif type == '3':
        unique_no = 'F' + str(localtime)
    elif type == 'bom':
        unique_no = 'B' + str(localtime)
    elif type == 'item':
        unique_no = 'I' + str(localtime)
    elif type == 'so':
        unique_no = 'So' + str(localtime)
    elif type == 'mrp':
        unique_no = 'MRP' + str(localtime)
    elif type == 'imp':
        unique_no = 'IMP' + str(localtime) + ''.join(random.choice('0123456789') for x in range(5))
    elif type == 'fs':
        unique_no = 'FS' + str(localtime) + ''.join(random.choice('0123456789') for x in range(5))
    else:
        unique_no = ''
    return unique_no


# 列表分页
class Pagination():
    def __init__(self, queryset, request):
        self.queryset = queryset
        self.request = request

    def paging(self):
        total_number = len(self.queryset)
        page = int(self.request.query_params.get('page', 1))
        pagesize = int(self.request.query_params.get('pagesize', 10))
        start = (int(page) - 1) * pagesize
        end = start + int(pagesize)
        if int(total_number) < end:
            end = int(total_number)
        return self.queryset[start:end]


# 将updata和create方法封装起来

class FormDataHandled(object):
    def __init__(self, data):
        self.data = data

    def create_update_customer(self):
        customers = Customer.objects.all()
        if self.data.get('customer_id'):
            # 更新
            customer = customers.filter(customer_code=self.data.get('customer_code')).values('customer_id')
            if len(customer) == 1 and self.data.get('customer_id') != list(customer)[0]['customer_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'customer_code重复'})
            customer = customers.filter(customer_id=self.data.get('customer_id'))
            if customer:
                customer.update(customer_code=self.data.get('customer_code'),
                                customer_name=self.data.get('customer_name'),
                                parent_customer_id=self.data.get('parent_customer').get('customer_id'),
                                spec=self.data.get('spec'), extend=self.data.get('extend'))
                customer = customers.get(customer_id=self.data.get('customer_id'))
                serializer = CustomerDetailSerializer(customer)
                return Response(serializer.data)
            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, "messages": 'customer不存在'})

        else:
            # 创建
            if customers.filter(customer_code=self.data.get('customer_code')):
                # 重复
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'customer_code重复'})
            else:
                # 未重复
                customer = Customer.objects.create(customer_code=self.data.get('customer_code'),
                                                   parent_customer_id=self.data.get('parent_customer').get(
                                                       'customer_id'),
                                                   customer_name=self.data.get('customer_name'),
                                                   spec=self.data.get('spec'), extend=self.data.get('extend'))
                serializer = CustomerDetailSerializer(customer)
                return Response(serializer.data)

    def create_update_supplier(self):
        suppliers = Supplier.objects.all()
        if self.data.get('supplier_id'):
            # 更新
            if self.data.get('supplier_id', 0) != 0:
                supplier = suppliers.filter(supplier_code=self.data.get('supplier_code')).values('supplier_id')
                if len(supplier) == 1 and self.data.get('supplier_id') != list(supplier)[0]['supplier_id']:
                    return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'supplier_code重复'})
                supplier = suppliers.filter(supplier_id=self.data.get('supplier_id'))
                if supplier:
                    supplier.update(supplier_code=self.data.get('supplier_code'),
                                    supplier_name=self.data.get('supplier_name'),
                                    parent_supplier_id=self.data.get('parent_supplier').get('supplier_id'),
                                    spec=self.data.get('spec'), extend=self.data.get('extend'))
                    supplier = suppliers.get(supplier_id=self.data.get('supplier_id'))
                    serializer = SupplierDetailSerializer(supplier)
                    return Response(serializer.data)
                else:
                    return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'supplier_id不存在'})
            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})


        else:
            # 创建
            if suppliers.filter(supplier_code=self.data.get('supplier_code')):
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'supplier_code重复'})
            else:
                supplier = Supplier.objects.create(supplier_code=self.data.get('supplier_code'),
                                                   supplier_name=self.data.get('supplier_name'),
                                                   parent_supplier_id=self.data.get('parent_supplier').get(
                                                       'supplier_id'),
                                                   spec=self.data.get('spec'), extend=self.data.get('extend'))
                serializer = SupplierDetailSerializer(supplier)
                return Response(serializer.data)

    def create_update_meta(self):
        metas = Meta.objects.all()
        if self.data.get('meta_id'):
            # 更新
            meta_id = self.data.get('meta_id', 0)
            meta_id_dict = metas.filter(meta_code=self.data.get('meta_code')).values('meta_id')
            print(meta_id_dict[0])
            if len(meta_id_dict) == 1 and self.data.get('meta_id') != meta_id_dict[0]['meta_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'meta_code重复'})
            else:
                meta = Meta.objects.filter(meta_id=meta_id).first()
                if meta:
                    meta.meta_name = self.data.get('meta_name')
                    meta.meta_code = self.data.get('meta_code')
                    meta.parent_meta_id = self.data.get('parent_meta').get('meta_id')
                    meta.extend = self.data.get('extend')
                    meta.spec = self.data.get('spec')
                    meta.save()
                    serializer = MetaDetialSerializer(meta)
                    return Response(serializer.data)
                else:
                    return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'meta不存在'})
        else:
            # 创建
            if metas.filter(meta_code=self.data.get('meta_code')):
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'meta_code重复'})
            else:
                meta = Meta.objects.create(meta_code=self.data.get('meta_code'), meta_name=self.data.get('meta_name'),
                                           spec=self.data.get('spec'), extend=self.data.get('extend'),
                                           parent_meta_id=self.data.get('parent_meta').get('meta_id'))
            serializer = MetaListSerializer(meta)
            return Response(serializer.data)

    def create_update_model(self):
        if self.data.get('model').get('model_id'):
            # 更新
            # 判断model_code是否重复
            model_data = self.data.get('model')
            model = Model.objects.filter(model_code=model_data.get('model_code')).values('model_id')
            if len(model) == 1 and model_data.get('model_id') != list(model)[0]['model_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'model_code重复'})
            model = Model.objects.filter(model_id=model_data.get('model_id')).first()
            if model:

                model.model_type_meta_id = model_data.get('model_type_meta').get('meta_id')
                model.model_code = model_data.get('model_code')
                model.model_name = model_data.get('model_name')
                model.spec = model_data.get('spec')
                model.extend = model_data.get('extend')
                model.unit_meta_id = model_data.get('unit_meta').get('meta_id')
                model.save()
            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'model不存在'})

            # 循环更新item信息
            update_items = self.data.get('item')
            for item in update_items:
                if item.get('delete', 0) == 1:  # delete字段为1,删除
                    Item.objects.filter(item_id=item.get('item_id')).delete()
                elif item.get('addlocal', 0) == 1:  # addlocal为1,新增
                    Item.objects.create(item_code=item.get('item_code'), item_name=item.get('item_name'),
                                        spec=item.get('spec'), extend=item.get('extend'),
                                        model_id=model_data.get('model_id'))

                else:
                    old_item = Item.objects.filter(item_id=item.get('item_id'))
                    old_item.update(
                        item_code=item.get('item_code'), item_name=item.get('item_name'),
                        spec=item.get('spec'), extend=item.get('extend'),
                        model_id=model_data.get('model_id'))
            model = Model.objects.get(model_id=model_data.get('model_id'))
            serializer = ModelDetialSerializer(model)
            items = Item.objects.filter(model_id=model_data.get('model_id'))
            serializer1 = ItemListSerializer(items, many=True)
            return Response({'model': serializer.data, 'item': serializer1.data})
        else:
            # 创建
            model_data = self.data.get('model')
            if Model.objects.filter(model_code=model_data.get('model_code')):
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'model_code已存在'})
            else:
                # 创建model
                model_type_meta = Meta.objects.filter(meta_id=model_data.get('model_type_meta').get('meta_id')).first()
                newmodel = Model.objects.create(model_code=model_data.get('model_code'),
                                                model_name=model_data.get('model_name'),
                                                spec=model_data.get('spec'), extend=model_data.get('extend'),
                                                unit_meta_id=model_data.get('unit_meta').get('meta_id'),
                                                model_type_meta=model_type_meta)
                if newmodel:
                    # 循环创建items
                    new_items = self.data.get('item')
                    for item in new_items:
                        Item.objects.create(item_code=item.get('item_code'), item_name=item.get('item_name'),
                                            spec=item.get('spec'), extend=item.get('extend'),
                                            model_id=newmodel.model_id)
                    serializer = ModelSerializer(newmodel)
                    items = Item.objects.filter(model_id=newmodel.model_id)

                    serializer1 = ItemListSerializer(items, many=True)
                    return Response({'model': serializer.data, 'item': serializer1.data})
                else:
                    return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'model参数错误!'})

    def create_update_bom(self):
        bom = self.data.get('bom')
        bom_items = self.data.get('bom_item')
        if bom.get('bom_id'):
            # 更新
            boms = Bom.objects.filter(bom_no=bom['bom_no']).values('bom_id')
            if len(boms) == 1 and bom['bom_id'] != list(boms)[0]['bom_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'bom_no已存在'})
            old_bom = Bom.objects.filter(bom_id=bom.get('bom_id'))
            if old_bom:
                old_bom.update(bom_no=bom.get('bom_no'), version=bom.get('version'),
                               spec=bom.get('spec'), extend=bom.get('extend'),
                               item_id=bom.get('item').get('item_id'),
                               model_id=bom.get('model').get('model_id'))

            # 更新bom_item信息
            for bom_item in bom_items:
                if bom_item.get('delete', 0) == 1:  # 获取delete字段为1，则删除该项
                    BomItem.objects.get(bom_item_id=bom_item.get('bom_item_id')).delete()
                elif bom_item.get('addlocal', 0) == 1:  # 获取addlocal字段为1，则新增该项
                    if bom_item.get('component_item').get('item_id') == 0:
                        bom_item['component_item']['item_id'] = None
                    BomItem.objects.create(quantity=bom_item.get('quantity'), spec=bom_item.get('spec'),
                                           extend=bom_item.get('extend'), bom_id=bom.get('bom_id'),
                                           component_model_id=bom_item.get('component_model').get('model_id'),
                                           component_item_id=bom_item.get('component_item').get('item_id'))
                else:
                    update_bom_item = BomItem.objects.filter(bom_item_id=bom_item.get('bom_item_id')).first()
                    if update_bom_item:
                        update_bom_item.quantity = bom_item.get('quantity')
                        update_bom_item.spec = bom_item.get('spec')
                        update_bom_item.extend = bom_item.get('extend')
                        update_bom_item.bom_id = bom_item.get('bom').get('bom_id')
                        # 更新组成model
                        component_model = bom_item.get('component_model')
                        update_bom_item.component_model = Model.objects.get(model_id=component_model.get('model_id'))
                        # 更新组成item
                        component_item = bom_item.get('component_item')
                        if component_item.get('item_id') != 0:
                            update_bom_item.component_item = Item.objects.get(item_id=component_item.get('item_id'))
                        else:
                            update_bom_item.component_item = None
                        update_bom_item.save()
                    else:
                        return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': '更新的item不存在'})
            update_bom = Bom.objects.get(bom_id=bom.get('bom_id'))
            serializer = BomSerializer(update_bom)
            update_bom_item = BomItem.objects.filter(bom_id=bom['bom_id'])
            serializer1 = BomItemSerializer(update_bom_item, many=True)
            return Response({'code': 0, 'bom': serializer.data, 'bom_item': serializer1.data})


        else:
            # 创建bom以及item
            if Bom.objects.filter(bom_no=bom.get('bom_no')):
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'bom_no已存在'})
            new_bom = Bom.objects.create(bom_no=bom.get('bom_no'), version=bom.get('version'),
                                         spec=bom.get('spec'), extend=bom.get('extend'),
                                         model_id=bom.get('model').get('model_id'),
                                         item_id=bom.get('item').get('item_id'))
            if new_bom:
                # 循环创建bom_item
                for bom_item in bom_items:
                    # 初始化bom_item的item单耗
                    BomItem.objects.create(quantity=bom_item.get('quantity'), spec=bom_item.get('spec'),
                                           extend=bom_item.get('extend'), bom_id=new_bom.bom_id,
                                           component_model_id=bom_item.get('component_model').get('model_id'),
                                           component_item_id=bom_item.get('component_item').get('item_id'))
                serializer = BomSerializer(new_bom)
                new_bom_item = BomItem.objects.filter(bom_id=new_bom.bom_id)
                serializer1 = BomItemSerializer(new_bom_item, many=True)
                return Response({'code': 0, 'bom': serializer.data, 'bom_item': serializer1.data})
            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': '表头参数错误!'})

    def create_update_so(self):
        so = self.data.get('so')
        so_items = self.data.get('so_item')
        # 更新
        if self.data.get('so_id'):
            sos = So.objects.filter(so_no=so['so_no']).values('so_id')
            if len(sos) == 1 and so['so_id'] != list(sos)[0]['so_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'so_no已存在'})
            old_so = So.objects.filter(so_id=so.get('so_id'))
            if old_so:
                old_so.update(so_no=so.get('so_no'),
                              customer_id=so.get('customer').get('customer_id'),
                              so_type_meta_id=so.get('so_type_meta').get('meta_id'),
                              so_date=so.get('so_date'),
                              delivery_date=so.get('delivery_date'),
                              spec=so.get('spec'), extend=so.get('spec'))
                # 循环更新so_item
                for so_item in so_items:
                    if so_item.get('delete', 0) == 1:
                        SoItem.objects.filter(so_item_id=so_item.get('so_item_id')).delete()
                    elif so_item.get('addlocal', 0) == 1:
                        new_so_item = SoItem.objects.create(so_id=so.get('so_id'),
                                                            item_id=so_item.get('item').get('item_id'),
                                                            currency_meta_id=so_item.get('currency_meta').get(
                                                                'meta_id'),
                                                            quantity=so_item.get('quantity'),
                                                            price=so_item.get('price'),
                                                            delivery_date=so_item.get('delivery_date'),
                                                            spec=so_item.get('spec'), extend=so_item.get('extend'),
                                                            )
                    else:
                        old_so_item = SoItem.objects.filter(so_item_id=so_item.get('so_item_id')).first()
                        if old_so_item:
                            update_so_item = old_so_item.update(so_id=so.get('so_id'),
                                                                item_id=so_item.get('item').get('item_id'),
                                                                currency_meta_id=so_item.get('currency_meta').get(
                                                                    'meta_id'),
                                                                quantity=so_item.get('quantity'),
                                                                price=so_item.get('price'),
                                                                delivery_date=so_item.get('delivery_date'),
                                                                spec=so_item.get('spec'), extend=so_item.get('extend'),
                                                                )
                        else:
                            return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'so_item不存在'})

                        serializer = SoListSerializer(old_so)
                        so_items = SoItem.objects.filter(so_id=old_so.so_id)
                        serializer1 = SoItemSerializer(so_items, many=True)
                        return Response({'so': serializer.data, 'so_item': serializer1.data})

        # 创建
        else:
            new_so = So.objects.create(so_no=so.get('so_no'),
                                       customer_id=so.get('customer').get('customer_id'),
                                       so_type_meta_id=so.get('so_type_meta').get('meta_id'),
                                       so_date=so.get('so_date'),
                                       delivery_date=so.get('delivery_date'),
                                       spec=so.get('spec'), extend=so.get('spec'))

            # return Response(serializer.data)
            # 循环创建Item
            for so_item in so_items:
                new_so_item = SoItem.objects.create(so_id=new_so.so_id,
                                                    item_id=so_item.get('item').get('item_id'),
                                                    currency_meta_id=so_item.get('currency_meta').get('meta_id'),
                                                    quantity=so_item.get('quantity'),
                                                    price=so_item.get('price'),
                                                    delivery_date=so_item.get('delivery_date'),
                                                    spec=so_item.get('spec'), extend=so_item.get('extend'),
                                                    )

            serializer = SoListSerializer(new_so)
            so_items = SoItem.objects.filter(so_id=new_so.so_id)
            serializer1 = SoItemSerializer(so_items, many=True)
            return Response({'so': serializer.data, 'so_item': serializer1.data})

    def create_update_department(self):
        data = self.data
        departments = Department.objects.all()
        if data.get('departemnt_id'):
            department = departments.filter(department_code=data.get('department_code')).values('department_id')
            if len(department) == 1 and data.get('department_id') != list(department)[0]['department_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'department_code重复'})
            departments.filter(department_id=data.get('department_id')) \
                .update(department_code=data.get('department_code'),
                        department_name=data.get('department_name'),
                        parent_department_id=data.get('parent_department').get('department_id'),
                        spec=data.get('spec'), extend=data.get('extend'))
            department = departments.get(department_id=data.get('department_id'))
            serializer = DepartmentDetailSerializer(department)
            return Response(serializer.data)
        else:
            if departments.filter(customer_code=data.get('department_code')):
                # 重复
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'department_code重复'})
            else:
                # 未重复
                customer = Department.objects.create(department_code=data.get('department_code'),
                                                     parent_department_id=data.get('parent_department').get(
                                                         'department_id'),
                                                     department_name=data.get('department_name'),
                                                     spec=data.get('spec'), extend=data.get('extend')
                                                     )
            serializer = DepartmentDetailSerializer(customer)
            return Response(serializer.data)

    def create_update_employee(self):
        data = self.data
        employees = Employee.objects.all()
        if data.get('employee_id'):
            employee = employees.filter(employee_code=data.get('employee_code')).values('employee_id')
            if len(employee) == 1 and data.get('employee_id') != list(employee)[0]['employee_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'employee_code重复'})
            employees.filter(employee_id=data.get('employee_id')) \
                .update(employee_code=data.get('employee_code'),
                        employee_name=data.get('employee_name'),
                        department_id=data.get('department').get('department_id'),
                        spec=data.get('spec'), extend=data.get('extend'))
            employee = employees.get(customer_id=data.get('customer_id'))
            serializer = EmployeeDetailSerializer(employee)
            return Response(serializer.data)


        else:
            if employees.filter(customer_code=data.get('employee_code')):
                # 重复
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'employee_code重复'})
            else:
                # 未重复
                employee = Employee.objects.create(employee_code=data.get('employee_code'),
                                                   department_id=data.get('department').get('department_id'),
                                                   employee_name=data.get('employee_name'),
                                                   spec=data.get('spec'), extend=data.get('extend')
                                                   )
                serializer = EmployeeDetailSerializer(employee)
                return Response(serializer.data)

    def create_update_mrp(self):
        mrp = self.data.get('mrp')
        mrp_items = self.data.get('mrp_items')
        # 有ID 则更新
        if mrp.get('mrp_id'):
            old_mrp = Mrp.objects.filter(mrp_id=mrp.get('mrp_id')).first()
            if old_mrp:
                old_mrp.update(mrp_no=mrp.get('mrp_no'), mrp_date=mrp.get('mrp_date'),
                               mrp_meta_type_id=mrp.get('mrp_meta_type').get('meta_id'),
                               delivery_date=mrp.get('delivery_date'),
                               spec=mrp.get('spec'), extend=mrp.get('extend'))
                # 循环更新mrp_items
                for mrp_item in mrp_items:
                    if mrp_item.get('delete', 0) == 1:  # 此时删除
                        MrpItem.objects.filter(mrp_item_id=mrp_item.get('mrp_iemt_id')).delete()
                    elif mrp_item.get('addlocal', 0) == 1:  # 此时创建
                        MrpItem.objects.create(mrp_id=old_mrp.mrp_id, quantity=mrp_item.get('quantity'),
                                               clothes_model_id=mrp_item.get('clothes_model').get('model_id'),
                                               material_item_id=mrp_item.get('material_item').get('item_id'),
                                               delivery_date=mrp_item.get('delivery_date'),
                                               spec=mrp_item.get('spec'), extend=mrp_item.get('extend'))
                    else:
                        old_mrp_item = MrpItem.objects.filter(mrp_item_id=mrp_item.get('mrp_item_id')).first()
                        if old_mrp_item:
                            old_mrp_item.update(quantity=mrp_item.get('quantity'),
                                                clothes_model_id=mrp_item.get('clothes_model').get('model_id'),
                                                material_item_id=mrp_item.get('material_item').get('item_id'),
                                                delivery_date=mrp_item.get('delivery_date'),
                                                spec=mrp_item.get('spec'), extend=mrp_item.get('extend'))
                        else:
                            return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'mrp_item不存在'})

            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'mrp不存在'})



        # 没ID 则创建
        else:
            new_mrp = Mrp.objects.create(mrp_no=mrp.get('mrp_no'), mrp_date=mrp.get('mrp_date'),
                                         mrp_meta_type_id=mrp.get('mrp_meta_type').get('meta_id'),
                                         delivery_date=mrp.get('delivery_date'),
                                         spec=mrp.get('spec'), extend=mrp.get('extend'))
            # 循环创建mrp_item
            if new_mrp:
                for mrp_item in mrp_items:
                    new_mrp_item = MrpItem.objects.create(mrp_id=new_mrp.mrp_id, quantity=mrp_item.get('quantity'),
                                                          clothes_model_id=mrp_item.get('clothes_model').get(
                                                              'model_id'),
                                                          material_item_id=mrp_item.get('material_item').get('item_id'),
                                                          delivery_date=mrp_item.get('delivery_date'),
                                                          spec=mrp_item.get('spec'), extend=mrp_item.get('extend'))

                serializer = MrpDetailSerializer(new_mrp)
                mrp_items = MrpItem.objects.filter(mrp_id=new_mrp.mrp_id)
                serializer1 = MrpItemDetailSerializer(mrp_items, many=True)
                return Response({'mrp': serializer.data, 'mrp_item': serializer1.data})
            else:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': '参数错误'})

    def create_update_po(self):
        po = self.data.get('po')
        po_items = self.data.get('po_item')
        # 更新
        if self.data.get('po_id'):
            pos = Po.objects.filter(po_no=po['po_no']).values('po_id')
            if len(pos) == 1 and po['po_id'] != list(pos)[0]['po_id']:
                return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'po_no已存在'})
            old_po = So.objects.filter(po_id=po.get('po_id')).first()
            if old_po:
                old_po.update(po_no=po.get('po_no'),
                              po_type_meta_id=po.get('po_type_meta').get('meta_id'),
                              po_date=po.get('po_date'),
                              delivery_date=po.get('delivery_date'),
                              spec=po.get('spec'), extend=po.get('spec'))
                # 循环更新so_item
                for po_item in po_items:
                    if po_item.get('delete', 0) == 1:
                        PoItem.objects.filter(po_item_id=po_item.get('po_item_id')).delete()
                    elif po_item.get('addlocal', 0) == 1:
                        new_po_item = PoItem.objects.create(po_id=old_po.po_id,
                                                            item_id=po_item.get('item').get('item_id'),
                                                            quantity=po_item.get('quantity'),
                                                            delivery_date=po_item.get('delivery_date'),
                                                            spec=po_item.get('spec'), extend=po_item.get('extend'), )
                    else:
                        old_po_item = PoItem.objects.filter(po_item_id=po_item.get('po_item_id')).first()
                        if old_po_item:
                            update_so_item = old_po_item.update(po_id=old_po.po_id,
                                                                item_id=po_item.get('item').get('item_id'),
                                                                quantity=po_item.get('quantity'),
                                                                delivery_date=po_item.get('delivery_date'),
                                                                spec=po_item.get('spec'), extend=po_item.get('extend'),
                                                                )
                        else:
                            return Response({'code': MSG_CODE_PARAMETER_ERR, 'message': 'po_item不存在'})

                        serializer = PoListSerializer(old_po)
                        po_items = PoItem.objects.filter(po_id=old_po.po_id)
                        serializer1 = PoItemDetailSerializer(po_items, many=True)
                        return Response({'so': serializer.data, 'so_item': serializer1.data})

        # 创建
        else:
            new_po = Po.objects.create(po_no=po.get('po_no'),
                                       po_type_meta_id=po.get('po_type_meta').get('meta_id'),
                                       po_date=po.get('po_date'),
                                       delivery_date=po.get('delivery_date'),
                                       spec=po.get('spec'), extend=po.get('spec'))

            # 循环创建Item
            for po_item in po_items:
                new_po_item = PoItem.objects.create(po_id=new_po.po_id,
                                                    item_id=po_item.get('item').get('item_id'),
                                                    quantity=po_item.get('quantity'),
                                                    delivery_date=po_item.get('delivery_date'),
                                                    spec=po_item.get('spec'), extend=po_item.get('extend'),
                                                    )

            serializer = PoListSerializer(new_po)
            po_items = PoItem.objects.filter(so_id=new_po.po_id)
            serializer1 = PoItemDetailSerializer(po_items, many=True)
            return Response({'so': serializer.data, 'so_item': serializer1.data})
