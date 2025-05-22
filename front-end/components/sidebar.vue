<script setup lang="ts">// for testing
    const items = ref([
        {
            sessions_Title: "Session_1"
        }, {
            sessions_Title: "Session_2"
        }, {
            sessions_Title: "Session_3"
        }, {
            sessions_Title: "Session_4"
        }, {
            sessions_Title: "Session_5"
        }, {
            sessions_Title: "Session_6"
        }, {
            sessions_Title: "Session_7"
        }, {
            sessions_Title: "Session_8"
        }, {
            sessions_Title: "Session_8"
        }, {
            sessions_Title: "Session_10"
        }
    ])

</script>

<template>

        
        <div class="p-4 bg-[#222222] overflow-hidden">
                <div class="text-center font-bold text-[40px]">
                    <h1>Sessions</h1>
                </div>
                <div class="grid gap-4 max-h-full overflow-y-auto">
                    <div v-for="item in items" class=" text-[20px] px-2 py-1 transition cursor-pointer hover:bg-neutral-700">
                        <span>{{ item.sessions_Title }}</span>
                    </div>
                </div>
        </div>

</template>