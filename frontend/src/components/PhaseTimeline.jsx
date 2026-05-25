import React from "react";
import { motion } from "framer-motion";

function PhaseTimeline({ phases = [], milestones = [] }) {
  if (!phases.length) {
    return <p className="muted empty-copy">No phases were generated.</p>;
  }

  return (
    <motion.div
      className="phase-timeline"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.12 }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.12 } },
      }}
    >
      {phases.map((phase, index) => (
        <motion.article
          className="phase-card surface-card lift-card"
          key={phase.id}
          variants={{
            hidden: { opacity: 0, x: 28 },
            visible: {
              opacity: 1,
              x: 0,
              transition: { duration: 0.58, ease: [0.22, 1, 0.36, 1] },
            },
          }}
          whileHover={{ y: -4 }}
        >
          <div className="timeline-marker">
            <div className="phase-index">{String(index + 1).padStart(2, "0")}</div>
          </div>
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
            {milestonesForPhase(milestones, phase.id).map((milestone) => (
              <div className="phase-milestone" key={milestone.id}>
                <strong>{milestone.name}</strong>
                <span>{milestone.description}</span>
              </div>
            ))}
          </div>
        </motion.article>
      ))}
    </motion.div>
  );
}

function milestonesForPhase(milestones, phaseId) {
  return milestones.filter((milestone) => milestone.target_phase_id === phaseId);
}

export default PhaseTimeline;
