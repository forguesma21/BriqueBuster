import { createStore } from "vuex";

interface State {
  loggedIn: boolean;
  userId: string;
  userName: string;
  cartCount: 0;
}

export default createStore({
  state: {
    loggedIn: false,
    userId: "",
    userName: "",
    cartCount: 0,
  },
  mutations: {
    async login(state: State, userId: string) {
      state.loggedIn = true;
      state.userId = userId;
    },
    logout(state: State) {
      state.loggedIn = false;
      state.userId = "";
    },
    setCartCount(state, count) {
      state.cartCount = count;
    },
    incrementCartCount(state) {
      state.cartCount++;
    },
    decrementCartCount(state) {
      state.cartCount = Math.max(0, state.cartCount - 1);
    },
  }
});

