"""Load story content from TOML with ergonomic attribute access"""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

type TomlValue = str | int | float | bool | list[TomlValue] | dict[str, TomlValue]

_DEFAULT_PATH = Path(__file__).parent / "content.toml"


@dataclass
class Narrative:
    introduction: str
    conclusion: str


@dataclass
class Prompts:
    instructions: str
    hints: list[str]
    _extra: dict[str, TomlValue] = field(default_factory=dict, repr=False)

    def __getattr__(self, name: str) -> TomlValue | None:
        if name.startswith("_"):
            raise AttributeError(name)
        return self._extra.get(name)


@dataclass
class Act:
    narrative: Narrative
    prompts: Prompts


@dataclass
class Content:
    _path: Path = field(default=_DEFAULT_PATH, repr=False)
    _acts: dict[str, Act] = field(init=False, repr=False)

    def __post_init__(self):
        with self._path.open("rb") as f:
            raw = tomllib.load(f)

        self._acts = {}
        for key, data in raw.items():
            prompts_raw = data["prompts"]
            self._acts[key] = Act(
                narrative=Narrative(**data["narrative"]),
                prompts=Prompts(
                    instructions=prompts_raw["instructions"],
                    hints=prompts_raw["hints"],
                    _extra={
                        k: v
                        for k, v in prompts_raw.items()
                        if k not in ("instructions", "hints")
                    },
                ),
            )

    def __getattr__(self, name: str) -> Act:
        if name in self._acts:
            return self._acts[name]
        raise AttributeError(name)


content = Content()
