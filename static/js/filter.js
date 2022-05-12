var viewFilter = false;

document.querySelector('#filter-bttn').addEventListener('click', e => {
    var filterBody = document.getElementById('filter-body');
    if (viewFilter == true){
        filterBody.style = "display: none";
        viewFilter = false;
    }
    else {
        filterBody.style = "display: block";
        viewFilter = true;
    }
  });