
class _Const(object):
    """
    Common constants

    Reuseable constants as a boilerplate
    """

    NAME_MAX_LENGTH = 150
    KEY_MAX_LENGTH = 4
    PASSWORD_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 254
    FILE_MAX_LENGTH = 128
    TEL_MAX_LENGTH = 100
    ADDRESS_MAX_LENGTH = 254
    IP_ADDRESS_MAX_LENGTH = 45
    DESC_MAX_LENGTH = 1024
    TITLE_MAX_LENGTH = 100
    DEFAULT_LINK_COUNT = 10

    QUERY_PARAM_SEARCH_QUERY = 'q'

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind const(%s)" % name)


class _ConstProject(_Const):
    """
    Project constants

    Just for this project
    """

    COLOR_MAX_LENGTH = 32
    TASK_COLOR_DEFAULT = 'white'
    MEMO_TIME_FORMAT = '%I:%M %p'


Const = _ConstProject()
