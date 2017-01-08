
window.onload = function() {

    var current,
    output,
    limit,
    zero,
    period,
    operator,
    current_figure,
    current_amount;

    current_figure = 0;
    current_amount = 0;

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


    },false);

    // var elem1 = document.querySelectorAll(".operator");
    // var len1 = elem1.length;
    //
    // for(var i = 0; i < len1; i++ ) {
    //
    //     elem1[i].addEventListener("click",function() {
    //     operator = this.value;
    //
    //      if(screen.innerHTML === "") {
    //         screen.innerHTML = screen.innerHTML.concat("");
    //
    //     }
    //     else if(output) {
    //         screen.innerHTML = output.concat(operator);
    //     }
    //   },false);
    // }
}
