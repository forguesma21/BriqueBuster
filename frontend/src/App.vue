<template>
  <div id="app">
    <NavBar />
    <router-view />
    <PiedPage />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import NavBar from '@/components/NavBar.vue'
import PiedPage from './components/common/PiedPage.vue'

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    PiedPage
  }
})
</script>
