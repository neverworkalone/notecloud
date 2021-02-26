<template>
  <div
    v-if="initialized"
  >

    <v-bottom-navigation
      v-model="menuIndex"
      background-color="#ECEFF1"
      class="mb-5"
      color="primary"
      shift
      grow
    >
      <v-btn
        @click="getQuestions($const('QUESTION_MENU_NEW'))"
      >
        <span>{{ $t('forums.QUESTION_NEW') }}</span>
        <v-icon>mdi-email-plus-outline</v-icon>
      </v-btn>

      <v-btn
        @click="getQuestions($const('QUESTION_MENU_OPEN'))"
      >
        <span>{{ $t('forums.QUESTION_OPEN') }}</span>
        <v-icon>mdi-email-open-outline</v-icon>
      </v-btn>

      <v-btn
        @click="getQuestions($const('QUESTION_MENU_CLOSED'))"
      >
        <span>{{ $t('forums.QUESTION_CLOSED') }}</span>
        <v-icon>mdi-email</v-icon>
      </v-btn>

      <v-btn
        @click="getQuestions($const('QUESTION_MENU_DELETED'))"
      >
        <span>{{ $t('forums.QUESTION_DELETED') }}</span>
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>
    </v-bottom-navigation>

    <v-container
      class="content pt-0"
    >
      <v-simple-table>
        <tbody>
          <tr
            v-for="question in questions"
            :key="question.id"
            @click="answer(question)"
            style="cursor: pointer;"
          >
            <td>
              <v-icon
                :color="question.user.is_prime ? 'info': 'grey'"
                v-if="question.user"
              >
                mdi-account-outline
              </v-icon>
              <v-icon
                color="info"
                v-if="question.address"
              >
                mdi-cellphone-basic
              </v-icon>
              {{ question.title }}

              <div
                class="ml-7"
                v-if="isMobile"
              >
                {{ getDateOrTime(question.date_or_time.created) }}
              </div>
            </td>
            <td
              width="120"
              v-if="!isMobile"
            >
              {{ getDateOrTime(question.date_or_time.created) }}
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
      menuIndex: 0,
      page: 1,
      questions: '',
      firstInit: false
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.menuIndex = this.$route.params.menu
    if (!this.menuIndex) {
      this.menuIndex = this.$const('QUESTION_MENU_DEFAULT')
    }
    this.page = this.$route.params.page
    if (!this.page) {
      this.page = 1
    }

    this.getQuestions(this.menuIndex, null, this.page)
  },
  methods: {
    firstPage: function () {
      this.getQuestions(this.menuIndex, this.pagination.firstLink)
    },
    prevPage: function () {
      this.getQuestions(this.menuIndex, this.pagination.prevLink)
    },
    nextPage: function () {
      this.getQuestions(this.menuIndex, this.pagination.nextLink)
    },
    getQuestions: function (index=0, url=null, page=0) {
      var vm = this
      var method = 'get'

      if (!page) {
        page = 1
      }

      if (!url) {
        var apiType = 'FORUMS_QUESTIONS_NEW'

        if (index == this.$const('QUESTION_MENU_OPEN')) {
          apiType = 'FORUMS_QUESTIONS_OPEN'
        }
        else if (index == this.$const('QUESTION_MENU_CLOSED')) {
          apiType = 'FORUMS_QUESTIONS_CLOSED'
        }
        else if (index == this.$const('QUESTION_MENU_DELETED')) {
          apiType = 'FORUMS_QUESTIONS_DELETED'
        }
        method = this.$api(apiType).method
        url = this.$api(apiType).url.replace(
          '{page}', page
        )
      }

      axios({
        method: method,
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
      .catch(function () {
      })
    },
    answer: function (question) {
      this.$router.push({
        name: 'forums.answer',
        params: {
          menu: this.menuIndex,
          page: this.pagination.currentPage,
          pk: question.id
        }
      })
    }
  }
}
</script>
