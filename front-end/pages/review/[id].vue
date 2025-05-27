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
            statement_content.value = response.data.statement;

        })
        .catch(async (error) => {
            //await navigateTo('/transcription');
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
            console.log('guh', enable.value.innerText)
            saveChanges();
        }

    }

    const saveChanges = () => {
        const newStatement = enable.value.innerText;
        $api.post('http://localhost:8000/api/update-statement', {
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
        })
        .catch((error) => {
            console.log(error);
        })
    }
</script>


<template>
   
    <div class="m-auto h-[calc(100%-61.5px)] w-[90%]">
        <h1 class="font-bold text-[50px]">Review Statement</h1>    

        <div class="flex justify-center h-[calc(100%-120px)] gap-6">
            <div class="relative w-full h-full border-2 border-red-500 rounded-xl bg-white p-4 overflow-hidden">
                <p ref="editableText" class="text-black h-full overflow-y-auto outline-none" >{{ statement_content }}</p>
                <button @click="toggleEdit('false')" class="bg-[#222222] absolute bottom-3 right-3 px-3 py-2">Save</button>
            </div>

            <div class="bg-white border-2 border-red-500 h-fit flex flex-col my-auto">
                <Icon @click="toggleEdit('true')" :style="{color: iconColor}" class="inline-block mx-3 my-5 cursor-pointer" size="60px" name="material-symbols:edit-outline"/>
                <Icon class="text-black inline-block mx-3 my-5 cursor-pointer" size="60px" name="gridicons:cross"/>
                <Icon class="text-black inline-block mx-3 my-5 cursor-pointer" size="60px" name="ri:save-3-line"/>
            </div>
        </div>

    </div>
</template>
