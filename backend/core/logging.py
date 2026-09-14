import json
import logging
from typing import Any


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """Emit a single JSON log line without secrets or full user content."""
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, default=str))
