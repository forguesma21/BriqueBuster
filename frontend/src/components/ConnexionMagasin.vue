<template>
  <div class="flex justify-center items-center min-h-screen">
    <div class="bg-white p-8 rounded-xl w-full max-w-md">
      <h2 class="font-sans text-3xl  text-center text-gray-800 mb-6">SE CONNECTER</h2>
      <p class="text-center font-bold text-gray-600 mb-8">Bienvenue chez Brique Buster</p>

      <form @submit.prevent="submitForm" class="space-y-6">
        <!-- Email -->
        <div>
          <label for="email" class="block text-sm mb-2 text-gray-700">COURRIEL</label>
          <input v-model="email" required :type="email" :id="email" placeholder="VOTRE COURRIEL"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500">
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm mb-2 text-gray-700">MOT DE PASSE</label>
          <input v-model="password" required :type="password" :id="password" placeholder="VOTRE MOT DE PASSE"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input type="checkbox" id="remember-me" class="mr-2">
            <label for="remember-me" class="text-gray-600">Remember me</label>
          </div>
          <a href="#" class="text-purple-600 text-sm">Recover password</a>
        </div>

        <ButtonRetro @click="connexion" class="w-full">
          SE CONNECTER
        </ButtonRetro>

        </form>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import ButtonRetro from "@/components/common/ButtonRetro.vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useToast } from "vue-toastification";
import { connexionUtilisateur } from '../api/utilisateurs.js';


 export default defineComponent({
    name: "ConnexionMagasin",
    components: {ButtonRetro},
    data() {
      return {
        email:'',
        password: ''
      }
    },
    setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast();

    const logIn = (userID: string) => {
      store.commit('login', userID)
      if (router.currentRoute.value.path.startsWith('/connexion')) {
        router.push('/accueil')
      }
    }

    return {
      logIn,
      toast
    }
  },
    methods : {
      async connexion() {
        if (this.validationConnexion()) {
         try {
            const utilisateur = {
                      courriel: this.email,
                      motDePasse: this.password
                    };
           const response = await connexionUtilisateur(utilisateur); // Appel de ton API

        if (response && response.utilisateurID) {
          this.logIn(response.utilisateurID);
        } else {
          this.toast.error("Erreur dans la réponse de l'API", {
            toastClassName: "bg-BbRed font-bold"
          });
        }
      } catch (error) {
        this.toast.error("Le courriel ou le mot de passe est invalide. Veuillez réessayer.", {
          toastClassName: "bg-BbRed font-bold"
        });
      }
    }
      },
      validationConnexion() {
        return this.courrielValide(this.email) && this.motDePasseValide(this.password)
      },
      courrielValide(courriel: string) {
        const formatCourriel = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(!formatCourriel.test(courriel)) {
          this.toast.warning("Le courriel ne respecte pas le format requis.", {toastClassName: "bg-trempanilloBeige font-bold"});
          return false;
        }
        return true;
      },
      motDePasseValide(motDePasse: string) {
        if (motDePasse.length == 0) {
          this.toast.warning("Le mot de passe ne peut pas être vide.", {toastClassName: "bg-trempanilloBeige font-bold"});
          return false;
        }
        return true;
      }
    }
  });
</script>

