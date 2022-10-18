<template>
    <el-button @click="router.push('/')" type="primary" :icon="HomeFilled">首页</el-button>
    <el-dialog :model-value="true" :show-close="false" :close-on-click-modal="false" :close-on-press-escape="false"
        title="请输入密码">
        <el-input v-model="password" type="password" show-password />
        <template #footer>
            <span class="dialog-footer">
                <el-button type="primary" @click="checkPassword">登录</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import axios from "axios";
import { ref } from 'vue'
import { ElLoading, ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const password = ref("")
const router = useRouter()

const checkPassword = async () => {
    const loadingInstance = ElLoading.service({ fullscreen: true })
    try {
        let res = await axios.post("/login", { 'password': password.value });
        ElMessage({
            message: '登录成功',
            type: 'success',
        });
        localStorage.setItem("jwt", res.data)
        router.push("/")
    } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""))
    }
    loadingInstance.close();
}
</script>
