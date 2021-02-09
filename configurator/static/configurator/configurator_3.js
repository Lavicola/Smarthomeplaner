
    function getToken(){
        let = csrf_token = document.getElementById("csrf").value;
        return csrf_token;
    
    }
    
    
    function setCanvas() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/configurator/setCanvas',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
        data: "canvas_map=" + JSON.stringify( canvas.toJSON(['id','name',"isDevice","connector"]) )
      }).then ( function (response){ 
                  console.log(response);
                  return true;                  
                }
              )  .catch(error => {                
                console.log(error.response.status);
                return false;
             })
    }
    
    
    
    function getCanvas() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/configurator/getCanvas',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
      }).then ( function (response){ //success function
        canvas.clear();
        canvas.loadFromJSON(response.data);
        canvas.renderAll(); 
        return true;
        }
      )  .catch(error => {                
        console.log(error.response.status);
        return false;
     }) }
    

    function saveRooms() {
        let csrf_token = getToken();
        axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/configurator/saveRooms',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json',
            'X-CSRFToken': csrf_token
          },
        data: buildJSON()
      }).then ( function (response){ //success function
        console.log(response);
      }
      
      )}



    function SaveData() {
        if(setCanvas()){
          saveRooms();
        }       
    }