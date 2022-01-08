<script setup lang="ts">
import { onMounted, ref, computed, reactive } from "vue";
import { ElMessage } from 'element-plus'

defineProps<{
  msg: string
}>();

interface CountryInfo {
  liveExchangerates: number;
  avgExchangerates: number;
  perExchangerate: number;
  crimeIndex: number;
  safetyIndex: number,
}

let bucket = ref(0);
let requiredSafetyIndex = ref(0);
let region = ref('');

const toast = (msg: string) => {
  ElMessage.success(msg)
}

const countrys = [
  'South Africa',
  'Sweden',
  'United Kingdom',
  'Japan',
  'Indonesia',
  'Australia',
  'Malaysia',
  'Euro Zone',
  'Canada',
  'Vietnam',
  'USA',
  'Hong Kong',
  'New Zealand',
  'Korea',
  'Philippines',
  'Thailand',
  'Singapore',
  'China',
  'Switzerland',
];
const contients: { [k: string]: string[] } = {
  'Asia': [
    'Philippines',
    'Korea',
    'Hong Kong',
    'Vietnam',
    'Japan',
    'Indonesia',
    'Thailand',
    'Singapore',
    'China',
    'Malaysia',
  ],
  'Africa': [
    'South Africa',
  ],
  'Europe': [
    'Sweden',
    'United Kingdom',
    'Euro Zone',
    'Switzerland',
  ],
  'North America': [
    'Canada',
    'USA',
  ],
  'South America': [],
  'Oceania': [
    'Australia',
    'New Zealand',
  ],
  'Antarctica': [],
};

let infos: { [k: string]: CountryInfo } = reactive({});

async function getInfo(country: string) {
  const params = new URLSearchParams({ country });
  const url = '/api';
  const resp = await fetch(`${url}?${params.toString()}`);
  if (resp.status != 200) {
    console.log('Query failed');
    return null;
  }
  const info: CountryInfo = await resp.json();
  return info;
}

async function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

onMounted(async () => {
  let ready = true;
  do {
    const promise: [string, CountryInfo | null][] = await Promise.all(
      countrys.map(async (c) => [c, await getInfo(c)])
    );
    for (const [c, info] of promise) {
      if (info === null) {
        ready = false;
        continue;
      }
      infos[c] = info;
    }
    await sleep(5000);
  } while (!ready);
  toast('Fectch done.');
});

function shouldDisplay(info: CountryInfo & { country: string }) {
  let countries = contients[region.value];
  return (info.safetyIndex >= requiredSafetyIndex.value)
    && (region.value === '' || countries?.indexOf(info.country) !== -1)
}

const infoTable = computed(() => Object.entries(infos).map(([c, info]) => ({ country: c, ...info })));
const filteredInfoTable = computed(() => infoTable.value.filter(shouldDisplay));
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
            <span class="<md:block w-10 align-middle">地區</span>
            <el-select clearable class="w-55 mx-2" v-model="region" placeholder="請選擇你希望旅遊的區域">
              <el-option
                v-for="contient in Object.keys(contients)"
                :label="contient"
                :value="contient"
              ></el-option>
            </el-select>
          </div>
          <div class="m-2 flex-row">
            <span class="<md:block w-30 md:ml-3 mr-6 text-left">治安等級大於 {{ requiredSafetyIndex }}</span>
            <el-slider class="w-40 inline-flex align-middle" v-model="requiredSafetyIndex"></el-slider>
          </div>
          <div class="lg:flex-grow <lg:w-full"></div>
        </el-row>
        <el-table :data="filteredInfoTable" style="width: 100%">
          <el-table-column prop="country" label="國家 / 地區" />
          <el-table-column prop="liveExchangerates" label="即時匯率" />
          <el-table-column prop="avgExchangerates" label="平均匯率" />
          <el-table-column label="匯率漲跌幅">
            <template #default="scope">{{ scope.row.perExchangerate }} %</template>
          </el-table-column>
          <el-table-column label="安全指數">
            <template #default="scope">{{ scope.row.safetyIndex || 'N/A' }}</template>
          </el-table-column>
          <el-table-column label="犯罪指數">
            <template #default="scope">{{ scope.row.crimeIndex || 'N/A' }}</template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>
