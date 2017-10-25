

// function ready(){
//
//   var plf = Object.keys(window.obj).length;
//   if (window.plf > 0){
//     // document.getElementById('start').disabled = false;
//       window.fruit_file(obj);
//   } else {
//     // document.getElementById('start').disabled = true;
//   }
// };
// document.addEventListener("DOMContentLoaded", ready);
// alert(window.plf);

  function check_settings(){
    document.getElementById('setting_start').value = 1;
  }


  function submit_figure(event) {

    // Проверка на нажатие кнопки Settings
    if (event.set_start.value == 1) {
      return false
    } else {
      document.getElementById('setting_start').value = 0;
    }

    if (window.dis == 0){
      moveprogress(0);
      window.subscribe = 0;
      window.clone_fruit = window.fruit;

      // h = 0;
      // for(var h in window.clone_fruit) {
      //   h += 1;
      // }
      // alert(h);
      window.knox = document.getElementById('rangeInput').value;
      window.limright = document.getElementById('rangeInput_1').value;
      window.attempt = document.getElementById('rangeInput_2').value;

      objSel = document.getElementById("selectImage");
      window.correto = getSelectedIndexes(objSel);
      // alert ( getSelectedIndexes(objSel) );

      // Запуск функции проверки промокода
      check_promokey();

      window.intervalID = setInterval(eee, 3000);
      window.cnvsopt = new CanvasLoader('canvasloader-optimization');
      cnvsopt.setShape('spiral'); // default is 'oval'
      cnvsopt.setDiameter(30); // default is 40
      cnvsopt.setDensity(18); // default is 40
      cnvsopt.setRange(0.5); // default is 1.3
      cnvsopt.setSpeed(1); // default is 2
      cnvsopt.setFPS(20); // default is 24
      cnvsopt.show(); // Hidden by default
    } else {
    /* Добавить обработчик если пользователь отписался от заявки на расчет */
      window.subscribe = 1;
    }
    status_opt('Запрос!');
    return false
  }

  function check_promokey(){
    var xmlhttp;
    // Are we using a modern browser or ...
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    } else {
      // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!xmlhttp){
      alert("Error initializing XMLHttpRequest!");
    }

    function GetResult(){
      if (xmlhttp.readyState==4 && xmlhttp.status==200) {
        var jsonret = JSON.parse(xmlhttp.responseText);

        if (jsonret[1] == "activated_key"){
            clearInterval(window.interval_tempkey);
            // location.href = '/export?unique=' + window.unique;
            window.flag_tempkey = 0;
            window.cltempkey.hide();
          }
      } else {
          alert("Server, data not available");
        }
      }

    xmlhttp.onload = GetResult;
    // xmlhttp.onerror = Bad_server;
    // send the request in an async way
    xmlhttp.open("POST", "/checkpromo.json", true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    var json_file = 'json_file=' + JSON.stringify(
      {'unique':window.unique
    });

    xmlhttp.send(json_file);
  }


  function submit_kml(form) {

    var searchForm = document.forms["myForm"];
    var keyBox = searchForm.elements["fkml"];

    var i = keyBox.value;
    i = i.substr(i.length - 4, i.length).toLowerCase();
    i = i.replace('.','');
    switch(i){
      case 'txt':
          form.submit();
          break;
      case 'xlsx':
          form.submit();
          break;
      default:
        alert('no extension file (txt) or (xlsx)');
        break;
    }
  }

  function submit_export() {
    if (window.flag_save == 0) {
        window.interval_export = setInterval(start_export, 3000);
        window.flag_save = 1;

        window.cl = new CanvasLoader('canvasloader-container');
        cl.setShape('spiral'); // default is 'oval'
        cl.setDiameter(40); // default is 40
        cl.setDensity(15); // default is 40
        cl.setRange(0.5); // default is 1.3
        cl.setSpeed(1); // default is 2
        cl.setFPS(17); // default is 24
        cl.show(); // Hidden by default

    } else {
      // alert(window.flag_save);
    }
  }

  function start_export(){
    var xmlhttp;
    // Are we using a modern browser or ...
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    } else {
      // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!xmlhttp){
      alert("Error initializing XMLHttpRequest!");
    }

    function GetResult(){
      if (xmlhttp.readyState==4 && xmlhttp.status==200) {
        var jsonret = JSON.parse(xmlhttp.responseText);

        if (jsonret[1] == "prepared_file"){
            clearInterval(window.interval_export);
            location.href = '/export?unique=' + window.unique;
            window.flag_save = 0;
            window.cl.hide();
          }
      } else {
          alert("Server, data not available");
        }
      }

    xmlhttp.onload = GetResult;
    // xmlhttp.onerror = Bad_server;
    // send the request in an async way
    xmlhttp.open("POST", "/feedback.json", true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    var json_file = 'json_file=' + JSON.stringify(
      {'exp': window.fruit,
      'unique':window.unique
    });

    xmlhttp.send(json_file);
  }

  function submit_tempkey() {
    if (window.flag_tempkey == 0) {
        window.interval_tempkey = setInterval(start_tempkey, 3000);
        window.flag_tempkey = 1;

        window.cltempkey = new CanvasLoader('canvasloader-tempkey');
        cltempkey.setShape('spiral'); // default is 'oval'
        cltempkey.setDiameter(25); // default is 40
        cltempkey.setDensity(15); // default is 40
        cltempkey.setRange(0.5); // default is 1.3
        cltempkey.setSpeed(1); // default is 2
        cltempkey.setFPS(17); // default is 24
        cltempkey.show(); // Hidden by default

    } else {
      // alert(window.flag_save);
    }
  }

  function start_tempkey(){
    var xmlhttp;
    // Are we using a modern browser or ...
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    } else {
      // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!xmlhttp){
      alert("Error initializing XMLHttpRequest!");
    }

    function GetResult(){
      if (xmlhttp.readyState==4 && xmlhttp.status==200) {
        var jsonret = JSON.parse(xmlhttp.responseText);

        if (jsonret.prop == "stop"){
            clearInterval(window.interval_tempkey);
            // location.href = '/export?unique=' + window.unique;
            window.flag_tempkey = 0;
            window.cltempkey.hide();

            var dict_arr = jsonret.arr;

            document.getElementById('date_start').innerHTML = dict_arr.date_start;
            document.getElementById('date_end').innerHTML = dict_arr.date_end;
            document.getElementById('tarif_name').innerHTML = dict_arr.tarif;
            document.getElementById('tarif_status').innerHTML = dict_arr.status;

            document.getElementById('init_key').value = '';

          }
      } else {
          alert("Server, data not available");
        }
      }

    xmlhttp.onload = GetResult;
    // xmlhttp.onerror = Bad_server;
    // send the request in an async way
    xmlhttp.open("POST", "/promokey.json", true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    prkey = document.getElementById('init_key').value;
    var json_file = 'json_file=' + JSON.stringify(
      {'promokey': prkey,
      'unique':window.unique
    });

    xmlhttp.send(json_file);
  }

  function optnew(){
    var div = document.createElement('div');
    div.id = 'optimization';
    home.appendChild(div);

    var div_load = document.createElement('div');
    div_load.className = 'loader-fb';
    optimization.appendChild(div_load);
  }

  function Bad_server(){
      alert( 'Sorry server is not responding ' );
      var element=document.getElementById('optimization');
      if (element){
        home.removeChild(element);
      }
      clearInterval(window.intervalID);
      status_opt('Обновите страницу!');
      document.getElementById('start').disabled = true;
      window.dis = 0;

  }

  function optlost(){
    var element=document.getElementById('optimization');
    if (element){
      home.removeChild(element);
    }
  }

  function status_opt(txt){
    form = document.forms.optimus;
    var elems = form.elements.tender;
    elems.value = txt;
  }

  // возвращает cookie с именем name, если есть, если нет, то undefined
  function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }

  function eee(){
      var xmlhttp;
      // Are we using a modern browser or ...
      if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
      } else {
        // code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
      if (!xmlhttp){
        alert("Error initializing XMLHttpRequest!");
      }

      function GetItems(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
          var jsonobj = JSON.parse(xmlhttp.responseText);

          if (jsonobj[1] == "stop"){
              window.dis = 0;
              status_opt('Старт!');
              clearInterval(window.intervalID);
              // optlost();
              document.getElementById('start').disabled = false;
              window.cnvsopt.hide();
            }
          else if(jsonobj[1] == "wait"){
              window.dis = 1;
              status_opt('Ожидание');
            }
          else if (jsonobj[1] == "start"){
                window.dis = 1;
                var getoptm=document.getElementById('optimization');
                if (!getoptm){
                  // optnew();
                }
                status_opt('Расчет');
          }
          else if (jsonobj[1] == "result"){
              window.dis = 0;
              status_opt('Старт!');
              clearInterval(window.intervalID);
              // optlost();
              document.getElementById('start').disabled = false;
              location.href = '/result?unique=' + window.unique;
              window.cnvsopt.hide();
            } else {
              alert('аннулирована заявка ' + jsonobj[1]);
              Bad_server();
              window.cnvsopt.hide();
            }

        var widthprogress = parseInt(jsonobj[4]);
        // alert(widthprogress);

        if (widthprogress > 0){
          moveprogress(widthprogress);
        } else {
          moveprogress(0);
        }

        sms = jsonobj[3];
        var smsdoc = document.getElementById('message');
        smsdoc.innerHTML = sms;

        appu = jsonobj[2];
        var appdoc = document.getElementById('usapp');
        appdoc.innerHTML = appu;

        uscur = jsonobj[5];
        var usridx = document.getElementById('usidx');
        usridx.innerHTML = uscur;

        } else {
            alert("Server, data not available");
            Bad_server();
            window.cnvsopt.hide();
          }
        }

      xmlhttp.onload = GetItems;
      xmlhttp.onerror = Bad_server;
      // send the request in an async way
      xmlhttp.open("POST", "/getallitems.json", true);
      xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
      // cookie = getCookie('account');
      // xmlhttp.setRequestHeader('Cookie', cookie);

      // u = 0;
      // for(var index in window.fruit) {
      //     u += 1;
      // }
      // alert(u);

      var json_name = 'json_name=' + JSON.stringify(
        {'unique':window.unique,
         'subscribe': window.subscribe,
         'fruit': window.clone_fruit,
         'knox': window.knox,
         'limright': window.limright,
         'attempt': window.attempt,
         'correto': window.correto
       });

      xmlhttp.send(json_name);
      window.clone_fruit = {};
    }

 var loadDeferredStyles = function() {
   var addStylesNode = document.getElementById("deferred-styles");
   var replacement = document.createElement("div");
   replacement.innerHTML = addStylesNode.textContent;
   document.body.appendChild(replacement)
   addStylesNode.parentElement.removeChild(addStylesNode);
 };
 var raf = requestAnimationFrame || mozRequestAnimationFrame ||
     webkitRequestAnimationFrame || msRequestAnimationFrame;
 if (raf) raf(function() { window.setTimeout(loadDeferredStyles, 0); });
 else window.addEventListener('load', loadDeferredStyles);
