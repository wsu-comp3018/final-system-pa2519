<script setup>
    let sidebarIsOpen = ref(false);
    function toggle() {
        sidebarIsOpen.value = !sidebarIsOpen.value;
    } 

    let uploadMenu = ref(false);
    function displayUploadMenu() {
        uploadMenu.value = !uploadMenu.value;
    }

    const inputFile = useTemplateRef('fileInput');
    function openFileInputWindow() {
        inputFile.value.click();
    }

    var files;
    function getFiles(e) {
        files = e.target.files;
    }

    let recordingStatus = false;
    let recordingEnabled = ref(false);
    let fullRecording = [];
    let chunk = [];
    let fullRecorder = null;
    let chunkRecorder = null;

    function Setup(){
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices
                .getUserMedia({
                    audio: true
                })
                .then((stream) => {
                    fullRecorder = new MediaRecorder(stream);
                    chunkRecorder = new MediaRecorder(stream);

                    fullRecorder.ondataavailable = (event) => {
                        fullRecording.push(event.data);
                    }


                    chunkRecorder.ondataavailable = (event) => {
                        chunk.push(event.data);
                        const blob = new Blob(chunk, {type: "audio/wav"});
                        chunk = [];
                        request_Transcription(blob);
                    }
                    
                    fullRecorder.onstop = () => {
                        fullRecording = [];
                    }

                    recordingStatus = true;
                })
                .catch ((err) => {
                    console.error(err);
                });
        }

    
    }
    Setup();

    
    var intervalID;
    function enableMicrophone() {
        if (!recordingStatus) return;

        recordingEnabled.value = !recordingEnabled.value;

        if (recordingEnabled.value) {
            fullRecorder.start();
            chunkRecorder.start();

            intervalID = setInterval(() => {
                    chunkRecorder.stop();
                    chunkRecorder.start();
            }, 3000);

        } else {
            clearInterval(intervalID);
            fullRecorder.stop();
            chunkRecorder.stop();
        }

        console.log(recordingEnabled.value);
    }

    const transcription = ref("");
    async function request_Transcription(chunkBlob){
        const formData = new FormData();
        formData.append("audio", chunkBlob);

        console.log("Requesting");
        try{
            const response = await $fetch("http://127.0.0.1:8000/transcription/transcribe/", {
                method: "POST", 
                body: formData, 
            });

            
            if (response != ""){
                transcription.value += response;
            }
            

        } catch (error) {
            console.error(error.message);
        }

    }
    
</script>


<template>
    <div class="flex flex-col h-full w-5/6 mx-auto">

        <!--Temporary Icon-->
        <Icon class="cursor-pointer absolute left-0 top-[50%] rotate-90" size="25px" name="iconamoon:menu-burger-horizontal-bold" @click="toggle"/>

        <div class="flex justify-center py-5 h-5/6 text-black">
            <div class="w-full bg-white rounded-xl overflow-hidden mx-3">
                <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Transcribed Text</h2>
                <p class="px-2 overflow-y-auto overflow-hidden">{{ transcription }}</p>
            </div>

            <div class="w-full bg-white rounded-xl overflow-auto mx-3">
                <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Key Points</h2>
                <p class="px-2">This is a text placeholder.</p>
            </div>
        </div>
            
        <div class="flex justify-center gap-3 text-[30px] mx-3">
            <div class="grow p-2 bg-[#222222] space-x-6 content-center rounded-xl">
                <button class="bg-red-600 p-2 rounded-xl" @click="enableMicrophone()">REC</button>
                <button @click="displayUploadMenu">Upload Templates</button>
                 
            </div>
            <div class="p-4 bg-[#222222] rounded-xl">
                <button class="">Generate Statement</button>
                
            </div>
        </div>

    </div>

    <div v-if="sidebarIsOpen" class="z-10 w-full absolute bg-[rgba(0,0,0,0.8)] text-white">
        <Icon class="absolute right-0 m-5 mt-3 cursor-pointer" size="50px" name="gridicons:cross" @click="toggle"/>
        <Sidebar/>
    </div>

    <div v-if="uploadMenu" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-full">
        <div class="p-5 bg-white text-black w-[300px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            
            <h1 class="text-[20px]">Upload a template</h1>
            <form method="post" enctype="">
                <input ref="fileInput" @change="getFiles" type="file" name="template" id="template" class="hidden">
                <button class="bg-red-500 w-full py-2" @click="openFileInputWindow">Upload</button>
                <div v-for="file in files">
                    <span>{{ file.name }}</span>
                </div>
            
            </form>
        </div>
    </div>
    
</template>