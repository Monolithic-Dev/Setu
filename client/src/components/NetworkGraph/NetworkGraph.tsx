import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { t, type Language } from "../../i18n/strings";
import "./NetworkGraph.css";

interface NetworkGraphProps {
  language: Language;
}

export function NetworkGraph({ language }: NetworkGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear any previous SVG contents to prevent duplicates on re-renders
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const container = svgRef.current.parentElement;
    const width = container?.clientWidth || 600;
    const height = container?.clientHeight || 400;
    
    // Set explicit viewBox for responsive scaling
    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g");

    // Placeholder text indicating empty state
    g.append("text")
      .attr("x", width / 2)
      .attr("y", height / 2)
      .attr("text-anchor", "middle")
      .attr("fill", "var(--text-muted, #666)")
      .attr("font-family", "inherit")
      .attr("font-size", "1rem")
      .text(t(language, "networkEmpty") || "Select an entity to view its network connections");

    // Placeholder icon/node
    g.append("circle")
      .attr("cx", width / 2)
      .attr("cy", height / 2 - 40)
      .attr("r", 20)
      .attr("fill", "var(--border-color, #e0e0e0)");

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 4])
      .on("zoom", (e) => g.attr("transform", e.transform));
      
    svg.call(zoom);

  }, [language]);

  return (
    <div className="network-graph-container">
      <div className="network-graph-header">
        <h3>{t(language, "appTitle") || "Network Graph"}</h3>
      </div>
      <div className="network-graph-canvas">
        <svg ref={svgRef} className="network-graph-svg" />
      </div>
    </div>
  );
}
