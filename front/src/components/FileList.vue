<template>
  <div class="filelist">
    <div class="flex">
      <el-button @click="router.push('/')" type="primary" :icon="HomeFilled">首页</el-button>
      <el-button @click="router.go(-1)" :icon="Back">返回</el-button>
      <el-button type="primary" @click="drawer = true">
        上传<el-icon class="el-icon--right">
          <Upload />
        </el-icon>
      </el-button>
      <el-button style="float:right" @click="logOut" type="primary" :icon="User">退出登录</el-button>
      <el-switch v-model="isDark" style="float:right" inline-prompt :active-icon="Moon" :inactive-icon="Sunny" />
    </div>
    <el-table :data="tableData" stripe table-layout="auto" @row-click="open">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="time" label="时间" />
      <el-table-column prop="size" label="大小" />
      <el-table-column column-key="operate" label="操作">
        <template #default="scope">
          <el-row class="mb-4">
            <el-dropdown v-if="scope.row.isfile">
              <el-button type="primary" round plain>
                <el-icon>
                  <Expand />
                </el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>
                    <el-link type="primary" :href="getDownload(scope.row.name)" target="_blank">
                      <el-icon>
                        <Download />
                      </el-icon>
                      下载
                    </el-link>
                  </el-dropdown-item>
                  <div v-if="scope.row.name.match(/mp4|mkv|avi|mov|rmvb|webm|flv$/)">
                    <el-dropdown-item>
                      <el-link type="primary" :href="getStream('', scope.row.name)" target="_blank">
                        <el-icon>
                          <VideoPlay />
                        </el-icon>
                        浏览器播放
                      </el-link>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-link type="primary" :href="getStream('iina://weblink?url=', scope.row.name)" target="_blank">
                        <el-icon>
                          <VideoPlay />
                        </el-icon>
                        IINA
                      </el-link>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-link type="primary" :href="getStream('vlc://', scope.row.name)" target="_blank">
                        <el-icon>
                          <VideoPlay />
                        </el-icon>
                        VLC
                      </el-link>
                    </el-dropdown-item>
                  </div>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-popconfirm title="确定要删除吗?" @confirm="deleteItem(scope.row.name)">
              <template #reference>
                <el-button type="danger" :icon="Delete" plain round></el-button>
              </template>
            </el-popconfirm>
          </el-row>
        </template>
      </el-table-column>
    </el-table>
    <el-drawer v-model="drawer">
      <template #header>
        <h4>上传文件</h4>
      </template>
      <template #default>
        <el-input v-model="filePath" placeholder="文件路径" />
        <el-upload drag action="/upload" :limit="1" :auto-upload="false" :on-change="onChangeFile">
          <el-icon class="el-icon--upload">
            <upload-filled />
          </el-icon>
          <div class="el-upload__text">
            拖动到此处或 <em>点击上传</em>
          </div>
        </el-upload>
      </template>
      <template #footer>
        <div style="flex: auto">
          <el-button type="primary" @click="onUpload">上传</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script>
import axios from "axios";
import { reactive, onMounted, defineComponent, toRefs, ref, computed } from "vue";
import { useRouter, useRoute } from 'vue-router'
import { HomeFilled, Back, Upload, Delete, Sunny, Moon, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { ElLoading } from 'element-plus'
import { useDark } from '@vueuse/core'

export default defineComponent({
  setup() {
    const isDark = useDark()
    const router = useRouter()
    const route = useRoute()
    const drawer = ref(false)
    const filePath = ref("")
    const uploadFile = ref(null)
    const token = ref("")
    const state = reactive({
      tableData: [],
    });
    const curPath = computed(() => {
      return route.path == "/" ? "" : route.path.substring(1) + "/";
    })
    const fetchData = async () => {
      const loadingInstance = ElLoading.service({ fullscreen: true })
      try {
        let fileData = await axios.get("/list?path=" + route.path.substring(1));
        state.tableData = fileData.data;
      } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""))
      }
      try {
        let res = await axios.get("/token");
        token.value = res.data;
      } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""))
      }
      loadingInstance.close();
    };
    const getDownload = (name) => {
      let url = axios.defaults.baseURL + "/download/";
      return url + curPath.value + name + "?token=" + token.value;
    }
    const getStream = (prefix, name) => {
      let url = axios.defaults.baseURL + "/stream/";
      if (axios.defaults.baseURL == "/api")
        url = window.location.origin + url
      return prefix + url + curPath.value + name + "?token=" + token.value;
    }
    const open = (row, column) => {
      if (row.isfile || column.columnKey == "operate")
        return
      router.push("/" + curPath.value + row.name);
    }
    onMounted(() => {
      fetchData();
    });
    const onUpload = async () => {
      const loadingInstance = ElLoading.service({ fullscreen: true })
      if (!filePath.value) {
        ElMessage.error("请填写路径");
        return;
      }
      if (!uploadFile.value) {
        ElMessage.error("请选择文件");
        return;
      }
      try {
        let formData = new FormData();
        formData.append("file", uploadFile.value.raw);
        await axios.post("/upload?path=" + filePath.value, formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        ElMessage({
          message: '上传成功',
          type: 'success',
        });
        router.go(0);
      } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""))
      }
      drawer.value = false;
      loadingInstance.close();
    }
    const onChangeFile = (file) => {
      uploadFile.value = file;
      filePath.value = curPath.value + file.name;
    }
    const deleteItem = async (name) => {
      const loadingInstance = ElLoading.service({ fullscreen: true })
      try {
        await axios.delete("/delete?path=" + curPath.value + name);
        ElMessage({
          message: '删除成功',
          type: 'success',
        });
        router.go(0);
      } catch (err) {
        ElMessage.error('请求出错了: ' + err.message + ", " + (err.response ? err.response.data : ""))
      }
      loadingInstance.close();
    };
    const logOut = () => {
      localStorage.removeItem('jwt')
      router.push('/login')
    };
    return {
      ...toRefs(state),
      onUpload,
      getDownload,
      onChangeFile,
      deleteItem,
      logOut,
      getStream,
      open,
      filePath,
      drawer,
      router,
      HomeFilled,
      Back,
      Upload,
      Delete,
      isDark,
      Sunny, Moon, User
    }
  }
})
</script>

<style>
.filelist {
  margin-top: 60px;
  margin-left: 60px;
  margin-right: 60px;
}
</style>
