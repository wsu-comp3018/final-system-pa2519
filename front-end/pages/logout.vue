<script setup>

    const { $api } = useNuxtApp();
    const logoutFailed = ref(false);
    const logout = () => {

        $api.post('http://localhost:8000/api/logout/', {withCredentials: true})
        .then((response) => {
            const token = useCookie('api_token');
            const refresh = useCookie('refresh_token')
            token.value = null;
            refresh.value = null;
            return navigateTo('/login')
        })
        .catch((error) => {
            logoutFailed.value = true;
        })
    }
    logout();
</script>

<template>
    <div class="w-full text-center text-[40px] m-auto" v-if="logoutFailed">
        <p>An error occured attempting to logout.</p>
    </div>
</template>