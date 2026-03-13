/**
 * Policy Engine
 *
 * Enforces permission checks, approval gates, and scope boundaries
 * before tool execution.
 */

export interface PolicyDecision {
  allowed: boolean;
  reason: string;
  requires_approval: boolean;
  approval_type?: string;
}

export interface PolicyContext {
  user_id: number;
  company_id: number;
  groups: string[];
  permissions: Record<string, boolean>;
  tool: string;
  operation: "read" | "write" | "create" | "unlink";
}

/**
 * Tools that always require approval before execution.
 */
const APPROVAL_REQUIRED_TOOLS = new Set([
  "odoo.create_draft_invoice",
  "odoo.update_record",
  "graph.create_draft_email",
  "graph.send_teams_notification",
]);

/**
 * Tools that are read-only and always allowed (subject to Odoo RBAC).
 */
const READ_ONLY_TOOLS = new Set([
  "odoo.search_partners",
  "odoo.get_invoices",
  "odoo.get_bills",
  "odoo.get_overdue_summary",
  "odoo.get_record_history",
  "odoo.get_user_context",
  "odoo.search_docs",
  "odoo.get_model_help",
  "odoo.search_sops",
  "odoo.check_permission",
]);

/**
 * Evaluate a policy decision for a tool invocation.
 */
export function evaluatePolicy(context: PolicyContext): PolicyDecision {
  // Read tools are always allowed at the policy layer
  // (Odoo RBAC still enforces at the gateway)
  if (READ_ONLY_TOOLS.has(context.tool)) {
    return {
      allowed: true,
      reason: "Read-only tool — Odoo RBAC enforced at gateway",
      requires_approval: false,
    };
  }

  // Check if tool requires approval
  if (APPROVAL_REQUIRED_TOOLS.has(context.tool)) {
    return {
      allowed: true,
      reason: "Write tool — requires user confirmation before execution",
      requires_approval: true,
      approval_type: "user_confirmation",
    };
  }

  // Check permission mapping
  const permissionKey = toolToPermission(context.tool);
  if (permissionKey && !context.permissions[permissionKey]) {
    return {
      allowed: false,
      reason: `Missing permission: ${permissionKey}`,
      requires_approval: false,
    };
  }

  return {
    allowed: true,
    reason: "Policy check passed",
    requires_approval: false,
  };
}

function toolToPermission(tool: string): string | null {
  const map: Record<string, string> = {
    "odoo.create_draft_invoice": "can_write_invoices",
    "odoo.create_activity": "can_write_partners",
    "odoo.post_message": "can_write_partners",
  };
  return map[tool] ?? null;
}
