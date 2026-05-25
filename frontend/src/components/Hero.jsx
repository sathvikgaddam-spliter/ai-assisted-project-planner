import React from "react";

function Hero() {
  return (
    <section className="hero-panel glass-card">
      <div className="brand-row">
        <div className="brand-mark">AI</div>
        <span>Project Planner</span>
      </div>
      <p className="eyebrow">Planning intelligence</p>
      <h1>Turn rough scope into an execution-ready project plan.</h1>
      <p className="hero-copy">
        A focused workspace for translating project ideas into phases, tasks, risks,
        dependencies, and decision-ready recommendations.
      </p>
      <div className="hero-metrics">
        <span>Structured plans</span>
        <span>Risk-aware output</span>
        <span>AI with fallback</span>
      </div>
    </section>
  );
}

export default Hero;
