<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

defineProps<{
  msg: string
}>();

let form = {
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
};

const count = ref(0);
const input = ref("element-plus");

const toast = () => {
  ElMessage.success('Hello')
}

function onSubmit() {
  console.log('submit!')
}
</script>

<template>
  <el-container>
    <el-header>Header</el-header>
    <el-main>
      <el-card>
        <template #header>
          <div>test test</div>
        </template>
        <el-form ref="form" :model="form" label-width="120px">
          <el-row>
            <el-col :span="4">
              <el-form-item label="旅費（新臺幣）">
                <el-input v-model="form.name"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="地區">
                <el-select v-model="form.region" placeholder="please select your zone">
                  <el-option label="Zone one" value="shanghai"></el-option>
                  <el-option label="Zone two" value="beijing"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="Activity form">
                <el-slider></el-slider>
              </el-form-item>
            </el-col>
            <el-col :span="2">
              <el-form-item>
                <el-button :icon="Search" type="success" @click="onSubmit">搜尋</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
    </el-main>
    <el-footer>
      <p>
        Full Example:
        <a
          href="https://github.com/element-plus/element-plus-vite-starter"
          target="_blank"
        >element-plus-vite-starter</a>
        | On demand Example:
        <a
          href="https://github.com/element-plus/unplugin-element-plus"
          target="_blank"
        >unplugin-element-plus/examples/vite</a>
      </p>
    </el-footer>
  </el-container>
</template>
