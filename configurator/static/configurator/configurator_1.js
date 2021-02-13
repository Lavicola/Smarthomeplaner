var canvas;
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
    centeredRotation: true,
    snapAngle: 180,
    selectable: true,
};

function set_canvas_event_handlers(canvas) {

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
    
    // enables dragging the canvas: alt + mouse down and move
    canvas.on('mouse:down', function(opt) {
        var evt = opt.e;
        if (evt.altKey === true) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
    });

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

function getRoomProperties() {
    let room_properties = default_Roomconfig;
    room_properties.fill = getRoomColor();
    room_properties.name = GenerateRoomname();
    room_properties.isDevice = false;
    room_properties.opacity = 0.5;
    return room_properties;

}

function add_Room() {
    let room_properties = getRoomProperties();

    const room = new fabric.Rect(room_properties);
    let textObject = new fabric.IText(room_properties.name, {
        left: 40,
        top: 40,
        fontSize: 18,
        fill: '#000000'
    });

    let group = new fabric.Group([room, textObject], {
        left: 150,
        top: 150
    });

    canvas.add(group);
    return true;
}

function GenerateRoomname() {
    let number = 2;
    let temp_name = getRoomCategory();
    let name = temp_name;
    while (RoomExists(name)) {
        name = temp_name + number;
        number++;
    }

    return name;
}

function RoomExists(a_room_name) {
    let l_rooms = GetRoomNames();
    let j = l_rooms.length;

    for (var i = 0; i < j; i++) {

        if (l_rooms[i] == a_room_name) {
            return true;
        }

    }
    return false;
}


function getRoomCategory() {
    category = document.getElementById("room_name").value;
    return category;
}

function getRoomColor() {
    room_color = document.getElementById("room_color").value;
    return room_color;
}


function buildJSON() {
    let canvas_objects = canvas.getObjects();
    let l_hash_map = CreateHashMap(canvas_objects); // [room_name]
    let l_rooms = GetRectTextGroups(canvas_objects);
    let l_room_names = GetRoomNames(canvas_objects);
    let l_devices = GetDevices(canvas_objects);
    let l_found;

    //check for every device in which room it is
    for (var i = 0; i < l_devices.length; i++) {
        //iterate through all rooms
        for (var j = 0; j < l_rooms.length; j++) {
            l_found = false;
            if (l_devices[i].isContainedWithinObject(l_rooms[j])) {
                device_tuple = {
                    device_id: l_devices[i].id,
                    connector: l_devices[i].connector
                };
                l_hash_map[l_room_names[j]].push(device_tuple);                
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


function CreateHashMap(a_canvas_objects) {

    let l_hash_map = {};
    let l_rooms = GetRoomNames(a_canvas_objects);

    for (var i = 0; i < l_rooms.length; i++) {
        l_hash_map[l_rooms[i]] = [];
    }
    return l_hash_map;

}

// This function returns a room object or None if the inserted group is not a (rect,text). The Group also must have an isDevice type
function GetRectOfRectTextGroup(group) {

    single_object = group._objects[0];
    // check if isDevice type exists if not return a placeholder string
    if (single_object.isDevice === undefined) {
        //console.log("object has no isDevice type");
        return "None";
        //if it is not a device it must be a room
    } else if (!single_object.isDevice) {
        return single_object;
    }

    return "None";
}


// This function returns every rectText group which are rooms
function GetRectTextGroups(groups) {
    rectTextGroups = [];
    for (var i = 0; i < groups.length; i++) {
        single_objects = groups[i]._objects;

        if (single_objects[0].isDevice === undefined) {
            //if it is not a device it must be a room
        } else if (!single_objects[0].isDevice) {
            rectTextGroups.push(groups[i]);
        }

    }
    return rectTextGroups;
}


//This function returns an array of Room names
function GetRoomNames(a_canvas_objects) {
    let room_names = [];
    let room;

    for (var i = 0; i < a_canvas_objects.length; i++) {
        room = GetRectOfRectTextGroup(a_canvas_objects[i]);

        if (room != "None") {
            room_names.push(room.name);
        }
    }
    return room_names;

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
    let svg_id = ev.dataTransfer.getData("text");
    svg_connector = getConnector(svg_id);
    svg_name = document.getElementById(svg_id).name;
    fabric.loadSVGFromURL(data, function(objects, options) {
        var svg = fabric.util.groupSVGElements(objects, options);
        svg.left = ev.layerX;
        svg.top = ev.layerY;
        svg.id = svg_id;
        svg.scaleToWidth(100);
        svg.scaleToHeight(100);
        svg.name = svg_name + " " + svg_connector;
        svg.isDevice = true;
        svg.connector = svg_connector;
        add_event_to_device(svg);

        canvas.add(svg);
    });


}

function remove_objects() {

    objects = canvas.getActiveObjects();
    for (var i = 0; i < objects.length; i++) {
        canvas.remove(objects[i]);
    }
}

function getConnector(device_id) {
    var dropdown_string = "dropdown-";
    let con = document.getElementById(dropdown_string + device_id);
    var connector = con.value;
    return connector;
}

function add_event_to_device(a_element) {
    a_element.on('mouseover', function() {
        document.getElementById("CurrentCanvasObject").innerHTML = a_element.name;
    });

    a_element.on('mouseout', function() {
        document.getElementById("CurrentCanvasObject").innerHTML = "Move over a Object to show the Name";
    });


}

function SetBackground() {
    fabric.Image.fromURL("https://images.unsplash.com/photo-1600456899121-68eda5705257?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=2025&q=80.jpg", function(img) {
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
            stretch: true,
            scaleX: canvas.width / img.width,
            scaleY: canvas.height / img.height
        });
    });

}



function initCanvas() {
    canvas = new fabric.Canvas('canvas_object');
    set_canvas_event_handlers(canvas);
}

function InitCanvasContainerEvents(){
    var canvasContainer = document.getElementById('canvas-wrapper');
    canvasContainer.addEventListener('dragenter', handleDragEnter, false);
    canvasContainer.addEventListener('dragover', handleDragOver, false);
    canvasContainer.addEventListener('dragleave', handleDragLeave, false);
    canvasContainer.addEventListener('drop', drop_handler, false);
}


function include(file) {
    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;
    document.getElementsByTagName('head').item(0).appendChild(script);
}



include("https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.2.0/fabric.min.js");

window.addEventListener("load", function() {
    initCanvas();
    InitCanvasContainerEvents();

});