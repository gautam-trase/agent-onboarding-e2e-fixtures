"""Invalid bundle: requirements.txt is deliberately absent."""


def run() -> None:
    """Fail loudly if a malformed fixture ever reaches sandbox execution."""
    raise RuntimeError("The server must reject this bundle before building or running it")
