<style scoped>
    button {
        padding: 8px;
        text-align: left;
        width: 100%;
        border-radius: 8px;
    }

    button:hover {
        background-color: #1f2937;
    }
</style>

<template> 
    <div class="flex justify-center gap-6 w-[1000px] m-auto">
        <div class="w-[25%] h-[650px] bg-[#222222] rounded-xl">
            <div class="p-7 text-[20px] text-pretty">
                <button>Account</button>
                <button>Statement Format Preferences</button>
            </div>
        </div>
        <div class="bg-[#222222] grow h-[650px] rounded-xl">
            <div class="text-center w-[50%] mx-auto bg-[#333333] p-6 rounded-b-lg">
                <h1>Account</h1>
            </div>
        </div>
    </div>
</template>