// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss', '@nuxt/icon', 
    
  
  ],


  runtimeConfig: {
    public:{
      apiUrl: process.env.NUXT_API_URL || process.env.VITE_API_URL,
    }
  },

  plugins: [
    '~/plugins/axios.client.ts',
  ],
  

  ssr: false,

  app: {
    head: {
      bodyAttrs: {
        style: 'background-color: black'
      }
    }
  },

  compatibilityDate: '2025-04-03'
})