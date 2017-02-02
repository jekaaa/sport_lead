/**
 * Created by Dexp on 02.11.2016.
 */
var a = document.getElementsByClassName("ava")[0];
var block = document.getElementsByClassName("red")[0];
var izm = document.getElementsByTagName("button")[0];
var del = document.getElementsByTagName("button")[1];

//a.width = 100;
//a.height = 100;
//a.style.backgroundImage = "url('../static/qqq.jpg')";
function F() {

    document.getElementsByClassName("red")[0].style.display = "block";
}

function F2() {
    document.getElementsByClassName("red")[0].style.display = "none";

}
a.onmouseover = F;
a.onmouseout = F2;

