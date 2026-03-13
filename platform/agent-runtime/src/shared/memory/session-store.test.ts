/**
 * Session Store — E2E Unit Tests
 *
 * SAP Joule equivalence: session memory, entity tracking, conversation history,
 * context continuity across turns, per-user/company isolation.
 */

import { describe, it, expect, beforeEach } from "vitest";
import { InMemorySessionStore, type ReferencedEntity, type ConversationEntry } from "./session-store.js";

describe("InMemorySessionStore", () => {
  let store: InMemorySessionStore;

  beforeEach(() => {
    store = new InMemorySessionStore();
  });

  // ── Session Lifecycle ──────────────────────────────────────

  describe("session lifecycle", () => {
    it("creates a new session with user and company context", async () => {
      const session = await store.create("sess-001", 1, 1);

      expect(session.session_id).toBe("sess-001");
      expect(session.user_id).toBe(1);
      expect(session.company_id).toBe(1);
      expect(session.created_at).toBeTruthy();
      expect(session.context.referenced_entities).toHaveLength(0);
      expect(session.context.conversation_history).toHaveLength(0);
    });

    it("retrieves an existing session", async () => {
      await store.create("sess-001", 1, 1);
      const session = await store.get("sess-001");

      expect(session).not.toBeNull();
      expect(session!.session_id).toBe("sess-001");
    });

    it("returns null for non-existent session", async () => {
      const session = await store.get("does-not-exist");
      expect(session).toBeNull();
    });

    it("deletes a session", async () => {
      await store.create("sess-001", 1, 1);
      await store.delete("sess-001");
      const session = await store.get("sess-001");

      expect(session).toBeNull();
    });

    it("updates the updated_at timestamp on set", async () => {
      const session = await store.create("sess-001", 1, 1);
      const firstUpdate = session.updated_at;

      // Small delay to ensure timestamp difference
      await new Promise((r) => setTimeout(r, 5));
      await store.set(session);
      const updated = await store.get("sess-001");

      expect(updated!.updated_at).not.toBe(firstUpdate);
    });
  });

  // ── Joule-like: Entity Tracking ─────────────────────────────

  describe("entity tracking (Joule context awareness)", () => {
    it("tracks referenced entities (invoices, partners, etc.)", async () => {
      await store.create("sess-001", 1, 1);
      await store.addEntity("sess-001", {
        model: "account.move",
        id: 142,
        name: "INV-2024-0142",
        last_accessed: new Date().toISOString(),
      });

      const session = await store.get("sess-001");
      expect(session!.context.referenced_entities).toHaveLength(1);
      expect(session!.context.referenced_entities[0].name).toBe("INV-2024-0142");
    });

    it("deduplicates entities by model+id", async () => {
      await store.create("sess-001", 1, 1);
      const entity: ReferencedEntity = {
        model: "account.move",
        id: 142,
        name: "INV-2024-0142",
        last_accessed: new Date().toISOString(),
      };

      await store.addEntity("sess-001", entity);
      await store.addEntity("sess-001", { ...entity, last_accessed: new Date().toISOString() });

      const session = await store.get("sess-001");
      expect(session!.context.referenced_entities).toHaveLength(1);
    });

    it("keeps different entities separate", async () => {
      await store.create("sess-001", 1, 1);
      await store.addEntity("sess-001", {
        model: "account.move",
        id: 142,
        name: "INV-2024-0142",
        last_accessed: new Date().toISOString(),
      });
      await store.addEntity("sess-001", {
        model: "res.partner",
        id: 10,
        name: "Acme Corp",
        last_accessed: new Date().toISOString(),
      });

      const session = await store.get("sess-001");
      expect(session!.context.referenced_entities).toHaveLength(2);
    });

    it("caps entity history at 20 entries", async () => {
      await store.create("sess-001", 1, 1);

      for (let i = 0; i < 25; i++) {
        await store.addEntity("sess-001", {
          model: "account.move",
          id: i,
          name: `INV-${i}`,
          last_accessed: new Date().toISOString(),
        });
      }

      const session = await store.get("sess-001");
      expect(session!.context.referenced_entities).toHaveLength(20);
      // Most recent should be kept
      expect(session!.context.referenced_entities[19].name).toBe("INV-24");
    });

    it("silently no-ops for non-existent session", async () => {
      await store.addEntity("does-not-exist", {
        model: "account.move",
        id: 1,
        name: "INV-001",
        last_accessed: new Date().toISOString(),
      });
      // Should not throw
    });
  });

  // ── Joule-like: Conversation History ────────────────────────

  describe("conversation history (Joule session memory)", () => {
    it("tracks user and assistant messages", async () => {
      await store.create("sess-001", 1, 1);
      await store.addConversation("sess-001", {
        role: "user",
        content: "Show overdue invoices",
        timestamp: new Date().toISOString(),
      });
      await store.addConversation("sess-001", {
        role: "assistant",
        content: "Here are the overdue invoices...",
        timestamp: new Date().toISOString(),
        tools_used: ["odoo.get_invoices", "odoo.get_overdue_summary"],
      });

      const session = await store.get("sess-001");
      expect(session!.context.conversation_history).toHaveLength(2);
      expect(session!.context.conversation_history[0].role).toBe("user");
      expect(session!.context.conversation_history[1].role).toBe("assistant");
    });

    it("records tools used per assistant turn", async () => {
      await store.create("sess-001", 1, 1);
      await store.addConversation("sess-001", {
        role: "assistant",
        content: "Found 5 overdue invoices",
        timestamp: new Date().toISOString(),
        tools_used: ["odoo.get_invoices", "odoo.get_overdue_summary"],
      });

      const session = await store.get("sess-001");
      expect(session!.context.conversation_history[0].tools_used).toContain("odoo.get_invoices");
    });

    it("caps conversation history at 50 turns", async () => {
      await store.create("sess-001", 1, 1);

      for (let i = 0; i < 55; i++) {
        await store.addConversation("sess-001", {
          role: i % 2 === 0 ? "user" : "assistant",
          content: `Message ${i}`,
          timestamp: new Date().toISOString(),
        });
      }

      const session = await store.get("sess-001");
      expect(session!.context.conversation_history).toHaveLength(50);
      // Most recent messages kept
      expect(session!.context.conversation_history[49].content).toBe("Message 54");
    });
  });

  // ── Session Isolation ──────────────────────────────────────

  describe("session isolation (Joule tenant scoping)", () => {
    it("isolates sessions by ID", async () => {
      await store.create("user-1-session", 1, 1);
      await store.create("user-2-session", 2, 1);

      await store.addEntity("user-1-session", {
        model: "account.move",
        id: 1,
        name: "INV-001",
        last_accessed: new Date().toISOString(),
      });

      const s1 = await store.get("user-1-session");
      const s2 = await store.get("user-2-session");

      expect(s1!.context.referenced_entities).toHaveLength(1);
      expect(s2!.context.referenced_entities).toHaveLength(0);
    });

    it("preserves company context per session", async () => {
      const s1 = await store.create("sess-co1", 1, 1);
      const s2 = await store.create("sess-co2", 1, 2);

      expect(s1.company_id).toBe(1);
      expect(s2.company_id).toBe(2);
    });
  });
});
