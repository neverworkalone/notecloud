<template>
  <div
    v-if="initialized"
  >
    <div class="content pt-0 pl-0 pr-0">
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
              v-for="item in data"
              :key="item.date"
              class="text-center pa-0"
            >
              <v-btn
                small
                depressed
                class="pt-5 pb-5"
                :color="weekdayColor(item)"
                @click="setDateCurrent(item)"
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
          <v-col
            v-for="task in selectedTasks"
            :key="task.id"
            :cols="isMobile ? '' : 'auto'"
            class="mr-auto"
          >
            <v-card
              :color="task.color"
              :min-width="$const('TASK_CARD_MIN_WIDTH')"
              :max-width="$const('TASK_CARD_MAX_WIDTH')"
              elevation="8"
            >
              <v-card-actions>
                <v-card-subtitle>
                  <v-hover v-slot="{ hover }">
                    <v-icon
                      class="mr-2"
                      :color="getCheckColor(hover, task)"
                      @click="toggleComplete(task)"
                    >
                      mdi-check-circle-outline
                    </v-icon>
                  </v-hover>
                  {{ getTaskDate(task) }}
                </v-card-subtitle>
                <v-spacer></v-spacer>
              </v-card-actions>
              <v-card-title
                v-text="task.content"
                v-if="!task.is_completed"
              ></v-card-title>
              <v-card-title
                v-if="task.is_completed"
                v-text="task.content"
                class="text-decoration-line-through"
              ></v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      selectedDay: '',
      dateBefore: '',
      dateAfter: '',
      dateCurrent: '',
      today: '',
      year: '',
      month: '',
      data: '',
      selectedTasks: '',
      isMobile: false,
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
    initialized () {
      return this.firstInit
    }
  },
  beforeDestroy () {
    if (typeof window === 'undefined') return
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
    badgeValue: function (item) {
      if (item.tasks.length == 0) {
        return false
      }
      else {
        return true
      }
    },
    badgeColor: function (item) {
      for (var i=0; i<item.tasks.length; i++) {
        if (item.tasks[i].is_completed == false) {
          return "red"
        }
      }

      if (item.tasks.length == 0) {
        return "white"
      }
      else {
        return "black"
      }
    },
    getCalendarDay: function (date) {
      return parseInt(date.split('-')[2])
    },
    setDateCurrent: function (item) {
      this.dateCurrent = item.date
      this.selectedTasks = item.tasks
    },
    getCheckColor: function (hover, task) {
      if (task.is_completed) {
        if (hover) {
          return ''
        }
        else {
          return 'success'
        }
      }
      else {
        if (hover) {
          return 'success'
        }
        else {
          return ''
        }
      }
    },
    getTaskDate: function (task) {
      var dateStr = task.date_from + ' ~ '
      if (task.is_completed) {
        dateStr += task.date_until
      }

      return dateStr
    },
    toggleComplete: function (task) {
      var vm = this

      axios({
        method: 'post',
        url: '/notes/tasks/' + task.id + '/complete/'
      })
      .then(function (response) {
        var completedData = response.data['data']

        for (var i=0; i<vm.data.length; i++) {
          for (var j=0; j<vm.data[i].tasks.length; j++) {
            if (vm.data[i].tasks[j].id == completedData.id) {
              vm.data[i].tasks[j].is_completed = completedData.is_completed
              vm.data[i].tasks[j].date_until = completedData.date_until
            }
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
        vm.data = response.data['data']

        for (var i=0; i<vm.data.length; i++) {
          if (vm.data[i].date == vm.dateCurrent) {
            vm.selectedTasks = vm.data[i].tasks
            break
          }
        }

        vm.setYearMonth(vm.dateCurrent.split('-'))
        vm.firstInit = true
      })
      .catch(function () {
      })
    },
    onResize () {
      this.isMobile = window.innerWidth < 600
    },
  }
}
</script>
