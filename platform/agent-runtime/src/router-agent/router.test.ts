import { describe, it, expect } from "vitest";
import { classifyIntent, createRouter } from "./router.js";

describe("classifyIntent", () => {
  it("routes invoice queries to business agent", () => {
    const result = classifyIntent("Show overdue invoices for top 20 customers");
    expect(result.agent).toBe("business");
    expect(result.confidence).toBeGreaterThan(0);
  });

  it("routes bill queries to business agent", () => {
    const result = classifyIntent("What vendor bills are pending payment?");
    expect(result.agent).toBe("business");
  });

  it("routes documentation questions to knowledge agent", () => {
    const result = classifyIntent("How to configure the accounting module?");
    expect(result.agent).toBe("knowledge");
  });

  it("routes troubleshooting to knowledge agent", () => {
    const result = classifyIntent("Explain this traceback error from invoice posting");
    expect(result.agent).toBe("knowledge");
  });

  it("routes multi-step processes to workflow agent", () => {
    const result = classifyIntent("Send email to notify and follow up with a reminder to escalate");
    expect(result.agent).toBe("workflow");
  });

  it("routes code questions to developer agent", () => {
    const result = classifyIntent("Generate a test for the invoice model");
    expect(result.agent).toBe("developer");
  });

  it("routes PR review to developer agent", () => {
    const result = classifyIntent("Review pull request #42 for security issues");
    expect(result.agent).toBe("developer");
  });

  it("defaults to business agent for ambiguous messages", () => {
    const result = classifyIntent("Hello, what can you do?");
    expect(result.agent).toBe("business");
    expect(result.confidence).toBe(0);
  });

  it("returns confidence based on signal density", () => {
    const strong = classifyIntent("Show overdue invoices and receivable payment status for customers");
    const weak = classifyIntent("Show invoices");
    expect(strong.confidence).toBeGreaterThanOrEqual(weak.confidence);
  });
});

describe("createRouter", () => {
  it("returns a route function", () => {
    const router = createRouter();
    expect(typeof router.route).toBe("function");
  });

  it("routes a message and returns agent response", async () => {
    const router = createRouter();
    const result = await router.route({
      message: "Show overdue invoices",
      userContext: {
        user_id: 1,
        user_name: "Test",
        company_id: 1,
        company_name: "Test Co",
        groups: [],
        permissions: {},
      },
      sessionId: "test-session",
      tools: {},
    });

    expect(result.agent).toBe("business");
    expect(result.session_id).toBe("test-session");
  });
});
