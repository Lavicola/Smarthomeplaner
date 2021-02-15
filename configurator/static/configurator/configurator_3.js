
    function getToken(){
        let = csrf_token = document.getElementById("csrf").value;
        return csrf_token;
    
    }
    
    
    function setCanvas() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: '/configurator/setCanvas',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
        data: "canvas_map=" + JSON.stringify( canvas.toJSON(['id','name',"isDevice","connector"]) )
      }).then(function (response){ 
                console.log("success");          
      }
              )  .catch(error => {                
                console.log(error.response.status);
                return false;
             })
          return true;                  
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
      }).then ( function (response){ //success function
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
        return false;
     }) 
    return true;
    }
    

    function saveRooms() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: '/configurator/saveRooms',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },

        data: "json_data=" + buildJSON(),
      }).then(function (response){ 
        console.log("success");          
}
      )  .catch(error => {                
        console.log(error.response.status);
        return false;
     })
    return true;
    }



    function SaveData() {
        if(setCanvas()){
          saveRooms();
        }       
    }

  