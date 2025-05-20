<script setup>

    definePageMeta({
        layout: 'logged-in'
    })

    let sidebarIsOpen = ref(false);
    const toggleSidebar = () => {
        sidebarIsOpen.value = !sidebarIsOpen.value;
    } 


    let uploadMenu = ref(false);
    const toggleUploadMenu = () => {
        uploadMenu.value = !uploadMenu.value;
    }

    const inputFile = useTemplateRef('fileInput');
    const openFileInputWindow = () => {
        inputFile.value.click();
    }

    var file = ref(null);
    const getFile = (e) => {
        file.value = e.target.files[0];
    }

    let fileError = ref("");
    const fileSubmit = () => {
        const { $api } = useNuxtApp();
        fileError.value = "";
        if (file.value.length === 0) {
            fileError.value = "Please submit a file.";
            return
        } else {
            
            const template = new FormData();
            template.append('template', file.value);

            $api.post("http://localhost:8000/api/upload/template/", template)
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log("Error", error);
            })
        }
   
    }

    let recordingStatus = false;
    let recordingEnabled = ref(false);
    let fullRecording = [];
    let chunk = [];
    let fullRecorder = null;
    let chunkRecorder = null;

    function Setup() {
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
                        const blob = new Blob(fullRecording, {type: "audio/wav"});
                        fullRecording = [];
                        sendFullAudioRecording(blob)
                    }


                    chunkRecorder.ondataavailable = (event) => {
                        chunk.push(event.data);
                        const blob = new Blob(chunk, {type: "audio/wav"});
                        chunk = [];
                        //request_Transcription(blob);
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

    function enableMicrophone () {
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
            // will need to replace later
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

    const sendFullAudioRecording = (audioBlob) => {
        const fullAudio = new FormData();
        fullAudio.append("fullAudio", audioBlob);

        const { $api } = useNuxtApp();
        $api.post("http://localhost:8000/api/upload/recording/", fullAudio)
        .then ((response) => {
            console.log(response);
        })
        .catch((error) => {
            console.log("Error", error);
        })
    }
    
</script>


<template>
    <div class="flex flex-col h-full w-5/6 mx-auto">

        <!--Temporary Icon. Opens sidebar-->
        <Icon class="cursor-pointer absolute left-0 top-[50%] rotate-90" size="25px" name="iconamoon:menu-burger-horizontal-bold" @click="toggleSidebar"/>

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
            <div class="flex items-center p-4 bg-[#222222] space-x-6 rounded-xl">
                <Icon size="37px" class="cursor-pointer" name="fluent:mic-record-20-regular" @click="enableMicrophone"/>
                <Icon size="37px" class="cursor-pointer" name="material-symbols:upload-file-outline" @click="toggleUploadMenu"/>
                 
            </div>
            <div class="p-4 bg-[#222222] rounded-xl">
                <button class="">Generate Statement</button>
                
            </div>
        </div>

    </div>


    <div v-if="sidebarIsOpen" class="z-10 w-full absolute bg-[rgba(0,0,0,0.8)] text-white">
        <Icon class="absolute right-0 m-5 mt-3 cursor-pointer" size="50px" name="gridicons:cross" @click="toggleSidebar"/>
        <Sidebar/>
    </div>


    <div v-if="uploadMenu" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-full">
        <div class="p-5 bg-white text-black w-[300px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <Icon class="absolute right-0 top-0 mt-2 mr-2 cursor-pointer" size="20px" name="gridicons:cross" @click="toggleUploadMenu"/>

            <h1 class="text-[20px]">Upload a template</h1>
            <form method="post" @submit.prevent="fileSubmit">
                <input ref="fileInput" @change="getFile" type="file" name="template" id="template" class="hidden">
                <button type="button" class="bg-blue-500 w-full py-2" @click="openFileInputWindow">Upload</button>
                <span class="text-red-500">{{ fileError }}</span>
                <p class="pt-2">Chosen file: <span v-if="file != null">{{ file.name }}</span></p>
                <input type="submit" value="submit" class="cursor-pointer">
            </form>
        

        </div>
    </div>
    
</template>