import { createApp } from 'vue'
import axios from 'axios';

import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/theme-chalk/dark/css-vars.css'
import router from './router'

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.config.productionTip = false;
app.use(ElementPlus);
app.use(router);
app.mount('#app');

axios.defaults.baseURL = process.env.VUE_APP_BASE_API ? process.env.VUE_APP_BASE_API : "/api";
axios.interceptors.request.use(
    config => {
        if (localStorage.getItem('jwt')) {
            config.headers.jwt = localStorage.getItem('jwt');
        } else if (!config.url.includes("login")) {
            router.push("/login");
            throw new Error("请登录");
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);
axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    if (error.response?.status == 401) {
        router.push("/login")
        throw new Error("请登录");
    }
    return Promise.reject(error);
});
