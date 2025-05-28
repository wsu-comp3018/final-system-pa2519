<style scoped>
    /*button {
        padding: 8px;
        text-align: left;
        width: 100%;
        border-radius: 8px;
    }

    button:hover {
        background-color: #1f2937;
    }*/
    input {
        border-width: 2px;
        border-color: #9c9ea5;
        width: 100%;
        height: 40px;
        background-color: #222222;
        padding: 12px 0 12px 0;
        outline: none;
        margin-bottom: 16px;
        text-indent: 8px;
    }

    input:focus {
        border-color: white;
    }

    label {
        display: block;
    }


    hr {
        margin: 20px 0 20px 0;
    }

    h1 {
        font-size: 20px;
        font-weight: bold;
    }
    
</style>

<script setup>
    definePageMeta({
        layout: 'logged-in'
    })

    const form = reactive({
        email: '',
        current_password: '',
        new_password: '',
    })
    
    const { $api } = useNuxtApp();
    const changeEmail = ref(false);
    const passwordError = ref(false);
    const updateSuccessful = ref(null);
    const updateErrorMessage = ref('');
    const userDetails = ref([]);

    const getAccountSettings = async () => {
        await $api.get('http://localhost:8000/api/get-usersettings', {withCredentials: true})
        .then((response) => {
            console.log(response.data.user)
            userDetails.value = response.data.user;
            console.log(userDetails.value)
        })
        .catch((error) => {
            console.log(error);
        })
    }
    getAccountSettings();


    const enableChangeEmail = () => {
        changeEmail.value = !changeEmail.value;
    }

    const saveChanges = () => {
        
        if (form.email === '' && form.current_password === '' && form.new_password === '') {
            return;
        }

        if(form.current_password && form.new_password === '') {
            updateErrorMessage.value = "Current password empty."
            passwordError.value = true;
            setTimeout(() => {
                passwordError.value = false;
            }, 3000);
            return;
        } else if (form.current_password === '' && form.new_password) {
            updateErrorMessage.value = "New password empty"
            passwordError.value = true;
            setTimeout(() => {
                passwordError.value = false;
            }, 3000);
            return;
        }

        $api.post('http://localhost:8000/api/update-account/', {
            email: form.email,
            current_password: form.current_password,
            new_password: form.new_password,
        }, {withCredentials: true})
        .then((response) => {
            updateSuccessful.value = true;
            setTimeout(() => {
                updateSuccessful.value = null;
            }, 3000);
        })
        .catch((error) => {
            if (error.status == 400) {
                updateErrorMessage.value = "Your current password is incorrect"
                passwordError.value = true;
                setTimeout(() => {
                    passwordError.value = false;
                }, 3000);
                
            } else {
                updateSuccessful.value = false;
                setTimeout(() => {
                    updateSuccessful.value = null;
                }, 3000);
            }
        })
    }

    const resetChanges = () => {
        form.email = '';
        form.current_password = '';
        form.new_password = '';

        if (changeEmail.value === true) {
            enableChangeEmail();
        }
    }

    const confirmPopup = ref(false);
    const showConfirmPopup = () => {
        confirmPopup.value = true;
    }

    const confirmDelete = (answer) => {
        if (answer === 'Yes') {
            confirmPopup.value = false;
            $api.post('http://localhost:8000/api/delete-account/', {withCredentials: true})
            .then((response) => {
                const token = useCookie('api_token');
                const refresh = useCookie('refresh_token');
                token.value = null;
                refresh.value = null;
                return navigateTo('/login')
            })
            .catch((error) => {
                displayErrorMessage();
                return;
            })
        } else {
            confirmPopup.value = false;
            return;
        }
    }

    const errorMessage = ref('Error in deleting account, try again.');
    const errorPopup = ref(false);
    const displayErrorMessage = () => {
        errorPopup.value = true;
        setTimeout(() => {
            errorPopup.value = false;
        }, 3000);
    }
    
</script>

<template> 

    <div class="flex flex-col w-[650px] mx-auto my-10 bg-[#222222] rounded-xl h-fit">
        <div class="w-1/2 mx-auto text-center bg-[rgb(51,51,51)] p-6 rounded-b-lg">
            <h1 >Account Settings</h1>
        </div>
        <div class="flex py-8 px-6">
            <div class="grow px-10">
                <span class="hidden">New changes have being made. Apply these changes.</span>
                <form>
                    <h1>Basic Details</h1>
                    <div class="flex justify-center gap-10 py-4">
                        <div class="flex-1">
                            <p>First Name</p>
                            <p>{{ userDetails.first_name }}</p>
                        </div>
                        <div class="flex-1">
                            <p>Last Name</p>
                            <p>{{ userDetails.last_name }}</p>
                        </div>
                    </div>

                    <hr>

                    <div>
                        <label for="email">Email Address</label>
                        <div class="flex">
                            <p class="py-3 grow">Your email address is <strong>{{ userDetails.email }}</strong></p>
                            <button type="button" class="text-blue-400 underline" @click="enableChangeEmail">change</button>
                        </div>
                         <input v-if="changeEmail" v-model="form.email" type="email" id="email" name="email">
                    </div>
                    <hr>

                    <h1>Password</h1>
                    <div class="flex gap-8 pt-4">
                        <div class="flex-1">
                            <label for="currentPass">Current Password</label>
                            <input type="password" v-model="form.current_password" id="currentPass" name="currentPass">
                        </div>
                        <div class="flex-1">
                            <label for="newPass">New Password</label>
                            <input type="password" v-model="form.new_password" id="newPass" name="newPass">
                        </div>
                    </div>

                    <div v-if="passwordError" class="text-center">
                        <span class="text-red-500">{{ updateErrorMessage }}</span>
                    </div>
                </form>

               <div class="grow gap-6 flex py-3">
                    <button class="bg-[#259c4b] px-4 py-2 rounded-md" @click="saveChanges">Save all changes</button>
                    <button class="bg-[#565656] px-4 py-2 rounded-md" @click="resetChanges">Cancel</button>
               </div>

               <span v-if="updateSuccessful == true" class="text-green-500">Changes made successfully</span>
               <span v-else-if="updateSuccessful == false" class="text-red-500">An error occured trying to update. Try again.</span>
               <hr>

               <div>
                    <p>
                        By clicking "Delete Account" you are requesting for all data related to this account to
                        be deleted. If necessary, save any data locally before following through with the action.
                    </p>
                    <button class="bg-[#ae1f1f] px-4 py-2 mt-4 rounded-md" @click="showConfirmPopup">Delete Account</button>
               </div>
            </div>
        </div>
    </div>

    <div v-if="confirmPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-dvh">
        <div class="p-5 bg-white text-black w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <p>Are you sure you want to delete your account?</p>
            
            <div class="flex justify-center gap-4 pt-3 text-white">
                <button class="bg-[#222222] px-3 py-1 rounded-md" @click="confirmDelete('Yes')">Yes</button>
                <button class="bg-[#222222] px-3 py-1 rounded-md" @click="confirmDelete('No')">No</button>
            </div>
        </div>
    </div>

    <div v-if="errorPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] w-full h-full">
        <div class="p-5 text-white w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <p>{{ errorMessage }}</p>
        </div>
    </div>
</template>