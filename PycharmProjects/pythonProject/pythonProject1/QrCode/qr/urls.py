from django.urls import path,include

from .views  import scancode,createqrcode,display_all_qr_codes,base

urlpatterns = [
    path('scancode/',scancode,name='scancode'),
    path('createqrcode/', createqrcode,name='createqrcode'),
    path('', base,name='base'),
    path('all_qr_codes/', display_all_qr_codes,name='display_all_qr_codes'),
]