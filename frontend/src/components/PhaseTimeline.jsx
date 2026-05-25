import React from "react";

function PhaseTimeline({ phases = [] }) {
  if (!phases.length) {
    return <p className="muted empty-copy">No phases were generated.</p>;
  }

  return (
    <div className="phase-timeline">
      {phases.map((phase, index) => (
        <article className="phase-card glass-card lift-card" key={phase.id}>
          <div className="phase-index">{String(index + 1).padStart(2, "0")}</div>
          <div className="phase-body">
            <div className="phase-title-row">
              <div>
                <p className="eyebrow">{phase.id}</p>
                <h3>{phase.name}</h3>
              </div>
              <span>{phase.estimated_duration}</span>
            </div>
            <p>{phase.objective}</p>
            <div className="task-stack">
              {(phase.tasks || []).map((task) => (
                <div className="task-card" key={task.id}>
                  <div>
                    <strong>{task.id}: {task.title}</strong>
                    <span>{task.description}</span>
                  </div>
                  <small>
                    {task.owner_role} / {task.estimated_effort}
                    {(task.dependencies || []).length > 0
                      ? ` / Depends on ${task.dependencies.join(", ")}`
                      : ""}
                  </small>
                </div>
              ))}
            </div>
            {(phase.deliverables || []).length > 0 && (
              <div className="tag-row">
                {phase.deliverables.map((deliverable) => (
                  <span key={deliverable}>{deliverable}</span>
                ))}
              </div>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}

export default PhaseTimeline;
