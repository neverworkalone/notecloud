<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="pa-0"
    >
      <v-text-field
        v-model="memo.title"
        outlined
        dense
      >
      </v-text-field>
    </v-container>
    <v-container
      class="content pa-0"
    >
      <TipTap
        class="mb-5"
        :options="options"
      />
    </v-container>

    <v-container
      class="text-center pb-0"
    >
      <v-btn
        :to="{
          name: 'notes.memoPage',
          params: {
            menu: menuIndex,
            page: page
          },
          query: {
            q: q
          }
        }"
      >
        {{ $t('common.BACK') }}
      </v-btn>

      <v-btn
        color="primary"
        class="ml-5"
        @click="save()"
      >
        {{ $t('common.SAVE') }}
      </v-btn>
    </v-container>
    <v-container
      class="text-right caption pa-0"
    >
       {{ updated_at }}
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import TipTap from '@/components/TipTap'
import FormatDate from '@/mixins/formatDate'

export default {
  mixins: [
    FormatDate
  ],
  components: {
    TipTap
  },
  data () {
    return {
      options: {
        content: ''
      },
      menuIndex: 1,
      page: 1,
      q: null,
      memo: null,
      firstInit: false
    }
  },
  computed: {
    title () {
      return this.memo.title
    },
    content () {
      return this.memo.content
    },
    updated_at () {
      return this.$t('editor.LAST_UPDATED_AT', {
        date_or_time: this.getDateOrTime(this.memo.date_or_time)
      })
    },
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.menuIndex = this.$route.params.menu
    if (!this.menuIndex) {
      this.menuIndex = this.$const('MEMO_MENU_DEFAULT')
    }
    this.page = this.$route.params.page
    if (!this.page) {
      this.page = 1
    }

    this.q = this.$route.query.q

    this.getMemo(this.$route.params.pk)
  },
  async beforeRouteLeave (to, from, next) {
    if (this.memo.content == this.options.content) {
      next()
    }
    else {
      const res = await this.$dialog.confirm({
        text: this.$t('editor.QUIT_EDITING'),
        actions: {
          false: {
            text: this.$t('common.CANCEL')
          },
          true: {
            color: 'primary',
            text: this.$t('common.OK'),
          }
        }
      })
      if (res) {
        next()
      }
      else {
        next(false)
      }
    }
  },
  methods: {
    save: function () {
      var vm = this

      axios({
        method: this.$api('NOTES_EDIT_MEMO').method,
        url: this.$api('NOTES_EDIT_MEMO').url.replace(
          '{pk}', this.memo.id
        ),
        data: {
          title: this.memo.title,
          content: this.options.content
        }
      })
      .then(function (response) {
        vm.memo = response.data['data']

        vm.$dialog.notify.success(
          vm.$t('memo.MEMO_SAVED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function (error) {
        if (error.response && error.response.data) {
          for (var field in error.response.data) {
            vm.$dialog.notify.info(
              field + ': ' + error.response.data[field], {
                position: 'top-right'
              }
            )
          }
        }
      })
    },
    getMemo: function (pk) {
      var vm = this

      axios({
        method: this.$api('NOTES_VIEW_MEMO').method,
        url: this.$api('NOTES_VIEW_MEMO').url.replace(
          '{pk}', pk
        )
      })
      .then(function (response) {
        vm.memo = response.data['data']
        vm.options.content = vm.memo.content
        vm.firstInit = true
      })
      .catch(function () {
      })
    }
  }
}
</script>
