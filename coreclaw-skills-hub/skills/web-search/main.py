#!/usr/bin/env python3
"""Simple web-search skill placeholder."""


def run(query: str) -> dict:
    return {
        "skill": "web-search",
        "query": query,
        "results": [],
    }


if __name__ == "__main__":
    print(run("example query"))
