from django.conf.urls import url

from axf import views

urlpatterns =[
    url(r'^$',views.home,name='index'),
    url(r'^home/$',views.home,name='home'),
    url(r'^cart/$',views.cart,name='cart'), #gouwuche
    url(r'^market/(\d+)/(\d+)/(\d+)/$',views.market,name='market'), #闪购超市
    url(r'^mine/$',views.mine,name='mine'),#我的

    url(r'^registe/$',views.registe,name='registe'),#注册
    url(r'^checkaccount/$',views.checkaccount,name='checkaccount'),#验证
    url(r'^logout/$', views.logout, name='logout'),#登出
    url(r'^login/$', views.login, name='login'),#登录

    url(r'^addcart/$',views.addcart,name='addcart'),  #添加购物车
    url(r'^subcart/$',views.subcart,name='subcart'),    # 购物车减操作

    # 修改选中状态
    url(r'^changecartstatus/$',views.changecartstatus,name='changecartstatus'),
    # quanxuan 取消全选
    url(r'^changecartselect/$',views.changecartselect,name='changecartselect'),
]