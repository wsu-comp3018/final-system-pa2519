<style scoped>
    input, select{
        @apply w-full
    }
</style>
<template>
    <div class="flex flex-col h-full w-[1100px] mx-auto my-5 overflow-hidden">

        <div class="my-5 p-2 bg-gray-500">
            <h1 class="font-bold text-[25px]">Filter</h1>
            <form class="flex gap-4 text-black">
                <input type="text" id="name" name="name" placeholder="Name">
                <input type="date" id="date" name="date" placeholder="Date">
                <input type="number" id="REF" name="REF" placeholder="REF #">
                <select id="statement_type" name="statement_type">
                    <option>Default</option>
                </select>
            </form>
        </div>

        <div class="flex justify-center gap-4 overflow-hidden">

            <div class="h-fit w-2/6 bg-gray-500">
                <h1 class="text-center text-[25px] bg-gray-800">Selected Statement</h1>
                <div class="px-5 py-2 h-[90%] overflow-y-auto">
                    <p class="text-[30px]">John Smith [REF: 10465]</p>
                    <p class="text-[20px]">
                        Case against his worksite manager, claims negligence. Can't work any more due to constant
                        migraines since accident, seeking insurance settlement. 
                    </p>
                </div>
            </div>

            <div class="grow overflow-y-auto overflow-hidden">
                <div class="flex mb-5 p-2 bg-gray-500">
                    <div>
                        <p class="text-[30px]">John Smith [REF: 10465]</p>
                        <p class="text-[20px]">Insurance Claim Case</p>
                    </div>
                    <div class="grow self-end text-right">
                        <button class="bg-gray-800 px-5 py-2 text-[20px]">Open</button>
                    </div>
                </div>
                
            </div>

        </div>
    </div>
</template>