var uname= document.querySelector ("#username");
uname.addEventListener('blur' function(evt){
    var error_div= document.querySelector("#error_div")
    if(uname.value === ""){
    //full name is empty

    error_div.innerHTML ="<p>full name must not be empty.</p>"
    }
    else{
    error_div.innerHTML="";
    }
});