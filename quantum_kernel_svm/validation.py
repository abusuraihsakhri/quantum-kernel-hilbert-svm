"""Strict parsing for CSV boolean columns."""


def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in ("true", "1", "yes", "y", "on"):
        return True
    if text in ("false", "0", "no", "n", "off", ""):
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")
