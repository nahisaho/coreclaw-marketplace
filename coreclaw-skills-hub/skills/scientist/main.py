#!/usr/bin/env python3
"""Entrypoint for imported skill: scientist (v0.2.3).

Harness-optimized scientific research assistant with verification loops,
quality gates, and English-only prompts for token efficiency.
"""


def run(input_data: dict | None = None) -> dict:
    return {
        "skill": "scientific-assistant",
        "version": "v0.5.0",
        "skill_path": "scientist",
        "status": "imported",
        "capabilities": [
            "verification-loop",
            "quality-gates",
            "english-only-prompts",
            "harness-optimized",
            "195-sub-skills",
        ],
        "harness": {
            "verification_loop": "PLAN → EXECUTE → VERIFY → REPORT",
            "quality_gates": [
                "figures-saved-to-disk",
                "figures-embedded-in-report",
                "results-as-json-csv",
                "english-only-figure-text",
            ],
            "token_optimization": "all-prompts-in-english",
        },
        "input": input_data or {},
    }


if __name__ == "__main__":
    print(run())
