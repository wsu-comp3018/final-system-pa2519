<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
        @apply border-2 border-gray-500 w-full h-[40px] bg-black mb-4 mt-2 py-6 indent-4;
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
        <h1 class="text-center text-[35px] p-5"><b>Create Your Account</b></h1>

        <div class="h-fit w-[450px] bg-[#222222] rounded-xl mx-auto">

            <div class="p-10">
                <form>
                    <div class="flex justify-center gap-5">
                        <div>
                            <label for="fname">FIRST NAME</label>
                            <input type="text" id="fname" name="fname" placeholder="First Name">
                        </div>
                        <div>
                            <label for="lname">LAST NAME</label>
                            <input type="text" id="lname" name="lname" placeholder="Last Name">
                        </div>    
                    </div>
                    <label for="email">EMAIL ADDRESS</label>
                    <input type="email" id="email" name="email" placeholder="Email">

                    <label for="password">PASSWORD</label>
                    <input type="password" id="password" name="password" placeholder="Password">

                    <input type="submit" value="Sign Up">
                </form>
            </div>

        </div>
    </div>
</template>