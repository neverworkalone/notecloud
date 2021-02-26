<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="content pt-0"
    >
      <v-simple-table>
        <tbody>
          <tr
            v-for="task in tasks"
            :key="task.id"
            style="cursor: pointer;"
            @click="goToDate(task)"
          >
            <td
              width="120"
            >
              {{ getDate(task) }}
            </td>
            <td>
              <v-icon
                color="success"
                v-if="task.is_completed"
              >
                mdi-check-circle
              </v-icon>
              {{ task.content }}
            </td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-container>

    <Pagination
      :pagination="pagination"
      :first="firstPage"
      :prev="prevPage"
      :next="nextPage"
    />

  </div>
</template>

<script>
import axios from 'axios'
import Mobile from '@/mixins/mobile'
import Pagination from '@/components/Pagination'

export default {
  mixins: [
    Mobile
  ],
  components: {
    Pagination
  },
  data () {
    return {
      pagination: {
        pageTotal: 1,
        currentPage: 1,
        firstLink: null,
        prevLink: null,
        nextLink: null
      },
      page: 1,
      q: null,
      tasks: null,
      firstInit: false
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.page = this.$route.query.page
    if (!this.page) {
      this.page = 1
    }
    this.q = this.$route.query.q

    this.searchTask(this.q)
  },
  methods: {
    firstPage: function () {
      this.searchTask(null, this.pagination.firstLink)
    },
    prevPage: function () {
      this.searchTask(null, this.pagination.prevLink)
    },
    nextPage: function () {
      this.searchTask(null, this.pagination.nextLink)
    },
    searchTask: function (q, url=null) {
      var vm = this

      if (!url) {
        url = this.$api('NOTES_SEARCH_TASKS').url.replace(
          '{q}', q
        )
      }

      axios({
        method: this.$api('NOTES_SEARCH_TASKS').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.tasks = response.data['data']
        vm.firstInit = true
      })
    },
    getDate: function (task) {
      if (task.date_until) {
        return task.date_until
      }
      else {
        return task.date_from
      }
    },
    goToDate: function (task) {
      this.$router.push({
        name: 'notes.tasks',
        query: {
          date: this.getDate(task)
        }
      })
    }
  }
}
</script>
