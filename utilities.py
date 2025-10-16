from pathlib import Path

def load_instruction(rel_path: str) -> str:
    base = Path(__file__).resolve().parent
    path = base / rel_path
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as e:
        raise RuntimeError(f"Instruction file not found: {path}") from e

def _env_only_str(d: dict[str, str | None]) -> dict[str, str]:
    # drop None values so dict[str, str] is satisfied
    return {k: v for k, v in d.items() if v is not None}