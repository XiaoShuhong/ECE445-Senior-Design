from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('upload_clothes/index',views.upload_clothes_index,name='upload_clothes_index'),
    path('upload_clothes/upload',views.do_upload,name='upload_clothes'),
    path('upload_clothes/success<str:category> <str:filename>',views.comfirm_category,name='comfirm_category'),
    path('gallery/index/<str:catename><int:pidx>',views.gallery_index,name='gallery_index'),
    path('gallery/index/detail/<str:catename><int:pidx>',views.change_cate,name='gallery_detail'),
    path('recom/index',views.recom_index,name='recom_index'),
    path('recom/outfit_display<str:style><str:weather>',views.generate_outfit,name='generate_outfit'),
    path('recom/call_hanger<str:imgid>',views.call_hanger,name='call_hanger'),
    
]
