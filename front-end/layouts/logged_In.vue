<script setup>
    const {$api} = useNuxtApp()
    const showAccountOptions = ref(false);
    const dropdown = () => {
        showAccountOptions.value = !showAccountOptions.value
    }

    const closePopups = (event) => {
        if (showAccountOptions.value === true) {
            if (event.key === 'Escape') {
                showAccountOptions.value = false;
            } 


        }
    }

    onMounted(() => {
        document.addEventListener('keydown', closePopups);
    })
    const logout = () => {

        $api.post('http://localhost:8000/api/logout/', {withCredentials: true})
        .then((response) => {
            const token = useCookie('api_token');
            const refresh = useCookie('refresh_token');
            token.value = null;
            refresh.value = null;
            return navigateTo('/login')
        })
        .catch((error) => {
            // logoutFailed.value = true;
        })
        .finally(() => {
            const token = useCookie('api_token');
            const refresh = useCookie('refresh_token');
            token.value = null;
            refresh.value = null;
            return navigateTo('/login')
        })
    }
</script>


<template>
    <div class="h-screen flex flex-col text-white overflow-auto">
        <div class="grid grid-cols-2 py-3 text-white bg-[#222222] px-5"> 
            <div class="flex items-center gap-5">
                <h1 class="text-center font-bold text-[25px]"><NuxtLink to="/">Statement Creation Tool</NuxtLink></h1>            
            </div>

            <nav class="flex justify-end items-center text-[20px] gap-5">
                <button><NuxtLink to="/history">Statements</NuxtLink></button>
                <button><NuxtLink to="/transcription">Record</NuxtLink></button>
                <div class="relative">
                    <Icon class="flex cursor-pointer" size="35px" name="material-symbols:account-circle" @focusout="dropdown" @click="dropdown"/>
                    <div v-if="showAccountOptions" class="bg-[#555555] absolute -right-1 text-nowrap flex flex-col p-2 gap-2 text-[15px]">
                        <button><NuxtLink to="/setting">Account Settings</NuxtLink></button>
                        <button><NuxtLink @click="logout" >Logout</NuxtLink></button>
                    </div>
                </div>

            </nav>
        </div>
        
        <slot />
    </div>
    
    
    
</template>