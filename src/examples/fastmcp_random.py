"""FastMCP demo server exposing a random integer tool."""
from __future__ import annotations

import logging
import random
from typing import Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastmcp-random")


class RandomDefaults(BaseModel):
    default_min: int = Field(0, description="Lower bound (inclusive)")
    default_max: int = Field(100, description="Upper bound (inclusive)")


defaults = RandomDefaults()

mcp = FastMCP(
    "fastmcp-random",
    instructions="Servidor MCP mínimo que entrega enteros aleatorios.",
)


@mcp.resource(
    "resource://defaults",
    name="defaults",
    description="Valores por defecto para min/max.",
    mime_type="application/json",
)
def read_defaults() -> str:
    """Expose the current default configuration as JSON."""

    return defaults.model_dump_json()


@mcp.tool
def random_int(
    min_value: Optional[int] = None, max_value: Optional[int] = None
) -> int:
    """Devuelve un entero aleatorio en el rango indicado."""

    lower = min_value if min_value is not None else defaults.default_min
    upper = max_value if max_value is not None else defaults.default_max
    if lower > upper:
        raise ValueError("min_value cannot be greater than max_value")
    value = random.randint(lower, upper)
    logger.info("random_int[%s,%s] -> %s", lower, upper, value)
    return value


if __name__ == "__main__":
    mcp.run()
