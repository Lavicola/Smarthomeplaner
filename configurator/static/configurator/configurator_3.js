

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
        restoreCanvas(response.data);
     setFeedbackText("Konfiguration wurde erfolgreich geladen");
    }).catch(error => {                
        console.log(error.response.status);
        setFeedbackText("Es ist ein Fehler aufgetreten, sind sie angemeldet?");
        return false;
     })      
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
        setFeedbackText("Konfiguration wurde erfolgreich gespeichert");
      }
      )  .catch(error => {                
        setFeedbackText("Fehler, bitte versuche es erneut bzw. melde dich an");
        return false;
     })
    return true;
    }


function setFeedbackText(text=""){
  document.getElementById("feedback_text").innerHTML = text;
  setTimeout(function(){
    document.getElementById("feedback_text").innerHTML=""; }, 3000);

}

