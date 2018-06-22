# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 10:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillRelation',
            fields=[
                ('bill_relation_id', models.BigAutoField(db_column='bill_relation_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('relation', models.CharField(blank=True, db_column='relation', max_length=20, null=True, verbose_name='表关系')),
                ('source_id', models.IntegerField(blank=True, db_column='source_id', default=None, null=True, verbose_name='源')),
                ('target_id', models.IntegerField(blank=True, db_column='target_id', null=True, verbose_name='目标')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '表关系',
                'verbose_name_plural': '表关系',
                'db_table': 'bill_relation',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.BigAutoField(db_column='customer_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('customer_code', models.CharField(blank=True, db_column='customer_code', max_length=20, null=True, unique=True, verbose_name='用户编码')),
                ('customer_name', models.CharField(blank=True, db_column='customer_name', max_length=50, null=True, verbose_name='用户名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('parent_customer', models.ForeignKey(blank=True, db_column='parent_customer_id', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='public.Customer', verbose_name='父类用户ID')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'customer',
                'ordering': ['-customer_name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.BigAutoField(db_column='department_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('department_code', models.CharField(blank=True, db_column='department_code', max_length=20, null=True, unique=True, verbose_name='部门编码')),
                ('department_name', models.CharField(blank=True, db_column='department_name', max_length=50, null=True, verbose_name='部门名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('parent_department', models.ForeignKey(blank=True, db_column='parent_department_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='public.Department', verbose_name='父类部门ID')),
            ],
            options={
                'verbose_name': '部门表',
                'verbose_name_plural': '部门表',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.BigAutoField(db_column='employee_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('employee_code', models.CharField(blank=True, db_column='employee_code', max_length=20, null=True, unique=True, verbose_name='员工编码')),
                ('employee_name', models.CharField(blank=True, db_column='employee_name', max_length=50, null=True, verbose_name='员工名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('department', models.ForeignKey(blank=True, db_column='department_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='public.Department', verbose_name='部门ID')),
            ],
            options={
                'verbose_name': '员工表',
                'verbose_name_plural': '员工表',
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.BigAutoField(db_column='item_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('item_code', models.CharField(blank=True, db_column='item_code', max_length=20, null=True, verbose_name='产品编码')),
                ('item_name', models.CharField(blank=True, db_column='item_name', max_length=50, null=True, verbose_name='产品名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '产品表',
                'verbose_name_plural': '产品表',
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('meta_id', models.BigAutoField(db_column='meta_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('meta_code', models.CharField(blank=True, db_column='meta_code', max_length=20, null=True, unique=True, verbose_name='元数据编码')),
                ('meta_name', models.CharField(blank=True, db_column='meta_name', max_length=50, null=True, verbose_name='元数据名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('parent_meta', models.ForeignKey(blank=True, db_column='parent_meta_id', db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='public.Meta', verbose_name='父元数据ID')),
            ],
            options={
                'verbose_name': '元数据表',
                'verbose_name_plural': '元数据表',
                'db_table': 'meta',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('model_id', models.BigAutoField(db_column='model_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('model_code', models.CharField(blank=True, db_column='model_code', max_length=20, null=True, unique=True, verbose_name='模型编码')),
                ('model_name', models.CharField(blank=True, db_column='model_name', max_length=50, null=True, verbose_name='模型名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('model_type_meta', models.ForeignKey(blank=True, db_column='moedl_type_meta_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='type_meta_id_of', to='public.Meta', verbose_name='类型ID')),
                ('unit_meta', models.ForeignKey(blank=True, db_column='unit_meta_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='meta_id_of', to='public.Meta', verbose_name='单位ID')),
            ],
            options={
                'verbose_name': 'model表',
                'verbose_name_plural': 'model表',
                'db_table': 'model',
                'ordering': ['-model_id'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.BigAutoField(db_column='supplier_id', primary_key=True, serialize=False, verbose_name='pk')),
                ('supplier_code', models.CharField(blank=True, db_column='supplier_code', max_length=20, null=True, unique=True, verbose_name='供应商编码')),
                ('supplier_name', models.CharField(blank=True, db_column='supplier_name', max_length=50, null=True, verbose_name='供应商名称')),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('extend', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('parent_supplier', models.ForeignKey(blank=True, db_column='parent_supplier_id', db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='public.Supplier', verbose_name='父类供应商ID')),
            ],
            options={
                'verbose_name': '供应商表',
                'verbose_name_plural': '供应商表',
                'db_table': 'supplier',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='model',
            field=models.ForeignKey(blank=True, db_column='model_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_id_of', to='public.Model', verbose_name='模型ID'),
        ),
    ]
