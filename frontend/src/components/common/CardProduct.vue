<template>
  <div class="relative w-full max-w-sm p-4 border-4 border-black bg-white shadow-[5px_5px_0px_0px_#E53373] hover:shadow-[7px_7px_0px_0px_#E53373] transition-all mb-6">
    <div class="w-full h-40 bg-gray-200 flex items-center justify-center border border-black mb-4">
      <span class="text-xl font-bold text-black">Image non disponible</span>
    </div>

    <div class="space-y-2">
      <h3 class="text-2xl font-bold text-BbBlack tracking-tight">{{ nom }}</h3>
      <p class="text-xl text-gray-700 font-bold">${{ prix }}</p>
      <p class="text-md text-gray-500">En stock: {{ enStock }}</p>

      <button
        @click="ajoutPanier"
        class="px-4 py-2 mt-3 bg-black text-white border-2 border-black hover:bg-white hover:text-black transition-all"
      >
        Ajouter au panier
      </button>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification'
import { useStore } from 'vuex'
import { defineComponent } from 'vue'
import { ajouterAuPanier } from '@/api/paniers'

export default defineComponent({
  name: 'CardProduct',
  props: {
    nom: String,
    prix: Number,
    enStock: Number,
    produitId: String
  },
  setup(props) {
    const toast = useToast()
    const store = useStore()

    const ajoutPanier = async () => {
      try {
        console.log("User connecté :", store.state.userId)
        console.log("Id produit", props.produitId)

        await ajouterAuPanier(store.state.userId, props.produitId, 1)
        store.commit("incrementCartCount", store.state.cartCount)

        toast.success(`${props.nom} a été ajouté au panier !`, {
          toastClassName: 'bg-trempanilloVert font-bold'
        })
      } catch (error) {
        console.error(error)
        toast.error(
          error?.response?.data?.message || 'Erreur lors de l’ajout au panier.',
          { toastClassName: 'bg-BbRed font-bold' }
        )
      }
    }

    return {
      ajoutPanier
    }
  }
})
</script>

<style scoped>
.bg-BbBlack {
  background-color: #111111;
}
.text-BbBlack {
  color: #111111;
}
</style>
