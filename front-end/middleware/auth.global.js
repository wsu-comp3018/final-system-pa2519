export default defineNuxtRouteMiddleware((to, from) => {
    const isToken = useCookie('api_token');
    if (!isToken.value && (to.path === '/' || to.path === '/signup' || to.path === '/login' || to.path === '/resetpassword')) {
        return;
    }

    if (!isToken.value && to.path !== '/login') {
        return navigateTo('/')
    }

    if (isToken.value && to.path === '/login') {
        return navigateTo('/transcription')
    }
}) 