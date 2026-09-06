from __future__ import annotations

import re

from typing import Final, Literal, NamedTuple

__version__ = "0.1.0"

ReleaseLevel = Literal["alpha", "beta", "candidate", "final"]

_VERSION_PATTERN: Final = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)(?:(?P<suffix>a|b|rc)(?P<serial>\d+))?$")

_LEVEL_BY_SUFFIX: Final[dict[str | None, ReleaseLevel]] = {
    "a": "alpha",
    "b": "beta",
    "rc": "candidate",
    None: "final"
}

_SUFFIX_BY_LEVEL: Final[dict[ReleaseLevel, str]] = {
    "alpha": "a",
    "beta": "b",
    "candidate": "rc",
    "final": ""
}

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: ReleaseLevel
    serial: int

    @classmethod
    def parse(cls, version: str) -> VersionInfo:
        match = _VERSION_PATTERN.match(version)

        if match is None:
            raise ValueError(f"invalid version string: {version!r}")

        serial = match["serial"]

        return cls(
            major=int(match["major"]),
            minor=int(match["minor"]),
            micro=int(match["micro"]),
            releaselevel=_LEVEL_BY_SUFFIX[match["suffix"]],
            serial=int(serial) if serial else 0
        )

    @property
    def is_prerelease(self) -> bool:
        return self.releaselevel != "final"

    def __str__(self) -> str:
        release = f"{self.major}.{self.minor}.{self.micro}"

        if not self.is_prerelease:
            return release

        return f"{release}{_SUFFIX_BY_LEVEL[self.releaselevel]}{self.serial}"

version_info: Final = VersionInfo.parse(__version__)

__all__ = ("VersionInfo", "version_info", "__version__")
