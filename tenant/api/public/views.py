from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.filters import DjangoFilterBackend
from .serializer import *
from tools import messages
from tools.utils import Pagination, FormDataHandled, make_unique_code
from django.db.models.deletion import ProtectedError


@api_view(('POST', 'GET'))
def make_model_code(request):
    model_type_meta_id = str(request.data.get(u'model_type_meta_id', ''))
    model_code = make_unique_code(type=model_type_meta_id)
    if model_code == '':
        return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误'})
    else:
        return Response({'code': 0, 'model_code': model_code})


# 生成item_code
@api_view(('POST', 'GET'))
def make_item_code(request):
    item_code = make_unique_code(type='item')
    return Response({'code': 0, 'item_code': item_code})


# 生成bom_no
@api_view(('POST', 'GET'))
def make_bom_no(request):
    bom_no = make_unique_code(type='bom')
    return Response({'code': 0, 'bom_no': bom_no})


# 生成so_no
@api_view(('GEt', 'POST'))
def make_so_no(request):
    so_no = make_unique_code(type='so')
    return Response({'code': 0, 'so_no': so_no})


# 获取顾客列表
class CustomerListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('customer_code', 'customer_name')
    search_fields = ('customer_code', 'customer_name', 'parent_customer__customer_name')
    total_number = 0

    def get_queryset(self):
        url_params = {}
        query_keys = ['customer_code', 'customer_name']
        for key in query_keys:
            if self.request.query_params.get(key):
                url_params[key] = self.request.query_params.get(key)
        return self.queryset.filter(**(url_params))

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if int(self.request.query_params.get('all', 0)) == 1:
            self.total_number = len(queryset)
            serializer = CustomerListSerializer(queryset, many=True)
        else:
            queryset = Pagination(queryset, self.request).paging()
            self.total_number = len(queryset)
            serializer = CustomerListSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'total_number': self.total_number})

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})
        try:
            Customer.objects.filter(customer_id__in=pks).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'code': messages.MSG_CODE_PROTECT_ERROR, 'message': '不允许级联删除！'})

    def create(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_customer()


# 获取顾客详情
class CustomerDetailView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer

    def get_object(self):
        customer_id = int(self.request.query_params.get('customer_id'))
        return self.queryset.filter(customer_id=customer_id).first()

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset:
            serializer = CustomerDetailSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': 'customer_id不存在！'})

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_customer()


# 获取供应商列表
class SupplierListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ('supplier_code', 'supplier_name')
    search_fields = ('supplier_code', 'supplier_name', 'parent_supplier__supplier_name')
    total_number = 0

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if int(self.request.query_params.get('all', 0)) == 1:
            self.total_number = len(queryset)
            serializer = SupplierListSerializer(queryset, many=True)
        else:
            queryset = Pagination(queryset, self.request).paging()
            self.total_number = len(queryset)
            serializer = SupplierListSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'total_number': self.total_number})

    def create(self, request, *args, **kwargs):
        data = self.request.data
        return FormDataHandled(data).create_update_supplier()

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数类型错误!'})
        try:
            Supplier.objects.filter(supplier_id__in=pks).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'code': messages.MSG_CODE_PROTECT_ERROR, 'message': '不允许级联删除！'})


# 获取供应商详情
class SupplierDetailView(generics.RetrieveUpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierDetailSerializer

    def get_object(self):
        supplier_id = int(self.request.query_params.get('supplier_id'))
        return self.queryset.filter(supplier_id=supplier_id).first()

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset:
            serializer = SupplierDetailSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': 'supplier_id不存在'})

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data).create_update_supplier()


# 获取部门列表
class DepartmentListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ('department_code', 'department_name')
    search_fields = ('department_code', 'department_name')
    total_number = 0

    def get_queryset(self):
        url_params = {}
        query_keys = ['departmnet_code', 'department_name']
        for key in query_keys:
            if self.request.query_params.get(key):
                url_params[key] = self.request.query_params.get(key)
        return self.queryset.filter(**(url_params))

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if int(self.request.query_params.get('all', 0)) == 1:
            self.total_number = len(queryset)
            serializer = DepartmentListSerializer(queryset, many=True)
        else:
            page = Pagination(queryset, self.request).paging()
            self.total_number = len(page)
            serializer = DepartmentListSerializer(page, many=True)
        return Response({'data': serializer.data, 'total_number': self.total_number})

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})
        Department.objects.filter(customer_id__in=pks).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_department()


# 获取部门详情
class DepartmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer

    def get_object(self):
        department_id = int(self.request.query_params.get('customer_id'))
        return self.queryset.get(department_id=department_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = DepartmentDetailSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_department()


# 获取员工列表
class EmployeeListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ('employee_code', 'employee_name', 'department_id')
    search_fields = ('employee_code', 'employee_name', 'department_id')
    total_number = 0

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if int(self.request.query_params.get('all', 0)) == 1:
            self.total_number = len(queryset)
            serializer = EmployeeListSerializer(queryset, many=True)
        else:
            page = Pagination(queryset, self.request).paging()
            self.total_number = len(page)
            serializer = EmployeeListSerializer(page, many=True)
        return Response({'data': serializer.data, 'total_number': self.total_number})

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})
        Customer.objects.filter(customer_id__in=pks).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        data = request.data
        employees = self.queryset
        if data.get('employee_id', 0) == 0:
            if employees.filter(customer_code=data.get('employee_code')):
                # 重复
                return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': 'employee_code重复'})
            else:
                # 未重复
                employee = Employee.objects.create(employee_code=data.get('employee_code'),
                                                   department_id=data.get('department_id'),
                                                   employee_name=data.get('employee_name'),
                                                   spec=data.get('spec'), extend=data.get('extend')
                                                   )
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})
        serializer = EmployeeListSerializer(employee)
        return Response(serializer.data)


# 获取员工详情
class EmployeeDetailView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer

    def get_object(self):
        employee_id = int(self.request.query_params.get('employee_id'))
        return self.queryset.get(employee_id=employee_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = EmployeeDetailSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_employee()


# 获取元数据列表
class MetaListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Meta.objects.all()
    serializer_class = MetaListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('meta_code', 'meta_name')
    ordering_fields = ('meta_id', 'meta_code',)
    ordering = ('meta_id',)  # 默认排序按meta_id升序
    filter_fields = ('parent_meta_id', 'meta_name', 'parent_meta__meta_name')

    def get_queryset(self):
        url_params = {}
        query_keys = ['parent_meta_id', 'meta_name']
        for key in query_keys:
            if self.request.query_params.get(key):
                url_params[key] = self.request.query_params.get(key)
        return self.queryset.filter(**(url_params))

    def get(self, request, *args, **kwargs):
        # 这是查询集的获取
        queryset = self.filter_queryset(self.get_queryset())
        serializer = MetaListSerializer(queryset, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_meta()

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数类型错误!'})
        try:
            Meta.objects.filter(meta_id__in=pks).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'code': messages.MSG_CODE_PROTECT_ERROR, 'message': '不允许级联删除'})


# 获取元数据详情
class MetaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Meta.objects.all()
    serializer_class = MetaDetialSerializer

    def get_object(self):
        meta_id = int(self.request.query_params.get('meta_id'))
        return self.queryset.filter(meta_id=meta_id).first()

    def get(self, request, *args, **kwargs):
        meta = self.get_object()
        serializer = MetaDetialSerializer(meta)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_meta()


# NewModel views获取list
class ModelListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('model_code', 'model_type_meta__meta_name', 'model_type_meta__meta_code', 'model_name',)
    ordering_fields = ('model_id',)
    ordering = ('-model_id',)
    filter_fields = ('model_type_meta_id', 'model_name',)
    total_number = 0

    def get_queryset(self):
        spec__customer_id = self.request.query_params.get("spec__customer_id", None)
        spec__season_meta_id = self.request.query_params.get("spec__season_meta_id", None)
        if spec__customer_id:
            self.queryset = self.queryset.filter(spec__customer_id=int(spec__customer_id))
        if spec__season_meta_id:
            self.queryset = self.queryset.filter(spec__season_meta_id=int(spec__season_meta_id))
        if self.request.query_params.get('exclude') == '1':
            self.queryset = self.queryset.exclude(model_type_meta_id=1)
        elif self.request.query_params.get('exclude') == '2':
            self.queryset = self.queryset.filter(model_type_meta_id=1)
        return self.queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        pagenator = Pagination(request=self.request, queryset=queryset)
        queryset = pagenator.paging()
        self.total_number = len(queryset)
        serializer = ModelSerializer(queryset, many=True)
        return Response({'data': serializer.data,
                         'total_number': self.total_number})

    def create(self, request, *args, **kwargs):
        # 创建model 信息
        data = request.data
        return FormDataHandled(data).create_update_model()

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误！'})
        Model.objects.filter(model_id__in=pks).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# NewModel views
class ModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    # 配置URL注意
    def get_object(self):
        model_id = self.request.query_params.get('model_id')
        return Model.objects.filter(model_id=model_id).first()

    def get(self, request, *args, **kwargs):
        # 获取model信息
        model = self.get_object()
        if model:
            serializer = ModelSerializer(model)
            return Response(serializer.data)
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数错误'})

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_model()


class ItemListview(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer

    def get_queryset(self):
        model_id = self.request.query_params.get('model_id')
        queryset = self.queryset.filter(model_id=model_id)
        return queryset
