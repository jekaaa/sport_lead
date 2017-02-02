/**
 * Created by Dexp on 08.12.2016.
 */
var redactor = document.getElementsByName("redactor")[0];
if (redactor) redactor.onclick = Save;

function Save() {
    var del = document.getElementsByName("delete")[0];
    var form = document.getElementsByTagName("form")[0];
    form.removeChild(del);
    form.removeChild(redactor);

    var div = document.createElement("div");
    div.innerHTML = "Новый результат";
    form.appendChild(div);

    var div2 = document.createElement("div");
    form.appendChild(div2);
    
    var input = document.createElement("input");
    input.name = "player";
    input.placeholder = "Введите имя участника";
    input.type = "text";
    input.className = "player2";
    div2.appendChild(input);

    var time = document.createElement("input");
    time.name = "time";
    time.type = "text";
    time.placeholder = "Введите время участника";
    time.className = "player2";
    div2.appendChild(time);
    
    var btn = document.createElement("input");
    btn.name = "save";
    btn.value = "Создать";
    btn.type = "submit";
    btn.className = "sub2";
    form.appendChild(btn);
    
}
