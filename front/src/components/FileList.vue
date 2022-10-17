<template>
  <div class="flex">
    <el-button @click="router.push('/')" type="primary" :icon="HomeFilled">首页</el-button>
    <el-button @click="router.go(-1)" :icon="Back">返回</el-button>
    <el-button type="primary" @click="drawer = true">
      上传<el-icon class="el-icon--right">
        <Upload />
      </el-icon>
    </el-button>
  </div>
  <el-table :data="tableData" @row-click="open" style="width: 100%">
    <el-table-column prop="name" label="名称" width="180" />
    <el-table-column prop="time" label="时间" width="180" />
    <el-table-column prop="size" label="大小" width="180" />
    <el-table-column label="操作">
      <template #default="scope">
        <div>
          <el-dropdown>
            <el-button type="primary" plain>
              操作<el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-if="scope.row.isfile">
                  <el-link type="primary" :href="getDownload(scope.row.name)" target="_blank">
                    <el-icon>
                      <Download />
                    </el-icon>
                    下载
                  </el-link>
                </el-dropdown-item>
                <el-dropdown-item v-if="scope.row.isfile && scope.row.name.match(/mp4|mkv|avi|mov|rmvb|webm|flv$/)">
                  <el-link type="primary" :href="getStream('iina://weblink?url=', scope.row.name)" target="_blank">
                    <el-icon>
                      <VideoPlay />
                    </el-icon>
                    IINA
                  </el-link>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button @click="deleteItem(scope.row.name)" type="danger" link>删除</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-drawer v-model="drawer">
    <template #title>
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
</template>

<script>
import axios from "axios";
import { reactive, onMounted, defineComponent, toRefs, ref, computed } from "vue";
import { useRouter, useRoute } from 'vue-router'
import { HomeFilled, Back, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { ElLoading } from 'element-plus'

export default defineComponent({
  setup() {
    const router = useRouter()
    const route = useRoute()
    const drawer = ref(false)
    const filePath = ref("")
    const uploadFile = ref(null)
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
      loadingInstance.close();
    };
    const getDownload = (name) => {
      let url = axios.defaults.baseURL + "/download?path=";
      return url + curPath.value + name;
    }
    const getStream = (prefix, name) => {
      let url = axios.defaults.baseURL + "/stream?path="
      return prefix + url + curPath.value + name;
    }
    const open = (row) => {
      if (row.isfile)
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
    return {
      ...toRefs(state),
      onUpload,
      getDownload,
      onChangeFile,
      deleteItem,
      getStream,
      open,
      filePath,
      drawer,
      router,
      HomeFilled,
      Back,
      Upload
    }
  }
})
</script>
