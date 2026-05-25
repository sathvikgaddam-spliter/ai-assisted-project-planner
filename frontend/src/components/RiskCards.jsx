import React from "react";

function RiskCards({ risks = [] }) {
  if (!risks.length) {
    return <p className="muted empty-copy">No risks were generated.</p>;
  }

  return (
    <div className="risk-grid">
      {risks.map((risk) => (
        <article className="risk-card glass-card lift-card" key={risk.id}>
          <div className="risk-topline">
            <span>{risk.id}</span>
            <strong>{risk.impact} impact</strong>
          </div>
          <h3>{risk.description}</h3>
          <p>{risk.mitigation}</p>
          <small>Likelihood: {risk.likelihood}</small>
        </article>
      ))}
    </div>
  );
}

export default RiskCards;
