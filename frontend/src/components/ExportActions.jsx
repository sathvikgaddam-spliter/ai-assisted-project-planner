import React, { useState } from "react";

function ExportActions({ apiBaseUrl, plan, projectDescription }) {
  const [copied, setCopied] = useState(false);
  const [promptZipLoading, setPromptZipLoading] = useState(false);
  const [agentZipLoading, setAgentZipLoading] = useState(false);
  const [zipError, setZipError] = useState("");

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

  async function downloadPromptPackZip() {
    setPromptZipLoading(true);
    setZipError("");

    try {
      await downloadZipFromEndpoint(
        `${apiBaseUrl}/generate-plan-zip`,
        projectDescription || plan.description,
        "project-plan.zip",
        "Unable to download prompt pack ZIP.",
      );
    } catch (requestError) {
      setZipError(requestError.message || "Unable to download prompt pack ZIP.");
    } finally {
      setPromptZipLoading(false);
    }
  }

  async function downloadCodingAgentZip() {
    setAgentZipLoading(true);
    setZipError("");

    try {
      await downloadZipFromEndpoint(
        `${apiBaseUrl}/generate-coding-agent-zip`,
        projectDescription || plan.description,
        "coding-agent-job.zip",
        "Unable to download coding agent ZIP.",
      );
    } catch (requestError) {
      setZipError(requestError.message || "Unable to download coding agent ZIP.");
    } finally {
      setAgentZipLoading(false);
    }
  }

  return (
    <div className="export-actions-wrap">
      <div className="export-actions">
        <button type="button" onClick={downloadJson}>Download JSON</button>
        <button type="button" onClick={downloadMarkdown}>Download Markdown</button>
        <button type="button" onClick={downloadPromptPackZip} disabled={promptZipLoading}>
          {promptZipLoading ? "Preparing ZIP" : "Download Prompt Pack ZIP"}
        </button>
        <button type="button" onClick={downloadCodingAgentZip} disabled={agentZipLoading}>
          {agentZipLoading ? "Preparing Agent ZIP" : "Download Coding Agent + Specs ZIP"}
        </button>
        <button type="button" onClick={copySummary}>{copied ? "Copied" : "Copy summary"}</button>
      </div>
      {zipError && <div className="export-error">{zipError}</div>}
    </div>
  );
}

async function downloadZipFromEndpoint(endpoint, projectDescription, fallbackFilename, defaultErrorMessage) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ project_description: projectDescription }),
  });

  if (!response.ok) {
    let message = defaultErrorMessage;
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch {
      // Keep the generic download error when the response is not JSON.
    }
    throw new Error(message);
  }

  const blob = await response.blob();
  downloadBlob(filenameFromResponse(response) || fallbackFilename, blob);
}

function downloadFile(filename, content, type) {
  const blob = new Blob([content], { type });
  downloadBlob(filename, blob);
}

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function filenameFromResponse(response) {
  const disposition = response.headers.get("content-disposition") || "";
  const match = disposition.match(/filename="?([^"]+)"?/i);
  return match ? match[1] : "";
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
