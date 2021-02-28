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
          src="@/assets/images/home/title_slim.png"
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
          <v-sheet
            v-if="sampleImageMobile1"
          >
            <v-img :src="sampleImageMobile1.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImageMobile2"
          >
            <v-img :src="sampleImageMobile2.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImageMobile3"
          >
            <v-img :src="sampleImageMobile3.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImageMobile4"
          >
            <v-img :src="sampleImageMobile4.src"></v-img>
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
          <v-sheet
            v-if="sampleImage1"
          >
            <v-img :src="sampleImage1.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImage2"
          >
            <v-img :src="sampleImage2.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImage3"
          >
            <v-img :src="sampleImage3.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImage4"
          >
            <v-img :src="sampleImage4.src"></v-img>
          </v-sheet>
        </v-carousel-item>
        <v-carousel-item>
          <v-sheet
            v-if="sampleImage5"
          >
            <v-img :src="sampleImage5.src"></v-img>
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
      ],
      sampleImage1: null,
      sampleImage2: null,
      sampleImage3: null,
      sampleImage4: null,
      sampleImage5: null,
      sampleImageMobile1: null,
      sampleImageMobile2: null,
      sampleImageMobile3: null,
      sampleImageMobile4: null
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  },
  mounted () {
    if (this.isMobile) {
      this.preloadMobile()
    }
    else {
      this.preloadDesktop()
    }
  },
  methods: {
    preloadDesktop: function () {
      var sampleSrc = [
        'https://cdn.checkcheck.one/images/home/sample1.png',
        'https://cdn.checkcheck.one/images/home/sample2.png',
        'https://cdn.checkcheck.one/images/home/sample3.png',
        'https://cdn.checkcheck.one/images/home/sample4.png',
        'https://cdn.checkcheck.one/images/home/sample5.png'
      ]
      this.sampleImage1 = new Image()
      this.sampleImage1.src = sampleSrc[0]
      this.sampleImage2 = new Image()
      this.sampleImage2.src = sampleSrc[1]
      this.sampleImage3 = new Image()
      this.sampleImage3.src = sampleSrc[2]
      this.sampleImage4 = new Image()
      this.sampleImage4.src = sampleSrc[3]
      this.sampleImage5 = new Image()
      this.sampleImage5.src = sampleSrc[4]
    },
    preloadMobile: function () {
      var sampleSrc = [
        'https://cdn.checkcheck.one/images/home/sample_mobile1.png',
        'https://cdn.checkcheck.one/images/home/sample_mobile2.png',
        'https://cdn.checkcheck.one/images/home/sample_mobile3.png',
        'https://cdn.checkcheck.one/images/home/sample_mobile4.png'
      ]
      this.sampleImageMobile1 = new Image()
      this.sampleImageMobile1.src = sampleSrc[0]
      this.sampleImageMobile2 = new Image()
      this.sampleImageMobile2.src = sampleSrc[1]
      this.sampleImageMobile3 = new Image()
      this.sampleImageMobile3.src = sampleSrc[2]
      this.sampleImageMobile4 = new Image()
      this.sampleImageMobile4.src = sampleSrc[3]
    }
  }
}
</script>
