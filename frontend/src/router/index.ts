import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import Accueil from '@/views/Accueil.vue'
const Panier = () => import('@/views/Panier.vue') // trying lazy routing
import Connexion from '@/views/Connexion.vue'
import Inscription from '@/views/Inscription.vue'
import Utilisateur from '@/views/Utilisateur.vue'
import Recherche from '@/views/Recherche.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/accueil'
  },
  {
    path: '/accueil',
    name: 'Accueil',
    component: Accueil
  },
  {
    path: '/panier',
    name: 'Panier',
    component: Panier
  },
  {
    path: '/profil',
    name: 'Profil',
    component: Utilisateur
  },
  {
    path: '/connexion',
    name: 'Connexion',
    component: Connexion
  },
  {
    path: '/inscription',
    name: 'Inscription',
    component: Inscription
  },
  {
    path: '/recherche',
    name: 'Recherche',
    component: Recherche
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
