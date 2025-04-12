<template>  
  <section class="relative w-full h-[500px] bg-no-repeat bg-cover bg-bottom" style="background-image: url('/hero_bg.svg');">
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="text-center ml-8">
          <div class="font-bold text-6xl w-[30] centered text-BbDarkBlue">Votre destination VHS!</div>
          <p class="mt-4 text-lg text-gray-700">Notre magasin propose un vaste choix de VHS classiques, cultes et rares. Venez rencontrer nos experts qui sauront vous conseiller pour dénicher la perle rare pour votre soirée cinéma.</p>
          <div class="font-bold text-6xl text-BbWhite mb-4 retro-text">BRIQUE BUSTER</div>
      </div>
    </div>
  </section>


  <div class="font-bold text-6xl text-BbDarkBlue flex flex-col items-center mt-32 mb-10">
    <div>Toutes nos cassettes</div>
  </div>
  <section class="flex flex-wrap gap-6 justify-center mt-8">
    <CardProduct
        v-if="produits"
      v-for="produit in produits"
      :key="produit.produitID"
      :nom="produit.nom"
      :prix="produit.prix"
      :enStock="produit.enStock"
      :produitId="produit.produitID"
    />
  </section>

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import CardProduct from '@/components/common/CardProduct.vue';
import { recuperer_produits } from '../api/produits.js';



export default defineComponent({
  name: "AccueilMagasin",
  components: {
    CardProduct
},
  setup() {
    const produits = ref([]);

    const chargerProduits = async () => {
      try {
        const data = await recuperer_produits();
        console.log('Produits chargés:', data);
        produits.value = data;
      } catch (error) {
        console.error('Erreur lors du chargement des produits :', error);
      }
    };

    onMounted(() => {
      chargerProduits();
    });

    return { produits };
  }
});
</script>

<style scoped>
.retro-text {
  text-shadow: 3px 3px 0px #ED6335, -3px -3px 0px #064C72;
  letter-spacing: 2px;
}

.retro-title {
  position: relative;
  display: inline-block;
  padding: 0 20px;
}

.retro-title::before, .retro-title::after {
  content: "★";
  font-size: 2rem;
  color: #ED6335;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.retro-title::before {
  left: -20px;
}

.retro-title::after {
  right: -20px;
}
</style>