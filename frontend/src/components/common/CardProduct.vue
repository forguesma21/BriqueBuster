<template>
  <div class="relative w-full max-w-sm p-4 border-4 border-black bg-white shadow-[5px_5px_0px_0px_#E53373] hover:shadow-[7px_7px_0px_0px_#E53373] transition-all mb-6">
    <!-- Image générique -->
    <div class="w-full h-40 bg-gray-200 flex items-center justify-center border border-black mb-4">
      <span class="text-xl font-bold text-black">Image non disponible</span>
    </div>

    <!-- Informations du produit -->
    <div class="space-y-2">
      <h3 class="text-2xl font-bold text-BbBlack tracking-tight">{{ nom }}</h3>
      <p class="text-xl text-gray-700 font-bold">${{ prix }}</p>
      <p class="text-md text-gray-500">En stock: {{ enStock }}</p>

      <!-- Bouton Ajouter au Panier -->
      <button
        @click="ajouterAuPanier"
        class="px-4 py-2 mt-3 bg-black text-white border-2 border-black hover:bg-white hover:text-black transition-all"
      >
        Ajouter au panier
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProductCard',
  props: {
    nom: {
      type: String,
      required: true
    },
    prix: {
      type: Number,
      required: true
    },
    enStock: {
      type: Number,
      required: true
    },
    produitId: {
      type: String,
      required: true
    }
  },
  methods: {
    ajouterAuPanier() {
      console.log(`Produit ajouté au panier: ${this.nom} (ID: ${this.produitId})`);
    }
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
