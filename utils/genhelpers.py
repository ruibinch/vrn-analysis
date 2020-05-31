from typing import Any, Iterator, List

def _chunks(lst: List[Any], n: int) -> Iterator[str]:
    """Yields successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
