

<template>
    <div class="h-screen flex flex-col text-white overflow-auto">
        <div class="grid grid-cols-2 py-3 text-white bg-[#222222] px-5"> 
            <div class="flex items-center gap-5">
                <h1 class="text-center font-bold text-[25px]">Statement Creation Tool</h1>            
            </div>

            <nav class="flex justify-end items-center text-[20px] gap-5">
                <button>About</button>
                <button>History</button>
                <button>Record</button>
                <button class="inline-block w-12 h-12 text-center border-2 border-white rounded-full">JM</button>       
            </nav>
        </div>
        
        <slot />
    </div>
    
    
    
</template>