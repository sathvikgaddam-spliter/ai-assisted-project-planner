import React from "react";
import { motion } from "framer-motion";
import DependencyMap from "./DependencyMap.jsx";
import ExportActions from "./ExportActions.jsx";
import MilestoneTracker from "./MilestoneTracker.jsx";
import PhaseTimeline from "./PhaseTimeline.jsx";
import RiskCards from "./RiskCards.jsx";
import StatCard from "./StatCard.jsx";

function ResultDashboard({ plan }) {
  if (!plan) {
    return (
      <motion.section
        className="empty-dashboard surface-card"
        initial={{ opacity: 0, y: 22 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.68, ease: [0.22, 1, 0.36, 1] }}
      >
        <motion.div
          className="empty-visual"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.11 } },
          }}
        >
          {[
            ["Prompt", "Hospital scheduling system"],
            ["Timeline", "Discovery -> Build -> Launch"],
            ["Signals", "Risks, milestones, dependencies"],
          ].map(([label, value]) => (
            <motion.div
              className="empty-preview-row"
              key={label}
              variants={{
                hidden: { opacity: 0, x: -14 },
                visible: { opacity: 1, x: 0 },
              }}
            >
              <span>{label}</span>
              <strong>{value}</strong>
            </motion.div>
          ))}
        </motion.div>
        <p className="eyebrow">Demo workspace</p>
        <h2>Select a sample prompt or write your own brief.</h2>
        <p>
          The generated dashboard will assemble timeline phases, milestone gates,
          dependencies, risks, recommendations, export actions, and AI mode details.
        </p>
        <motion.div
          className="empty-feature-grid"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.06, delayChildren: 0.18 } },
          }}
        >
          {["Timeline", "Exports", "Risk map", "Mode badge"].map((item) => (
            <motion.span
              key={item}
              variants={{
                hidden: { opacity: 0, y: 12 },
                visible: { opacity: 1, y: 0 },
              }}
            >
              {item}
            </motion.span>
          ))}
        </motion.div>
      </motion.section>
    );
  }

  const phases = plan.phases || [];
  const milestones = plan.milestones || [];
  const dependencies = plan.dependencies || [];
  const recommendations = plan.recommendations || [];
  const warnings = plan.warnings || [];
  const clarificationQuestions = plan.clarification_questions || [];
  const isFallbackMode = warnings.some((warning) => warning.toLowerCase().includes("fallback") || warning.toLowerCase().includes("ai planning failed"));

  return (
    <motion.section
      className="result-dashboard"
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.1 } },
      }}
    >
      <motion.section
        className="overview-card surface-card"
        variants={dashboardItem}
      >
        <div>
          <p className="eyebrow">{formatStatus(plan.status)}</p>
          <h2>{plan.project_name}</h2>
          <p>{plan.summary}</p>
        </div>
        <div className="overview-actions">
          <div className={`mode-badge ${isFallbackMode ? "fallback" : "ai"}`}>
            {isFallbackMode ? "Fallback Mode" : "AI Mode"}
          </div>
          <div className="status-pill">{plan.status}</div>
        </div>
        <ExportActions plan={plan} />
      </motion.section>

      <motion.div className="stat-grid" variants={dashboardItem}>
        <StatCard label="Domain" value={plan.domain} detail="Classification" />
        <StatCard label="Type" value={plan.project_type} detail="Planner output" />
        <StatCard label="Complexity" value={plan.complexity} detail="Delivery signal" />
      </motion.div>

      {clarificationQuestions.length > 0 && (
        <DashboardSection title="Clarification questions">
          <div className="note-list">
            {clarificationQuestions.map((question) => (
                <article className="note-card surface-card" key={question}>
                {question}
              </article>
            ))}
          </div>
        </DashboardSection>
      )}

      <DashboardSection title="Phases timeline">
        <PhaseTimeline phases={phases} milestones={milestones} />
      </DashboardSection>

      <DashboardSection title="Milestone tracker">
        <MilestoneTracker milestones={milestones} />
      </DashboardSection>

      <DashboardSection title="Risks">
        <RiskCards risks={plan.risks || []} />
      </DashboardSection>

      <DashboardSection title="Dependencies">
        <DependencyMap dependencies={dependencies} />
      </DashboardSection>

      <DashboardSection title="Recommendations">
        <CompactGrid
          items={recommendations}
          emptyText="No recommendations were generated."
          renderItem={(recommendation) => (
            <>
              <strong>{recommendation.category}</strong>
              <span>{recommendation.recommendation}</span>
              <small>{recommendation.rationale}</small>
            </>
          )}
        />
      </DashboardSection>

      {warnings.length > 0 && (
        <DashboardSection title="Warnings and debug notes">
          <div className="warning-stack">
            {warnings.map((warning) => (
              <article className="warning-card glass-card" key={warning}>
                {warning}
              </article>
            ))}
          </div>
        </DashboardSection>
      )}
    </motion.section>
  );
}

function DashboardSection({ title, children }) {
  return (
    <motion.section
      className="dashboard-section"
      variants={dashboardItem}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.16 }}
    >
      <div className="section-heading">
        <h2>{title}</h2>
      </div>
      {children}
    </motion.section>
  );
}

function CompactGrid({ items = [], renderItem, emptyText }) {
  if (!items.length) {
    return <p className="muted empty-copy">{emptyText}</p>;
  }

  return (
    <motion.div
      className="compact-grid"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.18 }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.07 } },
      }}
    >
      {items.map((item) => (
        <motion.article
          className="compact-item surface-card lift-card"
          key={item.id || item.name}
          variants={cardItem}
          whileHover={{ y: -4, transition: { duration: 0.18 } }}
        >
          {renderItem(item)}
        </motion.article>
      ))}
    </motion.div>
  );
}

function formatStatus(status = "") {
  return status.replaceAll("_", " ");
}

const dashboardItem = {
  hidden: { opacity: 0, y: 22 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.62, ease: [0.22, 1, 0.36, 1] },
  },
};

const cardItem = {
  hidden: { opacity: 0, y: 18 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
  },
};

export default ResultDashboard;
