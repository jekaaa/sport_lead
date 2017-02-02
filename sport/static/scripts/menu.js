/**
 * Created by Dexp on 18.12.2016.
 */
$(document).ready(function(){
   $(".block").mouseover(function(){
      $(this).children(".name").css("background","black").css("width","100%");
   });
   $(".block").mouseout(function(){
      $(this).children(".name").css("background","rgba(20,20,20,0.7)").css("width","80%");
   });
    $("a").mouseover(function () {
        $(this).siblings("a").children(".block").css("opacity","0.3");

    });
    $("a").mouseout(function () {
        $(this).siblings("a").children(".block").css("opacity","1");

    });
    $("a").click(function(event){
        event.preventDefault();
        var link = this.href
        $(this).children(".block").children(".name").css("display","none")
        $(this).siblings("a").children(".block").animate({width:"0%"},1000)
        $(this).children(".block").animate({width:"100%"},1000,function () {
            document.location = link;
        });

	});



});