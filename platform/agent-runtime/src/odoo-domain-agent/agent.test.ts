/**
 * Business Domain Agent — E2E Unit Tests
 *
 * SAP Joule equivalence: conversational ERP queries, role-based access,
 * cross-module data retrieval, draft creation with permission enforcement.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { BusinessDomainAgent, type OdooGatewayClient } from "./agent.js";
import { registerTools } from "../shared/contracts/tool-registry.js";
import type { AgentRequest } from "../shared/contracts/types.js";

function makeRequest(message: string, overrides: Partial<AgentRequest> = {}): AgentRequest {
  return {
    message,
    userContext: {
      user_id: 1,
      user_name: "Finance User",
      company_id: 1,
      company_name: "IPAI Corp",
      groups: ["account.group_account_invoice"],
      permissions: { can_read_invoices: true, can_write_invoices: true },
    },
    sessionId: "test-session-001",
    ...overrides,
  };
}

function createMockGateway(overrides: Record<string, unknown> = {}): OdooGatewayClient {
  return {
    call: vi.fn(async (tool: string) => {
      if (tool === "odoo.get_user_context") {
        return {
          user_id: 1,
          company_id: 1,
          permissions: { can_write_invoices: true, can_write_partners: true },
          ...overrides["user_context"] as object,
        };
      }
      if (tool === "odoo.check_permission") {
        return { allowed: overrides["permission_allowed"] ?? true };
      }
      return { records: [], total_count: 0 };
    }),
  };
}

describe("BusinessDomainAgent", () => {
  let tools = registerTools();

  // ── Joule-like: Conversational ERP Queries ──────────────────

  describe("conversational ERP queries (Joule equivalent)", () => {
    it("selects invoice tools for 'Show overdue invoices for top 20 customers'", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show overdue invoices for top 20 customers"));

      expect(result.agent).toBe("business");
      expect(result.tools_available).toContain("odoo.get_invoices");
      expect(result.tools_available).toContain("odoo.get_overdue_summary");
      expect(result.tools_available).toContain("odoo.search_partners");
    });

    it("selects bill tools for vendor bill queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("What vendor bills are pending payment?"));

      expect(result.tools_available).toContain("odoo.get_bills");
    });

    it("selects partner tools for customer/vendor searches", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Find all customers in Manila"));

      expect(result.tools_available).toContain("odoo.search_partners");
    });

    it("selects history tools for chatter/log queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show me the history of invoice INV-2024-0142"));

      expect(result.tools_available).toContain("odoo.get_record_history");
      expect(result.tools_available).toContain("odoo.get_invoices");
    });

    it("falls back to all read tools for ambiguous queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show me a summary"));

      // Should default to all get_ tools
      expect(result.tools_available.every((t: string) => t.startsWith("odoo.get_"))).toBe(true);
      expect(result.tools_available.length).toBeGreaterThan(0);
    });
  });

  // ── Joule-like: Role-Based Access Enforcement ───────────────

  describe("role-based security (Joule identity propagation equivalent)", () => {
    it("always fetches user context before processing", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      await agent.handle(makeRequest("Show invoices"));

      expect(gateway.call).toHaveBeenCalledWith("odoo.get_user_context", {});
    });

    it("checks permission before write operations", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      await agent.handle(makeRequest("Create a draft invoice for customer 42"));

      expect(gateway.call).toHaveBeenCalledWith("odoo.check_permission", {
        model: "account.move",
        operation: "write",
      });
    });

    it("denies write when permission check fails", async () => {
      const gateway = createMockGateway({ permission_allowed: false });
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Create a draft invoice for customer 42"));

      expect(result.message).toContain("Permission denied");
      expect(result.confidence).toBe(1);
    });

    it("allows write when permission check passes", async () => {
      const gateway = createMockGateway({ permission_allowed: true });
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Create a draft invoice for customer 42"));

      expect(result.message).not.toContain("Permission denied");
      expect(result.tools_available).toContain("odoo.create_draft_invoice");
    });

    it("does not check permissions for read-only queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      await agent.handle(makeRequest("Show overdue invoices"));

      // Should only call get_user_context, not check_permission
      const calls = (gateway.call as ReturnType<typeof vi.fn>).mock.calls;
      const permCalls = calls.filter(([tool]: string[]) => tool === "odoo.check_permission");
      expect(permCalls).toHaveLength(0);
    });
  });

  // ── Joule-like: Multi-Module Queries ────────────────────────

  describe("cross-module data retrieval", () => {
    it("combines invoice + customer tools for receivable queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show receivable balance by customer"));

      expect(result.tools_available).toContain("odoo.get_invoices");
      expect(result.tools_available).toContain("odoo.search_partners");
    });

    it("combines bill + vendor tools for payable queries", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show payable balance by vendor"));

      expect(result.tools_available).toContain("odoo.get_bills");
      expect(result.tools_available).toContain("odoo.search_partners");
    });

    it("selects activity creation for follow-up requests", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Create a follow-up task for this invoice"));

      expect(result.tools_available).toContain("odoo.create_activity");
    });
  });

  // ── Response Contract ──────────────────────────────────────

  describe("response contract", () => {
    it("always includes agent identifier", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show invoices"));

      expect(result.agent).toBe("business");
    });

    it("always includes session ID for continuity", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show invoices"));

      expect(result.session_id).toBe("test-session-001");
    });

    it("includes user context data in response", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show invoices"));

      expect(result.data).toBeDefined();
      expect((result.data as Record<string, unknown>).user_context).toBeDefined();
    });

    it("lists available tools in response", async () => {
      const gateway = createMockGateway();
      const agent = new BusinessDomainAgent(gateway, tools);
      const result = await agent.handle(makeRequest("Show invoices"));

      expect(result.tools_available.length).toBeGreaterThan(0);
    });
  });
});
