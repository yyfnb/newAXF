from django.conf.urls import url

from axf import views

urlpatterns =[
    url(r'^$',views.home,name='index'),
    url(r'^home/$',views.home,name='home'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^market/$',views.market,name='market'),
    url(r'^mine/$',views.mine,name='mine'),
]