<style scoped>
    input[type="email"], input[type="password"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        background-color: black;
        margin-bottom: 16px;
        margin-top: 8px;
        padding: 24px 0 24px 0;
        text-indent: 16px;
    }

    input[type="password"]{
        margin: 8px 0 8px 0;
        
    }

    input[type="submit"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        margin-top: 20px;
        padding: 10px;
        background-color: #6b7280;
        border-radius: 9999px;
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