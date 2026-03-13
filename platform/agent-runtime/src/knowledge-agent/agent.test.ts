/**
 * Knowledge Agent — E2E Unit Tests
 *
 * Kapa AI equivalence: grounded retrieval, citations, confidence scoring,
 * escalation on low confidence, troubleshooting, SOP lookup.
 */

import { describe, it, expect, vi } from "vitest";
import { KnowledgeAgent, type SearchClient, type SearchResult } from "./agent.js";
import type { AgentRequest } from "../shared/contracts/types.js";

function makeRequest(message: string): AgentRequest {
  return {
    message,
    userContext: {
      user_id: 1,
      user_name: "Support Agent",
      company_id: 1,
      company_name: "IPAI Corp",
      groups: [],
      permissions: {},
    },
    sessionId: "kb-session-001",
  };
}

function makeSearchResult(overrides: Partial<SearchResult> = {}): SearchResult {
  return {
    title: "Invoice Posting Guide",
    snippet: "To post an invoice, navigate to Accounting > Invoices...",
    source: "odoo-docs/accounting/invoices.md",
    section: "Posting Invoices",
    score: 0.85,
    last_indexed: "2026-03-10T00:00:00Z",
    ...overrides,
  };
}

function createMockSearch(results: SearchResult[] = []): SearchClient {
  return {
    hybridSearch: vi.fn(async () => results),
  };
}

describe("KnowledgeAgent", () => {

  // ── Kapa-like: Grounded Retrieval with Citations ────────────

  describe("grounded retrieval (Kapa equivalent)", () => {
    it("returns citations for every result", async () => {
      const search = createMockSearch([
        makeSearchResult({ score: 0.9 }),
        makeSearchResult({ title: "Second Doc", score: 0.7 }),
      ]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.citations).toBeDefined();
      expect(result.citations!.length).toBe(2);
      expect(result.citations![0].source).toBe("odoo-docs/accounting/invoices.md");
      expect(result.citations![0].section).toBe("Posting Invoices");
    });

    it("includes freshness metadata in citations", async () => {
      const search = createMockSearch([
        makeSearchResult({ last_indexed: "2026-03-10T00:00:00Z" }),
      ]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.citations![0].last_indexed).toBe("2026-03-10T00:00:00Z");
    });

    it("includes relevance score in citations", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.92 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.citations![0].score).toBe(0.92);
    });
  });

  // ── Kapa-like: Confidence Scoring ───────────────────────────

  describe("confidence scoring", () => {
    it("returns high confidence for strong matches (score >= 0.8)", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.9 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.confidence).toBe(0.9);
      expect(result.message).toContain("high");
    });

    it("returns medium confidence for moderate matches (0.5-0.8)", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.6 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to configure withholding tax?"));

      expect(result.confidence).toBe(0.6);
      expect(result.message).toContain("medium");
    });

    it("returns low confidence for weak matches (< 0.5)", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.3 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("Why is the sky blue?"));

      expect(result.confidence).toBe(0.3);
      expect(result.message).toContain("low");
    });

    it("returns low confidence when no results found", async () => {
      const search = createMockSearch([]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("Something completely unrelated"));

      expect(result.confidence).toBe(0.1);
    });
  });

  // ── Kapa-like: Escalation on Low Confidence ─────────────────

  describe("escalation routing", () => {
    it("suggests escalation when confidence is low", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.2 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("Why did the batch job fail at 3am?"));

      expect(result.actions).toBeDefined();
      expect(result.actions!.length).toBe(1);
      expect(result.actions![0].tool).toBe("escalate");
      expect(result.actions![0].requires_confirmation).toBe(true);
    });

    it("does not suggest escalation for high confidence answers", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.9 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.actions).toBeUndefined();
    });

    it("does not suggest escalation for medium confidence answers", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.6 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to configure payment terms?"));

      expect(result.actions).toBeUndefined();
    });

    it("escalation action includes original query and citations", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.2 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("Why did reconciliation fail?"));

      const escalation = result.actions![0];
      expect(escalation.parameters.query).toBe("Why did reconciliation fail?");
      expect(escalation.parameters.citations).toBeDefined();
    });
  });

  // ── Kapa-like: Intent-Based Index Selection ─────────────────

  describe("search strategy selection", () => {
    it("uses support-resolutions index for error/traceback queries", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.8 })]);
      const agent = new KnowledgeAgent(search);
      await agent.handle(makeRequest("What does this traceback mean?"));

      expect(search.hybridSearch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ index: "support-resolutions", doc_type: "troubleshooting" }),
      );
    });

    it("uses sops-runbooks index for policy/procedure queries", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.8 })]);
      const agent = new KnowledgeAgent(search);
      await agent.handle(makeRequest("What is the SOP for vendor onboarding?"));

      expect(search.hybridSearch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ index: "sops-runbooks", doc_type: "sop" }),
      );
    });

    it("uses odoo-docs index for module/field questions", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.8 })]);
      const agent = new KnowledgeAgent(search);
      await agent.handle(makeRequest("What fields are on the account.move model?"));

      expect(search.hybridSearch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ index: "odoo-docs", doc_type: "module_doc" }),
      );
    });

    it("defaults to odoo-docs index for general questions", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.8 })]);
      const agent = new KnowledgeAgent(search);
      await agent.handle(makeRequest("How do I set up a new company?"));

      expect(search.hybridSearch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ index: "odoo-docs" }),
      );
    });

    it("applies freshness weight to search options", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.8 })]);
      const agent = new KnowledgeAgent(search);
      await agent.handle(makeRequest("How to configure taxes?"));

      expect(search.hybridSearch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ freshness_weight: 0.2 }),
      );
    });
  });

  // ── Response Contract ──────────────────────────────────────

  describe("response contract", () => {
    it("always identifies as knowledge agent", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.9 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.agent).toBe("knowledge");
    });

    it("lists knowledge tools as available", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.9 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.tools_available).toContain("odoo.search_docs");
      expect(result.tools_available).toContain("odoo.get_model_help");
      expect(result.tools_available).toContain("odoo.search_sops");
    });

    it("preserves session ID", async () => {
      const search = createMockSearch([makeSearchResult({ score: 0.9 })]);
      const agent = new KnowledgeAgent(search);
      const result = await agent.handle(makeRequest("How to post an invoice?"));

      expect(result.session_id).toBe("kb-session-001");
    });
  });
});
