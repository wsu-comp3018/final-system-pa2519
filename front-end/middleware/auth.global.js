export default defineNuxtRouteMiddleware((to, from) => {
    const isToken = useCookie('token');
    if (!isToken.value && (to.path === '/' || to.path === '/signup' || to.path === '/login')) {
        return;
    }

    if (!isToken.value && to.path !== '/login') {
        return navigateTo('/')
    }

    if (isToken.value && to.path === '/login') {
        return navigateTo('/transcription')
    }
}) 