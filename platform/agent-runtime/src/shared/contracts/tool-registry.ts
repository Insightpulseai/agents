/**
 * Tool Registry
 *
 * Registers all available tools for the agent runtime.
 * Tools are loaded from schema definitions and bound to gateway clients.
 */

import type { ToolDefinition, ToolRegistry } from "./types.js";

/**
 * Register all Odoo gateway tools.
 * In production, these would be loaded from the gateway-tools.json schema
 * and bound to actual HTTP clients.
 */
export function registerTools(): ToolRegistry {
  const tools: ToolRegistry = {};

  // Read tools
  registerTool(tools, {
    name: "odoo.search_partners",
    description: "Search customers, vendors, or contacts by criteria.",
    parameters: { query: "string", partner_type: "string", limit: "number" },
    returns: { records: "array", total_count: "number" },
    category: "read",
  });

  registerTool(tools, {
    name: "odoo.get_invoices",
    description: "Fetch customer invoices with optional filters.",
    parameters: { state: "string", partner_id: "number", overdue_only: "boolean" },
    returns: { records: "array", total_count: "number", summary: "object" },
    category: "read",
  });

  registerTool(tools, {
    name: "odoo.get_bills",
    description: "Fetch vendor bills with optional filters.",
    parameters: { state: "string", partner_id: "number", overdue_only: "boolean" },
    returns: { records: "array", total_count: "number", summary: "object" },
    category: "read",
  });

  registerTool(tools, {
    name: "odoo.get_overdue_summary",
    description: "Get overdue invoice/bill analysis grouped by customer or vendor.",
    parameters: { type: "string", group_by: "string", limit: "number" },
    returns: { groups: "array", total_overdue: "number" },
    category: "read",
  });

  registerTool(tools, {
    name: "odoo.get_record_history",
    description: "Fetch chatter messages and tracking for a record.",
    parameters: { model: "string", res_id: "number" },
    returns: { messages: "array" },
    category: "read",
  });

  registerTool(tools, {
    name: "odoo.get_user_context",
    description: "Fetch current user permissions, company, and context.",
    parameters: {},
    returns: { user_id: "number", company_id: "number", permissions: "object" },
    category: "read",
  });

  // Write tools
  registerTool(tools, {
    name: "odoo.create_draft_invoice",
    description: "Create a customer invoice in draft state.",
    parameters: { partner_id: "number", lines: "array" },
    returns: { id: "number", name: "string", amount_total: "number" },
    category: "write",
    requires_permission: "can_write_invoices",
  });

  registerTool(tools, {
    name: "odoo.create_activity",
    description: "Schedule an activity on any record.",
    parameters: { model: "string", res_id: "number", summary: "string" },
    returns: { id: "number" },
    category: "write",
  });

  registerTool(tools, {
    name: "odoo.post_message",
    description: "Post a message to the chatter of any record.",
    parameters: { model: "string", res_id: "number", body: "string" },
    returns: { id: "number" },
    category: "write",
  });

  // Knowledge tools
  registerTool(tools, {
    name: "odoo.search_docs",
    description: "Search module documentation and help content.",
    parameters: { query: "string", module: "string", doc_type: "string" },
    returns: { results: "array" },
    category: "knowledge",
  });

  // Policy tools
  registerTool(tools, {
    name: "odoo.check_permission",
    description: "Verify if the current user can perform an action.",
    parameters: { model: "string", operation: "string" },
    returns: { allowed: "boolean", reason: "string" },
    category: "policy",
  });

  registerTool(tools, {
    name: "odoo.dry_run",
    description: "Preview the result of a write operation without executing.",
    parameters: { tool: "string", parameters: "object" },
    returns: { preview: "object", validation_errors: "array" },
    category: "policy",
  });

  return tools;
}

function registerTool(registry: ToolRegistry, tool: ToolDefinition): void {
  registry[tool.name] = tool;
}
