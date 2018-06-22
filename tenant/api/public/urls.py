from django.conf.urls import url
from . import views

urlpatterns = [
    url('make_model_code/$', views.make_model_code),
    url('make_item_code/$', views.make_item_code),
    url('make_bom_no/$', views.make_bom_no),
    url('make_so_no/$', views.make_so_no),

    url(r'customers/$', views.CustomerListView.as_view()),
    url(r'customer/$', views.CustomerDetailView.as_view()),

    url(r'suppliers/$', views.SupplierListView.as_view()),
    url(r'supplier/$', views.SupplierDetailView.as_view()),

    url(r'departments', views.DepartmentListView.as_view()),
    url(r'department', views.DepartmentDetailView.as_view()),

    url(r'employees', views.EmployeeListView.as_view()),
    url(r'employee', views.EmployeeDetailView.as_view()),

    url(r'metas/$', views.MetaListView.as_view()),
    url(r'meta/$', views.MetaDetailView.as_view()),

    url(r'models/$', views.ModelListView.as_view()),
    url(r'model/$', views.ModelDetailView.as_view()),

    url(r'items/$',views.ItemListview.as_view()),

]
