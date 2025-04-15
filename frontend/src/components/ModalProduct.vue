
<template>
  <div
    v-if="ouvert"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <div class="bg-white border-4 border-black shadow-[5px_5px_0_#E53373] max-w-lg w-full p-6 relative font-mono">
      <button
        @click="$emit('fermer')"
        class="absolute top-2 right-2 px-2 py-1 border border-black bg-BbBlack text-white hover:bg-white hover:text-black transition"
      >
        ✖
      </button>

      <h2 class="text-2xl font-bold mb-4 text-BbBlack">{{ film.nom }}</h2>
      <p><strong>Prix :</strong> {{ film.prix }} $</p>
      <p><strong>Stock :</strong> {{ film.enStock }}</p>
      <p><strong>Longueur :</strong> {{ film.longueur }} mins</p>
      <p><strong>Catégorie :</strong> {{ film.categorie }}</p>

      <p class="mt-4 text-sm text-gray-600">
        {{ film.description || 'Aucune description disponible.' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  film: {
    nom: string
    prix: number
    enStock: number
    description: string
    categorie: string
    longueur: number
  }
  ouvert: boolean
}>()

defineEmits(['fermer'])
</script>

<style scoped>
.bg-BbBlack {
  background-color: #111111;
}
.text-BbBlack {
  color: #111111;
}
</style>



<style scoped>

</style>