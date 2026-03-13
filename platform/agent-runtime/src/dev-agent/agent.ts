/**
 * Developer Agent
 *
 * Handles Odoo addon development assistance: code generation,
 * PR review, migration help, manifest validation, and test generation.
 */

import type { AgentRequest, AgentResponse } from "../shared/contracts/types.js";

export type DevTaskType =
  | "scaffold_addon"
  | "generate_view"
  | "generate_model"
  | "generate_test"
  | "review_pr"
  | "validate_manifest"
  | "migrate_version"
  | "explain_orm"
  | "general";

export class DeveloperAgent {
  async handle(request: AgentRequest): Promise<AgentResponse> {
    const taskType = this.classifyDevTask(request.message);

    return {
      agent: "developer",
      confidence: 0.85,
      message: `Developer Agent ready for task: ${taskType}`,
      tools_available: this.getToolsForTask(taskType),
      session_id: request.sessionId,
      data: {
        task_type: taskType,
        odoo_version: "19.0",
        conventions: {
          module_prefix: "ipai_",
          view_mode_list: "list",
          manifest_version: "19.0.1.0.0",
        },
      },
    };
  }

  private classifyDevTask(message: string): DevTaskType {
    const lower = message.toLowerCase();

    if (lower.includes("scaffold") || lower.includes("new addon") || lower.includes("new module")) return "scaffold_addon";
    if (lower.includes("view") || lower.includes("xml") || lower.includes("form") || lower.includes("list")) return "generate_view";
    if (lower.includes("model") || lower.includes("class") || lower.includes("field")) return "generate_model";
    if (lower.includes("test")) return "generate_test";
    if (lower.includes("pr") || lower.includes("review") || lower.includes("pull request")) return "review_pr";
    if (lower.includes("manifest") || lower.includes("__manifest__")) return "validate_manifest";
    if (lower.includes("migrate") || lower.includes("upgrade") || lower.includes("version")) return "migrate_version";
    if (lower.includes("orm") || lower.includes("domain") || lower.includes("computed")) return "explain_orm";
    return "general";
  }

  private getToolsForTask(task: DevTaskType): string[] {
    const toolMap: Record<DevTaskType, string[]> = {
      scaffold_addon: ["github.create_files", "github.create_pr"],
      generate_view: ["github.read_file", "github.create_files"],
      generate_model: ["github.read_file", "github.create_files"],
      generate_test: ["github.read_file", "github.create_files"],
      review_pr: ["github.get_pr", "github.get_diff", "github.post_review"],
      validate_manifest: ["github.read_file"],
      migrate_version: ["github.read_file", "github.create_files", "github.create_pr"],
      explain_orm: ["odoo.search_docs", "odoo.get_model_help"],
      general: ["github.read_file", "odoo.search_docs"],
    };
    return toolMap[task];
  }
}
