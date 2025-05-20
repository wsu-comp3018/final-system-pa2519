export default defineNuxtRouteMiddleware((to, from) => {
    const isToken = useCookie('token');
    if (!isToken.value && to.path === '/') {
        return;
    }

    if (!isToken.value && to.path !== '/login') {
        return navigateTo('/login')
    }

    if (isToken.value && to.path === '/login') {
        return navigateTo('/transcription')
    }
}) 