import { createRouter, createWebHashHistory } from "vue-router";
import FileList from '../components/FileList.vue'
import LoginView from '../components/LoginView.vue'


const routes = [
    {
        path: '/:path*',
        name: 'Home',
        component: FileList
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
})

export default router
