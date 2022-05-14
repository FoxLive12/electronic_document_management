var hideSide = false

document.querySelector('#burger').addEventListener('click', e => {   
    var side = document.getElementById('hide-side')
    var image = document.getElementById('burger')
    if (hideSide == false){
        side.style.display = 'block';
        image.setAttribute('src', '/static/image/icons/arrowleft.svg')
        hideSide = true;
    }
    else{
        side.style.display = 'none';
        image.setAttribute('src', '/static/image/icons/burger.svg')
        hideSide = false;
    }
});