/**
 * Created by Dexp on 31.12.2016.
 */
$(function() {
$(window).scroll(function(){
    var scrollTop = $(window).scrollTop();
    if(scrollTop != 0) $('nav').stop().animate({'opacity':'0.5'},400);
    else $('nav').stop().animate({'opacity':'1'},400);
});

$('nav').hover(
function (e) {
    var scrollTop = $(window).scrollTop();
    if(scrollTop != 0) $('nav').stop().animate({'opacity':'1'},400);
},
function (e) {
    var scrollTop = $(window).scrollTop();
    if(scrollTop != 0)$('nav').stop().animate({'opacity':'0.5'},400);
}
);
});
