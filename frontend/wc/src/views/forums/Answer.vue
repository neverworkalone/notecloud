<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="pa-0"
    >
      <v-container
        class="pa-0 text-h4"
      >
        {{ question.title }}
      </v-container>

      <v-container>
        <v-chip
          :color="stateColor"
          class="mr-2"
        >
          {{ state }}
        </v-chip>
        {{ question.created_at }}
      </v-container>

      <v-container
        class="text-body-1"
      >
        {{ question.content }}
      </v-container>

      <v-textarea
        v-model="question.answer"
        :label="$t('forums.ANSWER_LABEL')"
        background-color="grey lighten-4"
        auto-grow
        outlined
      >
      </v-textarea>

      <v-container>
        <v-row
          class="mb-6 ml-3 mr-3"
        >
          <v-btn
            block
            large
            elevation="9"
            color="blue-grey lighten-4"
            @click="$router.go(-1)"
            v-if="q"
          >
            {{ $t('common.BACK') }}
          </v-btn>
          <v-btn
            block
            large
            elevation="9"
            color="blue-grey lighten-4"
            :to="{
              name: 'forums.questionsPage',
              params: {
                menu: menuIndex,
                page: page
              }
            }"
            v-else
          >
            {{ $t('common.BACK') }}
          </v-btn>
        </v-row>
        <v-row
          class="text-center"
        >
          <v-col>
            <v-btn
              color="primary"
              @click="save($const('QUESTION_STATE_OPEN'))"
            >
              {{ $t('forums.QUESTION_OPEN') }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              color="success"
              @click="save($const('QUESTION_STATE_CLOSED'))"
            >
              {{ $t('forums.QUESTION_CLOSED') }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              color="error"
              @click="save($const('QUESTION_STATE_DELETED'))"
            >
              {{ $t('common.DELETE') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <v-container
        class="text-right caption pa-0"
        v-if="question.state != $const('QUESTION_STATE_NEW')"
      >
         {{ updated_at }}
      </v-container>

    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      menuIndex: 0,
      page: 1,
      q: null,
      question: null,
      state: null,
      answer: null,
      firstInit: false
    }
  },
  computed: {
    stateColor () {
      if (this.state == this.$const('QUESTION_STATE_OPEN')) {
        return 'primary'
      }
      else if (this.state == this.$const('QUESTION_STATE_CLOSED')) {
        return 'success'
      }
      else if (this.state == this.$const('QUESTION_STATE_DELETED')) {
        return 'error'
      }
      else {
        return 'brown lighten-2'
      }
    },
    updated_at () {
      return this.$t('editor.LAST_UPDATED_AT', {
        date_or_time: this.question.updated_at
      })
    },
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
    this.q = this.$route.query.q

    this.getQuestion(this.$route.params.pk)
  },
  methods: {
    getQuestion: function (pk) {
      var vm = this

      axios({
        method: this.$api('FORUM_QUESTION').method,
        url: this.$api('FORUM_QUESTION').url.replace(
          '{pk}', pk
        )
      })
      .then(function (response) {
        vm.question = response.data['data']
        vm.state = vm.question.state
        vm.firstInit = true
      })
    },
    save: function (state) {
      var vm = this

      axios({
        method: this.$api('FORUMS_ANSWER_QUESTION').method,
        url: this.$api('FORUMS_ANSWER_QUESTION').url.replace(
          '{pk}', this.question.id
        ),
        data: {
          state: state,
          answer: this.question.answer
        }
      })
      .then(function () {
        vm.$dialog.notify.success(
          vm.$t('memo.MEMO_SAVED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
    }
  }
}
</script>
