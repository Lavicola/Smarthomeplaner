function include(file) {   
    var script  = document.createElement('script'); 
    script.src  = file; 
    script.type = 'text/javascript'; 
    script.defer = true;     
    document.getElementsByTagName('head').item(0).appendChild(script); 
  } 
    
include("https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js");
include("https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js");



window.addEventListener("load", function(){
new Vue({
    el: '#additional_informations',
    delimiters: ['[',']'],
    data: {
      vulnerabilites: ["test","dsasa"],
      privacy_informations:["privaacy","dssa"],
    },
    mounted: function() {
      this.getdevices();
    },
    methods: {
      getVulnerabilities: function() {
        let api_base_url = '/api/vulnerability/';
        let api_url = api_base_url+"?device_id="+this.search_term
        axios.get(api_url)
            .then((response) => {
              this.vulnerabilites = response.data;
            })
      },
      getPrivacyIssues: function() {
        let api_base_url = '/configurator/api/device/';
        let api_url = api_base_url+"?name="+this.search_term
        axios.get(api_url)
            .then((response) => {
              this.privacy_informations = response.data;
            })
      },
      getAdditionalInformations: function() {
      this.getVulnerabilities();
      this.getPrivacyIssues();
      },
    }
  });

});