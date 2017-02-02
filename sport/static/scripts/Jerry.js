/**
 * Created by Dexp on 07.10.2016.
 */
$(document).ready(function() {
    $('select').material_select();
  });

function create_inputs() {
    var form = document.getElementsByClassName("row")[1];
    for (var i = 0; i < $('#number').val(); i++) {
        var div = document.createElement("div");
        div.className = 'input-field col offset-l1 offset-m1 l10 m10 s12';
        form.appendChild(div);
        var inp = document.createElement("input");
        inp.type = "text";
        inp.name = "input" + i;
        inp.placeholder = (i + 1) + ".Имя игрока или команды";
        inp.className = 'validate';
        div.appendChild(inp);
    }
};

function invalid(obj) {
    obj.removeClass('valid');
    obj.addClass('invalid');
}

function valid(obj) {
    obj.removeClass('invalid');
    obj.addClass('valid');
}

function check_pl() {
    if(!pl_input($('#number').val())){
        invalid($('#number'));
    }
    else{
    if($('#number').hasClass('invalid')){
        valid($('#number'));
    }
    }
}

function pl_input(number) {
    var list = ['4','8','16','32','64'];
    if(list.indexOf(number) != -1) return true;
    else return false;
}



$("form").submit(function () {

    if($('#type').is(':visible')) {
        if($("[name='type'] :selected").index() == 3 || $("[name='type'] :selected").index() == 4) check_pl();
    }

    if($('#typePL').is(':visible')) check_pl();

    var len = $('.invalid:visible').length

    if( len > 0) {
        $('.invalid').animate({opacity: 0}, 1000 );
	    $('.invalid').animate({opacity: 1}, 500 );
        return false;
    }
    else{
        var invisible_list = $('form div:hidden');
        for (var i=0;i<invisible_list.length;i++){
            $(invisible_list[i]).remove();
        }
        return true;
        /*$('.input-field:last').remove();
        $('.input-field').css('display','none');
        create_inputs();
        $('.row:last').append('<div class="input-field col offset-l5 l4 offset-m4 m4 offset-s3 s6">' +
            '<button class="btn waves-effect waves-light green" type="submit" name="submitted">готово ' +
            '<i class="material-icons right">send</i>' +
            '</button>');*/
    }
});




/*
//первая кнопка
var button = document.getElementsByName("b")[0];
button.onclick = N;
//центральный блок
var center = document.getElementsByClassName("center")[0]
//форма
var form = document.getElementsByClassName("interview")[0];
//вес
var weigth = document.getElementsByName("weigth")[0];
//количество участников
var number = document.getElementsByName("number")[0];

var date = document.getElementsByName("date")[0];

var description = document.getElementsByName("description")[0];
//вид спорта
var kind = document.getElementsByName("kind")[0];
//

var nameTournament = document.getElementsByName("nameTournament")[0];

var city = document.getElementsByName("city")[0];

//Проверка на корректный ввод параметров
function CorrectInput(groupNumber){

    if (kind.value == "Выберите вид спорта"){
        return 5;
    }
    if(nameTournament.value == ""){
        return 4;
    }

    if (1 < number.value && number.value < 65 ){
        if(groupNumber){

            if(groupNumber.value < number.value /2 && groupNumber.value > 1 ){
                return 1;

            }
            else{
                return 3;

            }
        }
        return 1;
    }

    return 2;

}

function PLInput(number) {
    var list = [4,8,16,32,64]
    if(list.indexOf(number) != -1) return true;
    else return false;
}

function errors(groupNumber) {

    var e = document.getElementsByClassName("error")[0];
    if(e){form.removeChild(e);}
    var error = document.createElement("div")
    if(CorrectInput(groupNumber) == 2){
        error.innerHTML = "Ошибка при вводе (ограничение по количеству людей - 64, по группам - 16)";
    }
    if(CorrectInput(groupNumber) == 3){
        error.innerHTML = "Ошибка количества групп (в группе должно быть минимум 2 человека)";
    }
    if(CorrectInput(groupNumber) == 4){
        error.innerHTML = "Ошибка при вводе (введите название мероприятия)";
    }
    if(CorrectInput(groupNumber) == 5){
        error.innerHTML = "Ошибка при выборе вида спорта ";
    }
    error.className = "error";

    form.appendChild(error);
    
}

function conceal(groupNumber,tournament,tournament2) {
    number.style.display = "none";
    date.style.display = "none";
    description.style.display = "none";
    form.removeChild(button);
    if(groupNumber) {
        groupNumber.style.display = "none";
    }
    if (tournament2){
        tournament2.style.display = "none";
    }
    nameTournament.style.display = "none";
    city.style.display = "none";

    if(tournament){
        tournament.style.display = "none";
    }
    kind.style.display = "none";
    var error = document.getElementsByClassName("error")[0];

    if(error) {
        form.removeChild(error);
    }
}

function createSubmit() {
    var go = document.createElement("button");
    go.name = "submitted";
    go.innerHTML = "go";
    go.type = "submit";
    go.id = "s";
    form.appendChild(go);
}


//Первая кнопка
function N (){
    //вид турнира
    var tournament = document.getElementsByName("type")[0];
    //количество групп
    var groupNumber = document.getElementsByName("group")[0];
    var tournament2 = document.getElementsByName("typePL")[0];

    if(tournament && tournament.options[1].selected) {

        if(CorrectInput(groupNumber) == 1){
            conceal(groupNumber,tournament,tournament2);
            var k = 0;
            var gN = groupNumber.value;
            var n = number.value;
            var nameGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"];

            while(gN > 0){
                var nameG = document.createElement("div");
                nameG.innerHTML = " Группа " + nameGroup[groupNumber.value - gN];
                form.appendChild(nameG);
                var numberInGroup = n/gN;
                var j = 1;
                while(numberInGroup > 0) {
                    var inp = document.createElement("input");
                    inp.type = "text";
                    inp.name = "input" + k;
                    inp.placeholder = j + ".Имя игрока или команды";
                    form.appendChild(inp);
                    numberInGroup--;
                    n--;
                    k++;
                    j++;
                }
                gN--;
            }

            createSubmit();

        }
        else{
            errors(groupNumber);
        }
    }
    else {
        if (tournament && tournament.options[4].selected || tournament2 && tournament2.options[1].selected) {
            if (CorrectInput(groupNumber) == 1) {
                console.log(number.value);
                if (PLInput(+number.value)) {

                    conceal(groupNumber, tournament, tournament2);
                    for (var i = 0; i < number.value; i++) {
                        var inp = document.createElement("input");
                        inp.type = "text";
                        inp.name = "input" + i;
                        inp.placeholder = (i + 1) + ".Имя игрока или команды";
                        form.appendChild(inp);
                    }
                    createSubmit();
                }
                else {

                    var e = document.getElementsByClassName("error")[0];
                    if (e) form.removeChild(e);
                    var error = document.createElement("div");
                    error.innerHTML = "Ошибка при вводе (в плей-офф участвуют только 4/8/16/32/64 человека)";
                    error.className = "error";
                    form.appendChild(error);
                }

            }
            else {
                errors(groupNumber);
            }
        }
        else {
            if (tournament && tournament.options[3].selected || tournament2 && tournament2.options[0].selected) {
                if (CorrectInput(groupNumber) == 1) {
                    if (PLInput(+number.value)) {
                        conceal(groupNumber, tournament, tournament2);
                        var k = 1
                        for (var i = 0; i < number.value; i++) {
                            if (i % 2 == 0) {
                                var name = document.createElement("div");
                                name.innerHTML = " Пара " + k;
                                form.appendChild(name);
                                k++;

                            }
                            var inp = document.createElement("input");
                            inp.type = "text";
                            inp.name = "input" + i;
                            inp.placeholder = (i % 2 + 1) + ".Имя игрока или команды";
                            form.appendChild(inp);
                        }
                        createSubmit();
                    }
                    else {

                        var e = document.getElementsByClassName("error")[0];
                        if (e) form.removeChild(e);
                        var error = document.createElement("div");
                        error.innerHTML = "Ошибка при вводе (в плей-офф участвуют только 4/8/16/32/64 человека)";
                        error.className = "error";
                        form.appendChild(error);
                    }

                }
                else {
                    errors(groupNumber);
                }
            }
            else {
                console.log(number.value);
                if (CorrectInput(groupNumber) == 1) {
                    conceal(groupNumber, tournament, tournament2);

                    for (var i = 0; i < number.value; i++) {
                        var inp = document.createElement("input");
                        inp.type = "text";
                        inp.name = "input" + i;
                        inp.placeholder = (i + 1) + ".Имя игрока или команды";
                        form.appendChild(inp);
                    }
                    createSubmit();

                }
                else {
                    errors(groupNumber);
                }
            }
        }
    }
}


/*
//Вторая кнопка submit
function M(){
    //var table = document.getElementsByClassName("t")[0];
    var names = document.getElementsByTagName("input");
    //table.style.display = "block";
    list = [];
    for(var i = 0; i<names.length;i++){
        Add(list,names[i].value);
    }
    //center.removeChild(form);

    if(tournament.options[0]){
        Groups(Toss(list,1));
    }
    if(tournament.options[1]){
        Play_off(list);
    }

    //form.removeChild(names);
    Groups(Toss(list,groupNumber.value));
}


//Рандом от 0 до введенного числа
function Rnd(number) {
    return Math.floor(Math.random() * (number));
}

//Добавление объекта в начало списка
function Add(list,object) {
    list.splice(0,0,object);
}

//Проверка на праильное количество групп
function CorrectGroup(len,group){
    if(group < 0 || group > len/2){return false}
    else return true;
}

//Жеребьевка по группам, иначе по парам
function Toss(list,group) {
    var newList = [];
    var len = list.length;

    if(!CorrectGroup(len,group)) {
        while (len > 0) {
            var pare = [];

            var one = Rnd(len);
            Add(pare,list[one]);//pare.splice(0, 0, list[one]);
            list.splice(one, 1);
            len--;

            if (len > 0) {
                var two = Rnd(len);
                Add(pare,list[two]);//pare.splice(1, 0, list[two]);
                list.splice(two, 1);
                len--;
            }

            Add(newList,pare);//newList.splice(0, 0, pare);
        }
        return newList;
    }

    while(group>0) {
        var groupList = [];
        var numberInGroup = len/group;
        while (numberInGroup > 0) {
            var r = Rnd(len);
            Add(groupList,list[r]);//groupList.splice(0, 0, list[r]);
            list.splice(r, 1);
            numberInGroup--;
            len--;
        }
        Add(newList,groupList);//newList.splice(0, 0, groupList);
        group--;
    }

    return newList;

}

//Группа на вход список списков групп
function Groups(list) {
    var c = document.getElementsByClassName("center")[0];
    var div = document.createElement("div");
    div.className = "post";
    for(var i=0;i<list.length;i++){
        var ol = document.createElement("ol");
        ol.className = "group";
        for(var j=0;j<list[i].length;j++){
            var li = document.createElement("li");
            li.innerHTML = list[i][j];
            ol.appendChild(li);
        }
        div.appendChild(ol);
    }
    c.appendChild(div);


}

function Play_off(list){
    var post = document.getElementsByClassName("post")[0];
    var numberGamers = list.length;
    var numberTour = Math.ceil( Math.log2(numberGamers));
    for(var i=0;i<numberTour;i++){
        var tour = document.createElement("div");
        //var width = post.style.width;
        tour.style.width = 100/numberTour + "%";
        tour.style.float = "left";
        tour.style.marginTop = "20px";
        form.appendChild(tour);
        for(var j=numberGamers/2;j>0;j--){
            var block = document.createElement("div");
            block.style.width = "90%";
            block.style.margin = "5%";
            block.style.height = "40px";

            block.style.backgroundColor = "black";
            tour.appendChild(block);

        }
        numberGamers/=2;
    }

}

//Play_off([1,1,1,1,1,1])*/