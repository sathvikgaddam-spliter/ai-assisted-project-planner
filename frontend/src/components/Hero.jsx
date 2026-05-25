import React from "react";
import { motion } from "framer-motion";

const heroGroup = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.16,
      delayChildren: 0.12,
    },
  },
};

const heroItem = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.72, ease: [0.22, 1, 0.36, 1] },
  },
};

function Hero() {
  return (
    <motion.section
      className="hero-panel"
      variants={heroGroup}
      initial="hidden"
      animate="visible"
    >
      <motion.div className="brand-row" variants={heroItem}>
        <div className="brand-mark">AI</div>
        <span>Project Planner</span>
      </motion.div>
      <motion.p className="eyebrow" variants={heroItem}>
        AI planning, beautifully structured
      </motion.p>
      <motion.h1 variants={heroItem}>Project planning, reimagined.</motion.h1>
      <motion.p className="hero-copy" variants={heroItem}>
        Transform a rough idea into an elegant execution plan with phases, milestones,
        risks, dependencies, and recommendations ready for review.
      </motion.p>
      <motion.div className="hero-actions" variants={heroItem}>
        <a href="#planner" className="hero-cta primary">Generate a plan</a>
        <a href="#results" className="hero-cta secondary">View dashboard</a>
      </motion.div>
      <motion.div className="hero-metrics" variants={heroItem}>
        <span>Export results</span>
        <span>Review risks</span>
        <span>Map dependencies</span>
      </motion.div>
    </motion.section>
  );
}

export default Hero;
