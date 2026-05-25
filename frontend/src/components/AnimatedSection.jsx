import React from "react";
import { motion } from "framer-motion";

const reveal = {
  hidden: { opacity: 0, y: 28 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.72, ease: [0.22, 1, 0.36, 1] },
  },
};

function AnimatedSection({ children, className = "", as = "section", delay = 0, ...props }) {
  const MotionTag = motion[as] || motion.section;

  return (
    <MotionTag
      className={className}
      variants={reveal}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.18 }}
      transition={{ delay }}
      {...props}
    >
      {children}
    </MotionTag>
  );
}

export default AnimatedSection;
