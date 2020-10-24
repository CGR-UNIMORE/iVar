function disabilita(tabella,elemento) {
    jQuery('#'+tabella+'_'+elemento+'__row').fadeTo('fast',0.5);
    jQuery('#'+tabella+'_'+elemento).fadeTo('fast',0.5);
    var bs = document.getElementsByName(elemento);
    for(var i=0; i<bs.length; i++){
        bs[i].checked=false;
        bs[i].disabled=true;
    }
}
function abilita(tabella,elemento) {
    jQuery('#'+tabella+'_'+elemento+'__row').fadeTo('fast',1);
    jQuery('#'+tabella+'_'+elemento).fadeTo('fast',1);
    var bs = document.getElementsByName(elemento);
    for(var i=0; i<bs.length; i++) {
        bs[i].disabled=false;
    }
}

function vuota(elemento) {
    var bs = document.getElementsByName(elemento);
    for(var i=0; i<bs.length; i++){
        bs[i].value="";
    }
}


function resize_iframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
  }
