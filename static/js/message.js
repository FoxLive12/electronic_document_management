var viewDoc = false;
document.querySelector('#action-view').addEventListener('click', e => {
    var areaView = document.getElementById('doc-view');
    if (viewDoc == true){
        areaView.style = "display: none";
        viewDoc = false;
    }
    else {
        areaView.style = "display: block";
        viewDoc = true;
    }
});

function handler(e){
    var el = e.target;
    console.log(el.innerHTML);
    if(el.innerHTML == "Посмотреть документ"){
      el.innerHTML = "Скрыть документ";
    } else {
      el.innerHTML = "Посмотреть документ";
    }
  }