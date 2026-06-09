import React from "react";
import { motion } from "framer-motion";

function MilestoneTracker({ milestones = [] }) {
  if (!milestones.length) {
    return <p className="muted empty-copy">No milestones were generated.</p>;
  }

  return (
    <motion.div
      className="milestone-track"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.18 }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.08 } },
      }}
    >
      {milestones.map((milestone, index) => (
        <motion.article
          className="milestone-card surface-card lift-card"
          key={milestone.id}
          variants={{
            hidden: { opacity: 0, y: 18 },
            visible: {
              opacity: 1,
              y: 0,
              transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
            },
          }}
          whileHover={{ y: -4 }}
        >
          <div className="milestone-dot">{index + 1}</div>
          <div>
            <strong>{milestone.name}</strong>
            <span>{milestone.description}</span>
            <small>Target phase: {milestone.target_phase_id}</small>
          </div>
        </motion.article>
      ))}
    </motion.div>
  );
}

export default MilestoneTracker;
