<script setup>

    definePageMeta({
        middleware: function (to, from) {
            const token = useCookie('api_token');
            if (token.value) {
                setPageLayout('logged-in')
            }
        }
    })
</script>

<template>
    
    <div class="h-full p-8">
        
        <div class="text-center w-[68%] mx-auto">
            <header>
                <h1 class="font-bold text-[60px]">
                    Save time, reduce effort.
                    Generate statements in seconds!
                </h1>
                <p class="text-[20px] w-[70%] py-6 mx-auto">
                    AI-powered tool with the ability to transcribe, record and generate statements. 
                    Designed specifically for investigators, insurers and legal teams.
                </p>

                <h2 class="text-[20px]">Powered by:</h2>
                <div class="flex gap-4 pb-4 justify-center">
                    <img src="~/assets/img/whisperAI.png" width="100" height="100">
                    <img src="~/assets/img/sparkNLP.png" width="200">
                </div>

                <button class="rounded-xl border border-1 px-6 py-3 mt-5" ><NuxtLink to="/login">GET STARTED</NuxtLink></button>
            </header>
        </div>
    </div>
        <footer>
            
        </footer>
</template>