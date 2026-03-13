/**
 * Tracing Middleware
 *
 * Adds distributed trace context to every request.
 */

import crypto from "node:crypto";
import type { Request, Response, NextFunction, RequestHandler } from "express";

export interface TraceContext {
  trace_id: string;
  span_id: string;
  start_time: number;
}

declare global {
  namespace Express {
    interface Request {
      trace?: TraceContext;
    }
  }
}

export function createTraceMiddleware(): RequestHandler {
  return (req: Request, res: Response, next: NextFunction): void => {
    const traceId = req.headers["x-trace-id"] as string || crypto.randomUUID();
    const spanId = crypto.randomUUID().slice(0, 16);

    req.trace = {
      trace_id: traceId,
      span_id: spanId,
      start_time: Date.now(),
    };

    res.setHeader("x-trace-id", traceId);

    res.on("finish", () => {
      const duration = Date.now() - (req.trace?.start_time ?? 0);
      console.log(JSON.stringify({
        trace_id: traceId,
        span_id: spanId,
        method: req.method,
        path: req.path,
        status: res.statusCode,
        duration_ms: duration,
        timestamp: new Date().toISOString(),
      }));
    });

    next();
  };
}
