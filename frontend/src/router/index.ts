import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import Accueil from '@/views/Accueil.vue'
import Produit from '@/views/Produit.vue'
import Panier from '@/views/Panier.vue'
import Connexion from '@/views/Connexion.vue'
import Inscription from '@/views/Inscription.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/accueil',
  },
  {
    path: '/accueil',
    name: 'Accueil',
    component: Accueil,
  },
  {
    path: '/produit/:id',
    name: 'Produit',
    component: Produit,
    props: true,
  },
  {
    path: '/panier',
    name: 'Panier',
    component: Panier,
  },
  {
    path: '/connexion',
    name: 'Connexion',
    component: Connexion,
  },
  {
    path: '/inscription',
    name: 'Inscription',
    component: Inscription,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
