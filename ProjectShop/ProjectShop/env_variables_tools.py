import os


class EnvironmentVariableError(Exception):
    pass


def get_environment_variable(alias):
    """
    Retrive environment variable and return it. Raise error if it doesn't exist.
    :param alias: str
    :return: str
    """
    variable = os.environ.get(alias)
    if not variable:
        raise EnvironmentVariableError(f"Key - {alias} not implemented")
    return variable
