import { createRouter, createWebHistory } from "vue-router";
import Accueil from "@/components/AccueilMagasin.vue";
import Produit from "@/components/ProduitMagasin.vue";
import Panier from "@/components/Panier.vue";
import Connexion from "@/components/ConnexionMagasin.vue";
import InscriptionMagasin from "@/components/InscriptionMagasin.vue";


const routes = [
    {
        path: "/",
        redirect: "/accueil",
    },
    {
        path: "/accueil",
        name: "Accueil",
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        component: Accueil,
    },
    {
        path: "/produit/:id",
        name: "Produit",
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        component: Produit,
    },
    {
        path: "/utilisateur",
        name: "Utilisateur",
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        component: Panier,
    },
    {
        path: "/connexion",
        name: "Connexion",
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        component: Connexion,
    },
    {
        path: "/inscription",
        name: "Inscription",
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        component: InscriptionMagasin,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        return { top: 0 };
    },
});

export default router;