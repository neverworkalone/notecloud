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
            v-for="question in questions"
            :key="question.id"
            style="cursor: pointer;"
            @click="answer(question)"
          >
            <td
              width="90"
              class="pa-0"
            >
              {{ getDateOrTime(question.date_or_time.created) }}
            </td>
            <td
              class="pa-1"
            >
              <v-icon
                small
                color="brown lighten-2"
                v-if="question.state == $const('QUESTION_STATE_NEW')"
              >
                mdi-email-plus-outline
              </v-icon>
              <v-icon
                small
                color="primary"
                v-else-if="question.state == $const('QUESTION_STATE_OPEN')"
              >
                mdi-email-open-outline
              </v-icon>
              <v-icon
                small
                color="success"
                v-else-if="question.state == $const('QUESTION_STATE_CLOSED')"
              >
                mdi-email
              </v-icon>
              <v-icon
                small
                color="error"
                v-else
              >
                mdi-trash-can-outline
              </v-icon>
              {{ question.title }}
            </td>
            <td
              width="150"
              class="text-center pa-0"
            >
              {{ getUserInfo(question) }}
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
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'
import Pagination from '@/components/Pagination'

export default {
  mixins: [
    FormatDate,
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
      questions: null,
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

    this.searchQuestions(this.q)
  },
  methods: {
    firstPage: function () {
      this.searchQuestions(null, this.pagination.firstLink)
    },
    prevPage: function () {
      this.searchQuestions(null, this.pagination.prevLink)
    },
    nextPage: function () {
      this.searchQuestions(null, this.pagination.nextLink)
    },
    searchQuestions: function (q, url=null) {
      var vm = this

      if (!url) {
        url = this.$api('FORUMS_SEARCH_QUESTIONS').url.replace(
          '{q}', q
        )
      }

      axios({
        method: this.$api('FORUMS_SEARCH_QUESTIONS').method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.questions = response.data['data']
        vm.firstInit = true
      })
    },
    getUserInfo: function (question) {
      if (question.user) {
        return question.user.username
      }
      else {
        return question.address
      }
    },
    answer: function (question) {
      this.$router.push({
        name: 'forums.answer',
        params: {
          menu: this.menuIndex,
          page: this.pagination.currentPage,
          pk: question.id
        },
        query: {
          q: this.q
        }
      })
    }
  }
}
</script>
