# MAX Engine & CLI Cheatsheet

Quick reference for working with the **Modular MAX SDK** (March 2026).

## CLI Commands

### 1. Model Loading & Benchmarking
```bash
# Benchmark a GGUF model directly
max benchmark --model qwen3-8b.gguf --iterations 100 --max-tokens 512

# Convert a HuggingFace model to MAX-optimized GGUF
max convert --model meta-llama/Llama-3-8B --output llama3.gguf
```

### 2. Serving (MAX Serve)
```bash
# Start an OpenAI-compatible server for a GGUF model
max serve --model llama3.gguf --port 41930 --backend mojo
```

## Performance Tips

### 1. Graph Fusion Verification
To see which layers are fused by the MAX Engine:
```bash
max explain --model llama3.gguf --verbosity high
```

### 2. Quantization Constants
When using `max convert`, you can specify the target quantization target:
- `Q4_K_M`: Optimal for RTX 40-series VRAM (16GB).
- `Q8_0`: High fidelity, good for CPU-only inference.

## Env Vars
- `MAX_LOG_LEVEL=debug`: Detailed graph processing logs.
- `MOJO_MAX_THREADS=32`: Override thread count for parallel kernels.
