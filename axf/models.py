from django.db import models

# Create your models here.

#基础类
class Base(models.Model):
    #图片
    img = models.CharField(max_length=100)
    #name
    name = models.CharField(max_length=100)
    #id
    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True


#lunbotu
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'

#daohang
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'
#mustbay
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

