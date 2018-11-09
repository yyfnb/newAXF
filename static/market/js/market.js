$(function () {
    $('.market').width(innerWidth)

    // 获取typeIndex
    typeIndex = $.cookie('typeIndex')
    if (typeIndex){ // 已经有点击分类
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 没有点击分类
        // 没有点击默认第一个
        $('.type-slider .type-item:first').addClass('active')
    }


    // 侧边栏


    // cookie
    // 设置cookie


    // 获取cookie


    // 删除cookie

    $('.type-item').click(function () {
        // $(this).addClass('active')
        // 记录位置
        $.cookie('typeIndex', $(this).index(), {expires:3, path:'/'})
    })


    // 分类按钮
    categoryBt = false  // 默认是隐藏
    $('#categoryBt').click(function () {
        // 取反
        categoryBt = !categoryBt

        categoryBt ? categoryViewShow() : categoryViewHide()

        // if (categoryBt){    // 显示
        //     $('.bounce-view.category-view').show()
        //     $('#categoryBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
        // } else {    // 隐藏
        //     $('.bounce-view.category-view').hide()
        //     $('#categoryBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
        // }
    })


    // 排序按钮
    sortBt = false  // 默认是隐藏
    $('#sortBt').click(function () {
        // 取反
        sortBt = !sortBt

        sortBt ? sortViewShow() : sortViewHide()
    })

    // 灰色蒙层
    $('.bounce-view').click(function () {
        sortBt = false
        sortViewHide()
        categoryBt = false
        categoryViewHide()
    })


    function categoryViewShow() {
        sortBt = false
        sortViewHide()
        $('.bounce-view.category-view').show()
        $('#categoryBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }
    function categoryViewHide() {
        $('.bounce-view.category-view').hide()
        $('#categoryBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }

    function sortViewShow() {
        categoryBt = false
        categoryViewHide()
        $('.bounce-view.sort-view').show()
        $('#sortBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }
    function sortViewHide() {
        $('.bounce-view.sort-view').hide()
        $('#sortBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }

     // 购物车操作
    $('.bt-wrapper .glyphicon-minus').hide()
    $('.bt-wrapper .num').hide()


    // 有商品数据的，即要显示； 否则不显示
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num){   // 有数据，即有添加购物车
            $(this).show()
            $(this).prev().show()
        }
    })


    // 加操作
    $('.bt-wrapper .glyphicon-plus').click(function () {
        // 商品ID
        var goodsid = $(this).attr('goodsid')
        console.log(goodsid)
        // that为了解决，在ajax中，this指向问题
        var $that = $(this)

        $.get('/addcart/',{'goodsid':goodsid}, function (response) {
            console.log(response)
            if (response.status == -1){ // 未登录
                window.open('/login/', target="_self")
            } else if (response.status == 1){   // 添加成功
                // 错误的！！！
                // $('.bt-wrapper .glyphicon-minus').show()
                // $('.bt-wrapper .num').show().html(response.number)



                // 只修改当前操作的商品
                // $(this).prev().show().html(response.number)
                // $(this).prev().prev().show()

                $that.prev().show().html(response.number)
                $that.prev().prev().show()
            }
        })
    })

    // 减操作
    $('.bt-wrapper .glyphicon-minus').click(function () {
        // 商品ID
        var goodsid = $(this).attr('goodsid')
        var $that = $(this)

        // 发起ajax请求
        $.get('/subcart/', {'goodsid':goodsid},function (response) {
            console.log(response)
            if (response.status == 1){  // 操作成功
                var number = response.number
                if (number > 0) {   // 显示，改变个数
                    $that.next().html(number)
                }  else {   // 隐藏减号和个数
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })
})