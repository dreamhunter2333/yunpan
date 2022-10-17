import { createWebHistory, createRouter } from "vue-router";
import FileList from '../components/FileList.vue'

const routes = [
    {
        path: '/:path*',
        name: 'Home',
        component: FileList
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router
