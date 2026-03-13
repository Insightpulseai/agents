/**
 * Knowledge Agent
 *
 * Handles documentation retrieval, SOP lookup, troubleshooting,
 * and contextual help with citations and confidence scoring.
 */

import type { AgentRequest, AgentResponse, Citation } from "../shared/contracts/types.js";

export interface SearchClient {
  hybridSearch(query: string, options: SearchOptions): Promise<SearchResult[]>;
}

export interface SearchOptions {
  index: string;
  doc_type?: string;
  module?: string;
  limit?: number;
  freshness_weight?: number;
}

export interface SearchResult {
  title: string;
  snippet: string;
  source: string;
  section: string;
  score: number;
  last_indexed: string;
}

type ConfidenceLevel = "high" | "medium" | "low";

export class KnowledgeAgent {
  private search: SearchClient;

  constructor(search: SearchClient) {
    this.search = search;
  }

  async handle(request: AgentRequest): Promise<AgentResponse> {
    // Step 1: Determine search strategy
    const strategy = this.classifyKnowledgeIntent(request.message);

    // Step 2: Execute search
    const results = await this.search.hybridSearch(request.message, {
      index: strategy.index,
      doc_type: strategy.doc_type,
      limit: 5,
      freshness_weight: 0.2,
    });

    // Step 3: Score confidence
    const confidence = this.scoreConfidence(results);

    // Step 4: Build citations
    const citations: Citation[] = results.map((r) => ({
      source: r.source,
      section: r.section,
      snippet: r.snippet,
      score: r.score,
      last_indexed: r.last_indexed,
    }));

    // Step 5: If low confidence, suggest escalation
    if (confidence.level === "low") {
      return {
        agent: "knowledge",
        confidence: confidence.score,
        message: `I found some potentially relevant information, but my confidence is low. Consider consulting the implementation team.`,
        tools_available: ["odoo.search_docs", "odoo.get_model_help", "odoo.search_sops"],
        session_id: request.sessionId,
        citations,
        actions: [{
          tool: "escalate",
          label: "Escalate to support",
          description: "Forward this question to the implementation team",
          parameters: { query: request.message, citations },
          requires_confirmation: true,
        }],
      };
    }

    return {
      agent: "knowledge",
      confidence: confidence.score,
      message: `Found ${results.length} relevant sources with ${confidence.level} confidence.`,
      tools_available: ["odoo.search_docs", "odoo.get_model_help", "odoo.search_sops"],
      session_id: request.sessionId,
      citations,
    };
  }

  private classifyKnowledgeIntent(message: string): { index: string; doc_type?: string } {
    const lower = message.toLowerCase();

    if (lower.includes("traceback") || lower.includes("error") || lower.includes("failed")) {
      return { index: "support-resolutions", doc_type: "troubleshooting" };
    }
    if (lower.includes("sop") || lower.includes("policy") || lower.includes("procedure")) {
      return { index: "sops-runbooks", doc_type: "sop" };
    }
    if (lower.includes("module") || lower.includes("field") || lower.includes("model")) {
      return { index: "odoo-docs", doc_type: "module_doc" };
    }
    return { index: "odoo-docs" };
  }

  private scoreConfidence(results: SearchResult[]): { level: ConfidenceLevel; score: number } {
    if (results.length === 0) {
      return { level: "low", score: 0.1 };
    }

    const topScore = results[0].score;

    if (topScore >= 0.8) return { level: "high", score: topScore };
    if (topScore >= 0.5) return { level: "medium", score: topScore };
    return { level: "low", score: topScore };
  }
}
