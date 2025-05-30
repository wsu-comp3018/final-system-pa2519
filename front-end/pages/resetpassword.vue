<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        background-color: black;
        
        padding: 24px 0 24px 0;
        text-indent: 16px;
    }

    label {
        margin-top: 16px;
        display: block;
    }

    input[type="submit"] {
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        margin-top: 20px;
        padding: 10px;
        background-color: #6b7280;
        border-radius: 9999px;
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
            new_password: '',
        },

        error: {
            email: '',
            new_password: '',
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

    const validate_NewPassword = () => {
        if (form.input.new_password === '') {
            form.error.new_password = 'Required';
        } else {
            form.error.new_password = '';
        }
    }

    const resetError = ref(false);
    const formValidation = () => {
        validate_Email();
    }
    
</script>

<!--Incomplete no functionality implemented for this page-->
<template>
    
    <div class="m-auto">

        <div class="w-[450px] bg-[#222222] rounded-xl">

            <div class="p-10">
                <h1 class="text-center text-[35px]"><b>Enter your email</b></h1>

                <form @submit.prevent="formValidation">

                    <label for="email">EMAIL ADDRESS *</label>
                    <input type="email" v-model="form.input.email" id="email" name="email" placeholder="Email" @blur="validate_Email">
                    <span>{{ form.error.email }}</span>

                    <p v-if="resetError" class="text-center pt-3"><span>Email is incorrect</span></p>

                    <input type="submit" value="Reset" class="cursor-pointer">
                </form>
            </div>

        </div>
    </div>
</template>
