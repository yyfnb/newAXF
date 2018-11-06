$(function () {
    $('.login').width(innerWidth)

    $('#subButton').on('click',function () {
        console.log('denglu')

        temp1 = checkingAccount()
        temp2 = checkingPassword()
        if( temp1 && temp2 ){
            $('.login form').submit()
        }

    })

    function checkingAccount() {
        var reg = /^[A-Za-z0-9]+$/
        var accountInput = $('#account input')
        if (reg.test(accountInput.val())){
            $('#account i').html('')
            $('#account').removeClass('has-error').addClass('has-success')
            $('#account span').removeClass('glyphicon-remove').addClass('glyphicon-ok')

            return true
        }else {    // 不符合
            $('#account i').html('账号由数字、字母组成')
            $('#account').removeClass('has-success').addClass('has-error')
            $('#account span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
            // $('#subButton').attr('disabled','disabled')
            return false
        }

    }

    function checkingPassword() {
        var reg = /^[\d]{6,12}$/
         var passwordInput = $('#password input')
        if (reg.test(passwordInput.val())) {  // 符合
            $('#password i').html('')
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
            return true
             } else {    // 不符合
            $('#password i').html('6~12位纯数字')
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
            return false
        }

    }
})