
var canvas;
const default_Roomconfig = {
    left: 0,
    top: 0,
    width: 200,
    height: 100,
    fill: 'rgba(255, 255, 255, 0.2)',
    stroke: '#686868',
    strokeWidth: 2,
    originX: 'left',
    originY: 'top',
    centeredRotation: true,
    snapAngle: 45,
    selectable: true,
};


// array of rects! https://stackoverflow.com/questions/17255867/adding-grid-over-fabric-js-canvas  
//taken from matiss.andersons
function drawGrid(canvas) {

    const gridSize = 40;
    const width = canvas.getWidth() + 1000;
    const height = canvas.getHeight() + 500;
    const left = (width % gridSize) / 2;
    const top = (height % gridSize) / 2;
    const lines = [];
    const lineOption = {
        stroke: 'rgba(0,0,0,1)',
        strokeWidth: 1,
        selectable: false
    };
    for (let i = Math.ceil(width / gridSize); i--;) {
        lines.push(new fabric.Line([gridSize * i, -top, gridSize * i, height], lineOption));
    }
    for (let i = Math.ceil(height / gridSize); i--;) {
        lines.push(new fabric.Line([-left, gridSize * i, width, gridSize * i], lineOption));
    }
    const oGridGroup = new fabric.Group(lines, {
        left: 0,
        top: 0
    });
    oGridGroup.selectable = false;
    canvas.add(oGridGroup);
}

function canvas_event_handlers(canvas) {

    //enables zoom and panning
    canvas.on('mouse:wheel', function(opt) {
        var delta = opt.e.deltaY;
        var zoom = canvas.getZoom();
        zoom *= 0.999 ** delta;
        if (zoom > 20) zoom = 20;
        if (zoom < 0.01) zoom = 0.01;
        canvas.zoomToPoint({
            x: opt.e.offsetX,
            y: opt.e.offsetY
        }, zoom);
        opt.e.preventDefault();
        opt.e.stopPropagation();
    });

    canvas.on('mouse:down', function(opt) {
        var evt = opt.e;
        if (evt.altKey === true) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
    });

    // enables dragging the canvas: alt + mouse down and move
    canvas.on('mouse:move', function(opt) {
        if (this.isDragging) {
            var e = opt.e;
            var vpt = this.viewportTransform;
            vpt[4] += e.clientX - this.lastPosX;
            vpt[5] += e.clientY - this.lastPosY;
            this.requestRenderAll();
            this.lastPosX = e.clientX;
            this.lastPosY = e.clientY;
        }
    });
    canvas.on('mouse:up', function(opt) {
        // on mouse up we want to recalculate new interaction
        // for all objects, so we call setViewportTransform
        this.setViewportTransform(this.viewportTransform);
        this.isDragging = false;
        this.selection = true;
    });




}

function generateId() {
    return Math.random().toString(36).substr(2, 8)
}

function add_Room() {
    let name = GenerateRoomname();
    let paras = default_Roomconfig;
    paras.name = name;
    paras.id = generateId();
    paras.isDevice = false;
    const room = new fabric.Rect(paras);
                    
    var textObject = new fabric.IText(name, {
        left: 40,
        top: 40,    
        fontSize: 18,
        fill: '#000000'                        
     }); 
                    
    var group = new fabric.Group([ room, textObject ], {
        left: 150,
        top: 150                          
     });

    canvas.add(group);    
    return true;
}

function GenerateRoomname(){
    let number = 2;
    let temp_name = getRoomCategory();
    let name = temp_name;
    while(RoomExists(name)){
        name = temp_name + number;
        number++;
    }

    return name;
}

function RoomExists(a_room_name){

    let l_rooms = GetRoomNames();

    let j = l_rooms.length;
    for (var i = 0; i < j; i++) {

        if(l_rooms[i] == a_room_name){
            return true;
        }

    }
    return false;

}


function getRoomCategory(){
    category = document.getElementById("room_name").value;
    return category;
 
 }
 

function buildJSON(){
    let l_hash_map = CreateHashMap(); // [room_name]
    let l_rooms = GetRectTextGroups(canvas.getObjects());
    let l_room_names = GetRoomNames();    
    let l_devices = GetDevices();
    
    //check for every device in which room it is
    for(var i=0;i<l_devices.length;i++){
        //iterate through all rooms
        for(var j=0;j<l_rooms.length;j++){
            if(l_devices[i].isContainedWithinObject(l_rooms[j])){
                device_tuple = {device_id: l_devices[i].name, connector: l_devices[i].connector }
                l_hash_map[l_room_names[j]].push(device_tuple);
            }
        }
    }
    
    try
    {
        return JSON.stringify(l_hash_map);
    } catch(error){
        console.error();
        return {}
    }
    
}


function CreateHashMap(){

    let l_hash_map = new Object();
    let l_rooms = GetRoomNames();

    for(var i=0;i<l_rooms.length;i++){
        l_hash_map[l_rooms[i]] = [];
    }
    return l_hash_map;

}

// This function returns a room object or None if the inserted group is not a (rect,text). The Group also must have an isDevice type
function GetRectOfRectTextGroup(group){

    single_object = group._objects[0];
    // check if isDevice type exists if not return a placeholder string
    if( single_object.isDevice === undefined){
        //console.log("object has no isDevice type");
        return "None";
        //if it is not a device it must be a room
    }else if (!single_object.isDevice){
        return single_object;
    }
    
    return "None";       
}


// This function returns every rectText group which are rooms
function GetRectTextGroups(groups){
    rectTextGroups = [];
    for(var i=0;i<groups.length;i++){
        single_objects = groups[i]._objects;
        
        if( single_objects[0].isDevice === undefined){            
            //if it is not a device it must be a room
        }else if (!single_objects[0].isDevice){
            rectTextGroups.push(groups[i]);
        }

    }
    return rectTextGroups;
}


//This function returns an array of Room names
function GetRoomNames(groups){
    let canvas_objects = canvas.getObjects();
    let room_names = [];
    let room ;

    for(var i=0;i<canvas_objects.length;i++){
        room = GetRectOfRectTextGroup(canvas_objects[i]);

        if(room != "None"){
            room_names.push(room.name);
        }
    }
    return room_names;

}

function GetDevices(){
    let canvas_obects = canvas.getObjects();
    let l_devices = [];

    for(var i=0;i<canvas_obects.length;i++){
        if(canvas_obects[i].isDevice){
            l_devices.push(canvas_obects[i]);
        }
    }

    return l_devices

    
}


function dragstart_handler(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault(); // Necessary.  https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/Drag_operations   
    }
    e.dataTransfer.dropEffect = 'copy';
    return false;
}

function handleDragEnter(e) {
    if (e.preventDefault) {
        e.preventDefault(); // Necessary.  https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/Drag_operations   
    }
    // this / e.target is the current hover target.
    this.classList.add('over');
}

function handleDragLeave(e) {
    this.classList.remove('over'); // this / e.target is previous target element.
}

function drop_handler(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("URL");
    let svg_name = ev.dataTransfer.getData("text");
    fabric.loadSVGFromURL(data, function(objects, options) {
        var svg = fabric.util.groupSVGElements(objects, options);
        svg.left = ev.layerX;
        svg.top = ev.layerY;
        svg.name = svg_name;
        svg.id = svg_name+ "_" + generateId(); // todo:make it unique!
        svg.isDevice = true;
        svg.connector = getConnector(svg_name);
        add_event_to_device(svg);

        canvas.add(svg);
    });


}

function remove_object() {
    canvas.remove(canvas.getActiveObject());
}

function getConnector(device_id){
    var dropdown_string = "dropdown-"
    let con = document.getElementById(dropdown_string+device_id);
    var connector = con.value;
    return connector
}

function add_event_to_device(a_element) {
    a_element.on('mouseover', function() {
    let device_name =document.getElementById(a_element.name);  
    document.getElementById("CurrentCanvasObject").innerHTML = device_name.name+" (" + a_element.connector+")";
    });

    a_element.on('mouseout', function() {
        let device_name =document.getElementById(a_element.name);  
        document.getElementById("CurrentCanvasObject").innerHTML ="Move over a Object to show the Name";
        });
    

}




function initCanvas(){

     canvas = new fabric.Canvas('canvas_object', {
        // backgroundColor: 'rgb(100,100,200)',
        selectionColor: 'blue',
        // ...
    });

    var canvasContainer = document.getElementById('canvas-wrapper');
    canvasContainer.addEventListener('dragenter', handleDragEnter, false);
    canvasContainer.addEventListener('dragover', handleDragOver, false);
    canvasContainer.addEventListener('dragleave', handleDragLeave, false);
    canvasContainer.addEventListener('drop', drop_handler, false);
    canvas_event_handlers(canvas);

    drawGrid();
}

function include(file) {   
    var script  = document.createElement('script'); 
    script.src  = file; 
    script.type = 'text/javascript'; 
    script.defer = true;     
    document.getElementsByTagName('head').item(0).appendChild(script); 
  } 
    


include("https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.2.0/fabric.min.js");

window.addEventListener("load", function(){
    initCanvas();


});




    
