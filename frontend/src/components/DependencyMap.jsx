import React from "react";

function DependencyMap({ dependencies = [] }) {
  if (!dependencies.length) {
    return <p className="muted empty-copy">No explicit dependencies were generated.</p>;
  }

  return (
    <div className="dependency-map">
      {dependencies.map((dependency, index) => (
        <article className="dependency-card glass-card lift-card" key={dependency.id}>
          <div className="dependency-node source">{dependency.source_task_id}</div>
          <div className="dependency-line">
            <span>{index + 1}</span>
          </div>
          <div className="dependency-node target">{dependency.target_task_id}</div>
          <p>{dependency.description}</p>
        </article>
      ))}
    </div>
  );
}

export default DependencyMap;
