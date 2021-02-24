<template>
  <div>
    <v-container
      class="pa-0"
    >
      <v-text-field
        v-model="title"
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
        @click="$router.push({ name: 'notes.memo' })"
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
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import TipTap from '@/components/TipTap'

export default {
  components: {
    TipTap
  },
  data () {
    return {
      options: {
        content: ''
      },
      title: '',
      saved: false
    }
  },
  async beforeRouteLeave (to, from, next) {
    if (this.saved || (!this.title && !this.options.content)) {
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
        method: this.$api('NOTES_NEW_MEMO').method,
        url: this.$api('NOTES_NEW_MEMO').url,
        data: {
          title: this.title,
          content: this.options.content
        }
      })
      .then(function () {
        vm.saved = true
        router.push({ name: 'notes.memo' })

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
    }
  }
}
</script>
