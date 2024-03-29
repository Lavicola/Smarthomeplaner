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


window.addEventListener("load", function(){
new Vue({
    el: '#vue_app',
    delimiters: ['{[',']}'],
    data: {
      search_term: "",
      seen: Boolean,
      devices: [],
      selected_category: 'all',
      vulnerabilities: [],
      data_protection:[],
      base_url : "/smarthome/devices/",
    },
    mounted: function() {
      this.getdevices();
      this.seen=false;
    },
    methods: {
      getdevices:function() {
        let api_base_url = '/api/devices/';
        axios.get(api_base_url)
            .then((response) => {
              this.devices = response.data;
            })
      },
      getSearchResults: function() {      
        let api_base_url = '/api/devices/';
        let api_url = "";
        if(this.selected_category != "all"){
          api_url = api_base_url+"?name="+this.search_term+"&category="+this.selected_category;
        }else{
          api_url = api_base_url+"?name="+this.search_term;
        }
        
        axios.get(api_url)
            .then((response) => {
              this.devices = response.data;
            })
      },
      getVulnerabilities: function(device_id) {
        let api_base_url = '/api/vulnerability/';
        let api_url = api_base_url+"?device_id="+device_id
        axios.get(api_url)
            .then((response) => {
              this.vulnerabilities = response.data;
            })
      },
      getDataProtectionInformation: function(device_id) {
        let api_base_url = '/api/data-protection/';
        let api_url = api_base_url+"?device_id="+device_id
        axios.get(api_url)
            .then((response) => {
              this.data_protection = response.data;
            })
      },
      getAdditionalInformation: function(event) {
        device_id=event.target.id;
        this.getVulnerabilities(device_id);
        this.getDataProtectionInformation(device_id);      
        if(!this.seen){
          this.seen=true;
        }        
      },
    }
  });

});