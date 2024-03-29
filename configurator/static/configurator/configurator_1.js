var canvas; // the fabric canvas
const noZoom = 1;
var angle = 0; // used to check if angle was changed.
var mousePosition = {x:0, y:0}; // needed for the Paste function



const default_Roomconfig = {
    left: 0,
    top: 0,
    width: 200,
    height: 100,
    fill: 'rgba(255, 255, 255, 0.2)',
    stroke: 'black',
    strokeWidth: 4,
    originX: 'left',
    originY: 'top',
    opacity: 0.5,
    centeredRotation: true,
    selectable: true,
};

function set_canvas_event_handlers(canvas) {


    canvas.on("after:render", function(){ canvas.calcOffset() });


    //enables zoom and panning http://fabricjs.com/fabric-intro-part-5
    canvas.on('mouse:wheel', function(opt) {
        var delta = opt.e.deltaY;
        var zoom = canvas.getZoom();
        zoom *= 0.999 ** delta;
        if (zoom > 2){
            zoom = 2;
        }
        if (zoom < 0.5){
            zoom = 0.5;
        } 
        canvas.setZoom(zoom);
        opt.e.preventDefault();
        opt.e.stopPropagation();
    });
    
    // enables dragging the canvas: alt + mouse down and move
    canvas.on('mouse:down', function(opt) {
        var evt = opt.e;
        // save the last state just in case
        if(opt.target){
            angle = opt.target.get('angle')
            statemachine.addNewState();
        }
        if (evt.altKey === true) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
    });

    canvas.on('mouse:move', function(opt) {
        mousePosition = canvas.getPointer(opt); //save mpuse position everytime we move

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
        if(opt.target){
            if(angle == opt.target.get('angle')){
            //User did not change the angle of the object remove last state 
            statemachine.redoStack.pop();
            }
        }
        this.isDragging = false;
        this.selection = true;
    });

        //If an object has been modified at all, save the new state
        this.canvas.on("object:moving", function(e) {
            statemachine.addNewState();
            statemachine.setLock(true);
        });
    
        //If an object has been modified at all, save the new state
        this.canvas.on("object:modified", function(e) {
            statemachine.setLock(false);
            });

        //If an object has been modified at all, save the new state
        this.canvas.on("object:scaling", function(e) {
            statemachine.addNewState();
            statemachine.setLock(true);
            
            });
            


}

function getRoomProperties() {
    let room_properties = default_Roomconfig;
    room_properties.fill = getRoomColor();
    return room_properties;

}


function resetRoomName(){
    document.getElementById("room_name").value = "";

}

function add_Room() {
    let room_properties = getRoomProperties();
    let room_name = getRoomName();

    const rectangle = new fabric.Rect(room_properties);
    let textObject = new fabric.IText(room_name, {
        left: 40,
        top: 40,
        fontSize: 18,
        fill: '#000000'
    });

    let room = new fabric.Group([rectangle, textObject], {
        left: 150,
        top: 150,
        snapAngle: 90,
        isDevice: false,
        name: room_name,

    });
    statemachine.addNewState();
    canvas.add(room);
    resetRoomName();
    return true;
}

function getRoomName() {
    let name = document.getElementById("room_name").value;
    return name;
}

function getRoomColor() {
    room_color = document.getElementById("room_color").value;
    return room_color;
}


function buildJSON() {
    let canvas_objects = canvas.getObjects();
    let l_rooms = GetRooms(canvas_objects);
    let l_hash_map = CreateHashMap(l_rooms);
    let l_devices = GetDevices(canvas_objects);
    let l_found = false;

    //check for every device in which room it is
    for (var i = 0; i < l_devices.length; i++) {
        //iterate through all rooms and check in which room the device is
        for (var j = 0; j < l_rooms.length; j++) {
            l_found = false;
            if (l_devices[i].isContainedWithinObject(l_rooms[j])) {
                device_tuple = {
                    device_id: l_devices[i].id,
                    connector: l_devices[i].connector
                };

                l_hash_map[l_rooms[j].name].push(device_tuple);                
                l_found=true;
                break;
            }
        }
        if(!l_found){
            alert("Das Gerät "+l_devices[i].name +" konnte keinen Raum zugeordnet werden");
        }
    }

    try {
        return JSON.stringify(l_hash_map);
    } catch (error) {
        console.error();
        return {};
    }

}


function GetRooms(a_canvas_objects){
let l_rooms = []

    for (var i = 0; i < a_canvas_objects.length; i++) {
        // if its not a device it must be a room
        if(!a_canvas_objects[i].isDevice){
            l_rooms.push(a_canvas_objects[i]);
        }
    }

    return l_rooms;

}


function CreateHashMap(a_rooms) {

    let l_hash_map = {};

    for (var i = 0; i < a_rooms.length; i++) {
        l_hash_map[a_rooms[i].name] = [];
    }
    return l_hash_map;

}


function GetDevices(canvas_objects) {
    let l_devices = [];

    for (var i = 0; i < canvas_objects.length; i++) {
        if (canvas_objects[i].isDevice) {
            l_devices.push(canvas_objects[i]);
        }
    }
    return l_devices;
}


function dragstart_handler(ev) {
    // for a drag operation set text to the id value
    ev.dataTransfer.setData("text", ev.target.id);
    
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();   
    }

    return false;
}


// transfer the img/svg to the canvas via build in function of fabric.js
function drop_handler(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("URL");
    let svg_id = ev.dataTransfer.getData("text");
    svg_connector = getConnector(svg_id);
    svg_name = document.getElementById(svg_id).name;
    if(data.split('.').pop() == "svg" ){
        fabric.loadSVGFromURL(data, function(objects, options) {
            var svg = fabric.util.groupSVGElements(objects, options);
            svg.left = ev.layerX / (canvas.getZoom());
            svg.top = ev.layerY / (canvas.getZoom());
            svg.id = svg_id;
            svg.scaleToWidth(100);
            svg.scaleToHeight(100);
            svg.name = svg_name + " " + svg_connector;
            svg.isDevice = true;
            svg.connector = svg_connector;
            add_event_to_device(svg);
            statemachine.addNewState();
            canvas.add(svg);
        });    
    }else{
            // jpg or png picutres. 
            fabric.Image.fromURL(data, function(img) {
                img.left = ev.layerX / (canvas.getZoom());
                img.top = ev.layerY / (canvas.getZoom());
                img.id = svg_id;
                img.scaleToWidth(100);
                img.scaleToHeight(100);
                img.name = svg_name + " " + svg_connector;
                img.isDevice = true;
                img.connector = svg_connector;
                add_event_to_device(img);
                statemachine.addNewState();
                canvas.add(img);
        });
    }
}
// remove every active object
function remove_objects() {
    objects = canvas.getActiveObjects();
    if(objects.length >=1){
        statemachine.addNewState();
        for (var i = 0; i < objects.length; i++) {
            canvas.remove(objects[i]);
        }
    }
}

function getConnector(device_id) {
    //the connector drop field is always dropdown_string + device_id. 
    var dropdown_string = "dropdown-";
    let con = document.getElementById(dropdown_string + device_id);
    var connector = con.value;
    return connector;
}

// In order to see the full name of the device every device needs the following 2 events
function add_event_to_device(a_element) {
    a_element.on('mouseover', function() {
        document.getElementById("CurrentCanvasObject").innerHTML = a_element.name;
    });

    a_element.on('mouseout', function() {
        document.getElementById("CurrentCanvasObject").innerHTML = "Hoover over any Device";
    });
}

// init canvas and set the canvas size to the width of the monitor 
function initCanvas() {
    canvas = new fabric.Canvas('canvas')
    fabric.Object.prototype.set({
        snapThreshold: 45,
        snapAngle: 90
    });;
    setTimeout(function(){ canvas.setWidth(window.innerWidth - 150); }, 200);
    set_canvas_event_handlers(canvas);   
}


function getCanvasContainer(){
    return document.getElementById('canvas-wrapper');
}

//The canvas container needs those function in order to fire the events.
function InitCanvasContainerEvents(){
    var canvasContainer = getCanvasContainer();
    canvasContainer.addEventListener('dragover', handleDragOver, false);
    canvasContainer.addEventListener('drop', drop_handler, false);
}

// set the short cuts of the canvas
function inCanvasContainerShortcuts(){
    canvasContainer = getCanvasContainer();
    canvasContainer.tabIndex = 1000;
    canvasContainer.onkeydown = function(e) 
    
    {
    if(e.ctrlKey){
        switch (e.keyCode) {
            // strg+c
            case 67:
                Copy();
                break;
            case 86:
                // strg+v
                Paste();
                break;
        }
     }else{
         // entf button
        switch (e.keyCode){
            case 46:
                remove_objects();
                break;
        }

     }
    }
}

//following the http://fabricjs.com/copypaste implementation with some changes.
function Copy() {
    
    element = canvas.getActiveObject();

    if(typeof element.name === "undefined" || ! element.isDevice){
        //we can only copy one element at a time. Copy more would break our application. Also we only allow to copy devices
        _clipboard = undefined;
        return;
    }

    element.clone(function(element) {
		_clipboard = element;
	},getCustomAttributes(element));
}
// we have to copy our customattributes
function getCustomAttributes(a_element){
    let custom_attributes = [];
    if(a_element.isDevice){
        custom_attributes = ["id","isDevice","name","connector"];
    }

    return custom_attributes;
}

//following the http://fabricjs.com/copypaste implementation with some changes.
function Paste() {
    if(typeof _clipboard === "undefined" || ! element.isDevice){
        return false;
    }
    //save state Before copying the element
    statemachine.addNewState();
	// clone again, so you can do multiple copies.
	_clipboard.clone(function(clonedObj) {
		canvas.discardActiveObject();
		clonedObj.set({
			left: mousePosition["x"],
			top: mousePosition["y"],
			evented: true,
		});
		if (clonedObj.type === 'activeSelection') {
			// active selection needs a reference to the canvas.
			clonedObj.canvas = canvas;
			clonedObj.forEachObject(function(obj) {
				canvas.add(obj);
			});
			// this should solve the unselectability
			clonedObj.setCoords();
		} else {
			canvas.add(clonedObj);
		}
		_clipboard.top += 10;
		_clipboard.left += 10;
        if(clonedObj.isDevice){
            add_event_to_device(clonedObj);
        }
		canvas.setActiveObject(clonedObj);
		canvas.requestRenderAll();
	},getCustomAttributes(_clipboard));
}










function include(file) {
    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;
    document.getElementsByTagName('head').item(0).appendChild(script);
}



class StateMachine {

    constructor() {
        this.redoStack = [this.getCurrentState()];
        this.unduStack = []
        // lock is needed for operations like move and scale, since those are called every (small) movement this means it is actually not the real last point after undo
        this.islocked = false;
    }


    setLock(islocked){
        this.islocked=islocked;
    }

    getLock(){
        return this.islocked;
    }

    getCurrentState(){
        return JSON.stringify(canvas.toJSON(['id','name',"isDevice","connector"]));
    }

    addNewState(){
        if(!this.getLock()){     
        this.redoStack.push(this.getCurrentState());
        return true;
        }else{
            return false;
        }
    }

    removeState(){
        if(this.redoStack.length == 0){
            return false;
        }else{
            // push the current canvas to the undu stack 
            this.unduStack.push(this.getCurrentState());
            this.restoreLastState(this.redoStack[this.redoStack.length-1]);
            this.redoStack.pop();
            return true;
        }        
    }

    restoreState(){

        if(this.unduStack.length == 0){
            return false;
        }else{
            this.redoStack.push(this.getCurrentState());
            this.restoreLastState(this.unduStack[this.unduStack.length-1]);
            this.unduStack.pop();
            return true;
        }

    }

 restoreCanvas(canvas_json){
    canvas.loadFromJSON(canvas_json, function() {
        canvas.renderAll(); 
     },function(o,object){
        if(object.isDevice){
          add_event_to_device(object);
        }
     })
}


  }



include("https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.2.0/fabric.min.js");

window.addEventListener("load", function() {
    initCanvas();
    InitCanvasContainerEvents();
    inCanvasContainerShortcuts();
    statemachine= new StateMachine();


});

