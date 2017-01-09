
window.onload = function() {

    var current,
    output,
    limit,
    zero,
    period,
    operator,
    current_figure,
    current_amount,
    fruit;

    var current_figure = 0;
    var current_amount = 0;

    var fruit_rm;
    var fruit = {};
    var idx_fruit;

    document.getElementById('size').value = 0;
    document.getElementById('figure').disabled = false;
    document.getElementById('count').disabled = false;

    document.getElementById('crf').childNodes.item(0).nodeValue = 'Figure: 0';
    document.getElementById('amf').childNodes.item(0).nodeValue = 'Amount: 0';

    document.getElementById('tof').childNodes.item(0).nodeValue = 'Total figure: 0';
    document.getElementById('tocn').childNodes.item(0).nodeValue = 'Total count : 0';
    document.getElementById('limcn').childNodes.item(0).nodeValue = 'Limit count : 700';

    var elem = document.querySelectorAll(".num");
    var len = elem.length;

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

      var str = String(fruit[idx_fruit].f) + ', ' + String(fruit[idx_fruit].c)
      label.innerHTML = str;

      fld.appendChild(label);
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

      if (remcount != 0){
        for (s = 0; s < remcount + 1; s++){
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
              rm.remove();

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
              document.getElementById('crf').childNodes.item(0).nodeValue = 'Figure: 0';
              document.getElementById('amf').childNodes.item(0).nodeValue = 'Amount: 0';
              current_figure = 0;
              current_amount = 0;
            }
          }
     },false);
    }

    document.querySelector("#figure").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = true;
        document.getElementById('count').disabled = false;
        document.getElementById('size').value = 0;

        var str = String(ch2)
        document.getElementById('crf').childNodes.item(0).nodeValue = 'Figure: ' + ch2;
        current_figure = ch2;

        if (current_figure > 0 && current_amount > 0){

          var size = Object.keys(fruit).length
          if (size == 0){
            idx_fruit = 0
          }
          fruit[idx_fruit] = {'f': current_figure, 'c': current_amount};
          fruitnew(idx_fruit);
          idx_fruit += 1;
        }

      }

    },false);

    document.querySelector("#count").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = true;
        document.getElementById('size').value = 0;

        var str = String(ch2)
        document.getElementById('amf').childNodes.item(0).nodeValue = 'Amount: ' + ch2;
        current_amount = ch2;

        if (current_figure > 0 && current_amount > 0){

          var size = Object.keys(fruit).length
          if (size == 0){
            idx_fruit = 0
          }
          fruit[idx_fruit] = {'f': current_figure, 'c': current_amount};
          fruitnew(idx_fruit);
          idx_fruit += 1;
        }

      }

    },false);

    document.querySelector("#delete").addEventListener("click",function() {

        document.getElementById('size').value = 0;
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = false;

        document.getElementById('crf').childNodes.item(0).nodeValue = 'Figure: 0';
        document.getElementById('amf').childNodes.item(0).nodeValue = 'Amount: 0';

        current_figure = 0;
        current_amount = 0;

        fruitremove();


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
}
