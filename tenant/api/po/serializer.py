from .models import *
from public.serializer import MetaDetialSerializer, ItemDetailSerializer
from rest_framework import serializers


class PoListSerializer(serializers.ModelSerializer):
    po_type_meta = MetaDetialSerializer(many=False, read_only=True)

    class Meta:
        model = Po
        fields = '__all__'


class PoDetailSerializer(serializers.ModelSerializer):
    po_type_meta = MetaDetialSerializer(many=False, read_only=True)

    class Meta:
        model = Po
        fields = '__all__'


class PoItemListSerializer(serializers.ModelSerializer):
    po = PoDetailSerializer(many=True, read_only=False)
    Item = ItemDetailSerializer(many=True, read_only=False)

    class Meta:
        model = PoItem
        fields = '__all__'


class PoItemDetailSerializer(serializers.ModelSerializer):
    po = PoDetailSerializer(many=True, read_only=False)
    Item = ItemDetailSerializer(many=True, read_only=False)

    class Meta:
        model = PoItem
        fields = '__all__'
