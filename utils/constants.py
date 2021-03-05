
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
    LENGTH_16 = 16
    LENGTH_32 = 32
    LENGTH_64 = 64
    LENGTH_128 = 128

    DEFAULT_LINK_COUNT = 10
    QUERY_PARAM_SEARCH = 'q'

    TIME_FORMAT_DEFAULT = '%I:%M %p'

    def __setattr__(self, name, value):
        raise AttributeError("cannot re-bind const(%s)" % name)


class _ConstProject(_Const):
    """
    Project constants

    Just for this project
    """

    COLOR_MAX_LENGTH = 32
    TASK_COLOR_DEFAULT = 'white'
    MEMO_TYPE_MAX_LENGTH = 32
    TIME_FORMAT_DEFAULT = '%I:%M %p'
    DOCTYPE_CODE = '<pre><code>'
    DOCTYPE_TABLE = '<table>'
    DOCTYPE_BULLET = '<ul><li>'
    DOCTYPE_ORDER = '<ol><li>'

    TRASH_KEEP_DAYS = 30

    QUERY_PARAM_STATE = 'state'
    QUESTION_STATE_NEW = 'new'
    QUESTION_STATE_OPEN = 'open'
    QUESTION_STATE_CLOSED = 'closed'
    QUESTION_STATE_DELETED = 'deleted'
    QUESTION_STATE_LIST = [
        QUESTION_STATE_OPEN,
        QUESTION_STATE_CLOSED,
        QUESTION_STATE_DELETED,
    ]


Const = _ConstProject()
