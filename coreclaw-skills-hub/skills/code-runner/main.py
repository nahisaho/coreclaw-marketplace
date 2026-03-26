#!/usr/bin/env python3
"""Simple code-runner skill placeholder."""


def run(source_code: str, language: str = "python") -> dict:
    return {
        "skill": "code-runner",
        "language": language,
        "source_code": source_code,
        "status": "not-executed",
    }


if __name__ == "__main__":
    print(run("print('hello')"))
