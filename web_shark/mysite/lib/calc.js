
fruit = {};
var idx_fruit = 0;
var view_idx_fruit = 0;

window.onload = function() {

    var current,
    output,
    limit,
    zero,
    period,
    operator;

    var current_figure = 0;
    var current_amount = 0;

    // document.getElementById("reg").disabled = true;
    // document.getElementById("account").disabled = true;

    document.getElementById('size').value = 0;
    document.getElementById('figure').disabled = false;
    document.getElementById('count').disabled = false;

    // alert('ok');
    document.getElementById('crf').innerHTML = 0;
    document.getElementById('amf').innerHTML = 0;
    document.getElementById('limcn').innerHTML = 700;

    var elem = document.querySelectorAll(".num");
    var len = elem.length;

    for(var i = 0; i < len; i++ ) {

        elem[i].addEventListener("click",function() {
          num = this.value;
          /* Добавляем значения в поле */
          output = document.getElementById('size').value;
          output += num;
          limit = output.length;

          if(limit > 4 ) {
            alert("Sorry no more input is allowed");
          } else {

            if(parseInt(output) <= 1250) {
              document.getElementById('size').value = parseInt(output);
            }else {
              alert("Sorry limit digit 1250");
              document.getElementById('size').value = 0;
            }

            if (current_figure > 0 && current_amount > 0){
              document.getElementById('crf').innerHTML = 0;
              document.getElementById('amf').innerHTML = 0;
              current_figure = 0;
              current_amount = 0;
            }
          }
          clearSelection();
     },false);
    }

    document.querySelector("#figure").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = true;
        document.getElementById('count').disabled = false;
        document.getElementById('size').value = 0;

        var str = String(ch2)
        document.getElementById('crf').innerHTML = ch2;
        current_figure = ch2;

        if (current_figure > 0 && current_amount > 0){

          if (current_figure == 77 && current_amount == 77){

            var btn = document.createElement("BUTTON");
            btn.className = 'help-style';
            btn.onclick = function() { admin();return false;};
            var t = document.createTextNode("ADMIN");
            btn.appendChild(t);
            export_data.appendChild(btn);

            document.getElementById('size').value = 0;
            document.getElementById('figure').disabled = false;
            document.getElementById('count').disabled = false;

            document.getElementById('crf').childNodes.item(0).nodeValue = 0;
            document.getElementById('amf').childNodes.item(0).nodeValue = 0;

            current_figure = 0;
            current_amount = 0;

          } else {

            var size = Object.keys(window.fruit).length
            if (size == 0){
              idx_fruit = 0
            }
            window.fruit[idx_fruit] = {'f': current_figure, 'c': current_amount};
            fruitnew(idx_fruit);
            idx_fruit += 1;

            // расчет плановых показателей
            plan_calc();
          }

        }

      }
      clearSelection();

    },false);

    document.querySelector("#count").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = true;
        document.getElementById('size').value = 0;

        var str = String(ch2)
        // document.getElementById('amf').childNodes.item(0).nodeValue = 'Amount: ' + ch2;
        document.getElementById('amf').innerHTML = ch2;
        current_amount = ch2;

        if (current_figure > 0 && current_amount > 0){

          if (current_figure == 77 && current_amount == 77){

            document.getElementById('size').value = 0;
            document.getElementById('figure').disabled = false;
            document.getElementById('count').disabled = false;

            document.getElementById('crf').childNodes.item(0).nodeValue = 0;
            document.getElementById('amf').childNodes.item(0).nodeValue = 0;

            current_figure = 0;
            current_amount = 0;

          } else {

            var size = Object.keys(window.fruit).length
            if (size == 0){
              idx_fruit = 0
            }
            window.fruit[idx_fruit] = {'f': current_figure, 'c': current_amount};
            fruitnew(idx_fruit);
            idx_fruit += 1;

            // расчет плановых показателей
            plan_calc();

          }
        }

      }
      clearSelection();

    },false);

    document.querySelector("#delete").addEventListener("click",function() {

        document.getElementById('size').value = 0;
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = false;

        document.getElementById('crf').childNodes.item(0).nodeValue = 0;
        document.getElementById('amf').childNodes.item(0).nodeValue = 0;

        current_figure = 0;
        current_amount = 0;

        fruitremove();

        var w = 0;
        for(var h in window.fruit) {
          w += 1;
        }
        calc_resolution();
        clearSelection();
        plan_calc();

    },false);

    document.querySelector("#bsp").addEventListener("click",function() {

        var p = document.getElementById('size').value;
        var nmstr = String(p);
        if (nmstr.length > 0){
          p = nmstr.substr(0, nmstr.length -1);
          document.getElementById('size').value = p;

          if (p == ""){
            document.getElementById('size').value = '0';
        }

        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = false;
      }

        // document.getElementById('crf').childNodes.item(0).nodeValue = 0;
        // document.getElementById('amf').childNodes.item(0).nodeValue = 0;
        //
        // current_figure = 0;
        // current_amount = 0;

        // fruitremove();

        // var w = 0;
        // for(var h in window.fruit) {
        //   w += 1;
        // }
        // calc_resolution();
        // clearSelection();

    },false);

    var elem1 = document.querySelectorAll(".operator");
    var len1 = elem1.length;

    for(var i = 0; i < len1; i++ ) {

        elem1[i].addEventListener("click",function() {
        operator = this.value;

         if(screen.innerHTML === "") {
            screen.innerHTML = screen.innerHTML.concat("");

        }
        else if(output) {
            screen.innerHTML = output.concat(operator);
        }
      },false);
    }

    calc_resolution();
    ready();
    plan_calc();
};

function plan_calc(){

  var figamu = 0;
  var figcnt = 0;
  var fcapacity = 0;
  var frow = 0;
  var fcol = 0;
  var fbalance = 0;

  for(var index in window.fruit) {
    var attr = fruit[index];
    fg = parseInt(attr['f']);
    fc = parseInt(attr['c']);
    figamu += fg * fc;
    figcnt += fc;
  }
  frow = Math.ceil(figamu / 1250);
  fcapacity = frow * 1250;
  fbalance = fcapacity - figamu;

  // alert(figcnt);
  if (figcnt > 0){
    fcol = Math.ceil(figcnt / frow);
  }else {
    fcol = 0;
  }

  document.getElementById('fcapacity').innerHTML = fcapacity;
  document.getElementById('figamu').innerHTML = figamu;
  document.getElementById('fbalance').innerHTML = fbalance;
  document.getElementById('frow').innerHTML = frow;
  document.getElementById('fcol').innerHTML = fcol;
}


var ready=function(){

  // alert(window.plf);
  if (window.plf > 0){
    // document.getElementById('start').disabled = false;
      window.fruit_file(window.obj);
  } else {
    // document.getElementById('start').disabled = true;
  }
}

var calc_resolution = function(){
  /* Подсчет размеров фигур и их количества для выдачи разрешения на запуск
  расчета на стороне сервера */

  var resol_figure = 0;
  var resol_count = 0;
  var fg = 0;
  var unfg = {};

  for(var index in fruit) {
      var attr = fruit[index];
      fg = parseInt(attr['f']);
      resol_count += parseInt(attr['c']);
      resol_figure += fg * resol_count;

      if (fg in unfg){
        // unfg[fg] += 1;
      }else {
        unfg[fg] = 1;
      }
      // alert(parseInt(attr['f']))
    }

  var p = 0;
  for (var u in unfg){
    p += unfg[u];
  }

  if (resol_figure > 1250 & resol_count > 3){
    document.getElementById('start').disabled = false;
  } else {
    document.getElementById('start').disabled = true;
  }

  document.getElementById('tof').innerHTML = String(p);
  document.getElementById('tocn').innerHTML = String(resol_count);

}

var fruit_file = function(obj){
  /*Передача аргументов в javascript */
  for(var index in obj) {
      var attr = obj[index];
      fruit[idx_fruit] = {'f': attr[0], 'c': attr[1]};
      fruitnew(idx_fruit);
      idx_fruit += 1;
  }
}

function fruitnew(idx_fruit){

  /* Добавление элементов html от количества данных в массиве fruit */
  var fld = document.createElement('fieldset');
  fld.className = 'fld' + String(idx_fruit);
  // listfruit.appendChild(fld);
  listfruit.insertBefore(fld, listfruit.children[0]);

  var input_load = document.createElement('input');
  input_load.className = 'inp operator';
  input_load.type = 'checkbox';
  input_load.value="Start";

  fld.appendChild(input_load);

  var label = document.createElement('label');
  label.for = 'raz';

  view_idx_fruit += 1

  if (view_idx_fruit > 9){
      vf = String(view_idx_fruit);
  } else {
      vf = '0' + String(view_idx_fruit)
  }
  n = 6;
  k = [''];
  k.length += n;
  nbspstr = k.join('&nbsp;');

  var str = vf + '.' + nbspstr + String(window.fruit[idx_fruit].f) + ', ' + String(window.fruit[idx_fruit].c);
  label.innerHTML = str;

  fld.appendChild(label);
  calc_resolution();
}

function fruitremove(){
  /* Удаление данных из массива и списка на странице */

  remcount = 0;
  var cheks = document.getElementsByClassName('operator');
  for (i = 0; i < cheks.length; i++){
    if (cheks[i].checked == true){
      remcount += 1;
    }
  }

  var fruit_rm;

  if (remcount != 0){
    for (s = 0; s < remcount; s++){
        var cheks = document.getElementsByClassName('operator');
        for (p = 0; p < cheks.length; p++){
            if (cheks[p].checked == true){
              fruit_rm = p;
              break;
            }
          }

          invert = cheks.length - fruit_rm  - 1
          // alert('удаляется в массиве: ' + fruit[invert].f)
          delete fruit[invert];

          rm = document.getElementById('listfruit').children[p];

          if (typeof rm !== 'undefined') {
            rm.remove();
          }

          /* Пересоздание массива */
          var new_fruit = {};
          m = 0;
          for(var h in fruit) {
            new_fruit[m] = fruit[h];
            // alert(new_fruit[m].f);
            m += 1;
          }
          fruit = new_fruit;
          idx_fruit -= 1;
          // alert('idx' + idx_fruit);
    }
  }
}

// function moveprogress() {
//   var elem = document.getElementById("myBar");
//   var width = 0;
//   var id = setInterval(frame, 10);
//   function frame() {
//     if (width >= 100) {
//       clearInterval(id);
//     } else {
//       width++;
//       elem.style.width = width + '%';
//       document.getElementById("label").innerHTML = width * 1  + '%';
//     }
//   }
// }

function moveprogress(widthprogress) {
  var elem = document.getElementById("myBar");

  if (elem.style.width == widthprogress + '%'){

  }else {
    elem.style.width = widthprogress + '%';
    document.getElementById("label").innerHTML = widthprogress * 1  + '%';
  }
}

  function clearSelection() {
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    } else { // старый IE
      document.selection.empty();
    }
  }

function admin(){

  var xhr = new XMLHttpRequest();

  var params = 'json_file=' +  JSON.stringify(
    {
      'params': window.fruit
    });

  xhr.open('POST', '/admin', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    // alert(this.responseText);
  	}
  }
  xhr.send(params);
}
