var check = false;
document.querySelector('#ic-view-pass').addEventListener('click', e => {   
    var psw = document.getElementById('passw-input')
    const image = document.getElementById('ic-view-pass')
    if (check == false){
        psw.setAttribute('type', 'text')
        image.setAttribute('src', '/static/image/icons/ic-hide-pass.svg')
        check = true
    }
    else{
        psw.setAttribute('type', 'password')
        image.setAttribute('src', '/static/image/icons/ic-view-pass.svg')
        check = false
    }
});

var re_check = false;
document.querySelector('#ic-view-re-pass').addEventListener('click', e => {   
    var psw = document.getElementById('re-passw-input')
    const image = document.getElementById('ic-view-re-pass')
    if (re_check == false){
        psw.setAttribute('type', 'text')
        image.setAttribute('src', '/static/image/icons/ic-hide-pass.svg')
        re_check = true
    }
    else{
        psw.setAttribute('type', 'password')
        image.setAttribute('src', '/static/image/icons/ic-view-pass.svg')
        re_check = false
    }
});

var viewSideNav = false;

document.querySelector('#open').addEventListener('click', e => {   
    var psw = document.getElementById('re-passw-input')
    const image = document.getElementById('ic-view-re-pass')
    if (re_check == false){
        psw.setAttribute('type', 'text')
        image.setAttribute('src', '/static/image/icons/ic-hide-pass.svg')
        re_check = true
    }
    else{
        psw.setAttribute('type', 'password')
        image.setAttribute('src', '/static/image/icons/ic-view-pass.svg')
        re_check = false
    }
});