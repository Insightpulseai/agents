/**
 * Router Agent
 *
 * Classifies user intent and routes to the appropriate domain agent.
 */

import type { AgentRequest, AgentResponse, ToolRegistry } from "../shared/contracts/types.js";

export type AgentType = "business" | "knowledge" | "workflow" | "developer";

export interface RouteResult {
  agent: AgentType;
  confidence: number;
  reasoning: string;
}

export interface RouterConfig {
  route(request: AgentRequest & { tools: ToolRegistry }): Promise<AgentResponse>;
}

/**
 * Intent classification signals for routing.
 */
const INTENT_SIGNALS: Record<AgentType, string[]> = {
  business: [
    "invoice", "bill", "payment", "customer", "vendor", "partner",
    "sales order", "purchase order", "project", "task", "stock",
    "inventory", "overdue", "receivable", "payable", "kpi", "dashboard",
  ],
  knowledge: [
    "how to", "what is", "explain", "documentation", "help", "guide",
    "sop", "policy", "troubleshoot", "error", "traceback", "why did",
    "what does", "module", "field", "view",
  ],
  workflow: [
    "follow up", "follow-up", "send email", "notify", "approve",
    "create and send", "draft email", "remind", "escalate",
    "onboard", "process", "workflow",
  ],
  developer: [
    "code", "addon", "module", "manifest", "xml", "view", "model",
    "migration", "test", "pr", "pull request", "commit", "branch",
    "orm", "domain", "computed field", "onchange",
  ],
};

/**
 * Classify intent based on keyword signals.
 * In production, this would use an LLM-based classifier.
 */
export function classifyIntent(message: string): RouteResult {
  const lower = message.toLowerCase();
  const scores: Record<AgentType, number> = {
    business: 0,
    knowledge: 0,
    workflow: 0,
    developer: 0,
  };

  for (const [agent, signals] of Object.entries(INTENT_SIGNALS)) {
    for (const signal of signals) {
      if (lower.includes(signal)) {
        scores[agent as AgentType]++;
      }
    }
  }

  const entries = Object.entries(scores) as [AgentType, number][];
  entries.sort((a, b) => b[1] - a[1]);

  const [topAgent, topScore] = entries[0];
  const totalSignals = entries.reduce((sum, [, s]) => sum + s, 0);

  return {
    agent: topScore > 0 ? topAgent : "business",
    confidence: totalSignals > 0 ? topScore / totalSignals : 0,
    reasoning: topScore > 0
      ? `Matched ${topScore} signals for ${topAgent} agent`
      : "No strong signals, defaulting to business agent",
  };
}

export function createRouter(): RouterConfig {
  return {
    async route(request) {
      const classification = classifyIntent(request.message);

      // In production, each agent type would have its own handler
      // For now, return the classification result as the response
      return {
        agent: classification.agent,
        confidence: classification.confidence,
        message: `Routed to ${classification.agent} agent: ${classification.reasoning}`,
        tools_available: Object.keys(request.tools),
        session_id: request.sessionId,
      };
    },
  };
}
