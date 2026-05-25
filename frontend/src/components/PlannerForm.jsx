import React from "react";

function PlannerForm({ description, error, loading, onDescriptionChange, onSubmit, samplePrompts = [] }) {
  return (
    <form className="planner-form glass-card" onSubmit={onSubmit}>
      <div className="form-heading">
        <div>
          <p className="eyebrow">Prompt</p>
          <h2>Project brief</h2>
        </div>
        <span>{description.trim().length} chars</span>
      </div>
      <textarea
        id="project-description"
        value={description}
        onChange={(event) => onDescriptionChange(event.target.value)}
        placeholder="Build a clinic appointment reminder workflow with SMS reminders and staff follow-up."
      />
      <div className="form-actions">
        <p>Include users, constraints, timeline, and success criteria when available.</p>
        <button type="submit" disabled={loading || description.trim().length < 3}>
          {loading ? "Generating" : "Generate Plan"}
        </button>
      </div>
      <div className="sample-prompts" aria-label="Sample prompts">
        <p className="eyebrow">Sample prompts</p>
        <div>
          {samplePrompts.map((prompt) => (
            <button
              className="sample-prompt"
              key={prompt}
              type="button"
              onClick={() => onDescriptionChange(prompt)}
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>
      {error && <div className="error-card">{error}</div>}
    </form>
  );
}

export default PlannerForm;
