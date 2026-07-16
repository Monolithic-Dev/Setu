import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { t, type Language } from "../../i18n/strings";
import { fetchNetworkGraph, NetworkGraphData } from "../../api/queryClient";
import "./NetworkGraph.css";

interface NetworkGraphProps {
  language: Language;
}

export function NetworkGraph({ language }: NetworkGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState<NetworkGraphData | null>(null);

  useEffect(() => {
    // Fetch a real graph for a demo person (e.g., Person 0001)
    fetchNetworkGraph("Person 0001").then(setData).catch(console.error);
  }, []);

  useEffect(() => {
    if (!svgRef.current || !data) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const container = svgRef.current.parentElement;
    const width = container?.clientWidth || 600;
    const height = container?.clientHeight || 400;

    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g");

    // Convert edges to expected D3 format
    const d3Nodes = data.nodes.map(n => ({ id: n.id, radius: 15, group: 1, label: n.label }));
    const d3Links = data.edges.map(e => ({ 
      source: e.source, 
      target: e.target, 
      value: e.confidence || 1,
      suggested_link: e.suggested_link,
      shared_associates: e.shared_associates,
      total_associates: e.total_associates,
      relationship: e.relationship
    }));

    const simulation = d3.forceSimulation(d3Nodes as any)
      .force("link", d3.forceLink(d3Links).id((d: any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(25));

    // Links with glow
    const link = g.append("g")
      .attr("stroke", "var(--primary-color)")
      .attr("stroke-opacity", 0.4)
      .selectAll("line")
      .data(d3Links)
      .join("line")
      .attr("stroke-width", (d: any) => Math.sqrt(d.value) * 2)
      .attr("class", "graph-link");

    link.append("title")
      .text((d: any) => {
        if (d.suggested_link && d.shared_associates && d.total_associates) {
          const sharedCount = d.shared_associates.length;
          const sId = typeof d.source === 'object' ? d.source.id : d.source;
          const tId = typeof d.target === 'object' ? d.target.id : d.target;
          return `AI Prediction (Jaccard Score: ${d.value})\n${sId} and ${tId} share ${sharedCount} of ${d.total_associates} known associates: ${d.shared_associates.join(", ")}`;
        }
        return `Relationship: ${d.relationship || 'Connected'}`;
      });

    // Nodes
    const node = g.append("g")
      .selectAll("circle")
      .data(d3Nodes)
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
      .data(d3Nodes)
      .join("text")
      .attr("class", "graph-label")
      .attr("dy", (d) => d.radius + 15)
      .attr("text-anchor", "middle")
      .text((d) => d.label || d.id);

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

  }, [data, language]);

  return (
    <div className="network-graph-container">
      <div className="network-graph-header">
        <h3>{t(language, "appTitle") || "Intelligence Network Mapping"}</h3>
        <span className="live-badge">LIVE ANALYSIS</span>
      </div>
      <div className="network-graph-canvas">
        {!data && <div style={{padding: "2rem", color: "var(--text-muted)", textAlign: "center"}}>Loading live intelligence network...</div>}
        <svg ref={svgRef} className="network-graph-svg" style={{display: data ? "block" : "none"}}/>
      </div>
    </div>
  );
}
