from django.shortcuts import render

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods


def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()
    #商品
    shopList = Shop.objects.all()
    shophead = shopList[0]
    shoptab = shopList[1:3]
    shopclass = shopList[3:7]
    shopcommend = shopList[7:11]
    #商品主题
    mainshows = MainShow.objects.all()
    data ={
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        "shoptab":shoptab,
        "shopclass":shopclass,
        "shopcommend":shopcommend,
        "mainshows":mainshows,


    }
    return render(request,'home/home.html',context=data)


def cart(request):
    return render(request,'cart/cart.html')


def market(request, categoryid, childid, sortid):    # 闪购超市
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 分类 点击 下标
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    # 将每个子类拆分出来
    childTypleList = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname': arr[0],
            'childid': arr[1]
        }
        childTypleList.append(dir)

    # 商品信息
    # goodsList = Goods.objects.all()[0:5]
    if childid == '0':  # 全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:   # 分类
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)


    # 排序
    if sortid == '1':
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2':
        goodsList = goodsList.order_by('price')
    elif sortid == '3':
        goodsList = goodsList.order_by(('-price'))

    data = {
        'foodtypes':foodtypes,
        'goodsList':goodsList,
        'childTypleList': childTypleList,
        'categoryid':categoryid,
        'childid': childid,
    }

    return render(request, 'market/market.html', context=data)


def mine(request):
    return render(request,'mine/mine.html')