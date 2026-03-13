/**
 * Odoo Web Widget Channel Adapter
 *
 * Receives messages from the Odoo backoffice web assistant widget.
 * Context-aware: receives current module, view, and record context.
 *
 * Auth: Odoo session token
 */

export interface OdooWebMessage {
  text: string;
  session_token: string;
  context: {
    model?: string;
    res_id?: number;
    view_type?: string;
    action_id?: number;
    menu_id?: number;
  };
}

export interface OdooWebConfig {
  agent_runtime_url: string;
  odoo_url: string;
}

export class OdooWebAdapter {
  private config: OdooWebConfig;

  constructor(config: OdooWebConfig) {
    this.config = config;
  }

  async handleMessage(message: OdooWebMessage) {
    // 1. Validate Odoo session and get user context
    const userContext = await this.validateSession(message.session_token);

    // 2. Enrich with current view context
    const enrichedMessage = this.enrichWithContext(message.text, message.context);

    // 3. Forward to agent runtime
    const response = await fetch(`${this.config.agent_runtime_url}/api/v1/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: enrichedMessage,
        user_context: userContext,
        session_id: message.session_token,
        odoo_context: message.context,
      }),
    });

    return response.json();
  }

  private async validateSession(token: string) {
    // In production: validate token against Odoo and extract user info
    return {
      user_id: 0,
      user_name: "unknown",
      company_id: 1,
      company_name: "Default",
      groups: [],
      permissions: {},
    };
  }

  private enrichWithContext(text: string, context: OdooWebMessage["context"]): string {
    const parts = [text];
    if (context.model) parts.push(`[Current model: ${context.model}]`);
    if (context.res_id) parts.push(`[Record ID: ${context.res_id}]`);
    if (context.view_type) parts.push(`[View: ${context.view_type}]`);
    return parts.join(" ");
  }
}
