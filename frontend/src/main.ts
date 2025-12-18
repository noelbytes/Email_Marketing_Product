import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {
  QueryClient,
  VueQueryPlugin,
  type VueQueryPluginOptions,
} from '@tanstack/vue-query'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})
const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClient,
}

app.use(createPinia())
app.use(router)
app.use(VueQueryPlugin, vueQueryPluginOptions)

app.mount('#app')
