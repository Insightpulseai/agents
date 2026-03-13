/**
 * Workflow Agent — E2E Unit Tests
 *
 * SAP Joule equivalence: cross-system workflows (Odoo + Outlook + Teams),
 * approval gates, multi-step execution, workflow state persistence.
 */

import { describe, it, expect, vi } from "vitest";
import { WorkflowAgent, type WorkflowStore, type WorkflowState } from "./agent.js";
import type { AgentRequest } from "../shared/contracts/types.js";

function makeRequest(message: string): AgentRequest {
  return {
    message,
    userContext: {
      user_id: 1,
      user_name: "Finance Manager",
      company_id: 1,
      company_name: "IPAI Corp",
      groups: ["account.group_account_manager"],
      permissions: { can_read_invoices: true, can_write_invoices: true },
    },
    sessionId: "wf-session-001",
  };
}

function createMockStore(): WorkflowStore {
  const storage = new Map<string, WorkflowState>();
  return {
    save: vi.fn(async (state) => { storage.set(state.workflow_id, state); }),
    load: vi.fn(async (id) => storage.get(id) ?? null),
  };
}

describe("WorkflowAgent", () => {

  // ── Joule-like: Invoice Follow-Up Workflow ──────────────────

  describe("invoice follow-up workflow (Joule cross-system equivalent)", () => {
    it("detects invoice follow-up intent", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on overdue invoice INV-2024-0142"));

      expect(result.message).toContain("invoice_followup");
    });

    it("builds 6-step cross-system workflow", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on this invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.steps).toHaveLength(6);
    });

    it("includes Odoo read steps (invoice, history, customer)", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on this invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const tools = workflow.steps.map((s) => s.tool);
      expect(tools).toContain("odoo.get_invoices");
      expect(tools).toContain("odoo.get_record_history");
      expect(tools).toContain("odoo.search_partners");
    });

    it("includes M365 cross-system steps (email draft, Teams notification)", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on this invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const tools = workflow.steps.map((s) => s.tool);
      expect(tools).toContain("graph.create_draft_email");
      expect(tools).toContain("graph.send_teams_notification");
    });

    it("includes Odoo write step (create activity)", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on this invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const tools = workflow.steps.map((s) => s.tool);
      expect(tools).toContain("odoo.create_activity");
    });

    it("requires approval for email draft step only", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on this invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const approvalSteps = workflow.steps.filter((s) => s.requires_approval);
      expect(approvalSteps).toHaveLength(1);
      expect(approvalSteps[0].tool).toBe("graph.create_draft_email");
    });
  });

  // ── Joule-like: Vendor Onboarding Workflow ──────────────────

  describe("vendor onboarding workflow", () => {
    it("detects vendor onboarding intent", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Onboard a new vendor for office supplies"));

      expect(result.message).toContain("vendor_onboarding");
    });

    it("builds 4-step onboarding workflow", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Onboard a new vendor"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.steps).toHaveLength(4);
    });

    it("requires approval for vendor creation", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Onboard a new vendor"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const createStep = workflow.steps.find((s) => s.id === "create_vendor");
      expect(createStep?.requires_approval).toBe(true);
    });

    it("includes Teams notification step", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Onboard a new vendor"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      const tools = workflow.steps.map((s) => s.tool);
      expect(tools).toContain("graph.send_teams_notification");
    });
  });

  // ── Joule-like: Expense Approval Workflow ───────────────────

  describe("expense approval workflow", () => {
    it("detects expense/approval intent", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Submit expense report for approval"));

      expect(result.message).toContain("expense_approval");
    });
  });

  // ── Workflow State Contract ─────────────────────────────────

  describe("workflow state and plan contract", () => {
    it("generates unique workflow ID", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const r1 = await agent.handle(makeRequest("Follow up on invoice"));
      const r2 = await agent.handle(makeRequest("Follow up on another invoice"));

      const wf1 = (r1.data as Record<string, unknown>).workflow as WorkflowState;
      const wf2 = (r2.data as Record<string, unknown>).workflow as WorkflowState;
      expect(wf1.workflow_id).not.toBe(wf2.workflow_id);
    });

    it("all steps start in pending status", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.steps.every((s) => s.status === "pending")).toBe(true);
    });

    it("workflow starts at step 0", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.current_step).toBe(0);
      expect(workflow.status).toBe("pending");
    });

    it("returns suggested actions matching workflow steps", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on invoice"));

      expect(result.actions).toBeDefined();
      expect(result.actions!.length).toBe(6);
      expect(result.actions!.some((a) => a.requires_confirmation)).toBe(true);
    });

    it("falls back to generic workflow for unrecognized patterns", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Do something complex"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.name).toBe("generic");
      expect(workflow.steps).toHaveLength(1);
    });

    it("includes timestamps", async () => {
      const store = createMockStore();
      const agent = new WorkflowAgent(store);
      const result = await agent.handle(makeRequest("Follow up on invoice"));

      const workflow = (result.data as Record<string, unknown>).workflow as WorkflowState;
      expect(workflow.created_at).toBeTruthy();
      expect(workflow.updated_at).toBeTruthy();
    });
  });
});
