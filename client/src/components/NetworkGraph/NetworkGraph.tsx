import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { t, type Language } from "../../i18n/strings";
import "./NetworkGraph.css";

interface NetworkGraphProps {
  language: Language;
}

const dummyData = {
  nodes: [
    { id: "Suspect A", group: 1, radius: 25 },
    { id: "Suspect B", group: 1, radius: 15 },
    { id: "Vehicle X", group: 2, radius: 10 },
    { id: "Location Y", group: 3, radius: 20 },
    { id: "Phone Z", group: 4, radius: 8 },
    { id: "Account W", group: 5, radius: 12 },
    { id: "Suspect C", group: 1, radius: 18 }
  ],
  links: [
    { source: "Suspect A", target: "Suspect B", value: 1 },
    { source: "Suspect A", target: "Location Y", value: 2 },
    { source: "Suspect B", target: "Vehicle X", value: 1 },
    { source: "Suspect C", target: "Location Y", value: 1 },
    { source: "Suspect A", target: "Phone Z", value: 1 },
    { source: "Suspect C", target: "Account W", value: 1 },
    { source: "Account W", target: "Suspect B", value: 2 }
  ]
};

export function NetworkGraph({ language }: NetworkGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const container = svgRef.current.parentElement;
    const width = container?.clientWidth || 600;
    const height = container?.clientHeight || 400;

    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g");

    const simulation = d3.forceSimulation(dummyData.nodes as any)
      .force("link", d3.forceLink(dummyData.links).id((d: any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius((d: any) => d.radius + 10));

    // Links with glow
    const link = g.append("g")
      .attr("stroke", "var(--primary-color)")
      .attr("stroke-opacity", 0.4)
      .selectAll("line")
      .data(dummyData.links)
      .join("line")
      .attr("stroke-width", (d) => Math.sqrt(d.value) * 2)
      .attr("class", "graph-link");

    // Nodes
    const node = g.append("g")
      .selectAll("circle")
      .data(dummyData.nodes)
      .join("circle")
      .attr("r", (d) => d.radius)
      .attr("fill", (d) => {
        const colors = ["#38bdf8", "#818cf8", "#fb7185", "#34d399", "#fbbf24"];
        return colors[d.group - 1];
      })
      .attr("class", "graph-node")
      .call(drag(simulation) as any);

    // Labels
    const label = g.append("g")
      .selectAll("text")
      .data(dummyData.nodes)
      .join("text")
      .attr("class", "graph-label")
      .attr("dy", (d) => d.radius + 15)
      .attr("text-anchor", "middle")
      .text((d) => d.id);

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node
        .attr("cx", (d: any) => d.x)
        .attr("cy", (d: any) => d.y);

      label
        .attr("x", (d: any) => d.x)
        .attr("y", (d: any) => d.y);
    });

    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 4])
      .on("zoom", (e) => g.attr("transform", e.transform));
      
    svg.call(zoom);

    function drag(simulation: any) {
      function dragstarted(event: any) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
      function dragged(event: any) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      function dragended(event: any) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
      return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }

  }, [language]);

  return (
    <div className="network-graph-container">
      <div className="network-graph-header">
        <h3>{t(language, "appTitle") || "Intelligence Network Mapping"}</h3>
        <span className="live-badge">LIVE ANALYSIS</span>
      </div>
      <div className="network-graph-canvas">
        <svg ref={svgRef} className="network-graph-svg" />
      </div>
    </div>
  );
}
