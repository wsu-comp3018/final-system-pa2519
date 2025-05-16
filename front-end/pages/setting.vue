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
    input[type="text"], input[type="password"], input[type="email"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        background-color: black;
        padding: 12px 0 12px 0;
        text-indent: 16px;
        outline: none;
        margin-bottom: 16px;
    }

    label {
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

    hr {
        margin: 15px 0 15px 0;
    }

    h1 {
        font-size: 20px;
        font-weight: bold;
    }
</style>

<template> 

    <div class="flex flex-col w-[700px] mx-auto my-10 bg-[#222222] rounded-xl h-fit">
        <div class="w-1/2 mx-auto text-center bg-[rgb(51,51,51)] p-6 rounded-b-lg">
            <h1 >Account Settings</h1>
        </div>
        <div class="flex py-8 px-12">
            <div class="grow px-10">
                <span class="hidden">New changes have being made. Apply these changes.</span>
                <form>
                    <h1>Basic Account Details</h1>
                    <div class="flex justify-center gap-10">
                        <div class="flex-1">
                            <label for="fname">First Name</label>
                            <input type="text" id="fname" name="fname">
                        </div>
                        <div class="flex-1">
                            <label for="lname">Last Name</label>
                            <input type="text" id="lname" name="fname">
                        </div>
                    </div>
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email">

                    <hr>

                    <h1>Password</h1>
                    <label for="currentPass">Current Password</label>
                    <input type="password" id="currentPass" name="currentPass">
                    <label for="newPass">New Password</label>
                    <input type="password" id="newPass" name="newPass">
                </form>

               <div class="grow gap-6 flex justify-end">
                    <button class="bg-green-500 p-2">Update</button>
                    <button class="bg-gray-500 p-2">Cancel</button>
               </div>

               <hr>

               <div>
                    <p>
                        By clicking "Delete Account" you are requesting for all data related to this account to
                        be deleted. If necessary, save any data locally before following through with the action.
                    </p>
                    <button class=" bg-red-500 p-1 mt-4">Delete Account</button>
               </div>
            </div>
        </div>
    </div>
</template>