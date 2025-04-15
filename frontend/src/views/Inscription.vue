<template>
  <div class="flex justify-center items-center min-h-screen">
    <div class="bg-white p-8 rounded-xl w-full max-w-md">
      <h2 class="font-sans text-3xl text-center text-gray-800 mb-6">S'INSCRIRE</h2>
      <p class="text-center font-bold text-gray-600 mb-8">Bienvenue chez Brique Buster</p>

      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label for="firstname" class="block text-sm mb-2 text-gray-700">PRÉNOM</label>
          <input
            v-model="firstname"
            required
            :type="firstname"
            :id="firstname"
            placeholder="VOTRE PRÉNOM"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div>
          <label for="lastname" class="block text-sm mb-2 text-gray-700">NOM</label>
          <input
            v-model="lastname"
            required
            :type="lastname"
            :id="lastname"
            placeholder="VOTRE NOM"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

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

        <ButtonRetro @click="inscription" class="w-full"> S'INSCRIRE </ButtonRetro>
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
import { inscriptionUtilisateur } from '@/api/utilisateurs'

const email = ref('')
const password = ref('')
const firstname = ref('')
const lastname = ref('')

const store = useStore()
const router = useRouter()
const toast = useToast()

const logIn = (userID: string) => {
  store.commit('login', userID)
  if (router.currentRoute.value.path.startsWith('/inscription')) {
    router.push('/accueil')
  }
}

const inscription = async () => {
  if (validationInscription()) {
    console.log("Attempt d'inscription")

    try {
      const utilisateur = {
        prenom: firstname.value,
        nom: lastname.value,
        motDePasse: password.value,
        courriel: email.value
      }

      console.log(utilisateur)
      const response = await inscriptionUtilisateur(utilisateur)
      logIn(response.utilisateurID)
    } catch (error: any) {
      const message =
        error?.response?.data?.message || error?.message || 'Une erreur inconnue est survenue'

      toast.error(message)
    }
  }
}

const validationInscription = () => {
  return (
    courrielValide(email.value) &&
    motDePasseValide(password.value) &&
    nomValide(lastname.value) &&
    prenomValide(firstname.value)
  )
}

const courrielValide = (courriel: string) => {
  const formatCourriel = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formatCourriel.test(courriel)) {
    toast.warning('Le courriel ne respecte pas le format requis.')
    return false
  }
  return true
}

const motDePasseValide = (motDePasse: string) => {
  const formatMotDePasse = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
  if (!formatMotDePasse.test(motDePasse)) {
    toast.warning('Le mot de passe ne respecte pas le format requis.')
    toast.warning(
      '1. Le mot de passe doit contenir au moins une lettre minuscule (a-z).\n' +
        '2. Le mot de passe doit contenir au moins une lettre majuscule (A-Z).\n' +
        '3. Le mot de passe doit contenir au moins un chiffre (0-9).\n' +
        '4. Le mot de passe doit contenir au moins un caractère spécial parmi ceux-ci : @ $ ! % * ? &\n' +
        "5. Le mot de passe doit être composé d'au moins 8 caractères."
    )
    return false
  }
  return true
}

const nomValide = (nom: string) => {
  const noSpaceName = nom.trim()
  if (noSpaceName.length === 0) {
    toast.warning('Le nom ne peut pas être vide.')
    return false
  }
  return true
}

const prenomValide = (prenom: string) => {
  const noSpaceFirstName = prenom.trim()
  if (noSpaceFirstName.length === 0) {
    toast.warning('Le prénom ne peut pas être vide.')
    return false
  }
  return true
}
</script>
