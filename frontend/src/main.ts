import { createApp } from "vue";
import store from './store'
import router from "@/router.ts";
import Toast, { POSITION, type PluginOptions } from "vue-toastification";
import "vue-toastification/dist/index.css";
import App from "@/App.vue";
import "@/style.css";

// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
const app = createApp(App);

const options: PluginOptions = {
    position: POSITION.BOTTOM_LEFT,
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: false,
    pauseOnHover: false,
    draggable: false,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: "button",
    icon: true,
    rtl: false,
    transition: "Vue-Toastification__fade",
    maxToasts: 20,
    newestOnTop: true,
    toastClassName: "bg-BbRed font-bold"
};

app.use(router);
app.use(store);
app.use(Toast, options);
app.mount("#app");
