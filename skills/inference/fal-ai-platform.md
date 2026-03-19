# Skill: fal.ai — Generative Media Inference Platform

source: https://fal.ai/docs
extracted: 2026-03-15
applies-to: agents, ops-platform, lakehouse

## What it is

Unified API for 1,000+ generative media models (image, video, audio, 3D, speech). Serverless model deployment for custom models on the same infrastructure. GPU compute instances (H100 SXM, 8xH100) for training and fine-tuning.

## When to use (decision matrix)

| Workload | Use | Platform |
|----------|-----|----------|
| Call hosted model (SDXL, Sora-class, etc.) | Model API | `fal_client.subscribe()` |
| Deploy custom/fine-tuned model as endpoint | fal Serverless | `fal.App` class |
| Training run, fine-tuning, batch ETL on GPU | fal Compute | Hourly, SSH |
| Real-time streaming output | WebSocket endpoint | `fal_client.stream()` |
| Async queue (long jobs) | Queue API | `queue.fal.run` + webhook |

## Core API Pattern (Async Queue — Preferred for IPAI)

```
POST https://queue.fal.run/{model-id}
Authorization: Key $FAL_KEY
→ returns request_id
→ poll or webhook on completion
```

## fal.App Serverless Pattern

```python
class MyModel(fal.App):
    machine_type = "GPU-H100"
    min_concurrency = 0   # scale to zero
    max_concurrency = 10

    def setup(self):
        # runs once per runner (warm)
        self.model = load()

    @fal.endpoint("/")
    def generate(self, prompt: str):
        return self.model(prompt)
```

## IPAI Integration Architecture

```
User request (ops-console / web)
  → Supabase Edge Function (ops-platform)
      → enqueue to ops.inference_jobs (Supabase Queue)
  → Edge Function worker
      → POST queue.fal.run/{model-id}
      → store request_id in ops.runs
  → Webhook from fal → Edge Function
      → update ops.run_events (completed/failed)
      → write output URL to Supabase Storage
      → emit Realtime event to ops-console
```

## Observability Hooks (map to ops.*)

- Prometheus metrics export → scrape into ops.metrics
- Log drains: Datadog / Elasticsearch → or pipe to Supabase via Edge Function
- Per-request analytics available via dashboard API

## SSOT/SOR Mapping

- fal is NEITHER SSOT nor SOR — it is a stateless compute layer
- Job state (request_id, status, result_url) → `ops.runs` + `ops.run_events` (Supabase SSOT)
- Outputs (images, video, audio) → Supabase Storage with metadata in Postgres
- Model registry (which fal model ID maps to which IPAI capability) → `ops.model_registry`

## Gaps / Watch

- No native multi-tenant RLS — auth is API-key only; enforce tenant isolation at Edge Function layer
- Shared mode (`app_auth="shared"`) — callers pay own usage; useful for portal surfaces
- Cold starts: use `min_concurrency=1` for latency-sensitive paths; `concurrency_buffer` for spikes
- No fal state should escape into the app layer — Supabase SSOT holds all job state

## Secrets Required

- `FAL_KEY` — API key for fal.ai (store in Supabase Vault + Azure Key Vault for CI)
