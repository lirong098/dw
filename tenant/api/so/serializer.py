from .models import *
from public.serializer import *


class BomSerializer(serializers.ModelSerializer):
    model = ModelSerializer(many=False, read_only=True)
    item = ItemListSerializer(many=False, read_only=True)

    class Meta:
        model = Bom
        fields = ('bom_id', 'bom_no', 'model', 'model_id', 'item', 'item_id', 'version', 'spec', 'extend')


class BomItemSerializer(serializers.ModelSerializer):
    component_model = ModelSerializer(many=False, read_only=True)
    component_item = ItemListSerializer(many=False, read_only=True)

    class Meta:
        model = BomItem
        fields = '__all__'


class BomItemBaseSerializer(serializers.ModelSerializer):
    bom = BomSerializer(many=False, read_only=True)
    component_model = ModelSerializer(many=False, read_only=True)
    component_item = ItemListSerializer(many=False, read_only=True)

    class Meta:
        model = BomItem
        fields = '__all__'


class SoListSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer(read_only=True, many=False)
    so_type_meta = MetaBaseSerializer(read_only=True, many=False)

    class Meta:
        model = So
        fields = ('so_id', 'so_no', 'customer', 'so_type_meta', 'so_date', 'delivery_date')


class SoDetailSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer(read_only=True, many=False)
    so_type_meta = MetaBaseSerializer(read_only=True, many=False)

    class Meta:
        model = So
        fields = ('so_id', 'so_no', 'so_date', 'delivery_date', 'spec', 'extend', 'customer', 'so_type_meta')


class SoItemSerializer(serializers.ModelSerializer):
    so = SoListSerializer(read_only=True, many=False)
    item = ItemListSerializer(read_only=True, many=False)
    currency_meta = MetaListSerializer(read_only=True, many=False)

    class Meta:
        model = SoItem
        fields = '__all__'


class MrpListSerializer(serializers.ModelSerializer):
    mrp_type_meta = MetaDetialSerializer(read_only=True, many=False)

    class Meta:
        model = Mrp
        fields = '__all__'


class MrpDetailSerializer(serializers.ModelSerializer):
    mrp_type_meta = MetaDetialSerializer(read_only=True, many=False)

    class Meta:
        model = Mrp
        fields = '__all__'


class MrpItemListSerializer(serializers.ModelSerializer):
    mrp = MrpDetailSerializer(read_only=True, many=False)
    clothes_model = ModelDetialSerializer(read_only=True, many=False)
    material_item = ItemDetailSerializer(read_only=True, many=False)

    class Meta:
        model = MrpItem
        fields = '__all__'


class MrpItemDetailSerializer(serializers.ModelSerializer):
    mrp = MrpDetailSerializer(read_only=True, many=False)
    clothes_model = ModelDetialSerializer(read_only=True, many=False)
    material_item = ItemDetailSerializer(read_only=True, many=False)

    class Meta:
        model = MrpItem
        fields = '__all__'

