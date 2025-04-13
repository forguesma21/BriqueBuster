import { createApp } from 'vue'
import App from "@/App.vue"
import router from './router'
import store from './store'
import "@/style.css";
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

const toastOptions = {
  position: 'bottom-left',
  timeout: 4000,
  toastClassName: 'bg-BbRed font-bold'
}
app.use(router)
app.use(store)
app.use(Toast, toastOptions)
app.mount('#app')
