/**
 * Developer Agent — E2E Unit Tests
 *
 * GitHub Copilot equivalence: addon scaffolding, PR review, migration,
 * manifest validation, ORM assistance, Odoo 19 conventions.
 */

import { describe, it, expect } from "vitest";
import { DeveloperAgent } from "./agent.js";
import type { AgentRequest } from "../shared/contracts/types.js";

function makeRequest(message: string): AgentRequest {
  return {
    message,
    userContext: {
      user_id: 1,
      user_name: "Odoo Developer",
      company_id: 1,
      company_name: "IPAI Corp",
      groups: ["developer"],
      permissions: {},
    },
    sessionId: "dev-session-001",
  };
}

describe("DeveloperAgent", () => {

  // ── Copilot-like: Task Classification ───────────────────────

  describe("task classification (Copilot equivalent)", () => {
    it("classifies addon scaffolding requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Scaffold a new addon for expense tracking"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("scaffold_addon");
    });

    it("classifies view generation requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Create a kanban view with status columns"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("generate_view");
    });

    it("classifies model generation from field mentions", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Add a new field to the invoice class"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("generate_model");
    });

    it("classifies test generation requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Generate unit test cases for the expense feature"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("generate_test");
    });

    it("classifies PR review requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Review PR #42 for security concerns"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("review_pr");
    });

    it("classifies manifest validation requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Validate __manifest__.py dependencies"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("validate_manifest");
    });

    it("classifies migration requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Migrate this addon to upgrade compatibility"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("migrate_version");
    });

    it("classifies ORM/domain questions", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Explain how computed caching works in the ORM"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("explain_orm");
    });

    it("defaults to general for unrecognized requests", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Help me with this code"));

      const data = result.data as Record<string, unknown>;
      expect(data.task_type).toBe("general");
    });
  });

  // ── Copilot-like: Tool Selection per Task ───────────────────

  describe("tool selection per task type", () => {
    it("uses file creation tools for scaffolding", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Scaffold a new module"));

      expect(result.tools_available).toContain("github.create_files");
      expect(result.tools_available).toContain("github.create_pr");
    });

    it("uses read + create tools for view generation", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Generate a list view"));

      expect(result.tools_available).toContain("github.read_file");
      expect(result.tools_available).toContain("github.create_files");
    });

    it("uses PR tools for review tasks", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Review this PR carefully"));

      expect(result.tools_available).toContain("github.get_pr");
      expect(result.tools_available).toContain("github.get_diff");
      expect(result.tools_available).toContain("github.post_review");
    });

    it("uses read-only tools for manifest validation", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Validate the manifest"));

      expect(result.tools_available).toContain("github.read_file");
      expect(result.tools_available).toHaveLength(1);
    });

    it("uses Odoo docs tools for ORM questions", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Explain ORM domains"));

      expect(result.tools_available).toContain("odoo.search_docs");
      expect(result.tools_available).toContain("odoo.get_model_help");
    });

    it("uses migration tools including PR creation", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Migrate to new version"));

      expect(result.tools_available).toContain("github.read_file");
      expect(result.tools_available).toContain("github.create_files");
      expect(result.tools_available).toContain("github.create_pr");
    });
  });

  // ── Odoo 19 Conventions ─────────────────────────────────────

  describe("Odoo 19 conventions enforcement", () => {
    it("returns Odoo 19 version in context", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Create a new addon"));

      const data = result.data as Record<string, unknown>;
      expect(data.odoo_version).toBe("19.0");
    });

    it("enforces ipai_ module prefix", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Create a new addon"));

      const conventions = (result.data as Record<string, unknown>).conventions as Record<string, string>;
      expect(conventions.module_prefix).toBe("ipai_");
    });

    it("uses list view mode (not tree)", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Generate a view"));

      const conventions = (result.data as Record<string, unknown>).conventions as Record<string, string>;
      expect(conventions.view_mode_list).toBe("list");
    });

    it("uses 19.0 manifest version format", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Create a new addon"));

      const conventions = (result.data as Record<string, unknown>).conventions as Record<string, string>;
      expect(conventions.manifest_version).toBe("19.0.1.0.0");
    });
  });

  // ── Response Contract ──────────────────────────────────────

  describe("response contract", () => {
    it("identifies as developer agent", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Help with code"));

      expect(result.agent).toBe("developer");
    });

    it("preserves session ID", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Help with code"));

      expect(result.session_id).toBe("dev-session-001");
    });

    it("always returns available tools", async () => {
      const agent = new DeveloperAgent();
      const result = await agent.handle(makeRequest("Help with code"));

      expect(result.tools_available.length).toBeGreaterThan(0);
    });
  });
});
