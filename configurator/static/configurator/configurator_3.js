

    function getToken(){
        let = csrf_token = document.getElementById("csrf").value;
        return csrf_token;
    
    }
    
    function getCanvas() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: '/configurator/getCanvas',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
      }).then ( function (response){ 
        canvas.clear();
        canvas.loadFromJSON(response.data, function() {
        canvas.renderAll(); 
     },function(o,object){
        if(object.isDevice){
          add_event_to_device(object);
        }
     })
        }).catch(error => {                
        console.log(error.response.status);
        setLoadText(false);
        return false;
     }) 
    setLoadText(true);
    return true;
    }
    

    function saveConfiguration() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: '/configurator/saveConfiguration',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
        data: { json_data: buildJSON(), canvas_map: JSON.stringify( canvas.toJSON(['id','name',"isDevice","connector"]) ) },
      }).then(function (response){ 
        console.log("success");          
}
      )  .catch(error => {                
        console.log(error.response.status);
        setSaveText(false)
        return false;
     })
     setSaveText(true)
    return true;
    }


function setSaveText(isTrue){
  if(isTrue){
      document.getElementById("save_text").innerHTML = "Konfiguration wurde erfolgreich gespeichert";
  }else{
      document.getElementById("save_text").innerHTML = "Fehler, bitte versuche es erneut bzw. melde dich an";
  }

  setTimeout(function(){
    document.getElementById("save_text").innerHTML=""; }, 3000);

}


function setLoadText(isTrue){
  if(isTrue){
      document.getElementById("load_text").innerHTML = "Konfiguration wurde erfolgreich geladen ";
  }else{
      document.getElementById("load_text").innerHTML = "Es ist ein Fehler aufgetreten, sind sie angemeldet?";
  }

  setTimeout(function(){
    document.getElementById("load_text").innerHTML=""; }, 3000);

}