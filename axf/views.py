import hashlib
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart
from py1809AXF import settings


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

# 购物车
def cart(request):
    token = request.session.get('token')
    # carts = []
    if token:
        # 显示该用户下 购物车信息
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        return render(request,'cart/cart.html',context={'carts':carts})
    else:
        # 跳转到登录页面
        return redirect('axf:login')


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

        # 购物车数据
    token = request.session.get('token')
    carts = []
    if token:  # 根据用户，获取对应用户下所有购物车数据
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)
    data = {
        'foodtypes':foodtypes,
        'goodsList':goodsList,
        'childTypleList': childTypleList,
        'categoryid':categoryid,
        'childid': childid,
        'carts': carts,
    }

    return render(request, 'market/market.html', context=data)


def mine(request):
    token = request.session.get('token')

    responseData = {}

    if token:  # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['isLogin'] = 1
    else:  # 未登录
        responseData['name'] = '未登录'
        responseData['img'] = '/static/uploads/axf.png'

    return render(request, 'mine/mine.html', context=responseData)


def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()

def registe(request):
    if request.method == 'GET':
        return render(request,'mine/registe.html')
    elif request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = genarate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')
        # return HttpResponse('ok')
    # icon
        imgName = user.account + '.png'
        imagePath = os.path.join(settings.MEDIA_ROOT,imgName)
        file = request.FILES.get('icon')
        with open(imagePath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        user.save()

        request.session['token'] = user.token

        return redirect('axf:mine')


def checkaccount(request):
    account = request.GET.get('account')
    responseData = {
        'msg': '账号可用',
        'status': 1  # 1标识可用，-1标识不可用
    }
    try:
        user = User.objects.get(account=account)
        responseData['msg'] = '账号已被占用'
        responseData['status'] = -1
        return JsonResponse(responseData)
    except:
        return JsonResponse(responseData)


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password):

    #             登录成功  更新token
                user.token = str(uuid.uuid5(uuid.uuid4(),'login'))
                user.save()

                request.session['token'] = user.token
                return redirect('axf:mine')
            else:
                return render(request,'mine/login.html',context={'passwdErr':'密码错误'})
        except:
            return  render(request,'mine/login.html',context={'acountErr':'账号不存在!'})


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg': '添加购物车成功',
        'status': 1  # 1标识添加成功，0标识添加失败，-1标识未登录
    }
    # print(goodsid)
    if token: # 登录 [直接操作模型]
        # 获取用户
        user = User.objects.get(token=token)
        # 获取商品
        goods = Goods.objects.get(pk=goodsid)

        # 商品已经在购物车，只修改商品个数
        # 商品不存在购物车，新建对象（加入一条新的数据）
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():  # 修改数量
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:  # 添加一条新记录
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['number'] = cart.number
        return JsonResponse(responseData)
    else: # 未登录 [跳转到登录页面]
        # 由于addcart这个是 用于 ajax操作， 所以这里是不能进行重定向!!
        # return redirect('axf:login')
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)


def subcart(request):
    # 获取数据
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    # 对应用户 和 商品
    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    # 删减操作
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '购物车减操作成功',
        'status': 1,
        'number': cart.number
    }

    return JsonResponse(responseData)


def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not  cart.isselect
    cart.save()
    responseData = {
        'msg': '选中状态改变',
        'status': 1,
        'isselect': cart.isselect
    }
    return JsonResponse(responseData)


def changecartselect(request):
    isselect = request.GET.get('isselect')
    if isselect == 'true':
        isselect=True
    else:
        isselect=False
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()

    return JsonResponse({'msg': '反宣状态改变', 'status':1})