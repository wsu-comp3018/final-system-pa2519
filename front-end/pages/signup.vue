<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
        @apply border-2 border-gray-500 w-full h-[40px] bg-black mb-4 mt-2 py-6 indent-4;
    }

    

    input[type="submit"]{
        @apply border-2 border-gray-500 rounded-full w-full mt-[20px] p-[10px] bg-gray-500;
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