import React, { useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import AnimatedSection from "./components/AnimatedSection.jsx";
import Hero from "./components/Hero.jsx";
import LoadingAnimation from "./components/LoadingAnimation.jsx";
import PlannerForm from "./components/PlannerForm.jsx";
import ResultDashboard from "./components/ResultDashboard.jsx";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const initialDescription =
  "Build a hospital appointment scheduling system with doctor availability and patient reminders";

const samplePrompts = [
  "Build a hospital appointment scheduling system",
  "Build an AI study planner for students",
  "Build a food delivery analytics dashboard",
  "Build a healthcare chatbot MVP",
];

function App() {
  const [description, setDescription] = useState(initialDescription);
  const [planDescription, setPlanDescription] = useState("");
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { scrollYProgress } = useScroll();
  const previewY = useTransform(scrollYProgress, [0, 0.45], [0, -36]);
  const previewShadow = useTransform(
    scrollYProgress,
    [0, 0.45],
    ["0 36px 90px rgba(0, 0, 0, 0.08)", "0 46px 110px rgba(0, 0, 0, 0.12)"],
  );

  async function handleSubmit(event) {
    event.preventDefault();
    const submittedDescription = description;
    setLoading(true);
    setError("");
    setPlan(null);
    setPlanDescription("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: submittedDescription }),
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to generate a project plan.");
      }
      setPlan(payload.plan);
      setPlanDescription(submittedDescription);
    } catch (requestError) {
      setError(requestError.message || "Unable to reach the planner API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <Hero />
      <AnimatedSection className="product-preview" aria-label="Product preview">
        <motion.div className="preview-parallax" style={{ y: previewY }}>
        <motion.div
          className="preview-card"
          style={{ boxShadow: previewShadow }}
          animate={{ y: [0, -8, 0] }}
          transition={{ duration: 6.5, repeat: Infinity, ease: "easeInOut" }}
        >
          <div className="preview-toolbar">
            <span />
            <span />
            <span />
          </div>
          <motion.div
            className="preview-grid"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.45 }}
            variants={{
              hidden: {},
              visible: { transition: { staggerChildren: 0.14, delayChildren: 0.18 } },
            }}
          >
            <PreviewPanel className="preview-input-panel">
              <div className="preview-panel-header">
                <span>Project brief</span>
                <strong>AI Mode</strong>
              </div>
              <h3>Hospital appointment scheduling system</h3>
              <p>
                Build a hospital appointment scheduling system with doctor availability,
                patient reminders, staff workflows, and milestone tracking.
              </p>
              <div className="preview-badge-row">
                <span>Healthcare</span>
                <span>System</span>
                <span>Medium complexity</span>
              </div>
              <div className="preview-mini-stats">
                <div>
                  <strong>6</strong>
                  <span>phases</span>
                </div>
                <div>
                  <strong>18</strong>
                  <span>tasks</span>
                </div>
                <div>
                  <strong>12</strong>
                  <span>dependencies</span>
                </div>
              </div>
            </PreviewPanel>

            <PreviewPanel className="preview-timeline-panel">
              <div className="preview-panel-header">
                <span>Phase timeline</span>
                <strong>6 phases</strong>
              </div>
              <div className="preview-phase-list">
                {["Discovery", "Architecture", "MVP build"].map((phase, index) => (
                  <div className="preview-phase" key={phase}>
                    <span>{index + 1}</span>
                    <div>
                      <strong>{phase}</strong>
                      <small>{["Requirements and users", "Core workflow design", "Scheduling and reminders"][index]}</small>
                    </div>
                  </div>
                ))}
              </div>
            </PreviewPanel>

            <PreviewPanel className="preview-insights-panel">
              <div className="preview-panel-header">
                <span>Execution signals</span>
                <strong>Review ready</strong>
              </div>
              <div className="preview-insight-grid">
                <div>
                  <span className="preview-dot blue" />
                  <strong>Milestone</strong>
                  <small>Provider availability validated</small>
                </div>
                <div>
                  <span className="preview-dot amber" />
                  <strong>Risk</strong>
                  <small>Reminder delivery compliance</small>
                </div>
              </div>
              <div className="preview-dependency">
                <span>Availability API</span>
                <strong>{"->"}</strong>
                <span>Booking workflow</span>
              </div>
            </PreviewPanel>
          </motion.div>
        </motion.div>
        </motion.div>
      </AnimatedSection>
      <AnimatedSection className="planner-section" id="planner">
        <div className="section-kicker">Plan generator</div>
        <h2>Describe the work. Get the plan.</h2>
        <p>
          Start with a project idea or choose a sample. The planner returns a structured
          execution view without changing your backend workflow.
        </p>
        <div className="planner-layout">
          <PlannerForm
            description={description}
            error={error}
            loading={loading}
            onDescriptionChange={setDescription}
            samplePrompts={samplePrompts}
            onSubmit={handleSubmit}
          />
        </div>
      </AnimatedSection>
      <AnimatedSection className="results-section" id="results">
        {loading ? (
          <LoadingAnimation />
        ) : (
          <ResultDashboard
            apiBaseUrl={API_BASE_URL}
            plan={plan}
            projectDescription={planDescription || description}
          />
        )}
      </AnimatedSection>
      <footer className="app-footer">
        <span>AI-Assisted Project Planner</span>
        <span>Built with React, FastAPI, Gemini</span>
      </footer>
    </main>
  );
}

function PreviewPanel({ children, className = "" }) {
  return (
    <motion.article
      className={`preview-panel ${className}`}
      variants={{
        hidden: { opacity: 0, y: 24, scale: 0.985 },
        visible: {
          opacity: 1,
          y: 0,
          scale: 1,
          transition: { duration: 0.68, ease: [0.22, 1, 0.36, 1] },
        },
      }}
    >
      {children}
    </motion.article>
  );
}

export default App;
