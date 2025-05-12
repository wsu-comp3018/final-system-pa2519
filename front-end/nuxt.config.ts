// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss', '@nuxt/icon',
    '@nuxtjs/auth'
  
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