import path from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

import WindiCSS from 'vite-plugin-windicss';
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  },
  resolve: {
    alias: {
      "~/": `${path.resolve(__dirname, "src")}/`,
    },
  },
  css: {
    preprocessorOptions: {
      // scss: {
      //   additionalData: `@use "~/styles/element/index.scss" as *;`,
      // },
    },
  },
  plugins: [
    vue(),
    WindiCSS(),
    Components({
      resolvers: [
        ElementPlusResolver({
          importStyle: "sass",
        }),
      ],
    }),
  ],
});
