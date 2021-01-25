function include(file) {   
    var script  = document.createElement('script'); 
    script.src  = file; 
    script.type = 'text/javascript'; 
    script.defer = true;     
    document.getElementsByTagName('head').item(0).appendChild(script); 
  } 

  include("https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js");
  include("https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js");
  include("https://unpkg.com/v-tooltip@2.0.2");

    new Vue({
      
        el: '#live_search',
        delimiters: ['[',']'],
        data: {
          search_term: "Search for device",
          message: "dsdsas",
          devices: [],
          selected_category: 'None',
          currentdevice: {},
          csrf_token: "",
        },
        mounted: function() {
          this.getdevices();
        },
        methods: {
          getToken:function(){
            this.csrf_token = document.getElementById("csrf").value;
          },
          getdevices: function() {
            let api_base_url = '/configurator/api/device/';
            axios.get(api_base_url)
                .then((response) => {
                  this.devices = response.data;
                })
          },
          greet: function(device) {
            this.message = device + "<br>" + device;
          },
          getSearchResults: function() {          
            let api_base_url = '/configurator/api/device/';
            let api_url = "";
            alert(this.selected_category);
            if(this.selected_category != "None"){
              api_url = api_base_url+"?name="+this.search_term+"&category="+this.selected_category;
            }else{
              api_url = api_base_url+"?name="+this.search_term;
            }
            
            axios.get(api_url)
                .then((response) => {
                  this.devices = response.data;
                })
          },
          getPrivacyIssues: function() {
            let api_base_url = '/configurator/api/device/';
            let api_url = api_base_url+"?name="+this.search_term
            axios.get(api_url)
                .then((response) => {
                  this.devices = response.data;
                })
          },
          setCanvas: function() {
            this.getToken();
            axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/configurator/setCanvas',
            headers:{
              "Content-Type": "application/x-www-form-urlencoded",
                'Accept': 'application/json',
                'X-CSRFToken': this.csrf_token
              },
            data: "canvas_map=" + JSON.stringify( canvas.toJSON(['id','name',"isDevice"]) )
          }).then ( function (response){ //success function
            console.log(response);
          }
          
          )},
          getCanvas: function() {
            this.getToken();
            axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/configurator/getCanvas',
            headers:{
              "Content-Type": "application/x-www-form-urlencoded",
                'Accept': 'application/json',
                'X-CSRFToken': this.csrf_token
              },
          }).then ( function (response){ //success function
            canvas.clear();
            canvas.loadFromJSON(response.data);
            canvas.renderAll(); 
            }
          
          )},
        }
      });

      