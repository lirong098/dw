from .models import *
from rest_framework import serializers


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'customer_code', 'customer_name', 'parent_customer_id')


class CustomerDetailSerializer(serializers.ModelSerializer):
    parent_customer = CustomerListSerializer(read_only=True, many=False)

    class Meta:
        model = Customer
        fields = '__all__'


class SupplierBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('supplier_id', 'supplier_name', 'supplier_code', 'parent_supplier_id')


class SupplierDetailSerializer(serializers.ModelSerializer):
    parent_supplier = SupplierBaseSerializer(read_only=True, many=False)

    class Meta:
        model = Supplier
        fields = '__all__'


class DepartmentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('department_id', 'department_code', 'department_name', 'parent_department_id')


class DepartmentDetailSerializer(serializers.ModelSerializer):
    parent_department = DepartmentBaseSerializer(read_only=True, many=False)

    class Meta:
        model = Department
        fields = '__all__'


class EmployeeListSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Employee
        fields = ('employee_id', 'employee_name', 'employee_code', 'department')


class EmployeeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class MetaBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = ('meta_id', 'meta_code', 'parent_meta_id', 'meta_name')


class MetaListSerializer(serializers.ModelSerializer):
    parent_meta = MetaBaseSerializer(many=False, read_only=True)

    class Meta:
        model = Meta
        fields = '__all__'


class MetaDetialSerializer(serializers.ModelSerializer):
    parent_meta = MetaBaseSerializer(many=False, read_only=True)

    class Meta:
        model = Meta
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    model_type_meta = MetaBaseSerializer(many=False, read_only=True)
    unit_meta = MetaDetialSerializer(many=False, read_only=True)
    customer = CustomerDetailSerializer(many=False, read_only=True)
    season = MetaBaseSerializer(many=False, read_only=True)

    class Meta:
        model = Model
        fields = ('model_id', 'model_code', 'model_type_meta', 'model_name',
                  'unit_meta', 'spec', 'extend', 'customer', 'season')


class ModelDetialSerializer(serializers.ModelSerializer):
    model_type_meta = MetaBaseSerializer(many=False, read_only=True)
    unit_meta = MetaDetialSerializer(many=False, read_only=True)
    customer = CustomerDetailSerializer(many=False, read_only=True)
    season = MetaBaseSerializer(many=False, read_only=True)

    class Meta:
        model = Model
        fields = ('model_id', 'model_code', 'model_name', 'model_type_meta',
                  'unit_meta', 'spec', 'extend', 'customer', 'season')


class ItemListSerializer(serializers.ModelSerializer):
    # model = ModelSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = ('item_id', 'item_code', 'item_name', 'model_id', 'spec', 'extend')


class ItemDetailSerializer(serializers.ModelSerializer):
    model = ModelSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
