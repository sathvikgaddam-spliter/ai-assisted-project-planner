import React, { useEffect, useState } from "react";

const loadingMessages = [
  "Understanding project...",
  "Analyzing requirements...",
  "Mapping dependencies...",
  "Generating execution plan...",
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
    <section className="loading-panel glass-card">
      <div className="loading-orbit">
        <span />
        <span />
        <span />
      </div>
      <p className="eyebrow">Planner running</p>
      <h2>{loadingMessages[messageIndex]}</h2>
      <div className="loading-steps">
        {loadingMessages.map((message, index) => (
          <span className={index <= messageIndex ? "active" : ""} key={message} />
        ))}
      </div>
    </section>
  );
}

export default LoadingAnimation;
