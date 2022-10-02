import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: HomeView,
    },
    {
      path: "/redeem-code",
      component: () => import("../views/RedeemCodeView.vue"),
    },
    {
      path: "/@cce$s-downl0ad",
      component: () => import("../views/AccessDownloadView.vue"),
    },
    {
      path: "/n0-down1oad-4-u",
      component: () => import("../views/NoDownloadForYouVue.vue"),
    },
    {
      path: "/d0wnload-mvz1k",
      component: () => import("../views/DownloadMusicView.vue"),
    }
  ],
});

export default router;
