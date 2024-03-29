const APIs = {
  ACCOUNTS_SIGNUP: {
    'method': 'post',
    'url': '/accounts/signup/'
  },
  ACCOUNTS_LOGIN: {
    'method': 'post',
    'url': '/accounts/login/'
  },
  ACCOUNTS_CONNECT: {
    'method': 'post',
    'url': '/accounts/connect/'
  },
  ACCOUNTS_LOGOUT: {
    'method': 'post',
    'url': '/accounts/logout/'
  },
  ACCOUNTS_DEVICE_REGISTER: {
    'method': 'post',
    'url': '/accounts/device/{pk}/register/'
  },
  ACCOUNTS_DEVICE_DELETE: {
    'method': 'delete',
    'url': '/accounts/device/{pk}/delete/'
  },
  ACCOUNTS_DEVICES: {
    'method': 'get',
    'url': '/accounts/devices/'
  },
  ACCOUNTS_PASSWORD_CHANGE: {
    'method': 'post',
    'url': '/accounts/password_change/'
  },
  ACCOUNTS_PASSWORD_RESET: {
    'method': 'post',
    'url': '/accounts/password_reset/'
  },
  ACCOUNTS_PASSWORD_RESET_CONFIRM: {
    'method': 'post',
    'url': '/accounts/password_reset_confirm/'
  },
  ACCOUNTS_SETTING_GET: {
    'method': 'get',
    'url': '/accounts/setting/'
  },
  ACCOUNTS_SETTING_SET: {
    'method': 'patch',
    'url': '/accounts/setting/'
  },
  ACCOUNTS_DEACTIVATE: {
    'method': 'post',
    'url': '/accounts/deactivate/'
  },

  NOTES_NEW_TASK: {
    'method': 'post',
    'url': '/notes/task/new/'
  },
  NOTES_EDIT_TASK: {
    'method': 'patch',
    'url': '/notes/task/{pk}/'
  },
  NOTES_DELETE_TASK: {
    'method': 'delete',
    'url': '/notes/task/{pk}/'
  },
  NOTES_COMPLETE_TASK: {
    'method': 'post',
    'url': '/notes/task/{pk}/complete/'
  },
  NOTES_TASKS: {
    'method': 'get',
    'url': '/notes/tasks/'
  },
  NOTES_TASKS_DATE: {
    'method': 'get',
    'url': '/notes/tasks/?date={date}'
  },
  NOTES_SEARCH_TASKS: {
    'method': 'get',
    'url': '/notes/tasks/search/?q={q}'
  },

  NOTES_NEW_MEMO: {
    'method': 'post',
    'url': '/notes/memo/new/'
  },
  NOTES_EDIT_MEMO: {
    'method': 'patch',
    'url': '/notes/memo/{pk}/'
  },
  NOTES_DELETE_MEMO: {
    'method': 'delete',
    'url': '/notes/memo/{pk}/'
  },
  NOTES_VIEW_MEMO: {
    'method': 'get',
    'url': '/notes/memo/{pk}/'
  },
  NOTES_RESTORE_MEMO: {
    'method': 'post',
    'url': '/notes/memo/{pk}/restore/'
  },
  NOTES_MEMOS: {
    'method': 'get',
    'url': '/notes/memos/?page={page}'
  },
  NOTES_TRASH_MEMOS: {
    'method': 'get',
    'url': '/notes/memos/trash/'
  },
  NOTES_EMPTY_TRASH_MEMOS: {
    'method': 'post',
    'url': '/notes/memos/trash/empty/'
  },
  NOTES_PINNED_MEMOS: {
    'method': 'get',
    'url': '/notes/memos/pinned/?page={page}'
  },
  NOTES_SHARED_MEMOS: {
    'method': 'get',
    'url': '/notes/memos/shared/?page={page}'
  },
  NOTES_SHARED_MEMO: {
    'method': 'get',
    'url': '/notes/memo/shared/{pk}/'
  },
  NOTES_PIN_MEMO: {
    'method': 'post',
    'url': '/notes/memo/{pk}/pin/'
  },
  NOTES_UNPIN_MEMO: {
    'method': 'post',
    'url': '/notes/memo/{pk}/unpin/'
  },
  NOTES_SHARE_MEMO: {
    'method': 'post',
    'url': '/notes/memo/{pk}/share/'
  },
  NOTES_UNSHARE_MEMO: {
    'method': 'post',
    'url': '/notes/memo/{pk}/unshare/'
  },
  FORUMS_NEW_QUESTION: {
    'method': 'post',
    'url': '/forums/question/new/'
  },
  FORUMS_ANSWER_QUESTION: {
    'method': 'post',
    'url': '/forums/question/{pk}/answer/'
  },
  FORUM_QUESTION: {
    'method': 'get',
    'url': 'forums/question/{pk}/'
  },
  FORUMS_QUESTIONS_NEW: {
    'method': 'get',
    'url': '/forums/questions/?state=new&page={page}'
  },
  FORUMS_QUESTIONS_OPEN: {
    'method': 'get',
    'url': '/forums/questions/?state=open&page={page}'
  },
  FORUMS_QUESTIONS_CLOSED: {
    'method': 'get',
    'url': '/forums/questions/?state=closed&page={page}'
  },
  FORUMS_QUESTIONS_DELETED: {
    'method': 'get',
    'url': '/forums/questions/?state=deleted&page={page}'
  },
  FORUMS_SEARCH_QUESTIONS: {
    'method': 'get',
    'url': '/forums/questions/?q={q}&page_size=0'
  }
}

APIs.install = function (Vue) {
  Vue.prototype.$baseURL = () => process.env.VUE_APP_API_SERVER
  Vue.prototype.$api = (key) => APIs[key]
};

export default APIs
