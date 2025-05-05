<style scoped>
    input[type="email"], input[type="password"]{
        @apply border-2 border-gray-500 w-full h-[40px] bg-black mb-6 mt-2 py-6 indent-4;
    }

    input[type="password"]{
        @apply my-2
    }

    input[type="submit"]{
        @apply border-2 border-gray-500 rounded-full w-full mt-[20px] p-[10px] bg-gray-500;
    }

</style>

<template>
    
    <div class="h-full p-10">
        <h1 class="flex justify-center text-[60px]"><b>WELCOME</b></h1>

        <div class="w-[450px] bg-[#222222] rounded-xl mx-auto">
            <h2 class="text-center text-[35px] p-5"><b>LOGIN</b></h2> 

            <div class="px-10 flex justify-center">
                <form>
                    <label for="email">EMAIL</label>
                    <input type="email" id="email" name="email" placeholder="Email">

                    <label for="password">PASSWORD</label>
                    <input type="password" id="password" name="password" placeholder="Password">
                    <button>Forgot Password?</button>

                    <input type="submit" value="Login">
                </form>
            </div>
            <p class="text-center p-6">Dont have a account? <NuxtLink to="/signup" class="hover:underline">Sign up here!</NuxtLink></p>

        </div>
    </div>
</template>