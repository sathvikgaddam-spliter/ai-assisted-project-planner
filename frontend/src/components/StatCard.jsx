import React from "react";

function StatCard({ label, value, detail }) {
  return (
    <article className="stat-card glass-card lift-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}

export default StatCard;
