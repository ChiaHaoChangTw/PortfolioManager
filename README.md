# Portfolio Manager

AI-assisted personal finance portfolio tracker and advisor.

> Built with [Claude Code](https://claude.ai/claude-code) by Anthropic.

## Overview

A conversational AI agent that helps you track, analyze, and rebalance your personal finance portfolio across multiple accounts and asset types.

## Usage

```bash
uv run portfolio.py                         # Interactive chat
uv run portfolio.py "How am I doing?"       # Single question
```

## Setup

```bash
cp data/holdings.yaml.example data/holdings.yaml    # create your private holdings file
cp .env.example .env                                # add your ANTHROPIC_API_KEY
uv sync --no-install-project                        # install dependencies
```

## Project Structure

```
PortfolioManager/
├── portfolio.py              # Main entry point
├── data/
│   ├── holdings.yaml         # Your holdings (gitignored)
│   ├── holdings.yaml.example # Template
│   └── targets.yaml          # Target allocation % (optional)
└── reports/                  # Generated reports (gitignored)
```

## Planned Features

- Live price fetching (yfinance + CoinGecko)
- Rebalancing suggestions with tax awareness
- Cost-basis and gains tracking
- News sentiment analysis for holdings
