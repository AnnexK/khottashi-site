function $(id) {
    return document.getElementById(id);
}

let canvas = $("example");
let form = $("appform");

const R = 10.0;
let v_id = 0;

function drawEdge(canvas, x1, y1, x2, y2) {
    let context = canvas.getContext("2d");
    
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.stroke();
}

function drawVertex(canvas, x, y) {
    let context = canvas.getContext("2d");

    context.fillStyle = "#ffffff";
    context.beginPath();
    context.arc(x, y, R, 0, 2*Math.PI);
    context.closePath();
    context.fill();
    context.stroke();
}

function Vertex(x, y) {
    this.id = v_id;
    v_id++;
    this.x = x;
    this.y = y;
    this.adjacent = new Array();
    
    this.draw = function() {
	drawVertex(canvas, this.x, this.y);
    }

    this.createEdge = function(w) {
	this.adjacent.push(w);
    }

    this.removeEdge = function(w) {
	this.adjacent = this.adjacent.filter(v => v != w);
	console.log(this.adjacent)
    }
}

function Graph() {
    this.vertices = new Array();

    this.addVertex = function(v) {
	if (this.vertices.includes(v)) {
	    throw new Error("Vertex already in graph");
	}

	if (this.getVertex(v.x, v.y) !== undefined) {
	    throw new Error("Vertices overlap");
	}
	
	this.vertices.push(v);
    }

    this.getVertex = function(x, y) {
	return this.vertices.filter(v => Math.pow(v.x-x, 2) + Math.pow(v.y-y, 2) <= Math.pow(R, 2))[0];
    }
    
    this.addEdge = function (v, w) {
	let V = this.vertices;
	if (!V.includes(v) || !V.includes(w)) {
	    throw new Error("Vertices not in graph");
	}
	v.createEdge(w);
	w.createEdge(v);
    }

    this.removeEdge = function (v, w) {
	let V = this.vertices;
	if (!V.includes(v) || !V.includes(w)) {
	    throw new Error("Vertices not in graph");
	}
	v.removeEdge(w);
	w.removeEdge(v);
    }

    this.removeVertex = function (v) {
	if (!this.vertices.includes(v)) {
	    throw new Error("Vertex not in graph");
	}
	this.vertices = this.vertices.filter(w => w != v);
	console.log(this.vertices);
	
	this.vertices.forEach(w => w.removeEdge(v));
    }

    this.drawEdges = function(v) {
	v.adjacent.forEach(function(w) {
	    drawEdge(canvas, v.x, v.y, w.x, w.y);
	});
    }
    
    this.draw = function() {
	this.vertices.forEach(v => this.drawEdges(v));
	this.vertices.forEach(v => v.draw());
    }

    this.to_dict = function() {
	let verts = this.vertices.map(v => [v.x, v.y]);
	let edges = []
	for (let i = 0; i < verts.length(); i++) {
	    for (let j = 0; j < verts[i].adjacent.length(); j++){
		edges.append([i, j]);
	    }
	}
	let ret = {
	    'name': this.name,
	    'verts': verts,
	    'edges': edges
	}
	return ret;
    }
}

function fromDict(dict) {
    function createEdge(G, edges, verts) {
	v = verts[edges.start];
	w = verts[edges.end];
	G.createEdge(G.getVertex(v.x, v.y), G.getVertex(w.x, w.y));
    }
    let G = new Graph();
    dict.verts.forEach(v => G.addVertex(new Vertex(v.x, v.y)));
    edges.verts.forEach(e => createEdge(G, e, dict.verts));

    return G;
}

let G = new Graph();

function onClickEdit (evt) {
    let context = canvas.getContext("2d");
    let rect = canvas.getBoundingClientRect();
    
    x = evt.pageX - rect.left;
    y = evt.pageY - rect.top;

    try {
	v = new Vertex(x, y);
	G.addVertex(v);
	G.vertices.forEach(w => {if (v != w) G.addEdge(v, w); });
    }
    catch(e) {
	alert(e.message);
    }
    
    context.clearRect(0, 0, canvas.width, canvas.height);    
    G.draw();
}

function onSubmit(evt) {
    evt.preventDefault();
    fetch("get_graph", {method: "POST",
			body: $("graphname")})
	.then(resp => resp.json())
	.then(res => fromDict(res))
}

canvas.addEventListener("mousedown",
			onClickEdit,
			false);

form.addEventListener("submit",
		      onSubmit,
		      false);
