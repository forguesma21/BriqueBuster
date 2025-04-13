<template>
  <div class="neo-brutal-container">

    <div class="user-header">
      <div v-if="user" class="user-card">
        <div class="pixel-avatar"></div>
        <div class="user-info">
          <h1 class="glitch-text">{{ user.nom.toUpperCase() }}</h1>
          <p class="user-email">{{ user.courriel }}</p>
        </div>
      </div>
    </div>

    <div class="loyalty-section">
      <div class="section-header">
        <h2>STATUT VHS CLUB</h2>
        <span class="vhs-status">{{ user.statut }}</span>
      </div>

      <div class="loyalty-progress">
        <div class="progress-label">
          <span>{{ user.points }} pts</span>
          <span>PROCHAIN PALIER: 1500 pts</span>
        </div>

        <div class="retro-progress-container">
          <div class="retro-progress-bar" :style="{ width: progressPourcentage + '%' }"></div>
          <div class="progress-segments">
            <div v-for="i in 8" :key="i" class="segment"></div>
          </div>
        </div>

        <div class="loyalty-benefits">
          <div class="benefit-item" :class="{ locked: user.points < 500 }">
            <div class="benefit-icon">🎬</div>
            <span>1 VHS GRATUITE</span>
          </div>
          <div class="benefit-item" :class="{ locked: user.points < 1000 }">
            <div class="benefit-icon">🍿</div>
            <span>POPCORN GRATUIT</span>
          </div>
          <div class="benefit-item" :class="{ locked: user.points < 1500 }">
            <div class="benefit-icon">🎟️</div>
            <span>SOIRÉE VIP</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Historique de location -->
    <div class="rental-history">
      <div class="section-header">
        <h2>HISTORIQUE DES LOCATIONS</h2>
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

            <div class="rental-status returned">RETOURNÉ</div>

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
              <div class="reorder-button">RELOUER TOUT</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { obtenirProfilUtilisateur } from '@/api/utilisateurs.js'
import { obtenirHistoriqueReservations } from '@/api/reservations.js'
const store = useStore()

const user = ref({
  nom: '',
  courriel: '',
  statut: '',
  points: 0
})

const reservations = ref([])
const openRental = ref<null | number>(null)

const progressPourcentage = computed(() => {
  return Math.min((user.value.points / 1500) * 100, 100)
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

    console.log("Profil store: ", store.state.userId)
    const profil = await obtenirProfilUtilisateur(store.state.userId)
    const historique = await obtenirHistoriqueReservations(store.state.userId)

    user.value = {
      nom: profil.nom,
      courriel: profil.courriel,
      statut: profil.statut,
      points: profil.points
    }

    reservations.value = historique
  } catch (error) {
    console.error('Erreur chargement profil :', error)
  }
}

onMounted(() => {
  chargerProfil()
})
</script>


<style scoped>
:root {
  --neon-purple: #9F00FF;
  --neon-green: #00FF66;
  --neon-red: #FF2D55;
  --neon-blue: #00CCFF;
  --retro-black: #121212;
  --retro-white: #F5F5F5;
  --retro-gray: #303030;
  --retro-yellow: #FFCC00;
}

.neo-brutal-container {
  font-family: 'Courier New', monospace;
  background-color: var(--retro-white);
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

h1, h2 {
  font-family: 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.user-header {
  margin-bottom: 40px;
}

.user-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #ffffff;
  border: 3px solid var(--retro-black);
  box-shadow: 8px 8px 0 var(--retro-black);
  position: relative;
}

.pixel-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #FF00FF, #00FFFF);
  border: 3px solid var(--retro-black);
  position: relative;
  image-rendering: pixelated;
}

.pixel-avatar:after {
  content: "";
  position: absolute;
  top: 20px;
  left: 20px;
  width: 40px;
  height: 40px;
  background-color: var(--retro-black);
  clip-path: polygon(0 0, 50% 0, 100% 50%, 0% 100%);
}

.user-info {
  margin-left: 20px;
  flex-grow: 1;
}

.glitch-text {
  font-size: 28px;
  margin: 0;
  position: relative;
  color: var(--retro-black);
}

.glitch-text:before, .glitch-text:after {
  content: "MARIE DUBOIS";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.8;
}

.glitch-text:before {
  left: 2px;
  color: var(--neon-red);
  clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%);
}

.glitch-text:after {
  left: -2px;
  color: var(--neon-blue);
  clip-path: polygon(0 55%, 100% 55%, 100% 100%, 0 100%);
}

.user-email {
  margin: 5px 0 0 0;
  font-size: 16px;
}

.edit-button {
  padding: 8px 15px;
  background-color: var(--retro-black);
  color: var(--retro-white);
  font-weight: bold;
  cursor: pointer;
  transform: rotate(-2deg);
  transition: transform 0.2s;
}

.edit-button:hover {
  transform: rotate(0deg) scale(1.05);
}

/* Loyalty section */
.loyalty-section {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #F0F0F0;
  border: 3px solid var(--retro-black);
  box-shadow: 8px 8px 0 var(--retro-black);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  font-size: 24px;
}

.vhs-status {
  padding: 5px 10px;
  background-color: var(--neon-purple);
  color: white;
  font-weight: bold;
  transform: rotate(2deg);
}

.loyalty-progress {
  margin-top: 30px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-weight: bold;
}

.retro-progress-container {
  height: 30px;
  background-color: var(--retro-black);
  border: 2px solid var(--retro-black);
  position: relative;
  margin-bottom: 20px;
}

.retro-progress-bar {
  height: 100%;
  background: repeating-linear-gradient(
    45deg,
    var(--neon-purple),
    var(--neon-purple) 10px,
    var(--neon-blue) 10px,
    var(--neon-blue) 20px
  );
  transition: width 0.5s ease;
  position: relative;
  width: 33%;
}

.progress-segments {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.segment {
  width: 2px;
  height: 100%;
  background-color: var(--retro-black);
  opacity: 0.7;
}

.loyalty-benefits {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.benefit-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  background-color: white;
  border: 2px solid var(--retro-black);
  width: 30%;
  transform: rotate(-1deg);
}

.benefit-item.locked {
  background-color: #E0E0E0;
  color: #707070;
  border: 2px dashed var(--retro-black);
}

.benefit-icon {
  font-size: 24px;
  margin-bottom: 10px;
}

/* Rental history */
.rental-history {
  padding: 20px;
  background-color: white;
  border: 3px solid var(--retro-black);
  box-shadow: 8px 8px 0 var(--retro-black);
}

.filter-button {
  padding: 6px 12px;
  background-color: var(--retro-gray);
  color: white;
  cursor: pointer;
}

.rental-list {
  margin-top: 20px;
}

.rental-item {
  margin-bottom: 15px;
  border: 2px solid var(--retro-black);
}

.rental-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #F5F5F5;
  cursor: pointer;
}

.rental-date {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.date-box {
  background-color: var(--retro-black);
  color: white;
  padding: 5px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1;
}

.date-day {
  font-size: 20px;
  font-weight: bold;
}

.date-month {
  font-size: 12px;
}

.year {
  margin-left: 8px;
  font-size: 14px;
}

.rental-overview {
  flex-grow: 1;
}

.rental-id {
  font-weight: bold;
}

.rental-summary {
  font-size: 14px;
  color: #666;
}

.rental-total {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-right: 20px;
}

.total-label {
  font-size: 12px;
  color: #666;
}

.total-amount {
  font-weight: bold;
  font-size: 18px;
}

.rental-status {
  padding: 5px 10px;
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  width: 100px;
}

.rental-status.returned {
  background-color: var(--neon-green);
  color: var(--retro-black);
}

.rental-status.late {
  background-color: var(--neon-red);
  color: white;
}

.expand-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--retro-black);
  color: white;
  border-radius: 50%;
  margin-left: 15px;
  font-size: 20px;
  font-weight: bold;
}

.rental-details {
  padding: 20px;
  background-color: white;
  border-top: 2px solid var(--retro-black);
}

.rental-items {
  margin-bottom: 20px;
}

.rental-item-row {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.item-thumb {
  width: 60px;
  height: 40px;
  margin-right: 15px;
  background-color: #e0e0e0;
}

.item-thumb.action {
  background-color: #FF4500;
}

.item-thumb.horror {
  background-color: #800080;
}

.item-thumb.comedy {
  background-color: #FFD700;
}

.item-thumb.scifi {
  background-color: #4682B4;
}

.item-thumb.drama {
  background-color: #8B0000;
}

.item-thumb.classic {
  background-color: #006400;
}

.item-info {
  flex-grow: 1;
}

.item-title {
  font-weight: bold;
}

.item-category {
  font-size: 12px;
  color: #666;
}

.item-duration, .item-price {
  width: 100px;
  text-align: right;
}

.rental-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px dashed var(--retro-black);
}

.rental-footer.alert {
  border-top: 1px dashed var(--neon-red);
}

.points-earned {
  font-weight: bold;
}

.points {
  color: var(--neon-green);
  margin-left: 10px;
}

.points.penalty {
  color: var(--neon-red);
}

.reorder-button {
  padding: 8px 15px;
  background-color: var(--retro-yellow);
  color: var(--retro-black);
  font-weight: bold;
  cursor: pointer;
  transform: rotate(1deg);
}

.reorder-button.disabled {
  background-color: #CCCCCC;
  color: #666666;
  cursor: not-allowed;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .user-card, .rental-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .rental-date, .rental-overview, .rental-total, .rental-status {
    margin-bottom: 10px;
    margin-right: 0;
  }

  .user-info {
    margin-left: 0;
    margin-top: 15px;
  }

  .edit-button {
    margin-top: 15px;
    align-self: flex-start;
  }

  .loyalty-benefits {
    flex-direction: column;
    gap: 15px;
  }

  .benefit-item {
    width: 100%;
  }

  .expand-icon {
    align-self: flex-end;
    margin-top: 10px;
  }

  .rental-item-row {
    flex-wrap: wrap;
  }

  .item-duration, .item-price {
    margin-top: 10px;
    text-align: left;
  }
}
</style>