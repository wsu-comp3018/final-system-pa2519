import axios, { AxiosError, AxiosHeaders } from 'axios'
import type { AxiosInstance, AxiosRequestConfig, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import Cookie from 'js-cookie'
import type { RuntimeConfig } from 'nuxt/schema'
import { signoutAndRedirect } from '~/assets/js/auth'
import type { ApiInjectionContext } from '~/types/axios'

interface FailedRequest {
    resolve: (value: AxiosResponse | PromiseLike<AxiosResponse>) => void
    reject: (reason?: any) => void
    config: AxiosRequestConfig
}

export default defineNuxtPlugin(() => {
    const runtimeConfig: RuntimeConfig = useRuntimeConfig()
    const REFRESH_URL: string | undefined = '/auth/token/refresh'
    const INSTANCE_KEY: string | undefined = 'api_token'
    const BASE_URL: string | undefined = runtimeConfig.public.apiUrl

    let isRefreshing = false
    let failedQueue: FailedRequest[] = []

    const getKey = (): string => {
        return Cookie.get(INSTANCE_KEY) || ''
    }

    const processQueue = (error: any, token?: string) => {
        failedQueue.forEach(({ resolve, reject, config }) => {
            if (token) {
                config.headers = {
                    ...config.headers,
                    Authorization: `Bearer ${token}`,
                }
                resolve(axios(config))
            } else {
                reject(error)
            }
        })
        failedQueue = []
    }

    const api: AxiosInstance = axios.create({
        baseURL: BASE_URL,
        headers: {
            Authorization: `Bearer ${getKey(false)}`,
            'X-Requested-With': 'XMLHttpRequest',
            Accept: 'application/json',
        },
    })

    const responseInterceptor = (instance: AxiosInstance) => {
        instance.interceptors.response.use(
            (response: AxiosResponse) => response,
            async (error: AxiosError) => {
                const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

                if (error.response?.status === 401 && !originalRequest._retry) {
                    if (isRefreshing) {
                        return new Promise<AxiosResponse>((resolve, reject) => {
                            failedQueue.push({ resolve, reject, config: originalRequest })
                        })
                    }

                    originalRequest._retry = true
                    isRefreshing = true

                    try {
                        const refreshResponse = await instance.post(REFRESH_URL, null, {
                            headers: {
                                Authorization: `Bearer ${getKey()}`,
                            },
                        })

                        const newToken = refreshResponse.data?.token
                        Cookie.set(INSTANCE_KEY, newToken)
                        processQueue(null, newToken)

                        originalRequest.headers = {
                            ...originalRequest.headers,
                            Authorization: `Bearer ${newToken}`,
                        }

                        return axios(originalRequest)
                    } catch (refreshError) {
                        processQueue(refreshError, undefined)
                        signoutAndRedirect(instance)
                        throw refreshError
                    } finally {
                        isRefreshing = false
                    }
                }

                return Promise.reject(error)
            }
        )
    }

    const requestInterceptor = (instance: AxiosInstance) => {
        instance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
            const token = getKey()
            if (token) {
                if (!config.headers) {
                    config.headers = new AxiosHeaders()
                }
                config.headers.set('Authorization', `Bearer ${token}`)
            }
            return config
        })
    }

    responseInterceptor(api)
    requestInterceptor(api)

    const context: ApiInjectionContext = {
        api,
        api_url: BASE_URL,
    }

    return {
        provide: {
            api: context.api,
            api_url: context.api_url,
        },
    }
})