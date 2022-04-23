from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('upload_clothes/index',views.upload_clothes_index,name='upload_clothes_index'),
    path('upload_clothes/upload',views.do_upload,name='upload_clothes'),
    path('gallery/index',views.gallery_index,name='gallery_index'),
    path('recom/index',views.recom_index,name='recom_index'),
    
]
