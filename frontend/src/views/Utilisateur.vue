<template>
  <div v-if="user" class="neo-brutal-container">

    <div class="user-header">
      <div class="user-card">
        <div class="pixel-avatar"></div>
        <div class="user-info">
          <h1 class="loyalty-mini-title">{{ user.nom.toUpperCase() }}</h1>
          <p class="user-email">{{ user.courriel }}</p>
        </div>
      </div>
    </div>

  <div class="loyalty-compact">
    <div class="loyalty-header">
      <h3 class="loyalty-mini-title">PROGRAMME FIDÉLITÉ</h3>
      <div class="loyalty-points">{{ user.points }} PTS</div>
    </div>

    <div class="loyalty-status-info">
      <div class="current-status">
        <div class="status-label">STATUT ACTUEL</div>
        <div class="status-badge">{{ user.statut }}</div>
      </div>

      <div class="next-status">
        <div class="next-label">PROCHAIN PALIER</div>
        <div class="next-target">{{ prochainPalierLabel }}</div>
      </div>
    </div>

    <div class="loyalty-tiers">
      <div
        v-for="(palier, index) in paliers"
        :key="palier.id"
        class="tier-chip"
        :class="{
          'active': user.statut === palier.nom,
          'completed': isTierCompleted(palier),
          'current': isCurrentTier(palier),
          'future': isFutureTier(palier)
        }"
      >
        <div class="tier-name">{{ palier.nom }}</div>
        <div class="tier-points">{{ palier.seuil }}</div>
      </div>
    </div>

    <div class="current-benefits">
      <div class="benefits-title">AVANTAGES ACTUELS</div>
      <div class="benefits-list">
        <div v-for="(benefit, idx) in getCurrentBenefits()" :key="idx" class="benefit-item">
          <span class="benefit-emoji">{{ benefit.emoji }}</span>
          <span class="benefit-text">{{ benefit.label }}</span>
        </div>
      </div>
    </div>
  </div>

    <!-- Historique de location -->
    <div class="loyalty-compact">
      <div class="loyalty-header">
        <h2 class="loyalty-mini-title">HISTORIQUE DES LOCATIONS</h2>
      </div>

      <div class="rental-list">
        <div
          v-for="(reservation, index) in reservations"
          :key="reservation.id"
          class="rental-item"
        >
          <div class="rental-header" @click="toggleRental(index)">
            <div class="rental-date">
              <div class="date-box">
                <span class="date-day">{{ getJour(reservation.date_reservation) }}</span>
                <span class="date-month">{{ getMois(reservation.date_reservation) }}</span>
              </div>
              <span class="year">{{ getAnnee(reservation.date_reservation) }}</span>
            </div>

            <div class="rental-overview">
              <div class="rental-id">#{{ reservation.id.slice(0, 6).toUpperCase() }}</div>
              <div class="rental-summary">{{ reservation.produits.length }} films • 7 jours</div>
            </div>

            <div class="rental-total">
              <span class="total-label">TOTAL</span>
              <span class="total-amount">{{ reservation.montant_total.toFixed(2) }} $</span>
            </div>

            <div class="expand-icon">
              <span>+</span>
            </div>
          </div>

          <div class="rental-details" v-if="openRental === index">
            <div class="rental-items">
              <div
                class="rental-item-row"
                v-for="produit in reservation.produits"
                :key="produit.produit_id"
              >
                <div class="item-thumb" :class="produit.categorie.toLowerCase()"></div>
                <div class="item-info">
                  <div class="item-title">{{ produit.nom }}</div>
                  <div class="item-category">{{ produit.categorie }} • {{ produit.annee }}</div>
                </div>
                <div class="item-duration">7 jours</div>
                <div class="item-price">{{ produit.prix.toFixed(2) }} $</div>
              </div>
            </div>

            <div class="rental-footer">
              <div class="points-earned">
                <span>POINTS GAGNÉS</span>
                <span class="points">+{{ reservation.points }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

   <div class="loyalty-categories">
  <div
    v-for="palier in paliers"
    :key="palier.id"
    class="category-pill"
    :class="{ active: palier.nom === user.statut }"
  >
    {{ palier.nom }}
  </div>

</div>


  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { obtenirProfilUtilisateur } from '@/api/utilisateurs.js'
import { obtenirHistoriqueReservations } from '@/api/reservations.js'
import { obtenirCategorieFidelite } from '@/api/fidelite.js'

const store = useStore()
const paliers = ref([])

const user = ref({
  nom: '',
  courriel: '',
  statut: '',
  points: 0
})

const reservations = ref([])
const openRental = ref<null | number>(null)

const chargerPaliers = async () => {
  try {
    const data = await obtenirCategorieFidelite()
    paliers.value = data.sort((a, b) => a.seuil - b.seuil)
  } catch (error) {
    console.error("Erreur chargement paliers :", error)
  }
}

const getBenefits = (nom: string) => {
  const benefitsMap = {
    'Cassette Basique': [
      { emoji: '📼', label: 'Accès au catalogue standard' },
      { emoji: '📰', label: 'Newsletter mensuelle' }
    ],
    'VHS Classique': [
      { emoji: '💰', label: 'Remise de 5% sur les locations' },
      { emoji: '🎬', label: '1 location gratuite' },
      { emoji: '⏱️', label: 'Réservation 24h à l’avance' }
    ],
    'Édition Collector': [
      { emoji: '💰', label: 'Remise de 10% sur tout' },
      { emoji: '🍿', label: 'Popcorn gratuit' },
      { emoji: '⏰', label: 'Location prolongée (+2 jours)' }
    ],
    'LaserDisc Élite': [
      { emoji: '💰', label: 'Remise de 15% sur tout' },
      { emoji: '🎂', label: 'Location gratuite anniversaire' },
      { emoji: '🎟️', label: 'Invitations avant-premières' }
    ],
    'Master du Magnétoscope': [
      { emoji: '💰', label: 'Remise de 25% sur tout' },
      { emoji: '🚚', label: 'Livraison gratuite' },
      { emoji: '🌟', label: 'Accès prioritaire nouveautés' },
      { emoji: '👑', label: 'Carte membre VIP' }
    ]
  }
  return benefitsMap[nom] || []
}

const prochainPalierLabel = computed(() => {
  const prochain = paliers.value.find(p => user.value.points < p.seuil)
  return prochain ? `${prochain.nom} (${prochain.seuil} pts)` : 'Niveau maximum atteint!'
})

const getJour = (dateStr: string) => new Date(dateStr).getDate()
const getMois = (dateStr: string) =>
  new Date(dateStr).toLocaleDateString('fr-FR', { month: 'short' }).toUpperCase()
const getAnnee = (dateStr: string) => new Date(dateStr).getFullYear()

const toggleRental = (id: number) => {
  openRental.value = openRental.value === id ? null : id
}

const chargerProfil = async () => {
  try {
    const profil = await obtenirProfilUtilisateur(store.state.userId)
    console.log("PROFILE : ", profil)

    user.value = {
      nom: profil.nom,
      courriel: profil.courriel,
      statut: profil.statut,
      points: profil.points
    }

    console.log("USER", user.value)

  } catch (error) {
    console.error('Erreur chargement profil :', error)
  }
}

const chargerReservations = async () => {
  try{
     const data = await obtenirHistoriqueReservations(store.state.userId)
    console.log("RESERVATIONS : ", data)
    reservations.value = data  // ✅ mise à jour de la ref


  }catch(error){
    console.error('Erreur chargement des reservations :', error)

  }
}

const isTierCompleted = (palier) => {
  const currentTierIndex = paliers.value.findIndex(p => p.nom === user.value.statut);
  const palierIndex = paliers.value.findIndex(p => p.id === palier.id);
  return palierIndex < currentTierIndex;
};

const isCurrentTier = (palier) => {
  return palier.nom === user.value.statut;
};

const isFutureTier = (palier) => {
  const currentTierIndex = paliers.value.findIndex(p => p.nom === user.value.statut);
  const palierIndex = paliers.value.findIndex(p => p.id === palier.id);
  return palierIndex > currentTierIndex;
};

const getCurrentBenefits = () => {
  return getBenefits(user.value.statut);
};

onMounted(() => {
  chargerProfil()
  chargerPaliers()
  chargerReservations()

})
</script>


<style scoped>
/* Base container */
.neo-brutal-container {
  font-family: 'Courier New', monospace;
  color: var(--text-dark);
  padding: 25px;
  max-width: 1200px;
  margin: 0 auto;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(255, 0, 255, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 20%);
}

/* Header and User Card */
.user-header {
  margin-bottom: 40px;
}

.user-card {
  display: flex;
  align-items: center;
  padding: 25px;
  background-color: var(--bg-card);
  border: 4px solid var(--accent-primary);
  box-shadow: 10px 10px 0 var(--bb-pink);
  position: relative;
  margin-bottom: 40px;
}

.pixel-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #E53373, #00FFFF);
  border: 3px solid #33FF99;
  position: relative;
  image-rendering: pixelated;
  margin-right: 20px;
  box-shadow: 5px 5px 0 #000000;
}

.pixel-avatar:after {
  content: "";
  position: absolute;
  top: 20px;
  left: 20px;
  width: 40px;
  height: 40px;
  background-color: #000;
  clip-path: polygon(0 0, 50% 0, 100% 50%, 0% 100%);
}

.user-email {
  margin: 5px 0 0 0;
  font-size: 16px;
  color: #BBBBBB;
}

/* Loyalty VHS Section */
@keyframes scanline {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.benefit-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 13px;
  color: #CCCCCC;
}

.active {
  background-color: #33FF99;
  color: #000000;
  border: 2px solid #000000;
}

/* Rental History */
.section-header h2 {
  margin: 0;
  font-size: 28px;
  color: var(--bb-orange);
  text-shadow: 3px 3px 0 #000000;
  letter-spacing: 2px;
}

.rental-list {
  margin-top: 25px;
}

.rental-item {
  margin-bottom: 20px;
  border: 3px solid #334466;
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.5);
}

.rental-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: var(--bg-card);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.rental-header:hover {
  background-color: var(--bg-alt);
}

.rental-date {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.date-box {
  background-color: var(--bb-pink);
  color: #FFFFFF;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1;
  box-shadow: 3px 3px 0 #000000;
}

.date-day {
  font-size: 24px;
  font-weight: bold;
}

.date-month {
  font-size: 14px;
}

.year {
  margin-left: 10px;
  font-size: 16px;
  color: var(--bb-dark-blue);
}

.rental-overview {
  flex-grow: 1;
}

.rental-id {
  font-weight: bold;
  font-size: 16px;
  color: var(--bb-pink);
}

.rental-summary {
  font-size: 14px;
  color: var(--bb-dark-blue);
  margin-top: 5px;
}

.rental-total {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-right: 20px;
}

.total-label {
  font-size: 12px;
  color: var(--bb-dark-blue);
}

.total-amount {
  font-weight: bold;
  font-size: 20px;
  color: var(--bb-dark-blue);
}

.rental-status {
  padding: 8px 12px;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  width: 100px;
}

.rental-status.returned {
  background-color: var(--accent-tertiary);
  color: #000000;
  box-shadow: 3px 3px 0 #000000;
}

.expand-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bb-pink);
  color: #000000;
  margin-left: 15px;
  font-size: 20px;
  font-weight: bold;
  box-shadow: 3px 3px 0 #000000;
}

.rental-details {
  padding: 20px;
  background-color: var(--bg-alt);
  border-top: 2px solid #334466;
}

.rental-items {
  margin-bottom: 20px;
}

.rental-item-row {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #334466;
}

.item-thumb {
  width: 60px;
  height: 40px;
  margin-right: 15px;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
}

.item-thumb.action { background-color: #FF4500; }
.item-thumb.horror { background-color: #800080; }
.item-thumb.comedy { background-color: #FFD700; }
.item-thumb.scifi { background-color: #4682B4; }
.item-thumb.drama { background-color: #8B0000; }
.item-thumb.classic { background-color: #006400; }

.item-info {
  flex-grow: 1;
}

.item-title {
  font-weight: bold;
  color: var(--text-dark);
}

.item-category {
  font-size: 12px;
  color: var(--text-medium);
  margin-top: 3px;
}

.item-duration, .item-price {
  width: 100px;
  text-align: right;
  color: var(--text-dark);
}

.rental-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 2px dashed #334466;
}

.points-earned {
  font-weight: bold;
  color: var(--text-dark);
}

.points {
  color: var(--accent-tertiary);
  margin-left: 10px;
  text-shadow: 1px 1px 0 #000000;
}

.reorder-button {
  padding: 10px 18px;
  background-color: #FF6B35;
  color: #000000;
  font-weight: bold;
  cursor: pointer;
  transform: rotate(2deg);
  box-shadow: 3px 3px 0 #000000;
  transition: all 0.2s ease;
}

.reorder-button:hover {
  transform: rotate(0) scale(1.05);
  box-shadow: 5px 5px 0 #000000;
}

/* Loyalty Categories */
.loyalty-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 40px;
  justify-content: center;
}

.category-pill {
  padding: 10px 20px;
  background-color: #1a1a2a;
  border: 2px solid #334466;
  color: #BBBBBB;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
}

.category-pill:hover {
  transform: translateY(-3px);
}

.category-pill.active {
  background-color: #33FF99;
  color: #000000;
  border-color: #000000;
  transform: translateY(-5px);
  box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.8);
}

/* Animation */
@keyframes shine {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .neo-brutal-container {
    padding: 15px;
  }

  .user-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .pixel-avatar {
    margin-right: 0;
    margin-bottom: 20px;
  }

  .rental-header {
    flex-wrap: wrap;
  }

  .rental-date, .rental-overview, .rental-total {
    margin-bottom: 15px;
    width: 100%;
  }

  .rental-status, .expand-icon {
    margin-left: auto;
  }

  .rental-item-row {
    flex-wrap: wrap;
  }

  .item-duration, .item-price {
    width: 50%;
    text-align: left;
    margin-top: 10px;
  }

  .rental-footer {
    flex-direction: column;
    gap: 15px;
  }
}

.loyalty-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.loyalty-mini-title {
  margin: 0;
  font-size: 18px;
  color: var(--bb-pink);
  text-shadow: 1px 1px 0 #000;
  letter-spacing: 1px;
}

.loyalty-points {
  background: #151525;
  color: var(--accent-primary);
  padding: 4px 10px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 2px 2px 0 #000;
  border: 1px solid var(--accent-primary);
}

.benefit-emoji {
  margin-right: 4px;
}

.loyalty-compact {
  background-color: var(--bg-card);
  border: 2px solid var(--accent-primary);
  box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.3);
  padding: 15px;
  margin-bottom: 25px;
  font-family: 'Courier New', monospace;
}

.loyalty-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px dashed #ccc;
  padding-bottom: 10px;
}

.loyalty-status-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.current-status, .next-status {
  text-align: center;
}

.status-label, .next-label {
  font-size: 9px;
  color: #777;
  margin-bottom: 3px;
}

.status-badge {
  background-color: #33FF99;
  color: #000;
  padding: 3px 8px;
  font-size: 12px;
  font-weight: bold;
  border: 1px solid #000;
  display: inline-block;
}

.next-target {
  font-size: 12px;
  color: #555;
}

.loyalty-tiers {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  position: relative;
}

.loyalty-tiers:after {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #ccc;
  z-index: 0;
}

.tier-chip {
  background: #eee;
  border: 1px solid #ccc;
  font-size: 10px;
  padding: 2px 6px;
  position: relative;
  z-index: 1;
  text-align: center;
}

.tier-name {
  font-weight: bold;
  color: #666;
  white-space: nowrap;
  font-size: 8px;
}

.tier-points {
  font-size: 9px;
  color: #888;
}

.tier-chip.completed {
  background-color: #e5ffe5;
  border-color: #99cc99;
}

.tier-chip.active, .tier-chip.current {
  background-color: #33FF99;
  border-color: #000;
  transform: scale(1.1);
  z-index: 2;
}

.tier-chip.active .tier-name,
.tier-chip.current .tier-name,
.tier-chip.active .tier-points,
.tier-chip.current .tier-points {
  color: #000;
}

.tier-chip.future {
  opacity: 0.7;
}

.current-benefits {
  background-color: #f9f9f9;
  border: 1px dashed #ddd;
  padding: 10px;
}

.benefits-title {
  font-size: 11px;
  color: #666;
  margin-bottom: 8px;
  font-weight: bold;
}

.benefits-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.benefit-item {
  background-color: #fff;
  border: 1px solid #eee;
  padding: 4px 8px;
  font-size: 10px;
  display: flex;
  align-items: center;
  color: #555;
}

.benefit-emoji {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .loyalty-tiers {
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
  }

  .loyalty-tiers:after {
    display: none;
  }

  .tier-chip {
    margin-bottom: 5px;
  }
}

</style>