<template>
  <v-container
    class="pa-0"
  >
    <v-container
      class="pt-0"
      style="font-size:32px;"
    >
      <b>
        {{ $t('FAQ.title') }}
      </b>
    </v-container>
    <v-expansion-panels
      focusable
    >
      <v-expansion-panel
        v-for="(item, i) in items"
        :key="i"
      >
        <v-expansion-panel-header>
          {{ $t(item.header) }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          {{ $t(item.content) }}
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      items: [
        {
          header: 'FAQ.header1',
          content: 'FAQ.content1'
        },
        {
          header: 'FAQ.header2',
          content: 'FAQ.content2'
        },
        {
          header: 'FAQ.header3',
          content: 'FAQ.content3'
        },
        {
          header: 'FAQ.header4',
          content: 'FAQ.content4'
        }
      ]
    }
  }
}
</script>

<style lang="scss">
.v-expansion-panel-content {
  padding-top:20px !important;
}
</style>
