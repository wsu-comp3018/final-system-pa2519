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

<script setup>
    const form = reactive({
        input: {
            email: '',
            password: '',
        },

        error: {
            email: '',
            password: '',
        }
    })

    var email_Regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    function validate_Email() {
        if (form.input.email === '') {
            form.error.email = 'Required';
        } else {

            if (email_Regex.test(form.input.email) ) {
                form.error.email = '';
            } else {
                form.error.email = 'Invalid email address';
            }
        }
    }

    function validate_Password() {
        if (form.input.password === '') {
            form.error.password = 'Required';
        } else {
            form.error.password = '';
        }
    }

</script>

<template>
    
    <div class="mx-auto p-10">
        <h1 class="flex justify-center text-[60px]"><b>WELCOME</b></h1>

        <div class="w-[450px] bg-[#222222] rounded-xl p-10">
            <h2 class="text-center text-[35px]"><b>LOGIN</b></h2> 

            <div class="flex justify-center">
                <form>
                    <label for="email">EMAIL</label>
                    <input type="email" id="email" name="email" placeholder="Email" @blur="validate_Email">

                    <label for="password">PASSWORD</label>
                    <input type="password" id="password" name="password" placeholder="Password" @blur="validate_Password">
                    <NuxtLink class="hover:underline ">Forgot Password?</NuxtLink>

                    <input type="submit" value="Login">
                </form>
            </div>
            <p class="text-center pt-4">Dont have a account? <NuxtLink to="/signup" class="hover:underline">Sign up here!</NuxtLink></p>

        </div>
    </div>
</template>