from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.filters import DjangoFilterBackend
from .serializer import *
from tools import messages
from tools.utils import Pagination, FormDataHandled


# Bom Views获取bom列表
class BomListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Bom.objects.all()
    serializer_class = BomSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('bom_no', 'model_id__model_name', 'item_id__item_name', 'model_id__model_type_meta_id__meta_name')
    ordering_fields = ('bom_id', 'bom_no',)
    ordering = ('-bom_id',)
    filter_fields = ('model_id__model_type_meta_id__meta_name',)
    total_number = 0

    def get_queryset(self):
        url_params = {}
        query_keys = ["bom_no", "model_id", "item_id"]
        if self.request.query_params.get('exclude') == '成衣':
            return Bom.objects.all().exclude(model_id__model_type_meta_id__meta_id=1)
        for key in query_keys:
            if self.request.query_params.get(key):
                url_params[key] = self.request.query_params.get(key)
        return Bom.objects.filter(**(url_params))

    def get(self, request, *args, **kwargs):
        # 根据参数过滤
        queryset = self.filter_queryset(queryset=self.get_queryset())
        queryset = Pagination(queryset, self.request).paging()
        self.total_number = len(queryset)
        serializer = BomSerializer(queryset, many=True)
        return Response({'code': 0, 'data': serializer.data, 'total_number': self.total_number})

    def post(self, request, *args, **kwargs):
        # 创建bom信息
        data = request.data
        return FormDataHandled(data=data).create_update_bom()

    def destroy(self, request, *args, **kwargs):
        pks = request.data
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数类型错误!'})
        Bom.objects.filter(bom_id__in=pks).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 获取单个bom表单详细信息
class BomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bom.objects.all()
    serializer_class = BomSerializer

    # 配置URL注意
    def get_object(self):
        return Bom.objects.filter(pk=int(self.request.query_params.get('bom_id'))).first()

    def get(self, request, *args, **kwargs):
        querset = self.get_object()
        if querset:
            serializer = BomSerializer(querset)
            return Response(serializer.data)
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': 'bom不存在'})

    def put(self, request, *args, **kwargs):
        # 更新bom信息
        data = request.data
        return FormDataHandled(data=data).create_update_bom()


# # bom_item List
# class BomItemListView(generics.ListCreateAPIView, generics.UpdateAPIView):
#     queryset = BomItem.objects.all()
#     serializer_class = BomItemSerializer
#     filter_backends = (SearchFilter, OrderingFilter)
#     search_fields = ('bom__bom_no', 'conponent_model__model_name', 'conponent_model__model_code', 'conponent_item__item_code')
#     ordering_fields = ('bom_id', 'bom_item_id')
#     ordering = ('bom_item_id')
#
#     def get_queryset(self):
#         return BomItem.objects.filter(bom_id=self.request.query_params.get('bom_id'))
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     # 批量更新bom_item 中的quantity
#     def update(self, request, *args, **kwargs):
#         items = self.request.data
#         if not isinstance(items, list):
#             return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数类型错误!'})
#         for item in items:
#             bom_item = BomItem.objects.get(bom_item_id=item['bom_item_id'])
#             bom_item.quantity = item['quantity']
#             bom_item.save()
#         return Response({'code': 0, 'message': '保存成功'})
#
#
# # BomItem detail
# class BomItemDetailView(generics.RetrieveUpdateAPIView):
#     queryset = BomItem.objects.all()
#     serializer_class = BomItemSerializer
#
#     def get_object(self):
#         try:
#             return BomItem.objects.get(pk=int(self.request.query_params.get('bom_item_id')))
#         except BomItem.DoesNotExist:
#             raise BomItem
#
#     # def put(self, request, *args, **kwargs):
#     #     # 更新bom_item中的spec信息
#     #     data = request.data
#     #     bom_item = BomItem.objects.get(bom_item_id=data['bom_item_id'])
#     #     bom_item.spec['consume_items'] = data['consume_items']
#     #     bom_item.save()
#     #     caculate = Caculate()
#     #     quantity = caculate.caculate_consumption(bom_item_id=data['bom_item_id'])
#     #     return Response({'quantity': quantity})
#     #     # update_bom_item = utils.FormDataHandled(data=data)
#     #     # return update_bom_item.update_bom_item_spec(data=data)
#

class SoListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = So.objects.all()
    serializer_class = SoListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('so_no', 'customer__customer_name', 'so_date', 'delivery_date')
    search_fields = ('so_no', 'customer__customer_name', 'so_date', 'delivery_date')
    ordering_fields = ('so_date', 'delivery_date')
    total_number = 0

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        if self.request.query_params.get('all', 0) == 1:
            self.total_number = len(queryset)
            serializer = SoListSerializer(queryset, many=True)
        else:
            queryset = Pagination(queryset, self.request).paging()
            serializer = SoListSerializer(queryset, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        data = self.request.data
        return FormDataHandled(data=data).create_update_so()

    def destroy(self, request, *args, **kwargs):
        pks = self.request
        if not isinstance(pks, list):
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': '参数类型错误!'})
        So.objects.filter(bom_id__in=pks).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SodetailView(generics.RetrieveUpdateAPIView):
    queryset = So.objects.all()
    serializer_class = SoDetailSerializer

    def get_object(self):
        so_id = self.request.query_params.get('so_id')
        so = self.queryset.filter(so_id=so_id).first()
        return so

    def get(self, request, *args, **kwargs):
        so = self.get_object()
        if so:
            serializer = SoDetailSerializer(so)
            return {serializer.data}
        else:
            return Response({'code': messages.MSG_CODE_PARAMETER_ERR, 'message': 'so不存在'})

    def put(self, request, *args, **kwargs):
        data = request.data
        return FormDataHandled(data=data).create_update_so()
