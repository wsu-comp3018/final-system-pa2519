<script setup>
    definePageMeta({
        layout: 'logged-in'
    })

    const iconColor = ref("black");
    const enable = useTemplateRef("editableText");
    function toggleEdit(isEditable) {
        if (isEditable == 'true') {
            enable.value.contentEditable = 'true';
            iconColor.value = "green"
        } else {
            enable.value.contentEditable = 'false';
            iconColor.value = "black"
        }

    }
</script>


<template>
   
    <div class="mx-20">
        <h1 class="font-bold text-[50px]">Review Statement</h1>    

        <div class="flex justify-center gap-6">
            <div class="relative h-[580px] w-full border-2 border-red-500 rounded-xl bg-white p-4 overflow-hidden">
                <p ref="editableText" class="text-black h-full overflow-y-auto outline-none">What is this?</p>
                <button  @click="toggleEdit('false')" class="bg-[#222222] absolute bottom-3 right-3 px-3 py-2">Save</button>
            </div>

            <div class="bg-white border-2 border-red-500 h-fit flex flex-col py-6 m-auto">
                <Icon @click="toggleEdit('true')" :style="{color: iconColor}" class="inline-block mx-3 my-5 cursor-pointer" size="80px" name="material-symbols:edit-outline"/>
                <Icon class="text-black inline-block mx-3 my-5 cursor-pointer" size="80px" name="gridicons:cross"/>
                <Icon class="text-black inline-block mx-3 my-5 cursor-pointer" size="80px" name="ri:save-3-line"/>
            </div>
        </div>

    </div>
</template>
