window.onload = function() {

    var current,
    screen,
    output,
    limit,
    zero,
    period,
    operator;

    document.getElementById('size').value = 0;
    document.getElementById('figure').disabled = false;
    document.getElementById('count').disabled = false;
    screen = document.getElementById("result");
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
          }
     },false);
    }

    document.querySelector("#figure").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = true;
        document.getElementById('count').disabled = false;
        document.getElementById('size').value = 0;
      }

    },false);

    document.querySelector("#count").addEventListener("click",function() {

      ch2 = document.getElementById('size').value;

      if(parseInt(ch2) != 0) {
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = true;
        document.getElementById('size').value = 0;
      }

    },false);

    document.querySelector("#delete").addEventListener("click",function() {

        document.getElementById('size').value = 0;
        document.getElementById('figure').disabled = false;
        document.getElementById('count').disabled = false;

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
