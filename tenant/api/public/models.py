from django.db import models
from django.contrib.postgres.fields import JSONField


class Meta(models.Model):
    meta_id = models.BigAutoField(primary_key=True, db_column='meta_id', verbose_name='pk')
    meta_code = models.CharField(max_length=20, db_column='meta_code', null=True,
                                 blank=True, unique=True, verbose_name='元数据编码')
    parent_meta = models.ForeignKey("self", default=None, db_column='parent_meta_id', null=True,
                                    verbose_name='父元数据ID', blank=True, db_constraint=False,
                                    on_delete=models.PROTECT)
    meta_name = models.CharField(max_length=50, db_column='meta_name', null=True, blank=True,
                                 verbose_name='元数据名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'meta'
        verbose_name = '元数据表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.meta_name

    def __str__(self):
        return self.meta_name


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True, db_column='customer_id', verbose_name='pk')
    customer_code = models.CharField(max_length=20, db_column='customer_code', null=True,
                                     blank=True, unique=True, verbose_name='用户编码')
    parent_customer = models.ForeignKey("self", default=None, db_column='parent_customer_id', null=True,
                                        blank=True, verbose_name='父类用户ID', db_constraint=False,
                                        on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=50, db_column='customer_name', null=True,
                                     blank=True, verbose_name='用户名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'customer'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ['-customer_name']

    def __unicode__(self):
        return self.customer_name

    def __str__(self):
        return self.customer_name


class Supplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True, db_column='supplier_id', verbose_name='pk')
    supplier_code = models.CharField(max_length=20, db_column='supplier_code', blank=True,
                                     unique=True, null=True, verbose_name='供应商编码')
    parent_supplier = models.ForeignKey('self', db_column='parent_supplier_id', verbose_name='父类供应商ID',
                                        blank=True, null=True, db_constraint=False, on_delete=models.PROTECT)
    supplier_name = models.CharField(max_length=50, db_column='supplier_name', null=True, blank=True,
                                     verbose_name='供应商名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.supplier_name

    def __str__(self):
        return self.supplier_name


class Department(models.Model):
    department_id = models.BigAutoField(primary_key=True, db_column='department_id', verbose_name='pk')
    department_code = models.CharField(max_length=20, db_column='department_code', null=True, blank=True,
                                       unique=True, verbose_name='部门编码')
    parent_department = models.ForeignKey('self', db_column='parent_department_id', verbose_name='父类部门ID',
                                          blank=True, null=True, db_constraint=False, on_delete=models.PROTECT)
    department_name = models.CharField(max_length=50, db_column='department_name', null=True, blank=True,
                                       verbose_name='部门名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'department'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.department_name

    def __str__(self):
        return self.department_name


class BillRelation(models.Model):
    bill_relation_id = models.BigAutoField(primary_key=True, db_column='bill_relation_id', verbose_name='pk')
    relation = models.CharField(max_length=20, db_column='relation', null=True, blank=True, verbose_name='表关系')
    source_id = models.IntegerField(db_column='source_id', null=True, blank=True, default=None, verbose_name='源')
    target_id = models.IntegerField(null=True, blank=True, db_column='target_id', verbose_name='目标')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'bill_relation'
        verbose_name = '表关系'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.relation

    def __str__(self):
        return self.relation


class Employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True, db_column='employee_id', verbose_name='pk')
    employee_code = models.CharField(max_length=20, db_column='employee_code', blank=True, null=True,
                                     verbose_name='员工编码', unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, db_column='department_id',
                                   blank=True, null=True, db_constraint=False, verbose_name='部门ID')
    employee_name = models.CharField(max_length=50, db_column='employee_name', blank=True, null=True,
                                     verbose_name='员工名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'employee'
        verbose_name = '员工表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.employee_name

    def __str__(self):
        return self.employee_name


class Model(models.Model):
    model_id = models.BigAutoField(primary_key=True, db_column='model_id', verbose_name='pk')
    model_code = models.CharField(max_length=20, db_column='model_code', blank=True, null=True,
                                  unique=True, verbose_name='模型编码')
    model_type_meta = models.ForeignKey(Meta, db_column='moedl_type_meta_id', on_delete=models.PROTECT,
                                        blank=True, null=True, db_constraint=False,
                                        related_name='type_meta_id_of', verbose_name='类型ID')
    model_name = models.CharField(max_length=50, db_column='model_name', blank=True, null=True,
                                  verbose_name='模型名称')
    unit_meta = models.ForeignKey(Meta, db_column='unit_meta_id', on_delete=models.PROTECT,
                                  blank=True, null=True, db_constraint=False, verbose_name='单位ID',
                                  related_name='meta_id_of')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'model'
        verbose_name = 'model表'
        verbose_name_plural = verbose_name
        ordering = ['-model_id']

    @property
    def customer(self):
        customer = Customer.objects.get(customer_id=int(self.spec['customer_id']))
        return customer

    @property
    def season(self):
        season = Meta.objects.get(meta_id=int(self.spec['season_meta_id']))
        return season

    def __unicode__(self):
        return self.model_name

    def __str__(self):
        return self.model_name


class Item(models.Model):
    item_id = models.BigAutoField(primary_key=True, db_column='item_id', verbose_name='pk')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='model_id',
                              blank=True, null=True, db_constraint=True,
                              related_name='model_id_of', verbose_name='模型ID')
    item_code = models.CharField(max_length=20, db_column='item_code', blank=True,
                                 null=True, verbose_name='产品编码')
    item_name = models.CharField(max_length=50, db_column='item_name', blank=True, null=True,
                                 verbose_name='产品名称')
    spec = JSONField(null=True, blank=True)
    extend = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'item'
        verbose_name = '产品表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.item_name

    def __str__(self):
        return self.item_name
