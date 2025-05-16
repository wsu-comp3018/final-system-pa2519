import type { AxiosInstance } from 'axios'

export interface ApiInjectionContext {
  api: AxiosInstance
  rootApi: AxiosInstance
  api_url: string
}

declare module '#app' {
  interface NuxtApp {
    $api: AxiosInstance
    $rootApi: AxiosInstance
    $api_url: string
  }
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: AxiosInstance
    $rootApi: AxiosInstance
    $api_url: string
  }
}