from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'boms/',views.BomListView.as_view()),
    url(r'bom/',views.BomDetailView.as_view()),

    url(r'sos/',views.SoListView.as_view()),
]