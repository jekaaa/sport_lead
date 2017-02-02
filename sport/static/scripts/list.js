/**
 * Created by Dexp on 18.10.2016.
 */
$(document).ready(function() {
    $('select').material_select();
});

$("#name").change(function () {
    $('#name').removeClass('valid');
    $('#name').removeClass('invalid');
    var spaces = /\s+/g;
    var name = $('#name').val().replace(spaces,' ');
    if (name.length < 2) {
        $('#name').addClass('invalid');
    }
    else {
        $('#name').addClass('valid');
    }
});

$('#number').change(function () {
    $('#number').removeClass('valid');
    $('#number').removeClass('invalid');
    var temp = /^[0-9]{1,2}$/g;
    if (temp.test($('#number').val()) && ($('#number').val() < 65) ) {
        $('#number').addClass('valid');
    }
    else {
        $('#number').addClass('invalid');
    }
});

$('#weight').change(function () {
    $('#weight').removeClass('valid');
    $('#weight').removeClass('invalid');
    var temp = /^(\d+(\+)?(,)?)+$/g;
    if (temp.test($('#weight').val()) ) {
        $('#weight').addClass('valid');
    }
    else {
        $('#weight').addClass('invalid');
    }
});

$('#group').change(function () {
    $('#group').removeClass('valid');
    $('#group').removeClass('invalid');
    var temp = /^[0-9]{1,2}$/g;
    if (temp.test($('#group').val()) && ($('#group').val() < $('#number').val()/2 +1) && ($('#group').val() < 17)) {
        $('#group').addClass('valid');
    }
    else {
        $('#group').addClass('invalid');
    }
});

$('#number_table').change(function () {
    $('#number_table').removeClass('valid');
    $('#number_table').removeClass('invalid');
    var temp = /^\d+$/g;
    if (temp.test($('#number_table').val())) {
        $('#number_table').addClass('valid');
    }
    else {
        $('#number_table').addClass('invalid');
    }
});


$("[name='kind']").change(function () {
    var arm = 'Армспорт';
    var listRoundRobin = ['Баскетбол','Волейбол','Гандбол','Регби','Футбол','Хоккей','Настольный теннис','Другое'];
    var listPlayOff = ['Бадминтон','Теннис','Единоборства'];
    $("#group_block").css('display','none');
    $("#typePL").css('display','none');
    $("#type").css('display','none');
    
    if (($("[name='kind'] :selected").val() == arm)){
        $("#typePL").css('display','none');
        $("#type").css('display','none');
        $("#win").parent().css('display','none');
        $("#draw").parent().css('display','none');
        $("#lose").parent().css('display','none');
        $("#weight").parent().css('display','block');
        $("#number").parent().css('display','none');
        $("#number_table").parent().css('display','block');
    }
    else {
        if(listRoundRobin.indexOf($("[name='kind'] :selected").val()) != -1){
            $("#typePL").css('display','none');
            $("#type").css('display','block');
            $("#win").parent().css('display','block');
            $("#draw").parent().css('display','block');
            $("#lose").parent().css('display','block');
            $("#weight").parent().css('display','none');
            $("#number").parent().css('display','block');
            $("#number_table").parent().css('display','none');
        }
        else{
            if(listPlayOff.indexOf($("[name='kind'] :selected").val()) != -1){
                $("#type").css('display','none');
                $("#typePL").css('display','block');
                $("#win").parent().css('display','block');
                $("#draw").parent().css('display','block');
                $("#lose").parent().css('display','block');
                $("#weight").parent().css('display','none');
                $("#number").parent().css('display','block');
                $("#number_table").parent().css('display','none');
            }
            else{
                $("#typePL").css('display','none');
                $("#type").css('display','none');
                $("#win").parent().css('display','none');
                $("#draw").parent().css('display','none');
                $("#lose").parent().css('display','none');
                $("#weight").parent().css('display','block');
                $("#number").parent().css('display','none');
                $("#number_table").parent().css('display','block');
            }
        }
    }
});

$("[name='type']").change(function () {
    $("#group_block").css('display','none');
    if($("[name='type'] :selected").index() == 1 || $("[name='type'] :selected").index() == 2){
        $("#group_block").css('display','block');
    }
});



/*var listTournament = ["Круговой турнир","Групповой турнир с плей-офф","Групповой турнир с плей-офф (случайное распределение)",
                      "Плей-офф","Плей-офф (случайное распределение)"];

var list2 = document.createElement("select");
list2.name = "type";

var i = 0;
while(i<listTournament.length){
    list2.options[i] = new Option(listTournament[i]) ;i++;
}

var form = document.getElementsByTagName('form')[0];

var list3 = document.createElement("select");
list3.name = "typePL";
list3.options[0] = new Option(listTournament[3]);
list3.options[1] = new Option(listTournament[4]);

var kind = document.getElementsByName("kind")[0];

var input = document.createElement("input");
    input.placeholder = "Введите количество групп";
    input.name = "group";
    input.type = "text";

function check(name) {
    var ch = document.getElementsByName(name)[0];
    if(ch) return true;
    else return false;
}


function L(){

    var list = document.getElementsByTagName("select")[0];
    var listRoundRobin = ['Баскетбол','Волейбол','Гандбол','Регби','Футбол','Хоккей','Настольный теннис','Другое'];
    var listPlayOff = ['Бадминтон','Теннис','Единоборства'];
    var error = document.getElementsByClassName("error")[0];
    var i = 0;
    if (error) form.removeChild(error);
    while(i < list.length){
        if(list.options[i].selected){
            if(listRoundRobin.indexOf(list.options[i].value) != -1){
                if(check("typePL")){
                    form.removeChild(list3);
                }
                if(!check("type")) {
                    form.appendChild(list2);break;
                }
                break;
            }

            if(listPlayOff.indexOf(list.options[i].value) != -1){
                if(check("type")){
                    form.removeChild(list2);
                }
                if(!check("typePL")){
                    form.appendChild(list3);break;
                }
                break;
            }

            if(check("type")){
                form.removeChild(list2);
                if(check("group")){
                    form.removeChild(input);
                }
                break;
            }

            if(check("typePL")){
                form.removeChild(list3);
                console.log("AAAA");
                if(check("group")){
                    form.removeChild(input);
                }
                break;
            }
            break;

        }
        i++;
    }
}

function I() {

    if(list2.options[1].selected || list2.options[2].selected){
        var error = document.getElementsByClassName("error")[0];
        if(!check("group")) form.appendChild(input);
        if (error) form.removeChild(error);
    }
    else {
        var error = document.getElementsByClassName("error")[0];
        if(check("group")) form.removeChild(input);
        if(error) form.removeChild(error);
    }
}



list2.onchange = I;
kind.onchange = L;*/