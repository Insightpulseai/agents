/**
 * GitHub Copilot Channel Adapter
 *
 * Receives messages from GitHub Copilot SDK extension.
 * Operates in IDE chat, CLI, and PR review contexts.
 * Scoped to Odoo addon development patterns.
 *
 * SDK: GitHub Copilot SDK (technical preview)
 * Auth: GitHub OAuth
 */

export interface GitHubCopilotMessage {
  text: string;
  github_user: string;
  context: {
    repo?: string;
    file_path?: string;
    pr_number?: number;
    branch?: string;
    selection?: string;
    surface: "ide_chat" | "cli" | "pr_review";
  };
}

export interface GitHubCopilotConfig {
  agent_runtime_url: string;
  github_app_id: string;
}

export class GitHubCopilotAdapter {
  private config: GitHubCopilotConfig;

  constructor(config: GitHubCopilotConfig) {
    this.config = config;
  }

  async handleMessage(message: GitHubCopilotMessage) {
    // 1. Map GitHub user to developer context
    const userContext = {
      user_id: 0,
      user_name: message.github_user,
      company_id: 1,
      company_name: "Development",
      groups: ["developer"],
      permissions: { can_read_repos: true },
    };

    // 2. Enrich with repo/file context
    const enrichedMessage = this.enrichWithRepoContext(message.text, message.context);

    // 3. Forward to agent runtime (developer agent)
    const response = await fetch(`${this.config.agent_runtime_url}/api/v1/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: enrichedMessage,
        user_context: userContext,
        session_id: `gh-${message.github_user}-${Date.now()}`,
        github_context: message.context,
        force_agent: "developer",
      }),
    });

    return response.json();
  }

  private enrichWithRepoContext(text: string, context: GitHubCopilotMessage["context"]): string {
    const parts = [text];
    if (context.repo) parts.push(`[Repo: ${context.repo}]`);
    if (context.file_path) parts.push(`[File: ${context.file_path}]`);
    if (context.pr_number) parts.push(`[PR: #${context.pr_number}]`);
    if (context.branch) parts.push(`[Branch: ${context.branch}]`);
    if (context.selection) parts.push(`[Selected code: ${context.selection}]`);
    return parts.join(" ");
  }
}
