<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

defineProps<{
  msg: string
}>();

let bucket = ref(0);
let safetyLevel = ref(0);
let region = ref('');

const toast = () => {
  ElMessage.success('Hello')
}

function onSubmit() {
  console.log('submit!')
}
</script>

<template>
  <el-container class="p-12">
    <el-header
      style="block-size: fit-content"
      class="md:m-auto lg:m-3 text-left text-5xl <md:text-4xl"
    >Smart Traveler</el-header>
    <el-main>
      <el-card class="lg:mx-12 lg:px-6 px-3">
        <el-row :gutter="24">
          <div class="m-2 flex-row">
            <span class="<md:block w-30 align-middle">旅費（新臺幣）</span>
            <el-input class="w-40 mx-2" v-model="bucket"></el-input>
          </div>
          <div class="m-2 flex-row">
            <span class="<md:block w-10 align-middle">地區</span>
            <el-select class="w-40 mx-2" v-model="region" placeholder="請選擇你希望旅遊的區域">
              <el-option label="Zone one" value="shanghai"></el-option>
              <el-option label="Zone two" value="beijing"></el-option>
            </el-select>
          </div>
          <div class="m-2 flex-row">
            <span class="<md:block w-30 md:ml-3 mr-6 text-left">治安等級大於 {{ safetyLevel }}</span>
            <el-slider class="w-50 inline-flex align-middle" v-model="safetyLevel"></el-slider>
          </div>
          <el-button
            style="block-size: fit-content"
            class="m-2"
            :icon="Search"
            type="success"
            @click="onSubmit"
          >搜尋</el-button>
        </el-row>
      </el-card>
    </el-main>
  </el-container>
</template>
