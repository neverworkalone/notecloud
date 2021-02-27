<template>
  <v-container
    class="content pt-0"
  >
    <v-sheet
      color="#eee"
      elevation="3"
      class="mb-5 pa-5"
    >
      {{ $t('FAQ.content4') }}
    </v-sheet>

    <v-container>
      <v-form
        v-model="validation"
      >
        <v-text-field
          v-model="address"
          :label="$t('forums.QUESTION_ADDRESS_LABEL')"
        >
        </v-text-field>
        <v-text-field
          v-model="title"
          :rules="[rules.required]"
          :label="$t('forums.QUESTION_TITLE_LABEL')"
          class="mb-4"
        >
        </v-text-field>
        <v-textarea
          v-model="content"
          :rules="[rules.required]"
          :label="$t('forums.QUESTION_CONTENT_LABEL')"
          background-color="grey lighten-5"
          auto-grow
          outlined
        >
        </v-textarea>

        <v-container
          class="text-center"
        >
          <v-btn
            color="primary"
            class="mb-10"
            @click="submit"
          >
            {{ $t('info.CONTACT') }}
          </v-btn>
        </v-container>
      </v-form>

    </v-container>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      validation: false,
      address: '',
      title: '',
      content: '',
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
      }
    }
  },
  mounted () {
  },
  methods: {
    submit: function () {
      var vm = this

      if (!this.validation) {
        this.$dialog.notify.info(
          this.$t('common.INPUT_ERROR'), {
            position: 'top-right'
          }
        )
        return
      }

      var address = null
      if (this.address) {
        address = this.address
      }

      axios({
        method: this.$api('FORUMS_NEW_QUESTION').method,
        url: this.$api('FORUMS_NEW_QUESTION').url,
        data: {
          address: address,
          title: this.title,
          content: this.content
        },
      })
      .then(function () {
        vm.$dialog.notify.success(
          vm.$t('forums.CONTACT_COMPLETED'), {
            position: 'bottom-right'
          }
        )
        vm.$router.push({ name: 'home' })
      })
    }
  }
}
</script>
