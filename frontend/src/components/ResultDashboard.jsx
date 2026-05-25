import React from "react";
import MilestoneTracker from "./MilestoneTracker.jsx";
import PhaseTimeline from "./PhaseTimeline.jsx";
import RiskCards from "./RiskCards.jsx";
import StatCard from "./StatCard.jsx";

function ResultDashboard({ plan }) {
  if (!plan) {
    return (
      <section className="empty-dashboard glass-card">
        <div className="empty-visual">
          <span />
          <span />
          <span />
        </div>
        <p className="eyebrow">Ready</p>
        <h2>Your generated project dashboard will appear here.</h2>
        <p>
          Run a plan to see delivery phases, milestone gates, dependencies, risks,
          recommendations, and debug notes in one workspace.
        </p>
      </section>
    );
  }

  const phases = plan.phases || [];
  const milestones = plan.milestones || [];
  const dependencies = plan.dependencies || [];
  const recommendations = plan.recommendations || [];
  const warnings = plan.warnings || [];
  const clarificationQuestions = plan.clarification_questions || [];

  return (
    <section className="result-dashboard">
      <section className="overview-card glass-card">
        <div>
          <p className="eyebrow">{formatStatus(plan.status)}</p>
          <h2>{plan.project_name}</h2>
          <p>{plan.summary}</p>
        </div>
        <div className="status-pill">{plan.status}</div>
      </section>

      <div className="stat-grid">
        <StatCard label="Domain" value={plan.domain} detail="Classification" />
        <StatCard label="Type" value={plan.project_type} detail="Planner output" />
        <StatCard label="Complexity" value={plan.complexity} detail="Delivery signal" />
      </div>

      {clarificationQuestions.length > 0 && (
        <DashboardSection title="Clarification questions">
          <div className="note-list">
            {clarificationQuestions.map((question) => (
              <article className="note-card glass-card" key={question}>
                {question}
              </article>
            ))}
          </div>
        </DashboardSection>
      )}

      <DashboardSection title="Phases timeline">
        <PhaseTimeline phases={phases} />
      </DashboardSection>

      <DashboardSection title="Milestone tracker">
        <MilestoneTracker milestones={milestones} />
      </DashboardSection>

      <DashboardSection title="Risks">
        <RiskCards risks={plan.risks || []} />
      </DashboardSection>

      <DashboardSection title="Dependencies">
        <CompactGrid
          items={dependencies}
          emptyText="No explicit dependencies were generated."
          renderItem={(dependency) => (
            <>
              <strong>{dependency.source_task_id} to {dependency.target_task_id}</strong>
              <span>{dependency.description}</span>
            </>
          )}
        />
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
    </section>
  );
}

function DashboardSection({ title, children }) {
  return (
    <section className="dashboard-section">
      <div className="section-heading">
        <h2>{title}</h2>
      </div>
      {children}
    </section>
  );
}

function CompactGrid({ items = [], renderItem, emptyText }) {
  if (!items.length) {
    return <p className="muted empty-copy">{emptyText}</p>;
  }

  return (
    <div className="compact-grid">
      {items.map((item) => (
        <article className="compact-item glass-card lift-card" key={item.id || item.name}>
          {renderItem(item)}
        </article>
      ))}
    </div>
  );
}

function formatStatus(status = "") {
  return status.replaceAll("_", " ");
}

export default ResultDashboard;
