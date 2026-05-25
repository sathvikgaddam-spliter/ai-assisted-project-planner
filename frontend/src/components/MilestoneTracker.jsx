import React from "react";

function MilestoneTracker({ milestones = [] }) {
  if (!milestones.length) {
    return <p className="muted empty-copy">No milestones were generated.</p>;
  }

  return (
    <div className="milestone-track">
      {milestones.map((milestone, index) => (
        <article className="milestone-card glass-card lift-card" key={milestone.id}>
          <div className="milestone-dot">{index + 1}</div>
          <div>
            <strong>{milestone.name}</strong>
            <span>{milestone.description}</span>
            <small>Target phase: {milestone.target_phase_id}</small>
          </div>
        </article>
      ))}
    </div>
  );
}

export default MilestoneTracker;
