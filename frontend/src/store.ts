import { createStore, useStore } from 'vuex';
import * as api from "@/scripts/api/Api.js";

interface State {
  loggedIn: boolean;
  userId: string;
  userName: string;
  cartCount: 0

}

export default createStore({
  state: {
    loggedIn: false,
    userId: '',
    userName: '',
    cartCount: 0
  },
  mutations: {
    async login(state: State, userId: string) {
      state.loggedIn = true;
      state.userId = userId;
      const utilisateur = await api.obtenirUtilisateur(state.userId);
      state.userName = utilisateur.nomUtilisateur;
    },
    logout(state: State) {
      state.loggedIn = false;
      state.userId = '';
      state.userName = '';
    },
   setCartCount(state, count) {
    state.cartCount = count
    },
    incrementCartCount(state) {
      state.cartCount++
    },
    decrementCartCount(state) {
      state.cartCount = Math.max(0, state.cartCount - 1)
    }
  },
  actions: {
    login({ commit }, userId: string) {
      commit('login', userId)
    },
    logout({ commit }) {
      commit('logout')
    },
  },
})

export function logOut() {
    const store = useStore()
    store.dispatch('logout')
  }

export function logIn(userId: string, nom: string, prenom: string) {
    const store = useStore()
    store.dispatch('login', userId)
  }
