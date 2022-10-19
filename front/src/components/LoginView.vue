<template>
  <div class="box">
    <div class="left">
      <!-- 图片部分 -->
    </div>
    <div class="right">
      <!-- 登录主界面 -->
      <h4>用户登陆</h4>
      <el-form :model="formData">
        <el-form-item prop="useraccount">
            <el-input type="text" placeholder="用户名" v-model="formData.useraccount"></el-input>
        </el-form-item>
        <el-form-item prop="password">
            <el-input type="password" placeholder="请输入密码" v-model="formData.password"></el-input>
        </el-form-item>
        <el-button type="primary" @click="checkPassword">Login</el-button>
    </el-form>
    <div class="more">
        <a href="#">注册账号</a>
        <a href="#">找回密码</a>
    </div>
    </div>

  </div>
</template>

<script setup>
import axios from "axios";
import { reactive } from 'vue'
import { ElLoading, ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'


const formData = reactive({
    useraccount: '',
    password: '',
});

const router = useRouter();

const checkPassword = async () => {
    const loadingInstance = ElLoading.service({ fullscreen: true });
    try {
        let res = await axios.post("/login", { 
            'useraccount': formData.useraccount,
            'password': formData.password 
        });
        ElMessage({
            message: '登录成功',
            type: 'success',
        });
        localStorage.setItem("jwt", res.data)
        router.push("/")
    } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""));
    }
    loadingInstance.close();
};
</script>

<style>
* {
    /* 清除内，外边距 */
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    font-size: 10px;
}

body {
    background: linear-gradient(120deg, #83C0E1 0%, #D6DCE9 100%) no-repeat;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.box {
    width: 90rem;
    height: 55rem;
    border-radius: 1.5rem;
    background-color: rgba(255, 255, 255, 0.5);
    margin: 10% auto;
    box-shadow: 0 0 1rem 0.2rem rgba(0, 0, 0, 0.1);
    display: flex;
}

.box .left {
    width: 35%;
    height: 100%;
    background-color: #83C0E1;
    border-radius: 1.5rem 0 0 1.5rem;
    background-image: url(../../public/resource/img/login.jpg);
    /* 有点超出 */
    background-size: cover;
    opacity: .85;
}

.box .right {
    flex: 1;
    height: 100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    border-radius: 0 1.5rem 1.5rem 0;

}

.box .right h4 {
    margin-top: 5rem;
    font-size: 3rem;
    text-align: center;
    color: #7092C8;
}

form {
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;

}

.box .right form .input {
    outline: none;
    width: 80%;
    height: 5rem;

    font-size: 1.6rem;
    padding: 1rem 0 0 1.2rem;
    border: none;
    border-bottom: 1px solid #7092C8;
    background: transparent;
    margin-top: 5rem;
}

.box .right form .button {
    width: 60%;
    height: 5rem;
    font-weight: 600;
    font-size: 1.6rem;
    background-image: linear-gradient(120deg, #83C0E1 0%, #D6DCE9 100%);
    border: none;
    margin-top: 6rem;
    border-radius: 0.5rem;
    transition: all .3s;
    color: aliceblue;
}

.box .right form .button:hover {
    /* 加个阴影 */
    box-shadow: 0 0 2rem 0.5rem rgba(0, 0, 0, 0.25);
}

.box .right .more {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0 100px;
    margin-top: 1rem;
}

.box .right .more a {
    margin-top: 4.5rem;
    font-size: 1.5rem;
    color: #666;
    text-decoration: none;
}

::selection {
    color: #fff;
    background-color: #7092C8;
}
</style>