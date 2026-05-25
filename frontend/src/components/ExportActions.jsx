import React, { useState } from "react";

function ExportActions({ plan }) {
  const [copied, setCopied] = useState(false);

  if (!plan) {
    return null;
  }

  function downloadJson() {
    downloadFile(`${slugify(plan.project_name)}.json`, JSON.stringify(plan, null, 2), "application/json");
  }

  function downloadMarkdown() {
    downloadFile(`${slugify(plan.project_name)}.md`, renderMarkdown(plan), "text/markdown");
  }

  async function copySummary() {
    const summary = `${plan.project_name}\n${plan.summary}\nDomain: ${plan.domain}\nType: ${plan.project_type}\nComplexity: ${plan.complexity}`;
    await navigator.clipboard.writeText(summary);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div className="export-actions">
      <button type="button" onClick={downloadJson}>Download JSON</button>
      <button type="button" onClick={downloadMarkdown}>Download Markdown</button>
      <button type="button" onClick={copySummary}>{copied ? "Copied" : "Copy summary"}</button>
    </div>
  );
}

function downloadFile(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function renderMarkdown(plan) {
  const lines = [
    `# ${plan.project_name}`,
    "",
    plan.summary,
    "",
    `- Domain: ${plan.domain}`,
    `- Project type: ${plan.project_type}`,
    `- Complexity: ${plan.complexity}`,
    `- Status: ${plan.status}`,
    "",
    "## Phases",
  ];

  for (const phase of plan.phases || []) {
    lines.push("", `### ${phase.id}: ${phase.name}`, phase.objective, "", `Estimated duration: ${phase.estimated_duration}`, "");
    for (const task of phase.tasks || []) {
      lines.push(`- ${task.id}: ${task.title} - ${task.description}`);
    }
  }

  appendList(lines, "Milestones", plan.milestones, (item) => `${item.id}: ${item.name} (${item.target_phase_id})`);
  appendList(lines, "Risks", plan.risks, (item) => `${item.id}: ${item.description} Mitigation: ${item.mitigation}`);
  appendList(lines, "Dependencies", plan.dependencies, (item) => `${item.source_task_id} -> ${item.target_task_id}: ${item.description}`);
  appendList(lines, "Recommendations", plan.recommendations, (item) => `${item.category}: ${item.recommendation}`);
  appendList(lines, "Warnings", plan.warnings, (item) => item);

  return `${lines.join("\n")}\n`;
}

function appendList(lines, title, items = [], renderItem) {
  if (!items.length) {
    return;
  }
  lines.push("", `## ${title}`);
  for (const item of items) {
    lines.push(`- ${renderItem(item)}`);
  }
}

function slugify(value = "project-plan") {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "project-plan";
}

export default ExportActions;
