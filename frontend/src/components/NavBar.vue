<template>
  <nav class="BbWhite p-4">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex flex-row items-center">
        <div class="flex flex-col items-center text-sm">
          <router-link to="/accueil">
            <img src="/BriqueB_logo.svg" alt="Logo Brique Buster" class="w-20 h20 hover:color-trempanilloCyan" />
          </router-link>
        </div>
      </div>

      <div class="hidden md:flex space-x-8">
        <router-link to="/accueil">
          <ButtonRetro>Shop</ButtonRetro>
        </router-link>

        <router-link to="/connexion">
          <ButtonRetro v-if="!loggedIn">Se Connecter</ButtonRetro>
        </router-link>

        <router-link to="/inscription">
          <ButtonRetro v-if="!loggedIn">S'inscrire</ButtonRetro>
        </router-link>

        <router-link to="/utilisateur">
          <ButtonRetro v-if="loggedIn">Compte</ButtonRetro>
        </router-link>

        <ButtonRetro @click="logOutAccount" v-if="loggedIn">Se Déconnecter</ButtonRetro>
      </div>

      <div class="flex items-center space-x-4">
        <router-link to="/accueil">
          <ButtonRetro>Recherche</ButtonRetro>
        </router-link>

        <router-link to="/utilisateur">
          <ButtonRetro class="flex items-center space-x-2 px-4 py-2 rounded">
            <svg class="w-6 h-6 text-black-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 3h18M3 3l3 18h12L21 3M3 3l4 4M17 7l4 4M5 19h14"></path>
            </svg>
            <div class="border-l-2 h-6 mx-2"></div>
            <span>0</span>
          </ButtonRetro>
        </router-link>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div class="md:hidden">
      <ButtonRetro>
        Toggle Menu
      </ButtonRetro>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { computed } from 'vue'

import ButtonRetro from '@/components/common/ButtonRetro.vue'

const store = useStore()
const router = useRouter()
const toast = useToast()

const loggedIn = computed(() => store.state.loggedIn)
const userName = computed(() => store.state.userName)

const logOut = () => {
  store.dispatch('logout')
  if (router.currentRoute.value.path.startsWith('/utilisateur')) {
    router.push('/accueil')
  }
}

const logOutAccount = () => {
  toast.success(`Au revoir ${userName.value} !`, {
    toastClassName: 'bg-green-500 text-white font-bold'
  })
  logOut()
}
</script>

<style scoped>
</style>
