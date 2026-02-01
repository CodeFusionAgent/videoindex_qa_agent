# VideoIndex Q&A Agent (Purple Agent)

A Purple Agent that answers questions about video content. Built for the [AgentBeats](https://agentbeats.dev) platform using the [A2A (Agent-to-Agent)](https://a2a-protocol.org/latest/) protocol.

## Overview

This agent serves as the baseline Q&A agent for the VideoIndex benchmark. When given a question about a video, it returns one of the multiple-choice answer options randomly. This simulates a video understanding agent for evaluation purposes.

## How It Works

```
┌─────────────────┐                        ┌─────────────────┐
│   Eval Agent    │     Question           │    Q&A Agent    │
│  (Green Agent)  │ ──────────────────────▶│ (Purple Agent)  │
│                 │                        │                 │
│                 │◀────────────────────── │  Return random  │
│                 │     Answer             │  answer option  │
└─────────────────┘                        └─────────────────┘
```

## Project Structure

```
src/
├─ server.py      # Server setup and agent card configuration
├─ executor.py    # A2A request handling and task lifecycle
└─ agent.py       # Q&A logic: returns random answer from options
data/
└─ longtvqa.yaml  # Questions with multiple-choice options
tests/
└─ test_agent.py  # A2A conformance tests
Dockerfile        # Docker configuration
pyproject.toml    # Python dependencies
```

## Data Format

Questions and answer options are stored in YAML files under `data/`:

```yaml
questions:
  - qid: 133290
    question: "Why did Raj tell himself to turn his pelvis...?"
    episode: "s01e02"
    clip: "s01e02_seg02_clip_12"
    options:
      a0: "Raj was trying to get away from Penny."
      a1: "Raj is weird."
      a2: "Raj likes to give himself odd instructions."
      a3: "Raj had become excited and did not want Penny to know."
      a4: "Raj did not like hugging Penny."
```

The agent randomly selects one of the options (a0-a4) to return.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QA_DATA_DIR` | Directory containing YAML Q&A files | `data` |

## Running Locally

```bash
# Install dependencies
uv sync

# Run the server
uv run src/server.py
```

## Running with Docker

```bash
# Build the image
docker build -t videoindex-qa-agent .

# Run the container
docker run -p 9010:9010 videoindex-qa-agent
```

## Related Repositories

- [videoindex_eval_agent](https://github.com/CodeFusionAgent/videoindex_eval_agent) - Green Agent that evaluates Q&A responses
- [leaderboard_videoindex](https://github.com/CodeFusionAgent/leaderboard_videoindex) - Leaderboard and evaluation scenarios

## License

MIT
