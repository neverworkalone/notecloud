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
  TASK_COLORS: [
    { color: 'white' },
    { color: 'yellow' },
    { color: 'red lighten-2' },
    { color: 'pink lighten-2' },
    { color: 'purple lighten-3' },
    { color: 'deep-purple lighten-3' },
    { color: 'indigo lighten-2' },
    { color: 'blue lighten-3' },
    { color: 'light-blue lighten-2' },
    { color: 'cyan lighten-2' },
    { color: 'teal lighten-2' },
    { color: 'green lighten-1' },
    { color: 'light-green lighten-1' },
    { color: 'lime' },
    { color: 'amber' },
    { color: 'orange' },
    { color: 'deep-orange accent-1' },
    { color: 'brown lighten-2' },
    { color: 'blue-grey lighten-1' },
    { color: 'grey' },
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
