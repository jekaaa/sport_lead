var redactor = document.getElementsByName("redactor")[0];
if (redactor) redactor.onclick = Save;

function Save() {
    var del = document.getElementsByName("delete")[0];
    var form = document.getElementsByTagName("form")[0];
    form.removeChild(del);
    form.removeChild(redactor);

    var div = document.createElement("div");
    div.innerHTML = "Новый матч";
    form.appendChild(div);

    var div2 = document.createElement("div");
    form.appendChild(div2);

    var input1 = document.createElement("input");
    input1.name = "player1";
    input1.placeholder = "Введите название первой команды";
    input1.type = "text";
    input1.className = "player";
    div2.appendChild(input1);

    var score1 = document.createElement("input");
    score1.name = "score1";
    score1.type = "text";
    score1.className = "number";
    div2.appendChild(score1);

    var score2 = document.createElement("input");
    score2.name = "score2";
    score2.type = "text";
    score2.className = "number";
    div2.appendChild(score2);

    var input2 = document.createElement("input");
    input2.name = "player2";
    input2.placeholder = "Введите название второй команды";
    input2.type = "text";
    input2.className = "player";
    div2.appendChild(input2);

    var div3 = document.createElement("div");
    form.appendChild(div3);

    var date = document.createElement("input");
    date.name = "date";
    date.type = "date";
    div3.appendChild(date);

    var btn =document.createElement("input");
    btn.name = "save";
    btn.value = "Создать";
    btn.type = "submit";
    btn.className = "sub2";
    form.appendChild(btn);

}