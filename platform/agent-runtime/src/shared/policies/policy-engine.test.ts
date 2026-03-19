import { describe, it, expect } from "vitest";
import { evaluatePolicy, type PolicyContext } from "./policy-engine.js";

function makeContext(overrides: Partial<PolicyContext> = {}): PolicyContext {
  return {
    user_id: 1,
    company_id: 1,
    groups: [],
    permissions: {
      can_read_invoices: true,
      can_write_invoices: true,
      can_read_partners: true,
      can_write_partners: true,
    },
    tool: "odoo.search_partners",
    operation: "read",
    ...overrides,
  };
}

describe("evaluatePolicy", () => {
  it("allows read-only tools unconditionally", () => {
    const result = evaluatePolicy(makeContext({ tool: "odoo.search_partners" }));
    expect(result.allowed).toBe(true);
    expect(result.requires_approval).toBe(false);
  });

  it("allows all read tools", () => {
    const readTools = [
      "odoo.get_invoices",
      "odoo.get_bills",
      "odoo.get_overdue_summary",
      "odoo.get_record_history",
      "odoo.get_user_context",
      "odoo.search_docs",
      "odoo.check_permission",
    ];
    for (const tool of readTools) {
      const result = evaluatePolicy(makeContext({ tool }));
      expect(result.allowed, `${tool} should be allowed`).toBe(true);
    }
  });

  it("requires approval for write tools", () => {
    const result = evaluatePolicy(makeContext({ tool: "odoo.create_draft_invoice" }));
    expect(result.allowed).toBe(true);
    expect(result.requires_approval).toBe(true);
  });

  it("requires approval for graph tools", () => {
    const result = evaluatePolicy(makeContext({ tool: "graph.create_draft_email" }));
    expect(result.allowed).toBe(true);
    expect(result.requires_approval).toBe(true);
  });

  it("denies write tools when permission is missing", () => {
    const result = evaluatePolicy(makeContext({
      tool: "odoo.create_activity",
      permissions: { can_write_partners: false },
    }));
    expect(result.allowed).toBe(false);
    expect(result.reason).toContain("Missing permission");
  });

  it("allows write tools when permission is present", () => {
    const result = evaluatePolicy(makeContext({
      tool: "odoo.post_message",
      permissions: { can_write_partners: true },
    }));
    expect(result.allowed).toBe(true);
  });
});
