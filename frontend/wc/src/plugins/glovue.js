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
    { color: 'white', sibling: 'grey lighten-3' },
    { color: 'yellow', sibling: 'yellow accent-1' },
    { color: 'red lighten-2', sibling: 'red accent-1' },
    { color: 'pink lighten-2', sibling: 'pink accent-1' },
    { color: 'purple lighten-3', sibling: 'purple lighten-2' },
    { color: 'deep-purple lighten-3', sibling: 'deep-purple lighten-2' },
    { color: 'indigo lighten-2', sibling: 'indigo lighten-1' },
    { color: 'blue lighten-3', sibling: 'blue lighten-1' },
    { color: 'light-blue lighten-2', sibling: 'light-blue' },
    { color: 'cyan lighten-2', sibling: 'cyan darken-1' },
    { color: 'teal lighten-2', sibling: 'teal' },
    { color: 'green lighten-1', sibling: 'green darken-1' },
    { color: 'light-green lighten-1', sibling: 'light-green darken-1' },
    { color: 'lime', sibling: 'lime darken-1' },
    { color: 'amber', sibling: 'amber darken-2' },
    { color: 'orange lighten-1', sibling: 'orange darken-1' },
    { color: 'deep-orange accent-1', sibling: 'deep-orange lighten-1' },
    { color: 'brown lighten-2', sibling: 'brown' },
    { color: 'blue-grey lighten-1', sibling: 'blue-grey' },
    { color: 'grey', sibling: 'grey darken-1' }
  ],
  PASSWORD_MIN: 8,
  TASK_CARD_MIN_WIDTH: '240',
  TASK_CARD_MAX_WIDTH: '348',
  TASK_NEW_MAX_WIDTH: '530',
  RANDOM_COLOR_FOR_NEW: false,
  DEFAULT_COLOR_INDEX: 0,
  SNACKBAR_TIMEOUT_MS: 2000,
}

Const.install = function (Vue) {
  Vue.prototype.$const = (key) => Const[key]
  Vue.prototype.$apiURL = () => process.env.VUE_APP_API_SERVER
};

export default Const
