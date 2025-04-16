<template>
  <div class="flex justify-center items-center min-h-screen">
    <div class="bg-white p-8 rounded-xl w-full max-w-md">
      <h2 class="font-sans text-3xl text-center text-gray-800 mb-6">SE CONNECTER</h2>
      <p class="text-center font-bold text-gray-600 mb-8">Bienvenue chez Brique Buster</p>

      <form @submit.prevent="submitForm" class="space-y-6">
        <!-- Email -->
        <div>
          <label for="email" class="block text-sm mb-2 text-gray-700">COURRIEL</label>
          <input
            v-model="email"
            required
            :type="email"
            :id="email"
            placeholder="VOTRE COURRIEL"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm mb-2 text-gray-700">MOT DE PASSE</label>
          <input
            v-model="password"
            required
            :type="password"
            :id="password"
            placeholder="VOTRE MOT DE PASSE"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input type="checkbox" id="remember-me" class="mr-2" />
            <label for="remember-me" class="text-gray-600">Remember me</label>
          </div>
          <a href="#" class="text-purple-600 text-sm">Recover password</a>
        </div>

        <ButtonRetro @click="connexion" class="w-full"> SE CONNECTER </ButtonRetro>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import ButtonRetro from '@/components/common/ButtonRetro.vue'
import { connexionUtilisateur } from '@/api/utilisateurs'

const email = ref('')
const password = ref('')

const toast = useToast()
const router = useRouter()
const store = useStore()

const courrielValide = (courriel: string): boolean => {
  const formatCourriel = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formatCourriel.test(courriel)) {
    toast.error('Le courriel ne respecte pas le format requis.')
    return false
  }
  return true
}

const motDePasseValide = (mdp: string): boolean => {
  if (mdp.length === 0) {
    toast.warning('Le mot de passe ne peut pas être vide.')
    return false
  }
  return true
}

const validationConnexion = () => {
  return courrielValide(email.value) && motDePasseValide(password.value)
}

const logIn = (userID: string) => {
  store.commit('login', userID)
  if (router.currentRoute.value.path.startsWith('/connexion')) {
    router.push('/accueil')
  }
}

const connexion = async () => {
  if (!validationConnexion()) return

  try {
    const utilisateur = {
      courriel: email.value,
      motDePasse: password.value
    }

    const response = await connexionUtilisateur(utilisateur)

    if (response && response.utilisateurID) {
      logIn(response.utilisateurID)
    } else {
      toast.error("Erreur dans la réponse de l'API")
    }
  } catch (error) {
    toast.error('Le courriel ou le mot de passe est invalide. Veuillez réessayer.')
  }
}
</script>
