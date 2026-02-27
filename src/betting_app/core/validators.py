from __future__ import annotations


def normalize_numbers(values: list[int]) -> tuple[int, int, int, int]:
    if len(values) != 4:
        raise ValueError("A bet must contain exactly 4 numbers.")

    if any(not isinstance(item, int) for item in values):
        raise ValueError("All bet values must be integers.")

    if any(item < 1 or item > 99 for item in values):
        raise ValueError("Each number must be between 1 and 99.")

    unique = sorted(set(values))
    if len(unique) != 4:
        raise ValueError("Bet numbers must be unique.")

    return tuple(unique)  # type: ignore[return-value]
