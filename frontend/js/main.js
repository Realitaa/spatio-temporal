// frontend/js/main.js
import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import ui from '@nuxt/ui/vue-plugin'
import axios from "axios";
import Layout from "./layout/default.vue";
import AppVue from "./App.vue";

document.addEventListener("DOMContentLoaded", () => {
	axios.defaults.xsrfCookieName = "csrftoken";
	axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

    const appElement = document.getElementById('app');
    const initialPage = JSON.parse(appElement.dataset.page);

    createInertiaApp({
        page: initialPage,
        resolve: (name) => {
            const pages = import.meta.glob("./pages/**/*.vue", { eager: true });
            let page = pages[`./pages/${name}.vue`];
            page.default.layout = page.default.layout || Layout;
            return page;
        },
        setup({ el, App, props, plugin }) {
            createApp({ render: () => h(AppVue, { inertiaApp: App, inertiaProps: props }) })
                .use(plugin)
								.use(ui)
                .mount(el);
        },
    });
});