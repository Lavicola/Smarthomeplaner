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
    el: '#live_search',
    delimiters: ['{[',']}'],
    data: {
      search_term: "",
      seen: Boolean,
      devices: [],
      selected_category: 'None',
      vulnerabilities: [],
      privacy_issues:[],
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
      getVulnerabilities: function(device_id) {
        let api_base_url = '/api/vulnerability/';
        let api_url = api_base_url+"?device_id="+device_id
        axios.get(api_url)
            .then((response) => {
              this.vulnerabilities = response.data;
            })
      },
      getPrivacyIssues: function(device_id) {

        let api_base_url = '/api/privacy/';
        let api_url = api_base_url+"?device_id="+device_id
        axios.get(api_url)
            .then((response) => {
              this.privacy_issues = response.data;
            })
      },
      getAdditionalInformations: function(event) {
        device_id=event.target.id;
        this.getPrivacyIssues(device_id);      
        this.getVulnerabilities(device_id);
        if(!this.seen){
          this.seen=true;
        }
        


      },
    }
  });

});