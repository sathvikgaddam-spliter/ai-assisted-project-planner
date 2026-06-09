import React from "react";
import { motion } from "framer-motion";

function PlannerForm({ description, error, loading, onDescriptionChange, onSubmit, samplePrompts = [] }) {
  return (
    <motion.form
      className="planner-form surface-card"
      onSubmit={onSubmit}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.28 }}
      transition={{ duration: 0.64, ease: [0.22, 1, 0.36, 1] }}
    >
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
        <motion.button
          type="submit"
          disabled={loading || description.trim().length < 3}
          whileHover={{ scale: loading ? 1 : 1.018 }}
          whileTap={{ scale: loading ? 1 : 0.985 }}
          transition={{ duration: 0.18 }}
        >
          {loading ? "Generating" : "Generate Plan"}
        </motion.button>
      </div>
      <div className="sample-prompts" aria-label="Sample prompts">
        <p className="eyebrow">Sample prompts</p>
        <div>
          {samplePrompts.map((prompt, index) => (
            <motion.button
              className="sample-prompt"
              key={prompt}
              type="button"
              onClick={() => onDescriptionChange(prompt)}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              whileHover={{ y: -3, scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.42, delay: index * 0.045, ease: [0.22, 1, 0.36, 1] }}
            >
              {prompt}
            </motion.button>
          ))}
        </div>
      </div>
      {error && <div className="error-card">{error}</div>}
    </motion.form>
  );
}

export default PlannerForm;
