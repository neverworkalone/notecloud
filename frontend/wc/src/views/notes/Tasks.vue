<template>
  <div
    v-if="initialized"
  >
    <div
      :class="isMobile ? 'content pt-0 pl-0 pr-0' : 'content pt-0'"
    >
      <div
        class="headline float-left"
        v-text="getYearMonth"
      >
      </div>
      <div
        class="float-right"
      >
        <v-btn
          small
          @click="getTasks(dateBefore)"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn
          small
          @click="getTasks(today)"
        >
          {{ $t('tasks.TODAY') }}
        </v-btn>
        <v-btn
          small
          @click="getTasks(dateAfter)"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>
    </div>

    <div
      class="content pa-0 pt-5"
    >
      <v-simple-table>
        <thead>
          <tr>
            <th
              v-for="item in calendar"
              :key="item.date"
              class="text-center pa-0"
            >
              <v-btn
                small
                depressed
                class="pt-5 pb-5"
                :color="weekdayColor(item)"
                @click="getTasks(item.date)"
              >
                <v-badge
                  dot
                  bordered
                  :value="badgeValue(item)"
                  :color="badgeColor(item)"
                >
                  {{ getCalendarDay(item.date) }}<br>
                  {{ $t('calendar.' + item.weekday) }}
                </v-badge>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody>
        </tbody>
      </v-simple-table>

      <v-container>
        <v-row>
          <v-dialog
            v-model="editDialog"
            transition="dialog-bottom-transition"
            width="90%"
            :max-width="$const('TASK_NEW_MAX_WIDTH')"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-col
                v-for="task in tasks"
                :key="task.id"
                :cols="isMobile ? '' : 'auto'"
                class="mr-auto"
              >
                <v-card
                  elevation=8
                  :color="task.color"
                  :min-width="isMobile? $const('TASK_CARD_MIN_WIDTH') : $const('TASK_CARD_MAX_WIDTH')"
                  :max-width="$const('TASK_CARD_MAX_WIDTH')"
                >
                  <v-card-actions>
                    <v-card-subtitle>
                      <v-hover v-slot="{ hover }">
                        <v-icon
                          large
                          class="mr-2"
                          :color="hover ? 'teal' : ''"
                          @click="toggleComplete(task)"
                          v-if="!task.is_completed"
                        >
                          mdi-check-circle-outline
                        </v-icon>
                        <v-icon
                          large
                          class="mr-2"
                          :color="hover ? '' : 'teal'"
                          @click="toggleComplete(task)"
                          v-else
                        >
                          mdi-check-circle
                        </v-icon>
                      </v-hover>
                      {{ getTaskDate(task) }}
                    </v-card-subtitle>
                  </v-card-actions>

                  <v-card-title
                    class="pt-0 pb-0"
                    v-text="task.content"
                    v-bind="attrs"
                    v-on="on"
                    @click="initializeEditDialog(task)"
                    v-if="!task.is_completed"
                  ></v-card-title>
                  <v-card-title
                    class="pt-0 pb-0 text-decoration-line-through"
                    v-text="task.content"
                    v-else
                  ></v-card-title>

                  <v-card-actions
                    class="pt-0"
                  >
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      @click="setShowMore(task.index)"
                    >
                      <v-icon>{{ showMore[task.index] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-card-actions>

                  <v-expand-transition>
                    <div v-show="showMore[task.index]">
                      <v-divider></v-divider>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col
                              v-for="color in colors"
                              :key="color.color"
                              :cols="isMobile ? '' : 'auto'"
                              class="mr-auto"
                            >
                              <v-btn
                                x-small
                                :color="color.color"
                                @click="updateColor(task.id, color.color)"
                              >
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                    </div>
                  </v-expand-transition>
                </v-card>
              </v-col>
            </template>

            <v-card
              :color="editColor"
            >
              <v-card-subtitle
                class="pt-2 pb-0 pl-4"
              >
                <v-icon
                  class="ml-0"
                >
                  mdi-calendar-check
                </v-icon>
                {{ editDate }} ~
              </v-card-subtitle>
              <v-col
                class="pb-0"
              >
                <v-textarea
                  v-model="editContent"
                  :background-color="editColor"
                  solo
                  auto-grow
                  autofocus
                ></v-textarea>
              </v-col>
              <v-card-text
                class=""
              >
                <v-card-actions
                  class="pt-0 mt-0 pr-0"
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    large
                    color="primary"
                    class="pl-8 pr-8"
                    @click="editTask()"
                  >
                    {{ $t('common.SAVE') }}
                  </v-btn>
                  <v-spacer></v-spacer>
                    <v-btn
                      icon
                      @click="editDialogExpand = !editDialogExpand"
                    >
                      <v-icon>{{ editDialogExpand ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-card-actions>

                  <v-expand-transition>
                    <div
                      v-show="editDialogExpand"
                      class="pt-2"
                    >
                      <v-divider></v-divider>

                        <v-container>
                          <v-row>
                            <v-col
                              v-for="color in colors"
                              :key="color.color"
                              :cols="isMobile ? '' : 'auto'"
                            >
                              <v-btn
                                x-small
                                :color="color.color"
                                @click="editColor = color.color"
                              >
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-container>
                    </div>
                  </v-expand-transition>

              </v-card-text>
            </v-card>
          </v-dialog>

          <v-col
            :cols="isMobile? '' : 'auto'"
            class="mr-auto"
          >
            <v-dialog
              v-model="newDialog"
              transition="dialog-bottom-transition"
              width="90%"
              :max-width="$const('TASK_NEW_MAX_WIDTH')"
            >

              <template v-slot:activator="{ on, attrs }">
                <v-card
                  :color="randomColor.color"
                  :min-width="isMobile ? $const('TASK_CARD_MIN_WIDTH') : $const('TASK_CARD_MAX_WIDTH')"
                  :max-width="$const('TASK_CARD_MAX_WIDTH')"
                  class="text-center pa-10"
                >
                  <v-btn
                    fab
                    x-large
                    elevation=8
                    class="pa-12"
                    :color="randomColor.sibling"
                    v-bind="attrs"
                    v-on="on"
                    @click="initializeNewDialog()"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-card>
              </template>

              <v-card
                :color="getNewColor"
              >
                <v-card-subtitle
                  class="pt-2 pb-0 pl-4"
                >
                  <v-icon
                    class="ml-0"
                  >
                    mdi-calendar-check
                  </v-icon>
                  {{ dateCurrent }} ~
                </v-card-subtitle>
                <v-col
                  class="pb-0"
                >
                  <v-textarea
                    v-model="newContent"
                    :background-color="getNewColor"
                    solo
                    auto-grow
                    autofocus
                  ></v-textarea>
                </v-col>
                <v-card-text
                  class=""
                >
                  <v-card-actions
                    class="pt-0 mt-0 pr-0"
                  >
                    <v-spacer></v-spacer>
                    <v-btn
                      large
                      color="primary"
                      class="pl-8 pr-8"
                      @click="newTask()"
                    >
                      {{ $t('common.CREATE') }}
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      @click="newDialogExpand = !newDialogExpand"
                    >
                      <v-icon>{{ newDialogExpand ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                    </v-btn>
                  </v-card-actions>

                  <v-expand-transition>
                    <div
                      v-show="newDialogExpand"
                      class="pt-2"
                    >
                      <v-divider></v-divider>
                      <v-container>
                        <v-row>
                          <v-col
                            v-for="color in colors"
                            :key="color.color"
                            :cols="isMobile ? '' : 'auto'"
                          >
                            <v-btn
                              x-small
                              :color="color.color"
                              @click="newColor = color.color"
                            >
                            </v-btn>
                          </v-col>
                        </v-row>
                      </v-container>
                    </div>
                  </v-expand-transition>
                </v-card-text>
              </v-card>

            </v-dialog>
          </v-col>

        </v-row>
      </v-container>
    </div>

  </div>
</template>

<style lang="scss">
.v-card__title {
  white-space: break-spaces;
}
</style>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      dateBefore: '',
      dateAfter: '',
      dateCurrent: '',
      today: '',
      year: '',
      month: '',
      calendar: '',
      tasks: '',
      isMobile: false,
      showMore: [],
      colors: this.$const('TASK_COLORS'),
      randomColor: [],
      newColor: '',
      newContent: '',
      editContent: '',
      editColor: '',
      editDate: '',
      editDialog: false,
      editDialogExpand: false,
      newDialog: false,
      newDialogExpand: false,
      firstInit: false
    }
  },
  computed: {
    getYearMonth () {
      return this.$t('tasks.YEAR_MONTH', {
        year: this.year,
        month: this.$t('calendar.' + this.month)
      })
    },
    getNewColor () {
      return this.newColor
    },
    initialized () {
      return this.firstInit
    }
  },
  beforeDestroy () {
    if (typeof window === 'undefined') {
      return
    }
    window.removeEventListener('resize', this.onResize, { passive: true })
  },
  mounted () {
    this.onResize()
    window.addEventListener('resize', this.onResize, { passive: true })

    this.getTasks()
  },
  methods: {
    setYearMonth: function (date) {
      this.year = date[0]
      this.month = date[1]
    },
    weekdayColor: function (item) {
      if (item.date == this.dateCurrent) {
        return "primary"
      }
      else {
        return "white"
      }
    },
    getRandomColor: function () {
      if (this.$const('RANDOM_COLOR_FOR_NEW')) {
        var index = Math.floor(Math.random() * Math.floor(this.colors.length))
        this.randomColor = this.colors[index]
      }
      else {
        this.randomColor = this.colors[this.$const('DEFAULT_COLOR_FOR_NEW')]
      }
    },
    initializeEditDialog: function (task) {
      this.editID = task.id
      this.editContent = task.content
      this.editColor = task.color
      this.editDate = task.date_from
      this.editDialogExpand = false
    },
    initializeNewDialog: function () {
      this.newColor = this.randomColor.color
      this.newContent = ''
      this.newDialogExpand = false
    },
    badgeValue: function (item) {
      if (item.count == 0) {
        return false
      }
      else {
        return true
      }
    },
    badgeColor: function (item) {
      if (item.all_completed) {
        return "black"
      }
      else if (item.incompleted_exist) {
        return "red"
      }
      else {
        return "white"
      }
    },
    getCalendarDay: function (date) {
      return parseInt(date.split('-')[2])
    },
    getTaskDate: function (task) {
      var dateStr = task.date_from + ' ~ '
      if (task.is_completed) {
        dateStr += task.date_until
      }

      return dateStr
    },
    initializeShowMore: function () {
      this.showMore = []

      for (var i=0; i<this.tasks.length; i++) {
        this.showMore.push(false)
        this.tasks[i].index = i
      }
    },
    setShowMore: function (index) {
      var newShowMore = []
      for (var i=0; i<this.showMore.length; i++) {
        newShowMore.push(this.showMore[i])
      }
      newShowMore[index] = !this.showMore[index]
      this.showMore = newShowMore
    },
    editTask: function () {
      var vm = this

      axios({
        method: 'patch',
        url: '/notes/tasks/' + this.editID + '/',
        data: {
          'content': this.editContent,
          'color': this.editColor
        }
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == data.id) {
            vm.tasks[i].content = data.content
            vm.tasks[i].color = data.color
          }
        }

        vm.editMore = false
        vm.editDialog = false
      })
      .catch(function () {
      })
    },
    newTask: function () {
      var vm = this

      axios({
        method: 'post',
        url: '/notes/tasks/new/',
        data: {
          'date_from': this.dateCurrent,
          'content': this.newContent,
          'color': this.newColor
        }
      })
      .then(function (response) {
        var data = response.data['data']

        vm.tasks.push(data)
        vm.initializeShowMore()
        vm.getRandomColor()
        vm.newDialog = false
      })
      .catch(function () {
      })
    },
    toggleComplete: function (task) {
      var vm = this

      axios({
        method: 'post',
        url: '/notes/tasks/' + task.id + '/complete/'
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == data.id) {
            vm.tasks[i].is_completed = data.is_completed
            vm.tasks[i].date_until = data.date_until
          }
        }
      })
      .catch(function () {
      })
    },
    updateColor: function (id, color) {
      var vm = this

      axios({
        method: 'patch',
        url: '/notes/tasks/' + id + '/',
        data: {
          color: color,
        },
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == data.id) {
            vm.tasks[i].color = data.color
          }
        }
      })
      .catch(function () {
      })
    },
    getTasks: function (date) {
      var vm = this
      var url = '/notes/tasks'

      if (date) {
        url = '/notes/tasks/?date=' + date
      }

      axios({
        method: 'get',
        url: url
      })
      .then(function (response) {
        vm.dateBefore = response.data['pagination']['date_before']
        vm.dateAfter = response.data['pagination']['date_after']
        vm.dateCurrent = response.data['pagination']['date_current']
        vm.today = response.data['pagination']['today']
        vm.calendar = response.data['data']['calendar']
        vm.tasks = response.data['data']['tasks']

        vm.setYearMonth(vm.dateCurrent.split('-'))
        vm.initializeShowMore()
        vm.getRandomColor()
        vm.firstInit = true
      })
      .catch(function () {
      })
    },
    onResize () {
      this.isMobile = window.innerWidth < 600
    }
  }
}
</script>
