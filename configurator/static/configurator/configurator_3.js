

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
        setFeedbackText("Es ist ein Fehler aufgetreten, sind sie angemeldet?");
        return false;
     }) 
     setFeedbackText("Konfiguration wurde erfolgreich geladen");
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
        setFeedbackText("Fehler, bitte versuche es erneut bzw. melde dich an");
        return false;
     })
     setFeedbackText("Konfiguration wurde erfolgreich gespeichert");
    return true;
    }


function setFeedbackText(text=""){
  document.getElementById("feedback_text").innerHTML = text;
  setTimeout(function(){
    document.getElementById("feedback_text").innerHTML=""; }, 3000);

}

