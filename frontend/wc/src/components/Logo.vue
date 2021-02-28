<template>
  <v-badge
    content="Beta"
    overlap
    :offset-y="30"
  >

    <router-link
      :to="to"
      v-if="to"
    >
      <v-img
        src="@/assets/images/home/checkcheck.png"
        width="144"
        height="60"
      ></v-img>
    </router-link>

    <v-img
      src="@/assets/images/home/checkcheck.png"
      width="144"
      height="60"
      v-else
    ></v-img>

  </v-badge>
</template>

<script>
export default {
  props: {
    to: Object
  }
}
</script>
