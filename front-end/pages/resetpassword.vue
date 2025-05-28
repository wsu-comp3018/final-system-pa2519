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
            current_password: '',
            new_password: '',
        },

        error: {
            email: '',
            password: '',
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

    const validate_CurrentPassword = () => {
        if (form.input.current_password === '') {
            form.error.current_password = 'Required';
        } else {
            form.error.current_password = '';
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
        validate_FirstName();
        validate_LastName();
        validate_Email();
        validate_Password();
        validate_ConfirmPass();

        console.log(form.input.fname);

        if (form.error.email !== "" || form.error.current_password !== "" || form.error.new_password !== "") {
            return;
        }

        $api.post('http://localhost:8000/api/reset/', {
            email: form.input.email,
            current_password: form.input.current_password,
            new_password: form.input.new_password,
        }, {withCredentials: true})
        .then((response) => {
            console.log(response);
            if (response.status == 200) {
                navigateTo('/login');
            }
        })
        .catch((error) => {
            resetError.value = true;
            setTimeout(() => {
                resetError.value = false;
            }, 3000);
            console.log("Error: ", error);
        })
    }
    
</script>

<template>
    
    <div class="m-auto">

        <div class="w-[450px] bg-[#222222] rounded-xl">

            <div class="p-10">
                <h1 class="text-center text-[35px]"><b>Reset Your Password</b></h1>

                <form @submit.prevent="formValidation">

                    <label for="email">EMAIL ADDRESS *</label>
                    <input type="email" v-model="form.input.email" id="email" name="email" placeholder="Email" @blur="validate_Email">
                    <span>{{ form.error.email }}</span>

                    <label for="password">CURRENT PASSWORD *</label>
                    <input type="password" v-model="form.input.current_password" id="password" name="password" placeholder="Password" @blur="validate_CurrentPassword">
                    <span>{{ form.error.current_password }}</span>

                    <label for="confirm_pass">NEW PASSWORD *</label>
                    <input type="password" v-model="form.input.new_password" id="confirm_pass" name="password" placeholder="Password" @blur="validate_NewPassword">
                    <span>{{ form.error.new_password }}</span>

                    <p v-if="resetError" class="text-center pt-3"><span>Email or password is incorrect</span></p>

                    <input type="submit" value="Reset" class="cursor-pointer">
                </form>
            </div>

        </div>
    </div>
</template>
