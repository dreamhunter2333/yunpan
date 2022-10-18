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
axios.defaults.baseURL = process.env.VUE_APP_BASE_API ? process.env.VUE_APP_BASE_API : "";

app.config.productionTip = false;
app.use(ElementPlus);
app.use(router);
app.mount('#app');
