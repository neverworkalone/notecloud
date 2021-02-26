export default [
  {
    path: '/notes/tasks',
    name: 'notes.tasks',
    meta: { requiresAuth: true },
    component: () => import('@/views/notes/Tasks.vue')
  },
  {
    path: '/notes/tasks/list',
    name: 'notes.taskList',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/TaskList.vue')
  },
  {
    path: '/notes/tasks/search/:q',
    name: 'notes.searchTask',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/SearchTask.vue')
  },
  {
    path: '/notes/memo',
    name: 'notes.memo',
    redirect: {
      name: 'notes.memoPage',
      params: {
        menu: 1,
        page: 1
      }
    }
  },
  {
    path: '/notes/memo/:q',
    name: 'notes.searchMemo',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/SearchMemo.vue')
  },
  {
    path: '/notes/memo/:menu/:page',
    name: 'notes.memoPage',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/Memo.vue')
  },
  {
    path: '/notes/memo/edit/:menu/:page/:pk',
    name: 'notes.editMemo',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/EditMemo.vue')
  },
  {
    path: '/notes/memo/new',
    name: 'notes.newMemo',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/NewMemo.vue')
  },
  {
    path: '/notes/memo/trash',
    name: 'notes.trash',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import('@/views/notes/Trash.vue')
  }
]
