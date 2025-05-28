

<template>
    <div class="h-screen flex flex-col text-white overflow-auto">
        <div class="grid grid-cols-2 py-3 text-white bg-[#222222] px-5"> 
            <div class="flex items-center gap-5">
                <h1 class="text-center font-bold text-[25px]"><NuxtLink to="/">Statement Creation Tool</NuxtLink></h1>            
            </div>

            <nav class="flex justify-end items-center text-[20px] gap-5">
                <button><NuxtLink to="/login">Login</NuxtLink></button> 
            </nav>
        </div>
        
        <slot />
    </div>
    
    
    
</template>