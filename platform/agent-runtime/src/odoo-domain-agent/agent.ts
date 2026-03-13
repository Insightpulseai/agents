/**
 * Business Domain Agent
 *
 * Handles ERP/CRM/finance/project queries and actions against Odoo.
 * All operations go through the Odoo Agent Gateway — no direct model access.
 */

import type { AgentRequest, AgentResponse, ToolRegistry } from "../shared/contracts/types.js";

export interface OdooGatewayClient {
  call(tool: string, params: Record<string, unknown>): Promise<unknown>;
}

const FINANCE_TOOLS = [
  "odoo.search_partners",
  "odoo.get_invoices",
  "odoo.get_bills",
  "odoo.get_overdue_summary",
  "odoo.get_record_history",
  "odoo.get_user_context",
  "odoo.create_draft_invoice",
  "odoo.create_activity",
  "odoo.post_message",
];

export class BusinessDomainAgent {
  private gateway: OdooGatewayClient;
  private tools: ToolRegistry;

  constructor(gateway: OdooGatewayClient, tools: ToolRegistry) {
    this.gateway = gateway;
    this.tools = tools;
  }

  async handle(request: AgentRequest): Promise<AgentResponse> {
    // Step 1: Verify user context and permissions
    const userContext = await this.gateway.call("odoo.get_user_context", {});

    // Step 2: Determine which tools are needed based on the message
    const selectedTools = this.selectTools(request.message);

    // Step 3: Check permissions for write tools
    for (const tool of selectedTools) {
      const def = this.tools[tool];
      if (def?.category === "write" && def.requires_permission) {
        const permCheck = await this.gateway.call("odoo.check_permission", {
          model: this.toolToModel(tool),
          operation: "write",
        });
        if (!(permCheck as { allowed: boolean }).allowed) {
          return {
            agent: "business",
            confidence: 1,
            message: `Permission denied: you do not have write access for this operation.`,
            tools_available: selectedTools,
            session_id: request.sessionId,
          };
        }
      }
    }

    // Step 4: Execute tool chain
    // In production, this would use LLM-driven tool selection and chaining.
    // This scaffolding shows the permission-checked, gateway-mediated pattern.
    return {
      agent: "business",
      confidence: 0.9,
      message: `Business Domain Agent ready. Selected tools: ${selectedTools.join(", ")}`,
      tools_available: selectedTools,
      session_id: request.sessionId,
      data: { user_context: userContext },
    };
  }

  private selectTools(message: string): string[] {
    const lower = message.toLowerCase();
    const selected: string[] = [];

    if (lower.includes("invoice") || lower.includes("receivable")) {
      selected.push("odoo.get_invoices");
    }
    if (lower.includes("bill") || lower.includes("payable")) {
      selected.push("odoo.get_bills");
    }
    if (lower.includes("overdue")) {
      selected.push("odoo.get_overdue_summary");
    }
    if (lower.includes("customer") || lower.includes("vendor") || lower.includes("partner")) {
      selected.push("odoo.search_partners");
    }
    if (lower.includes("history") || lower.includes("chatter") || lower.includes("log")) {
      selected.push("odoo.get_record_history");
    }
    if (lower.includes("follow") || lower.includes("task") || lower.includes("activity")) {
      selected.push("odoo.create_activity");
    }
    if (lower.includes("draft") && lower.includes("invoice")) {
      selected.push("odoo.create_draft_invoice");
    }

    return selected.length > 0 ? selected : FINANCE_TOOLS.filter((t) => t.startsWith("odoo.get_"));
  }

  private toolToModel(tool: string): string {
    const modelMap: Record<string, string> = {
      "odoo.create_draft_invoice": "account.move",
      "odoo.create_activity": "mail.activity",
      "odoo.post_message": "mail.message",
    };
    return modelMap[tool] ?? "unknown";
  }
}
