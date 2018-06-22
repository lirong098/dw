from django.db import models
from django.contrib.postgres.fields import JSONField
from public.models import Meta, Item


class Po(models.Model):
    po_id = models.BigAutoField(primary_key=True, db_column='po_id', verbose_name='pk')
    po_no = models.CharField(max_length=20, db_column='po_no', blank=True, null=True,
                             verbose_name='采购订单单号')
    po_type_meta = models.ForeignKey(Meta, db_column='po_type_meta_id', on_delete=models.PROTECT,
                                     blank=True, null=True, db_constraint=False,
                                     related_name='po_type_meta_id_of')
    po_date = models.DateField(db_column='po_date', blank=True, null=True, verbose_name='采购订单日期')
    delivery_data = models.DateField(db_column='delivery_data', blank=True, null=True, verbose_name='采购订单交期')

    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'po'
        verbose_name = '采购订单表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.po_no

    def __str__(self):
        return self.po_no


class PoItem(models.Model):
    po_item_id = models.BigAutoField(primary_key=True, db_column='po_item_id', verbose_name='pk')
    po = models.ForeignKey(Po, db_column='po_id', on_delete=models.CASCADE,
                           blank=True, null=True, db_constraint=True, related_name='po_id_of1')
    item = models.ForeignKey(Item, db_column='item_id', on_delete=models.PROTECT,
                             blank=True, null=True, db_constraint=False, related_name='item_id_of1')
    quantity = models.IntegerField(db_column='quantity', blank=True, null=True, verbose_name='数量')
    delivery_date = models.DateField(db_column='delivery_date', blank=True, null=True)
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'po_item'
        verbose_name = '采购订单表子表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.po_item_id)

    def __str__(self):
        return str(self.po_item_id)
