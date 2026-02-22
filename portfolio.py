#!/usr/bin/env python3
"""
Portfolio Manager: AI-powered personal finance assistant.

Usage:
    uv run portfolio.py                    # Interactive chat
    uv run portfolio.py "How am I doing?"  # Single question
"""

import sys
from pathlib import Path

import yaml
from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()           # reads .env and sets ANTHROPIC_API_KEY as env variable
client = Anthropic()    # picks up the key automatically from env
console = Console()     # rich printer — handles colors and markdown rendering
DATA_DIR = Path("data") # base path for holdings.yaml, targets.yaml


def load_data(filename: str) -> dict:
    """Read a YAML file from the data/ folder. Returns {} if file doesn't exist."""
    path = DATA_DIR / filename
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_system_prompt() -> str:
    """Construct the model's context from current holdings and target allocations."""
    holdings = load_data("holdings.yaml")
    targets  = load_data("targets.yaml")

    holdings_text = (
        yaml.dump(holdings, default_flow_style=False)
        if holdings
        else "No holdings data found. Copy data/holdings.yaml.example to data/holdings.yaml and fill in your values."
    )
    targets_text = (
        yaml.dump(targets, default_flow_style=False)
        if targets
        else "No target allocations defined yet."
    )

    return f"""You are a personal finance assistant helping manage a diversified portfolio.

## Current Holdings
{holdings_text}

## Target Allocation
{targets_text}

## Guidelines
- Be concise and specific to the user's actual holdings
- Flag opportunities related to tax-advantaged accounts (401K, HSA) when relevant
- Crypto is high-risk/volatile: never suggest increasing allocation beyond target
- When suggesting rebalancing, prefer buying underweight assets over selling (avoids taxable events)
- For total net worth, include Taiwan accounts converted to USD
- Format responses clearly using markdown when helpful
"""


def call_model(system: str, messages: list) -> str:
    """Send messages to Claude Haiku and return the reply text."""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # cheaper Claude model, can switch to other models
        max_tokens=1024,
        system=system,
        messages=messages,
    )
    return response.content[0].text


MAX_TURNS = 10  # summarize conversation history after this many back-and-forth turns


def summarize_conversation(messages: list, system: str) -> list:
    """Compact history by asking the model to summarize, then reset to a single summary pair."""
    summary = call_model(
        system=system,
        messages=messages + [{
            "role": "user",
            "content": "Summarize our conversation so far in bullet points, focusing on decisions made and key facts about my portfolio.",
        }],
    )
    return [
        {"role": "user",      "content": f"[Conversation summary]\n{summary}"},
        {"role": "assistant", "content": "Got it, I have the context from our previous discussion."},
    ]


def chat(question: str | None = None) -> None:
    system = build_system_prompt()
    messages = []

    if question:
        # Single question mode: one request, print answer, exit
        reply = call_model(system, [{"role": "user", "content": question}])
        console.print(Markdown(reply))
        return

    # Interactive mode: keeps conversation history across turns
    console.print("[bold green]Portfolio Manager[/bold green] (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        reply = call_model(system, messages)  # full history sent each turn so model remembers context
        messages.append({"role": "assistant", "content": reply})

        # Compact history every MAX_TURNS to keep context window manageable
        if len(messages) >= MAX_TURNS * 2:
            console.print("[dim](Compacting conversation history...)[/dim]\n")
            messages = summarize_conversation(messages, system)

        console.print("\n[bold blue]Assistant:[/bold blue]")
        console.print(Markdown(reply))
        console.print()


if __name__ == "__main__":
    # Capture anything typed after `portfolio.py` as a single question
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    chat(question)
