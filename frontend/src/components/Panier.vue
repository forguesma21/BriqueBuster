<template>
  <div class="container mx-auto mt-8 p-8">
    <div class="relative w-full max-w-4xl mx-auto p-6 border-4 border-black bg-white shadow-[5px_5px_0px_0px_#FF69B4] hover:shadow-[7px_7px_0px_0px_#FF69B4] transition-all">
      <h1 class="text-4xl font-bold text-BbBlack mb-6">Votre Panier</h1>

      <div v-if="produits.length === 0" class="text-center text-xl text-gray-500">
        Votre panier est vide.
      </div>

      <div v-else>
        <div class="space-y-4">
          <div v-for="produit in produits" :key="produit.produit_id" class="flex justify-between items-center border-2 border-black p-4">
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
        <div class="mt-6 text-right text-2xl font-bold">
          Total : ${{ total.toFixed(2) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { obtenirPanier } from '../api/paniers.js';  // Import de ton API

export default defineComponent({
  name: 'Panier',
  setup() {
    const produits = ref([]);
    const total = ref(0);
    const userID = 'ton_user_id_ici';  // Remplace par l'identifiant de ton utilisateur

    const chargerPanier = async () => {
      try {
        const data = await obtenirPanier(userID);
        produits.value = data.produits;
        total.value = data.total;
      } catch (error) {
        console.error("Erreur lors du chargement du panier :", error);
      }
    };

    const retirerProduit = (produitID) => {
      produits.value = produits.value.filter(produit => produit.produit_id !== produitID);
      total.value = produits.value.reduce((acc, produit) => acc + produit.prix * produit.quantite, 0);
    };

    onMounted(() => {
      chargerPanier();
    });

    return { produits, total, retirerProduit };
  }
});
</script>

<style scoped>
.bg-BbBlack {
  background-color: #111111;
}
.text-BbBlack {
  color: #111111;
}
</style>
