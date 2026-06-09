import React from "react";
import { motion } from "framer-motion";

function RiskCards({ risks = [] }) {
  if (!risks.length) {
    return <p className="muted empty-copy">No risks were generated.</p>;
  }

  return (
    <motion.div
      className="risk-grid"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.18 }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.08 } },
      }}
    >
      {risks.map((risk) => (
        <motion.article
          className="risk-card surface-card lift-card"
          key={risk.id}
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
          <div className="risk-topline">
            <span>{risk.id}</span>
            <strong>{risk.impact} impact</strong>
          </div>
          <h3>{risk.description}</h3>
          <p>{risk.mitigation}</p>
          <small>Likelihood: {risk.likelihood}</small>
        </motion.article>
      ))}
    </motion.div>
  );
}

export default RiskCards;
