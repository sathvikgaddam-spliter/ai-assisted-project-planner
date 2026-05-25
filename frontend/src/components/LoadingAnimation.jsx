import React, { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

const loadingMessages = [
  "Understanding your idea",
  "Structuring phases",
  "Mapping dependencies",
  "Preparing your execution plan",
];

function LoadingAnimation() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setMessageIndex((currentIndex) => (currentIndex + 1) % loadingMessages.length);
    }, 900);

    return () => window.clearInterval(intervalId);
  }, []);

  return (
    <motion.section
      className="loading-panel surface-card"
      initial={{ opacity: 0, y: 22 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.58, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="loading-preview" aria-hidden="true">
        {[0, 1, 2].map((item) => (
          <motion.span
            key={item}
            animate={{ opacity: [0.45, 1, 0.45], x: [0, 8, 0] }}
            transition={{
              duration: 1.9,
              delay: item * 0.18,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>
      <p className="eyebrow">Planner running</p>
      <AnimatePresence mode="wait">
        <motion.h2
          key={loadingMessages[messageIndex]}
          initial={{ opacity: 0, y: 12, filter: "blur(6px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          exit={{ opacity: 0, y: -10, filter: "blur(6px)" }}
          transition={{ duration: 0.38, ease: [0.22, 1, 0.36, 1] }}
        >
          {loadingMessages[messageIndex]}
        </motion.h2>
      </AnimatePresence>
      <div className="progress-rail">
        <motion.span
          animate={{ width: `${((messageIndex + 1) / loadingMessages.length) * 100}%` }}
          transition={{ duration: 0.52, ease: [0.22, 1, 0.36, 1] }}
        />
      </div>
      <div className="loading-steps">
        {loadingMessages.map((message, index) => (
          <motion.span
            className={index <= messageIndex ? "active" : ""}
            key={message}
            animate={{ scaleX: index <= messageIndex ? 1 : 0.72 }}
            transition={{ duration: 0.28 }}
          />
        ))}
      </div>
    </motion.section>
  );
}

export default LoadingAnimation;
