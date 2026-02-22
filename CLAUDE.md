# Portfolio Manager

AI-assisted personal finance portfolio tracker and advisor.

## Goal

Analyze and manage a diversified portfolio across US and Taiwan accounts. Provide
rebalancing suggestions, P&L tracking, news sentiment, and tax/cost-basis reporting.

## Key Files

- `data/holdings.yaml`: Current balances and positions (**gitignored**, update manually)
- `data/targets.yaml`: Target asset allocation percentages
- `portfolio.py`: Main interactive agent entry point

## Running

```bash
uv run portfolio.py              # Interactive chat
uv run portfolio.py "question"   # Single question
```

## Conventions

- All values in USD unless noted; Taiwan accounts tracked in TWD with a manual `usd_equiv` field
- `holdings.yaml` is a point-in-time snapshot: update it after any significant transaction
- Cost basis (`avg_cost`) is tracked per lot in holdings for tax purposes
- **Never commit real balances, account numbers, or personal data to git**
- Taiwan accounts: use current TWD/USD rate when updating `usd_equiv`

## Financial Priority Order (general guidance for agents)

1. Max 401K to capture any employer match first
2. Max HSA contributions (triple tax-advantaged: pre-tax in, grows tax-free, tax-free out for medical)
3. Keep 3–6 months of expenses in HYSA or cash (emergency fund)
4. Pay off high-interest debt before investing in taxable brokerage
5. Invest surplus in low-cost index funds in taxable brokerage

## Agent Guidelines

- Be concise and specific to the user's actual holdings
- Always flag tax-advantaged accounts (401K, HSA) when relevant to a decision
- For crypto: treat as high-risk/volatile; never suggest over-allocating
- Rebalancing: prefer buying underweight assets over selling (avoids taxable events)
- When calculating total net worth, include Taiwan accounts converted to USD

## Planned Future Agents

- `agents/tracker.py`: Live price fetching & P&L (yfinance + CoinGecko)
- `agents/rebalancer.py`: Rebalancing suggestions with tax awareness
- `agents/tax_reporter.py`: Cost-basis, realized/unrealized gains, lot tracking
- `agents/sentiment.py`: News & sentiment analysis for held assets
