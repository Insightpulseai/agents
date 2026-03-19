/**
 * Core type definitions for the Odoo Copilot agent runtime.
 */

export interface UserContext {
  user_id: number;
  user_name: string;
  company_id: number;
  company_name: string;
  groups: string[];
  permissions: Record<string, boolean>;
}

export interface AgentRequest {
  message: string;
  userContext: UserContext;
  sessionId: string;
}

export interface AgentResponse {
  agent: string;
  confidence: number;
  message: string;
  tools_available: string[];
  session_id: string;
  data?: unknown;
  citations?: Citation[];
  actions?: SuggestedAction[];
}

export interface Citation {
  source: string;
  section: string;
  snippet: string;
  score: number;
  last_indexed: string;
}

export interface SuggestedAction {
  tool: string;
  label: string;
  description: string;
  parameters: Record<string, unknown>;
  requires_confirmation: boolean;
}

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  returns: Record<string, unknown>;
  category: "read" | "write" | "knowledge" | "policy";
  requires_permission?: string;
}

export type ToolRegistry = Record<string, ToolDefinition>;

export interface TraceContext {
  trace_id: string;
  span_id: string;
  parent_span_id?: string;
  timestamp: string;
  service: string;
}

export interface AuditEvent {
  trace_id: string;
  user_id: number;
  company_id: number;
  tool: string;
  operation: string;
  input_summary: string;
  output_summary: string;
  duration_ms: number;
  timestamp: string;
  success: boolean;
  error?: string;
}
