---
name: mlops-model-lifecycle
description: "Umbrella for ML/LLM model lifecycle work: model hub operations, local/server inference, quantization, evaluation, experiment tracking, model surgery, DSPy optimization, and specialized model toolchains."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [mlops, llm, inference, evaluation, huggingface, wandb, dspy, quantization, umbrella]
---

# MLOps Model Lifecycle

Use this class-level skill for end-to-end model work: discovering/downloading/uploading models, running local or server inference, benchmarking, tracking experiments, optimizing prompts/programs, performing model surgery, and operating specialized model packages such as SAM or AudioCraft.

## Workflow map

- **Model hub operations:** Search, download, upload, and authenticate with Hugging Face. Prefer CLI/API checks over guessed model paths.
- **Local inference and quantization:** Use llama.cpp/GGUF when the target is local CPU/GPU inference, quantized checkpoints, or OpenAI-compatible local servers.
- **High-throughput serving:** Use vLLM when the target is production-ish OpenAI-compatible serving, batching, tensor parallelism, or quantized hosted inference.
- **Evaluation:** Use lm-evaluation-harness for benchmark runs and custom tasks. Record exact model, revision, task, limit, batch size, and hardware.
- **Experiment tracking:** Use W&B for runs, sweeps, artifacts, dashboards, and model registry workflows.
- **Declarative optimization:** Use DSPy for trainable prompt/program pipelines, optimizers, and RAG-style evaluation loops.
- **Model surgery/safety research:** Use obliteratus when the user explicitly asks about abliteration/refusal-vector methods.
- **Specialized model families:** Use SAM for segmentation and AudioCraft/MusicGen for audio/music generation.

## Absorbed specialist packages

The former narrow MLOps skills are consolidated here with their complete package contents re-homed under `references/absorbed-skills/<skill>/`, `templates/absorbed-skills/<skill>/`, `scripts/absorbed-skills/<skill>/`, and `assets/absorbed-skills/<skill>/` where present.

Absorbed areas: Hugging Face Hub, llama.cpp, vLLM, lm-evaluation-harness, Weights & Biases, DSPy, Obliteratus, Segment Anything, and AudioCraft.

## Quality gates

1. Verify tool availability and credentials before issuing long-running ML commands.
2. Pin versions/revisions when results must be reproducible.
3. Capture hardware/context (`nvidia-smi`, CPU/RAM, disk) for performance claims.
4. For benchmarks, run a smoke test with a small limit before a full run.
5. For model serving, verify health with a real request against the endpoint before reporting success.

## Pitfalls

- Do not claim benchmark numbers without real run output.
- Do not mix local model paths and Hugging Face repo IDs without checking which a tool expects.
- Treat provider/model licensing, gated repos, and token availability as prerequisites, not afterthoughts.
