<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
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

    input[type="submit"] {
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
    
    const form = {}
    
</script>

<template>
    
    <div class="h-full m-auto">
        <h1 class="text-center text-[35px] p-5"><b>Create Your Account</b></h1>

        <div class="h-fit w-[450px] bg-[#222222] rounded-xl">

            <div class="p-10">
                <form id="signup-form" method="post" action="" @submit.prevent="formValidation">
                    <div class="flex justify-center gap-5">
                        <div>
                            <label for="fname">FIRST NAME *</label>
                            <input type="text" v-model="form.fname" id="fname" name="fname" placeholder="First Name" />
                        </div>
                        <div>
                            <label for="lname">LAST NAME *</label>
                            <input type="text" v-model="lname" id="lname" name="lname" placeholder="Last Name">
                        </div>    
                    </div>
                    <label for="email">EMAIL ADDRESS *</label>
                    <input type="email" v-model="email" id="email" name="email" placeholder="Email">

                    <label for="password">PASSWORD *</label>
                    <input type="password" v-model="password" id="password" name="password" placeholder="Password">

                    <label for="password">CONFIRM PASSWORD *</label>
                    <input type="password" v-model="confirm_pass" id="password" name="password" placeholder="Password">

                    <input type="submit" value="Sign Up" class="cursor-pointer">
                </form>

                <span v-if="error.fname" class="text-white">{{ error.fname }}</span>
            </div>

        </div>
    </div>
</template>