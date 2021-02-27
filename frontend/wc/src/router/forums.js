export default [
  {
    path: '/forums/contact',
    name: 'forums.contact',
    component: () => import('@/views/forums/Contact.vue')
  },
  {
    path: '/forums/questions',
    name: 'forums.questions',
    redirect: {
      name: 'forums.questionsPage',
      params: {
        menu: 0,
        page: 1
      }
    }
  },
  {
    path: '/forums/questions/search/:q',
    name: 'forums.searchQuestions',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/forums/SearchQuestions.vue')
  },
  {
    path: '/forums/questions/list',
    name: 'forums.questionsList',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/forums/QuestionsList.vue')
  },
  {
    path: '/forums/questions/:menu/:page',
    name: 'forums.questionsPage',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/forums/Questions.vue')
  },
  {
    path: '/forums/questions/edit/:menu/:page/:pk',
    name: 'forums.answer',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/forums/Answer.vue')
  },
]
