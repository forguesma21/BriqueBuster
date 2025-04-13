<template>
  <div v-if="produits" class="container mx-auto mt-8 p-8">
    <div class="relative w-full max-w-4xl mx-auto p-6 border-4 border-black bg-white shadow-[5px_5px_0px_0px_#FF69B4] hover:shadow-[7px_7px_0px_0px_#FF69B4] transition-all">
      <h1 class="text-4xl font-bold text-BbBlack mb-6">Votre Panier</h1>

      <div v-if="produits.length === 0" class="text-center text-xl text-gray-500">
        Votre panier est vide.
      </div>

      <div v-else>
        <div v-if="produits" class="space-y-4">
          <div
            v-for="produit in produits"
            :key="produit.produit_id"
            class="flex justify-between items-center border-2 border-black p-4"
          >
            <div>
              <h2 class="text-2xl font-bold text-BbBlack">{{ produit.nom }}</h2>
              <p class="text-gray-700">Quantité : {{ produit.quantite }}</p>
              <p class="text-gray-700">Prix Unitaire : ${{ produit.prix.toFixed(2) }}</p>
            </div>
            <button
              @click="retirerProduit(produit.produit_id)"
              class="px-4 py-2 bg-black text-white border-2 border-black hover:bg-white hover:text-black transition-all"
            >
              Retirer
            </button>
          </div>
        </div>

        <!-- Prix Total -->
        <div class="mt-6 flex justify-between items-center">
          <div class="text-2xl font-bold">
            Total : ${{ total.toFixed(2) }}
          </div>

          <button
            @click="reserverPanierUtilisateur"
            class="px-6 py-3 bg-BbBlack text-white font-bold border-2 border-black hover:bg-white hover:text-black transition-all"
          >
            Réserver
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { obtenirPanier } from '@/api/paniers.js'
import { useToast } from 'vue-toastification'
import { retirerProduitDuPanier} from "@/api/paniers.js";
import { reserverPanier } from '@/api/reservations.js'


export default defineComponent({
  name: 'Panier',
  setup() {
    const store = useStore()
    const produits = ref([])
    const toast = useToast()


    const total = computed(() =>
      produits.value.reduce((acc, produit) => acc + produit.prix * produit.quantite, 0)
    )

    const chargerPanier = async () => {
      try {
        const userID = store.state.userId
        if (!userID) throw new Error('Utilisateur non connecté.')

        const data = await obtenirPanier(userID)
        produits.value = data
        console.log("🔍 Produits reçus :", produits.value)

      } catch (error) {
        console.error('Erreur lors du chargement du panier :', error)
      }
    }

    const retirerProduit = async (produitId) => {
    try {
      await retirerProduitDuPanier(store.state.userId, produitId)
      toast.success("Produit retiré avec succès", {
        toastClassName: "bg-trempanilloVert font-bold"
      })
      await chargerPanier()
    } catch (error) {
      toast.error(error.message, {
        toastClassName: "bg-BbRed font-bold"
      })
    }
    }

    const reserverPanierUtilisateur = async () => {
  try {
    const userId = store.state.userId
    if (!userId || produits.value.length === 0) {
      toast.warning("Impossible de réserver : panier vide ou non connecté", {
        toastClassName: "bg-BbRed font-bold"
      })
      return
    }

    await reserverPanier(userId)

    toast.success("Réservation réussie 🎉", {
      toastClassName: "bg-trempanilloVert font-bold"
    })

    produits.value = []
  } catch (error) {
    toast.error(error.message, {
      toastClassName: "bg-BbRed font-bold"
    })
  }
}


    onMounted(() => {
      chargerPanier()
    })

    return {
      produits,
      total,
      retirerProduit,
      reserverPanierUtilisateur
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
