import React from "react";
import { motion } from "framer-motion";

function DependencyMap({ dependencies = [] }) {
  if (!dependencies.length) {
    return <p className="muted empty-copy">No explicit dependencies were generated.</p>;
  }

  return (
    <motion.div
      className="dependency-map"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.18 }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.08 } },
      }}
    >
      {dependencies.map((dependency, index) => (
        <motion.article
          className="dependency-card surface-card lift-card"
          key={dependency.id}
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
          <div className="dependency-node source">{dependency.source_task_id}</div>
          <div className="dependency-line">
            <span>{index + 1}</span>
          </div>
          <div className="dependency-node target">{dependency.target_task_id}</div>
          <p>{dependency.description}</p>
        </motion.article>
      ))}
    </motion.div>
  );
}

export default DependencyMap;
