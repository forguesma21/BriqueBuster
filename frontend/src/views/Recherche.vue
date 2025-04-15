<template>
  <div class="retro-search">
    <label for="recherche" class="label">Recherche de produits :</label>
    <input
      id="recherche"
      type="text"
      v-model="terme"
      @input="lancerRecherche"
      placeholder="Nom d'une cassette.."
      class="input"
    />
    <p v-if="terme && produits.length === 0 && !chargement" class="text-center text-gray-500 mt-4">
      Aucun produit trouvé.
    </p>

    <p v-if="chargement" class="text-center text-gray-500 mt-4">
      🔄 Recherche en cours...
    </p>
  </div>

  <section class="flex flex-wrap gap-6 justify-center mt-8">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <CardProduct
        v-for="produit in produits"
        :key="produit.id"
        :nom="produit.nom"
        :prix="produit.prix"
        :en-stock="produit.en_stock"
        :produit-id="produit.id"
      />
    </div>
  </section>


</template>

<script setup lang="ts">
import { ref } from 'vue'
import CardProduct from '@/components/common/CardProduct.vue'
import { recherche_produits } from '@/api/produits'

const terme = ref('')
const produits = ref<any[]>([])
const chargement = ref(false)

const lancerRecherche = async () => {
  if (terme.value.trim() === '') {
    produits.value = []
    return
  }

  chargement.value = true
  try {
    const resultat = await recherche_produits(terme.value)
    produits.value = resultat.produits || []
  } catch (err) {
    console.error('Erreur de recherche :', err)
    produits.value = []
  } finally {
    chargement.value = false
  }
}
</script>

<style scoped>
.retro-search {
  background-color: white;
  border: 3px double var(--bb-pink);
  padding: 1rem;
  max-width: 450px;
  margin: 2rem auto;
  font-family: 'Courier New', Courier, monospace;
  box-shadow: 3px 3px 0px #888;
}

.label {
  display: block;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.input {
  width: 100%;
  padding: 0.6rem;
  font-size: 1rem;
  border: 2px inset #999;
  background-color: #fff;
  color: #111;
}

</style>
