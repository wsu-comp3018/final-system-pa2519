<script setup>
    definePageMeta({
        layout: 'logged-in',

    })

    const { $api } = useNuxtApp();
    const route = useRoute();
    const statement_content = ref('');
    const id = route.params.id;

    const getStatement = () => {

        $api.post('http://localhost:8000/api/get-statement/', {
            statement_id: id,
        }, {withCredentials: true})
        .then((response) => {
            statement_content.value = response.data.statement.split(/\n/);

        })
        .catch(async (error) => {
            await navigateTo('/transcription');
            console.log(error);
        })
    }
    getStatement();

    const iconColor = ref("black");
    const enable = useTemplateRef("editableText");
    const toggleEdit = (isEditable) => {
        if (isEditable == 'true') {
            enable.value.contentEditable = 'true';
            iconColor.value = "green";
        } else {
            enable.value.contentEditable = 'false';
            iconColor.value = "black";
            //console.log('guh', enable.value.innerText)
            saveChanges();
        }

    }

    const saveChanges = () => {
        const newStatement = enable.value.innerText;
        $api.post('http://localhost:8000/api/update-statement/', {
            statement_id: id,
            updated_statement: newStatement,
        }, {withCredentials: true}) 
        .then((response) => {
            console.log(response);
        })
        .catch((error) => {
            console.log(error);
        })
    }

    const deleteStatement = () => {

        $api.post('http://localhost:8000/delete-statement/', {
            statement_id: id,
        }, {withCredentials: true})
        .then((response) => {
            console.log(response)
            return navigateTo('/history')
        })
        .catch((error) => {
            console.log(error);
        })
    }

    const confirmPopup = ref(false);
    const showConfirmPopup = () => {
        console.log('here')
        confirmPopup.value = true;
        console.log(confirmPopup.value)
    }

    const confirmDelete = (answer) => {
        if (answer === 'Yes') {
            confirmPopup.value = false;
            $api.post('http://localhost:8000/api/delete-statement/', {statement_id: id}, {withCredentials: true})
            .then((response) => {
                return navigateTo('/history')
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

    const errorMessage = ref('Error in deleting statement, try again.');
    const errorPopup = ref(false);
    const displayErrorMessage = () => {
        errorPopup.value = true;
        setTimeout(() => {
            errorPopup.value = false;
        }, 3000);
    }
</script>


<template>
   
    <div class="m-auto h-[calc(100%-61.5px)] w-[90%]">
        <h1 class="font-bold text-[50px]">Review Statement</h1>    

        <div class="flex justify-center h-[calc(100%-120px)] gap-6">
            <div class="relative w-full h-full border-[5px] border-[#484949] rounded-xl bg-white p-4 overflow-hidden">
                <p ref="editableText" class="text-black h-full overflow-y-auto outline-none" >
                    <p v-for="line in statement_content">{{ line }}</p>
                </p>
                <button @click="toggleEdit('false')" class="bg-[#222222] absolute bottom-3 right-3 px-3 py-1 rounded-md">Save</button>
            </div>

            <div class="bg-white border-[5px] border-[#555656] h-fit flex flex-col my-auto">
                <Icon @click="toggleEdit('true')" :style="{color: iconColor}" class="inline-block mx-3 my-5 cursor-pointer" size="65px" name="material-symbols:edit-outline"/>
                <Icon class="text-black inline-block mx-3 my-5 cursor-pointer" size="65px" name="gridicons:cross" @click="showConfirmPopup"/>
            </div>
        </div>

    </div>

    <div v-if="confirmPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-dvh">
        <div class="p-5 bg-white text-black w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <p>Are you sure you want to delete the statement?</p>
            
            <div class="flex justify-center gap-4 pt-3">
                <button class="px-2 py-1" @click="confirmDelete('Yes')">Yes</button>
                <button class="px-2 py-1" @click="confirmDelete('No')">No</button>
            </div>
        </div>
    </div>

    <div v-if="errorPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] w-full h-full">
        <div class="p-5 text-white w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <p>{{ errorMessage }}</p>
        </div>
    </div>
</template>
