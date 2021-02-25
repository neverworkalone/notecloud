<template>
  <v-container
    class="pa-0"
  >
    <v-container
      class="content text-center pa-0"
    >
      <v-container
        class="pt-0"
        style="max-width:320px;"
      >
        <v-img
          src="@/assets/images/title_slim.png"
        ></v-img>
      </v-container>
      <v-container
        class="pb-1"
        :style="isMobile ? 'font-size:36px;' : 'font-size:72px;'"
      >
        <b>
          {{ $t('landing.CHECKCHECK_TODAY') }}
        </b>
      </v-container>
      <v-container
        class="pb-0"
        style="max-width:580px;"
      >
        <v-list>
          <v-list-item
            v-for="(slide, i) in slides"
            :key="i"
          >
            <p class="text-body-1">
              <v-icon>{{ slide.icon }}</v-icon>
              {{ $t(slide.text) }}
            </p>
          </v-list-item>
        </v-list>
      </v-container>
      <v-container
        class="mb-0"
      >
        <v-btn
          x-large
          color="primary"
          :to="user ? { name: 'notes.tasks' } : { name: 'accounts.signup' }"
        >
          <v-icon
            class="mr-2"
          >
            mdi-check
          </v-icon>
          {{ $t('landing.GET_IT_FREE') }}<br>
          {{ $t('landing.WITH_ONLY_EMAIL') }}
        </v-btn>
      </v-container>
    </v-container>

    <v-container
      class="content"
    >
      <v-carousel
        :continuous="false"
        :cycle="false"
        hide-delimiters
        height="550"
        v-if="isMobile"
      >
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample_mobile1.png"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample_mobile2.png"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample_mobile3.png"></v-img>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
      <v-carousel
        :continuous="false"
        :cycle="false"
        hide-delimiters
        v-else
      >
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample1.png"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample2.png"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample3.png"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet>
            <v-img src="@/assets/images/sample4.png"></v-img>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
    </v-container>

    <FAQ />

    <v-container
      class="content text-center"
    >
      <v-btn
        large
        color="primary"
        :to="{ name: 'forums.contact' }"
      >
        {{ $t('landing.CONTACT_US') }}
      </v-btn>
    </v-container>

  </v-container>
</template>

<script>
import Mobile from '@/mixins/mobile'
import FAQ from '@/components/FAQ'
import { mapState } from 'vuex'

export default {
  mixins: [
    Mobile
  ],
  components: {
    FAQ
  },
  data () {
    return {
      slides: [
        {
          icon: 'mdi-flash-circle',
          text: 'slides.1'
        },
        {
          icon: 'mdi-notebook-outline',
          text: 'slides.2'
        },
        {
          icon: 'mdi-web',
          text: 'slides.3'
        }
      ]
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  },
  mounted () {
  }
}
</script>
