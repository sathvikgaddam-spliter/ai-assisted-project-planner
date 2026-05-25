import React, { useState } from "react";
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
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPlan(null);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_description: description }),
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to generate a project plan.");
      }
      setPlan(payload);
    } catch (requestError) {
      setError(requestError.message || "Unable to reach the planner API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace-grid">
        <div className="compose-column fade-in">
          <Hero />
          <PlannerForm
            description={description}
            error={error}
            loading={loading}
            onDescriptionChange={setDescription}
            samplePrompts={samplePrompts}
            onSubmit={handleSubmit}
          />
        </div>
        <div className="dashboard-column slide-in">
          {loading ? <LoadingAnimation /> : <ResultDashboard plan={plan} />}
        </div>
      </section>
      <footer className="app-footer">
        <span>AI-Assisted Project Planner</span>
        <span>Built with React, FastAPI, Gemini</span>
      </footer>
    </main>
  );
}

export default App;
