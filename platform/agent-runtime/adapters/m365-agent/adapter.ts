/**
 * Microsoft 365 Copilot Channel Adapter
 *
 * Receives messages from Microsoft 365 Copilot custom engine agent
 * and routes them to the agent runtime. Returns adaptive cards
 * and text responses to the M365 surface.
 *
 * SDK: Microsoft 365 Agents SDK
 * Auth: Azure AD / Entra ID (OAuth 2.0 on-behalf-of)
 */

export interface M365AgentConfig {
  app_id: string;
  tenant_id: string;
  agent_runtime_url: string;
}

export interface M365Message {
  text: string;
  user_id: string;
  tenant_id: string;
  conversation_id: string;
  channel: "copilot" | "teams" | "outlook";
}

export interface AdaptiveCardResponse {
  type: "AdaptiveCard";
  version: string;
  body: unknown[];
  actions?: unknown[];
}

export class M365AgentAdapter {
  private config: M365AgentConfig;

  constructor(config: M365AgentConfig) {
    this.config = config;
  }

  /**
   * Handle incoming message from M365 Copilot.
   * Maps M365 identity to Odoo user context and forwards to agent runtime.
   */
  async handleMessage(message: M365Message): Promise<AdaptiveCardResponse | string> {
    // 1. Resolve M365 user to Odoo user context
    const userContext = await this.resolveUserContext(message.user_id, message.tenant_id);

    // 2. Forward to agent runtime
    const response = await fetch(`${this.config.agent_runtime_url}/api/v1/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message.text,
        user_context: userContext,
        session_id: message.conversation_id,
      }),
    });

    const result = await response.json();

    // 3. Format response for M365 surface
    if (result.data && typeof result.data === "object") {
      return this.formatAdaptiveCard(result);
    }

    return result.message;
  }

  private async resolveUserContext(userId: string, tenantId: string) {
    // In production: call Microsoft Graph to get user profile,
    // then map to Odoo user via email/UPN matching
    return {
      user_id: 0,
      user_name: userId,
      company_id: 1,
      company_name: "Default",
      groups: [],
      permissions: {},
      m365_tenant_id: tenantId,
    };
  }

  private formatAdaptiveCard(result: Record<string, unknown>): AdaptiveCardResponse {
    return {
      type: "AdaptiveCard",
      version: "1.5",
      body: [
        {
          type: "TextBlock",
          text: result.message,
          wrap: true,
        },
      ],
    };
  }
}
