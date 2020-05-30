def _chunks(lst: List, n: int) -> Generator[List[str]]:
    """Yields successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
