const Const = {
  SITENAME: 'notecloud',
  LANGUAGES: [
    {
      code: 'en',
      name: 'English'
    },
    {
      code: 'ko',
      name: '한국어'
    },
  ],
  PASSWORD_MIN: 8,
  TASK_CARD_MIN_WIDTH: '240',
  TASK_CARD_MAX_WIDTH: '348',
}

Const.install = function (Vue) {
  Vue.prototype.$const = (key) => Const[key]
  Vue.prototype.$apiURL = () => process.env.VUE_APP_API_SERVER
};

export default Const
