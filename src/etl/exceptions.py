class ETLError(Exception):
    """
    Base ETL Exception
    """
    pass


class ValidationError(ETLError):
    pass


class LoaderError(ETLError):
    pass