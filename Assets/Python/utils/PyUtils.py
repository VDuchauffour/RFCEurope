def all(iterable):
    """Return True if all elements of the iterable are true (or if the iterable is empty)."""
    for element in iterable:
        if not element:
            return False
    return True


def any(iterable):
    """Return True if any element of the iterable is true. If the iterable is empty, return False."""
    for element in iterable:
        if element:
            return True
    return False
