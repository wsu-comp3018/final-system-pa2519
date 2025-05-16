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

import ExampleComponent from '~/components/ExampleComponent.vue';
    const { $api } = useNuxtApp();
    const handleSignup = () => {
        $api.get("signup").then((resp) => {
            console.log(resp)
    })
    .catch((err) => {
        console.log(err)
    })
    }

    const form = reactive({
        input: {
            fname: '',
            lname: '',
            email: '',
            password: '',
            confirm_pass: '',
        },

        error: {
            fname: '',
            lname: '',
            email: '',
            password: '',
            confirm_pass: '',
        }
    })

    function validate_FirstName() {
        if (form.input.fname === '') {
            form.error.fname = 'Required';
        } else {
            form.error.fname = '';
        }
    }

    function validate_LastName() {
        if (form.input.lname === '') {
            form.error.lname = 'Required';
        } else {
            form.error.lname = '';
        }
    }

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

    function validate_ConfirmPass() {
        if (form.input.password !== form.input.confirm_pass) {
            form.error.confirm_pass = 'This password does not match';
        } else {
            form.error.confirm_pass = '';
        }
    }

    function formValidation() {
        if (form.input.fname === '') {
            form.error.fname === 'Required';
        }
    }
    
</script>

<template>
    
    <div class="m-auto">

        <div class="w-[550px] bg-[#222222] rounded-xl">

            <div class="p-10">
                <h1 class="text-center text-[35px]"><b>Create Your Account</b></h1>

                <form id="signup-form" method="post" action="" @submit.prevent="formValidation">
                    <div class="flex justify-center gap-10">
                        <div class="flex-1">
                            <label for="fname">FIRST NAME *</label>
                            <input type="text" v-model="form.input.fname" id="fname" name="fname" placeholder="First Name" @blur="validate_FirstName">
                            <span>{{ form.error.fname }}</span>
                        </div>
                        <div class="flex-1">
                            <label for="lname">LAST NAME *</label>
                            <input type="text" v-model="form.input.lname" id="lname" name="lname" placeholder="Last Name" @blur="validate_LastName">
                            <span>{{ form.error.lname }}</span>
                        </div>    
                    </div>
                    <label for="email">EMAIL ADDRESS *</label>
                    <input type="email" v-model="form.input.email" id="email" name="email" placeholder="Email" @blur="validate_Email">
                    <span>{{ form.error.email }}</span>

                    <label for="password">PASSWORD *</label>
                    <input type="password" v-model="form.input.password" id="password" name="password" placeholder="Password" @blur="validate_Password">
                    <span>{{ form.error.password }}</span>

                    <label for="password">CONFIRM PASSWORD *</label>
                    <input type="password" v-model="form.input.confirm_pass" id="password" name="password" placeholder="Password" @input="validate_ConfirmPass">
                    <span>{{ form.error.confirm_pass }}</span>

                    <button @click="handleSignup" class="cursor-pointer">Sign Up</button> 
                </form>

                <!--<span v-if="error.fname" class="text-white">{{ error.fname }}</span>-->
            </div>

        </div>
    </div>
</template>
