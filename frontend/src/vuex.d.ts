import type { Store } from 'vuex'

declare module '@vue/runtime-core' {
  // declare your own store states
  interface State {
    connected: boolean;
    userId: string;
  }

  // provide typings for `this.$store`
  interface ComponentCustomProperties {
    $store: Store<State>
  }
}