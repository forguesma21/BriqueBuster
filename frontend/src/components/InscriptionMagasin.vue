<template>
 <div class="flex justify-center items-center min-h-screen">
    <div class="bg-white p-8 rounded-xl w-full max-w-md">
      <h2 class="font-sans text-3xl  text-center text-gray-800 mb-6">S'INSCRIRE</h2>
      <p class="text-center font-bold text-gray-600 mb-8">Bienvenue chez Brique Buster</p>

      <form @submit.prevent="submitForm" class="space-y-6">
         <div>
          <label for="firstname" class="block text-sm mb-2 text-gray-700">PRÉNOM</label>
          <input v-model="firstname" required :type="firstname" :id="firstname" placeholder="VOTRE PRÉNOM"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500">
        </div>

         <div>
          <label for="lastname" class="block text-sm mb-2 text-gray-700">NOM</label>
          <input v-model="lastname" required :type="lastname" :id="lastname" placeholder="VOTRE NOM"
            class="placeholder:text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500">
        </div>

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

        <ButtonRetro @click="inscription" class="w-full">
          S'INSCRIRE
        </ButtonRetro>

        </form>
    </div>
  </div>
</template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useRouter } from "vue-router";
  import { useStore } from "vuex";
  import { useToast } from "vue-toastification";
  import ButtonRetro from "../components/common/ButtonRetro.vue";
  import { inscriptionUtilisateur } from '../api/utilisateurs.js';

  
  export default defineComponent({
    name: "InscriptionMagasin",
    components: {
      ButtonRetro
    },
    data() {
      return {
        email:'',
        password: '',
        firstname: '',
        lastname: '',
      }
    },
    setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast();

    const logIn = (userID: string) => {
      store.commit('login', userID)
      if (router.currentRoute.value.path.startsWith('/inscription')) {
        router.push('/accueil')
      }
    }

    return {
      logIn,
      toast
    }
  },
    methods : {
      async inscription() {
        if (this.validationInscription()) {
          console.log("Attempt d'inscription")
          try {
              const utilisateur = {
                prenom: this.firstname,
                nom: this.lastname,
                motDePasse: this.password,
                courriel: this.email};

              console.log(utilisateur)
              const response = await inscriptionUtilisateur(utilisateur);
              this.logIn(response.utilisateurID); // Enregis
          }catch(error){
            this.toast.error("Avez-vous un compte?\nCe courriel est déjà utilisé par un autre utilisateur!", {toastClassName: "bg-BbRed font-bold"});
          }
          
        }
      },
      validationInscription() {
        return (this.courrielValide(this.email) && this.motDePasseValide(this.password) && this.nomValide(this.lastname) && this.prenomValide(this.firstname))
      },
      courrielValide(courriel: string) {
        const formatCourriel = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!formatCourriel.test(courriel)) {
          this.toast.warning("Le courriel ne respecte pas le format requis.", {toastClassName: "bg-trempanilloBeige font-bold"});
          return false;
        }
        return true;
      },
      motDePasseValide(motDePasse: string) {
        const formatMotDePasse = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        if (!formatMotDePasse.test(motDePasse)) {
          this.toast.warning("Le mot de passe ne respecte pas le format requis.", {toastClassName: "bg-trempanilloBeige font-bold"});
          this.toast.warning("1. Le mot de passe doit contenir au moins une lettre minuscule (a-z).\n" +
                             "2. Le mot de passe doit contenir au moins une lettre majuscule (A-Z).\n" +
                             "3. Le mot de passe doit contenir au moins un chiffre (0-9).\n" +
                             "4. Le mot de passe doit contenir au moins un caractère spécial parmi ceux-ci : @ $ ! % * ? &\n" +
                             "5. Le mot de passe doit être composé d'au moins 8 caractères."
                             , {toastClassName: "bg-trempanilloBeige font-bold"});
          return false;
        }
        return true ;
      },
      nomValide(nom: string) {
        const noSpaceName = nom.trim();

        if(noSpaceName.length == 0) {
          this.toast.warning("Le nom ne peut pas être vide.", {toastClassName: "bg-BbRed font-bold"});
          return false;
        }
        return true; ;
      },
      prenomValide(prenom: string) {
        const noSpaceFirstName = prenom.trim();
        if(noSpaceFirstName.length == 0) {
          this.toast.warning("Le prénom ne peut pas être vide.", {toastClassName: "bg-BbRed font-bold"});
          return false;
        }
        return true; ;
      }}
  });
  
  </script>