/**
 * Odoo Copilot Agent Runtime — Entry Point
 *
 * Starts the agent runtime server with all registered agents and tools.
 */

import express from "express";
import { createRouter } from "./router-agent/router.js";
import { registerTools } from "./shared/contracts/tool-registry.js";
import { createTraceMiddleware } from "./shared/tracing/middleware.js";

const app = express();
const PORT = process.env.PORT || 3100;

app.use(express.json());
app.use(createTraceMiddleware());

// Health check
app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "odoo-copilot-agent-runtime" });
});

// Agent message endpoint — receives messages from channel adapters
app.post("/api/v1/message", async (req, res) => {
  const { message, user_context, session_id } = req.body;

  const router = createRouter();
  const tools = registerTools();

  const result = await router.route({
    message,
    userContext: user_context,
    sessionId: session_id,
    tools,
  });

  res.json(result);
});

app.listen(PORT, () => {
  console.log(`Agent runtime listening on port ${PORT}`);
});

export { app };
