#!/usr/bin/env -S uv run python
"""
Life.git - Learn git through life decisions

Run with: ./lifegit.py start
Or:       uv run python lifegit.py start
"""

from lifegit.cli import app

if __name__ == "__main__":
    app()
