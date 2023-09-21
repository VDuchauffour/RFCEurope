class NotACallableError(ValueError):
    """Raised when is not a function."""

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return "Must be a callable, received %s" % type(self.var)


class NotTypeExpectedError(TypeError):
    """Raised when the expected type is not the same."""

    def __init__(self, expected, received):
        self.expected = expected
        self.received = received

    def __str__(self):
        return "Must be an %s, received %s" % (
            self.expected,
            self.received,
        )


class OutputTypeError(NotTypeExpectedError):
    """Raised when the `output_type` of an object is not correct."""
