import React, { useEffect, useState } from "react";

const loadingMessages = [
  "Understanding your project...",
  "Identifying stakeholders...",
  "Mapping dependencies...",
  "Designing execution phases...",
  "Finalizing recommendations...",
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
      <div className="progress-rail">
        <span style={{ width: `${((messageIndex + 1) / loadingMessages.length) * 100}%` }} />
      </div>
      <div className="loading-steps">
        {loadingMessages.map((message, index) => (
          <span className={index <= messageIndex ? "active" : ""} key={message} />
        ))}
      </div>
    </section>
  );
}

export default LoadingAnimation;
