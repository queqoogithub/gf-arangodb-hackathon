<script>
    import { onMount, afterUpdate } from 'svelte';
    import * as d3 from 'd3';
    
    /**
     * @typedef {Object} Node
     * @property {string} id - Unique identifier for the node
     * @property {string} label - Display text for the node
     * @property {number} [x] - X position (managed by d3)
     * @property {number} [y] - Y position (managed by d3)
     */
    
    /**
     * @typedef {Object} Edge
     * @property {string|Node} source - Source node ID or node object
     * @property {string|Node} target - Target node ID or node object
     * @property {number} [weight] - Optional weight affecting the line thickness
     */
    
    /**
     * @typedef {Object} GraphData
     * @property {Node[]} nodes - Array of nodes
     * @property {Edge[]} edges - Array of edges
     */
    
    /** @type {GraphData} */
    export let graphData = { nodes: [], edges: [] };
    
    /** @type {Record<string, string>} - Map of node IDs to color values */
    export let nodeColors = {}; 
    
    /** @type {SVGSVGElement|undefined} */
    let svg;
    
    /** @type {number} */
    let width = 400;
    
    /** @type {number} */
    let height = 250;
    
    $: if (graphData && svg) {
      renderGraph();
    }
    
    onMount(() => {
      if (graphData.nodes.length > 0) {
        renderGraph();
      }
    });
    
    afterUpdate(() => {
      if (graphData.nodes.length > 0) {
        renderGraph();
      }
    });
    
    /** 
     * Renders the graph visualization using D3
     * @returns {void}
     */
    function renderGraph() {
      // Clear previous graph
      d3.select(svg).selectAll("*").remove();
      
      const svgEl = d3.select(svg);
      
      // Ensure all edges reference node objects, not just IDs
      const nodeById = new Map(graphData.nodes.map(node => [node.id, node]));
      const links = graphData.edges
        .filter(edge => {
          // Filter out edges referencing non-existent nodes
          const sourceExists = typeof edge.source === 'string' ? nodeById.has(edge.source) : true;
          const targetExists = typeof edge.target === 'string' ? nodeById.has(edge.target) : true;
          return sourceExists && targetExists;
        })
        .map(edge => ({
          ...edge,
          source: typeof edge.source === 'string' ? nodeById.get(edge.source) : edge.source,
          target: typeof edge.target === 'string' ? nodeById.get(edge.target) : edge.target
        }));
      
      // Setup simulation
      const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(links).id(/** @param {Node} d */ d => d.id).distance(100))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height / 2));

      // Draw links
      const link = svgEl.append("g")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .attr("stroke-width", /** @param {Edge} d */ d => Math.sqrt(d.weight || 1));
      
      // Draw nodes
      const node = svgEl.append("g")
        .selectAll("circle")
        .data(graphData.nodes)
        .enter().append("circle")
        .attr("r", 15)
        .attr("fill", /** @param {Node} d */ d => nodeColors[d.id] || "#ccc")
        .call(drag(simulation));
      
      // Add labels
      const labels = svgEl.append("g")
        .selectAll("text")
        .data(graphData.nodes)
        .enter().append("text")
        .text(/** @param {Node} d */ d => d.label)
        .attr("font-size", "10px")
        .attr("text-anchor", "middle")
        .attr("dy", "0.35em");
      
      // Update positions on tick
      simulation.on("tick", () => {
        link
          .attr("x1", /** @param {Edge} d */ d => d.source && typeof d.source === 'object' ? d.source.x : 0)
          .attr("y1", /** @param {Edge} d */ d => d.source && typeof d.source === 'object' ? d.source.y : 0)
          .attr("x2", /** @param {Edge} d */ d => d.target && typeof d.target === 'object' ? d.target.x : 0)
          .attr("y2", /** @param {Edge} d */ d => d.target && typeof d.target === 'object' ? d.target.y : 0);
        
        node
          .attr("cx", /** @param {Node} d */ d => d.x)
          .attr("cy", /** @param {Node} d */ d => d.y);
        
        labels
          .attr("x", /** @param {Node} d */ d => d.x)
          .attr("y", /** @param {Node} d */ d => d.y);
      });
      
      /**
       * Add drag functionality to nodes
       * @param {any} simulation - The D3 force simulation
       * @returns {Function} - D3 drag behavior
       */
      function drag(simulation) {
        /**
         * Handles the start of a drag event
         * @param {any} event - The drag event
         */
        function dragstarted(event) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
        }
        
        /**
         * Handles the drag movement
         * @param {any} event - The drag event
         */
        function dragged(event) {
          event.subject.fx = event.x;
          event.subject.fy = event.y;
        }
        
        /**
         * Handles the end of a drag event
         * @param {any} event - The drag event
         */
        function dragended(event) {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
        }
        
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }
    }
  </script>
  
  <svg bind:this={svg} width={width} height={height}></svg>