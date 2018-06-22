from django.db import models
from django.contrib.postgres.fields import JSONField
from public.models import Customer, Meta, Item, Model

class So(models.Model):
    so_id = models.BigAutoField(primary_key=True, db_column='so_id', verbose_name='pk')
    so_no = models.CharField(max_length=20, db_column='so_no', blank=True, null=True,
                             verbose_name='销售订单单号')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, db_column='customer_id',
                                 blank=True, null=True, db_constraint=False, verbose_name='顾客ID')
    so_type_meta = models.ForeignKey(Meta, on_delete=models.PROTECT, db_column='so_type_meta_id',
                                     null=True, blank=True, db_constraint=False,
                                     verbose_name='so_type_meta_id_of')
    so_date = models.DateField(db_column='so_date', blank=True, null=True, verbose_name='销售订单日期')
    delivery_date = models.DateField(db_column='delivery_date', blank=True, null=True,
                                     verbose_name='销售订单交期')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'so'
        verbose_name = '销售订单表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.so_no

    def __str__(self):
        return self.so_no


class SoItem(models.Model):
    so_item_id = models.BigAutoField(primary_key=True, db_column='so_item_id', verbose_name='pk')
    so = models.ForeignKey(So, db_column='so_id', on_delete=models.CASCADE,
                           blank=True, null=True, db_constraint=True, related_name='so_id_of')
    item = models.ForeignKey(Item, db_column='item_id', on_delete=models.PROTECT,
                             blank=True, null=True, db_constraint=False, related_name='item_id_of')
    quantity = models.IntegerField(db_column='quantity', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, db_column='price',
                                blank=True, null=True)
    currency_meta = models.ForeignKey(Meta, db_column='currency_meta_id', on_delete=models.PROTECT,
                                      blank=True, null=True, db_constraint=False,
                                      related_name='currency_meta_id_of')
    delivery_date = models.DateField(db_column='delivery_date', null=True, blank=True)
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'so_item'
        verbose_name = '销售订单子表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.so_item_id)

    def __str__(self):
        return str(self.so_item_id)


class Bom(models.Model):
    bom_id = models.BigAutoField(primary_key=True, db_column='bom_id', verbose_name='pk')
    bom_no = models.CharField(max_length=20, db_column='bom_no', unique=True, blank=True,
                              verbose_name='bom单号', null=True)
    model = models.ForeignKey(Model, db_column='model_id', on_delete=models.PROTECT,
                              blank=True, null=True, db_constraint=False,
                              related_name='bom_model_id_of')
    item = models.ForeignKey(Item, db_column='item_id', on_delete=models.PROTECT,
                             blank=True, null=True, db_constraint=False,
                             related_name='bom_item_id_of')
    version=models.IntegerField(db_column='veision',blank=True,null=True,verbose_name='版本号')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'bom'
        verbose_name = 'bom表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.bom_no

    def __str__(self):
        return self.bom_no


class BomItem(models.Model):
    bom_item_id = models.BigAutoField(primary_key=True, db_column='bom_item_id', verbose_name='pk')
    bom = models.ForeignKey(Bom, db_column='bom_id', on_delete=models.CASCADE,
                            blank=True, null=True, db_constraint=True, related_name='bom_id_of')
    component_model = models.ForeignKey(Model, db_column='component_model_id', on_delete=models.PROTECT,
                                        blank=True, null=True, db_constraint=False, default=None,
                                        related_name='component_model_id_of')
    component_item = models.ForeignKey(Item, db_column='componemt_item_id', on_delete=models.PROTECT,
                                       blank=True, null=True, db_constraint=False, default=None,
                                       related_name='component_item_id_of')
    quantity = models.DecimalField(max_digits=9, decimal_places=2, db_column='quantity', verbose_name='数量',
                                   blank=True, null=True)
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'bom_item'
        verbose_name = 'bom子表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.bom_item_id)

    def __str__(self):
        return str(self.bom_item_id)


class Mrp(models.Model):
    mrp_id = models.BigAutoField(primary_key=True, db_column='mrp_id', verbose_name='pk')
    mrp_no = models.CharField(max_length=20, db_column='mrp_no', null=True, blank=True,
                              verbose_name='mrp编号')
    mrp_type_meta = models.ForeignKey(Meta, db_column='mrp_type_meta_id', on_delete=models.PROTECT,
                                      null=True, blank=True, db_constraint=False,
                                      related_name='mrp_type_of', verbose_name='mrp类型')
    mrp_date = models.DateField(db_column='mrp_date', blank=True, null=True)
    delivery_date = models.DateField(db_column='delivery_date', blank=True, null=True)
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'mrp'
        verbose_name = 'mrp表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.mrp_no

    def __str__(self):
        return self.mrp_no


class MrpItem(models.Model):
    mrp_item_id = models.BigAutoField(primary_key=True, db_column='mrp_item_id', verbose_name='pk')
    mrp = models.ForeignKey(Mrp, db_column='mrp_id', on_delete=models.CASCADE, verbose_name='关联mrp',
                            blank=True, null=True, db_constraint=True, related_name='mrp_id_of')
    clothes_model = models.ForeignKey(Model, db_column='clothes_model_id', on_delete=models.PROTECT,
                                      blank=True, null=True, db_constraint=False,
                                      related_name='clothes_model_of', verbose_name='mrp成衣model')
    material_item = models.ForeignKey(Item, db_column='material_item_id', on_delete=models.PROTECT,
                                      blank=True, null=True, db_constraint=False,
                                      related_name='material_item_of', verbose_name='mrp材料item')
    quantity = models.DecimalField(db_column='quantity', max_digits=9, decimal_places=2, verbose_name='数量',
                                   null=True, blank=True)
    delivery_date = models.DateField(db_column='delivery', blank=True, null=True)
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'mrp_item'
        verbose_name = 'mrp子项表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.mrp_item_id) + '-->' + self.mrp_id.mrp_no

    def __str__(self):
        return str(self.mrp_item_id) + '-->' + self.mrp_id.mrp_no
