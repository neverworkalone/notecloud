<template>
  <div
    v-if="initialized"
  >
    <div
      :class="isMobile ? 'content pt-0 pl-0 pr-0' : 'content pt-0'"
    >

      <v-dialog
        v-model="datePickerDialog"
        width="300"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-icon
            v-bind="attrs"
            v-on="on"
            small
          >
            mdi-calendar-month
          </v-icon>
          <div
            class="headline float-left"
            v-text="getYearMonth"
            v-bind="attrs"
            v-on="on"
          >
          </div>
        </template>
        <v-row
          justify="center"
        >
          <v-date-picker
             v-model="datePicker"
             elevation="15"
             class="ml-6 mr-0"
             :locale="($root.$i18n.locale == 'ko') ? 'ko-kr': 'en-us'"
             :day-format="pickerDayFormat"
           >
           </v-date-picker>
        </v-row>
        <v-row
          class="text-center ma-0 pt-3 pb-0"
        >
          <v-col
          >
            <v-btn
              color="primary"
              block
              @click="pickerMove()"
            >
              {{ $t('common.MOVE') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-dialog>

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

      <v-container
      >
        <v-dialog
          v-model="editDialog"
          transition="dialog-bottom-transition"
          width="90%"
          :max-width="$const('TASK_NEW_MAX_WIDTH')"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-row>
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
                    <v-row
                      align="center"
                      justify="space-around"
                      class="pa-7 pl-5 pr-2"
                    >
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

                      <v-menu
                        transition="slide-y-transition"
                        bottom
                        offset-y
                        class="mx-auto"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            small
                            text
                            class="ml-auto"
                            v-bind="attrs"
                            v-on="on"
                          >
                            <v-icon>mdi-dots-vertical</v-icon>
                          </v-btn>
                        </template>
                        <v-list>
                          <v-list-item
                            @click="copyToClipboard(task)"
                          >
                            <v-list-item-content>
                              <v-list-item-title>
                                <v-icon
                                  class="mr-1"
                                >
                                  mdi-clipboard-text-outline
                                </v-icon>
                                {{ $t('tasks.COPY_CONTENT') }}
                              </v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-divider></v-divider>
                          <v-list-item
                            two-line
                            @click="deleteTask(task)"
                          >
                            <v-list-item-content>
                              <v-list-item-title>
                                <v-icon
                                  color="error"
                                  class="mr-1"
                                >
                                  mdi-trash-can-outline
                                </v-icon>
                                <font color="error">
                                  {{ $t('tasks.DELETE_TASK') }}
                                </font>
                              </v-list-item-title>
                              <v-list-item-subtitle
                                class="ml-8"
                              >
                                {{ $t('tasks.DELETE_TASK_DESCRIPTION') }}
                              </v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </v-menu>
                    </v-row>
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
                      {{ formatDate(dateCurrent) }} ~
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
      </v-container>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  data () {
    return {
      datePickerDialog: false,
      datePicker: '',
      dateBefore: '',
      dateAfter: '',
      dateCurrent: '',
      today: '',
      year: '',
      month: '',
      calendar: '',
      tasks: '',
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
  mounted () {
    this.getTasks()
  },
  methods: {
    pickerDayFormat: function (day) {
      return parseInt(day.substr(8,9))
    },
    pickerMove: function () {
      this.getTasks(this.datePicker)
      this.datePickerDialog = false
    },
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
        this.randomColor = this.colors[this.$const('DEFAULT_COLOR_INDEX')]
      }
    },
    initializeEditDialog: function (task) {
      this.editID = task.id
      this.editContent = task.content
      this.editColor = task.color
      this.editDate = this.formatDate(task.date_from)
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
      var dateFrom = this.formatDate(task.date_from)
      var dateStr = dateFrom + ' ~ '
      if (task.is_completed) {
        var dateUntil = this.formatDate(task.date_until)
        dateStr += dateUntil
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
    copyToClipboard: function (task) {
      this.$clipboard(task.content)
      this.$dialog.notify.success(
        this.$t('tasks.COPIED_TO_CLIPBOARD'), {
          position: 'bottom-right',
          timeout: 2000
        }
      )
    },
    editTask: function () {
      var vm = this

      axios({
        method: this.$api('NOTES_EDIT_TASK').method,
        url: this.$api('NOTES_EDIT_TASK').url.replace(
          '{pk}', this.editID
        ),
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
            break
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
        method: this.$api('NOTES_NEW_TASK').method,
        url: this.$api('NOTES_NEW_TASK').url,
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
        method: this.$api('NOTES_COMPLETE_TASK').method,
        url: this.$api('NOTES_COMPLETE_TASK').url.replace(
          '{pk}', task.id
        )
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == data.id) {
            vm.tasks[i].is_completed = data.is_completed
            vm.tasks[i].date_until = data.date_until

            if (data.is_completed) {
              vm.$dialog.notify.success(
                vm.$t('tasks.TASK_COMPLETED'), {
                  position: 'bottom-right',
                  timeout: 2000
                }
              )
            }
            break
          }
        }
      })
      .catch(function () {
      })
    },
    updateColor: function (id, color) {
      var vm = this

      axios({
        method: this.$api('NOTES_EDIT_TASK').method,
        url: this.$api('NOTES_EDIT_TASK').url.replace(
          '{pk}', id
        ),
        data: {
          color: color,
        },
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == data.id) {
            vm.tasks[i].color = data.color
            break
          }
        }
      })
      .catch(function () {
      })
    },
    deleteTask: function (task) {
      var vm = this

      axios({
        method: this.$api('NOTES_DELETE_TASK').method,
        url: this.$api('NOTES_DELETE_TASK').url.replace(
          '{pk}', task.id
        )
      })
      .then(function () {
        for (var i=0; i<vm.tasks.length; i++) {
          if (vm.tasks[i].id == task.id) {
            vm.tasks.splice(i, 1)
            break
          }
        }

        vm.$dialog.notify.success(
          vm.$t('common.DELETED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function () {
      })
    },
    getTasks: function (date) {
      var vm = this
      var url = this.$api('NOTES_TASKS').url

      if (date) {
        url = this.$api('NOTES_TASKS_DATE').url.replace(
          '{date}', date
        )
      }

      axios({
        method: this.$api('NOTES_TASKS').method,
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

        vm.datePicker = vm.dateCurrent
        vm.firstInit = true
      })
      .catch(function () {
      })
    }
  }
}
</script>

<style lang="scss">
.v-card__title {
  white-space: break-spaces;
}
</style>
