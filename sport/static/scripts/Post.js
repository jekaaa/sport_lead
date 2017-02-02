/**
 * Created by Dexp on 18.10.2016.
 */
function Post(name,table) {
    this.name = name;
    this.table = table;
    
    var center = document.getElementsByClassName("center")[0];
    var div = document.createElement("div");
    //var p = document.createElement("p");
    //p.innerHTML = this.name;
    div.innerHTML = this.name;
    div.className = "post";
    //div.appendChild(p);
    center.appendChild(div);
    var button = document.createElement("button");
    button.className = "close";
    div.appendChild(button);
    button.onclick = F;

    function F() {
        center.removeChild(div);
    }

}

new Post("Football Ekaterinburg Uralmash",0);new Post(0,1);
