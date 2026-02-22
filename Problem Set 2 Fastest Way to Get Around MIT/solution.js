// =====================
// Node
// =====================
class Node {
  constructor(name) {
    this.name = String(name);
  }

  getName() {
    return this.name;
  }

  toString() {
    return this.name;
  }

  equals(other) {
    return other instanceof Node && this.name === other.name;
  }
}
// =====================
// Edge
// =====================
class Edge {
  constructor(src, dest) {
    this.src = src;
    this.dest = dest;
  }

  getSource() {
    return this.src;
  }

  getDestination() {
    return this.dest;
  }

  toString() {
    return `${this.src}->${this.dest}`;
  }
}

// =====================
// WeightedEdge
// =====================
class WeightedEdge extends Edge {
  constructor(src, dest, totalDistance, outdoorDistance) {
    super(src, dest);
    this.totalDistance = Number(totalDistance);
    this.outdoorDistance = Number(outdoorDistance);
  }

  getTotalDistance() {
    return this.totalDistance;
  }

  getOutdoorDistance() {
    return this.outdoorDistance;
  }

  toString() {
    return `${this.src}->${this.dest} (${this.totalDistance}, ${this.outdoorDistance})`;
  }
}

// =====================
// Digraph
// =====================
class Digraph {
  constructor() {
    this.nodes = new Set(); // store node names
    this.edges = new Map(); // name -> edges
  }

  addNode(node) {
    const name = node.getName();

    if (this.nodes.has(name)) {
      throw new Error("Duplicate node");
    }

    this.nodes.add(name);
    this.edges.set(name, []);
  }

  hasNode(node) {
    return this.nodes.has(node.getName());
  }

  getEdgesForNode(node) {
    return this.edges.get(node.getName());
  }

  addEdge(edge) {
    const src = edge.getSource().getName();
    const dest = edge.getDestination().getName();

    if (!this.nodes.has(src) || !this.nodes.has(dest)) {
      throw new Error("Node not in graph");
    }

    this.edges.get(src).push(edge);
  }

  getAllNodes() {
    return this.nodes;
  }
}

// =====================
// loadMap (Node.js version)
// =====================
const fs = require("fs");

function loadMap(mapFilename) {
  const graph = new Digraph();
  const edges = [];
  const nodeMap = new Map(); // ensures unique Node objects

  console.log("Loading map from file...");

  const data = fs.readFileSync(mapFilename, "utf-8");
  const lines = data.split("\n");

  for (let line of lines) {
    line = line.trim();
    if (!line) continue;

    const [srcName, destName, totalDis, outdoor] = line.split(" ");

    // Ensure we reuse Node objects
    if (!nodeMap.has(srcName)) {
      nodeMap.set(srcName, new Node(srcName));
    }
    if (!nodeMap.has(destName)) {
      nodeMap.set(destName, new Node(destName));
    }

    const srcNode = nodeMap.get(srcName);
    const destNode = nodeMap.get(destName);

    const edge = new WeightedEdge(srcNode, destNode, totalDis, outdoor);

    edges.push(edge);
  }

  // Add nodes to graph
  for (let node of nodeMap.values()) {
    graph.addNode(node);
  }

  // Add edges
  for (let edge of edges) {
    graph.addEdge(edge);
  }

  return graph;
}

// Example usage (Node.js):
const g = loadMap("./mit_map.txt");
// console.log(g.toString());

function getBestPath(
  digraph,
  start,
  end,
  path,
  maxDistOutdoors,
  bestDist,
  bestPath,
) {
  //   let startNode = new Node(start);
  //   let endNode = new Node(end);
  //   console.log("startNode: ", startNode);
  //   console.log("endNode: ", endNode);
  if (!(digraph.nodes.has(start) && digraph.nodes.has(end))) {
    throw Error("Node is not in the graph");
  }

  if (!path) {
    path = [[], 0, 0];
  }

  let [nodes, currentDist, currentOutdoor] = path;
  nodes = [...nodes, start];

  if (start === end) {
    return [nodes, currentDist];
  }
  //
  let listOfEdges = digraph.edges.get(start);
  for (let edge of listOfEdges) {
    let nextName = edge.getDestination().getName();
    // console.log("NextNode: ", nextNode);

    if (!nodes.includes(nextName)) {
      //   console.log("Node: ", nextName);
      let newDist = currentDist + edge.getTotalDistance();
      let newOutdoor = currentOutdoor + edge.getOutdoorDistance();

      if (newOutdoor <= maxDistOutdoors) {
        if (bestDist === null || newDist < bestDist) {
          let result = getBestPath(
            digraph,
            nextName,
            end,
            [nodes, newDist, newOutdoor],
            maxDistOutdoors,
            bestDist,
            bestPath,
          );

          if (result != null) {
            let [newPath, newBestDist] = result;

            if (bestDist == null || newBestDist < bestDist) {
              // console.log(result);
              bestDist = result[1];
              bestPath = result[0];
            }
          }
        }
      }
    }
  }

  if (bestPath == null) {
    return null;
  }

  return [bestPath, bestDist];
}

let foundPath = getBestPath(g, "2", "32", null, 100000, null, null);

console.log(foundPath);

let newNode = new Node("2");

// console.log(g.hasNode(newNode));
// console.log(g.getEdgesForNode(newNode));
// console.log(g.getAllNodes());
