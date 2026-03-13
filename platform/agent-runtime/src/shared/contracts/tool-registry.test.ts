import { describe, it, expect } from "vitest";
import { registerTools } from "./tool-registry.js";

describe("registerTools", () => {
  const tools = registerTools();

  it("registers all expected read tools", () => {
    const readTools = [
      "odoo.search_partners",
      "odoo.get_invoices",
      "odoo.get_bills",
      "odoo.get_overdue_summary",
      "odoo.get_record_history",
      "odoo.get_user_context",
    ];
    for (const name of readTools) {
      expect(tools[name]).toBeDefined();
      expect(tools[name].category).toBe("read");
    }
  });

  it("registers all expected write tools", () => {
    const writeTools = [
      "odoo.create_draft_invoice",
      "odoo.create_activity",
      "odoo.post_message",
    ];
    for (const name of writeTools) {
      expect(tools[name]).toBeDefined();
      expect(tools[name].category).toBe("write");
    }
  });

  it("registers knowledge tools", () => {
    expect(tools["odoo.search_docs"]).toBeDefined();
    expect(tools["odoo.search_docs"].category).toBe("knowledge");
  });

  it("registers policy tools", () => {
    expect(tools["odoo.check_permission"]).toBeDefined();
    expect(tools["odoo.check_permission"].category).toBe("policy");
    expect(tools["odoo.dry_run"]).toBeDefined();
    expect(tools["odoo.dry_run"].category).toBe("policy");
  });

  it("requires permission for write tools that need it", () => {
    expect(tools["odoo.create_draft_invoice"].requires_permission).toBe("can_write_invoices");
  });

  it("does not require permission for read tools", () => {
    expect(tools["odoo.search_partners"].requires_permission).toBeUndefined();
  });

  it("has descriptions for all tools", () => {
    for (const [name, tool] of Object.entries(tools)) {
      expect(tool.description, `${name} should have a description`).toBeTruthy();
    }
  });
});
