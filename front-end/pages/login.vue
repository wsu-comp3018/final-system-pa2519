<style scoped>
    input[type="email"], input[type="password"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        background-color: black;
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

    label {
        display: block;
        margin-top:16px;
    }

    span {
        color: red;
    }

</style>

<script setup>

    const { $api } = useNuxtApp();

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
    const validate_Email = () => {
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

    const validate_Password = () => {
        if (form.input.password === '') {
            form.error.password = 'Required';
        } else {
            form.error.password = '';
        }
    }

    const loginError = ref(false);
    const formValidation = () => {
        validate_Email();
        validate_Password();

        if(form.error.password !== '' && form.error.email !== '') {
            return;
        }
        $api.post("http://localhost:8000/api/login/", {
            email: form.input.email,
            password: form.input.password,
        }, {withCredentials: true})
        .then((response) => {
            console.log(response)
            return navigateTo('/transcription')
        })
        .catch ((error) => {
            loginError.value = true;
            setTimeout(() => {
                loginError.value = false;
            }, 3000);
            console.log("Error occured: ", error)
        })

        
    }

</script>

<template>
    
    <div class="m-auto p-10">
        <h1 class="flex justify-center text-[60px]"><b>WELCOME</b></h1>

        <div class="w-[450px] bg-[#222222] rounded-xl p-10">
            <h2 class="text-center text-[35px]"><b>LOGIN</b></h2> 

            <div class="flex justify-center">
                <form class="w-full" @submit.prevent="formValidation">
                    <label for="email">EMAIL</label>
                    <input type="email" id="email" v-model="form.input.email" name="email" placeholder="Email" @blur="validate_Email">
                    <span class="text-red-500">{{ form.error.email }}</span>

                    <label for="password">PASSWORD</label>
                    <input type="password" id="password" v-model="form.input.password" name="password" placeholder="Password" @blur="validate_Password">
                    <span class="text-red-500">{{ form.error.password }}</span>

                    <div>
                        <button><NuxtLink class="hover:underline inline" to="/resetpassword">Forgot Password?</NuxtLink></button>
                    </div>

                    <p v-if="loginError" class="text-center pt-3"><span>Email or password is incorrect</span></p>

                    <input type="submit" value="Login" class="cursor-pointer">
                </form>
            </div>
            <p class="text-center pt-4">Dont have a account? <NuxtLink to="/signup" class="hover:underline">Sign up here!</NuxtLink></p>

        </div>
    </div>
</template>