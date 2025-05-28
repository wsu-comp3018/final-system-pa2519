<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        
        padding: 24px 0 24px 0;
        text-indent: 16px;
    }

    label {
        margin-top: 16px;
        display: block;
    }

</style>

<script setup>

    definePageMeta({
        layout: 'logged-in'
    })

    const form = reactive({
        input: {
            client_fname: '',
            client_lname: '',
            session_Name: '',
        }
    })
    let currentSessionID = ref(null);
    const emptyError = ref(false);
    const creationError = ref(false);
    let isNewSession = ref(false);
    const transcription = ref("");
    const summary = ref("");
    const { $api } = useNuxtApp();


    const closePopups = (event) => {
        if (event.key === 'Escape') {
            isNewSession.value = false;
            uploadMenu.value = false;

            form.input.client_fname = '';
            form.input.client_lname = '';
            form.input.session_Name = '';

            file.value = [];
        }
    }

    onMounted(() => {
        document.addEventListener('keydown', closePopups);
    })
    
    const sessionList = ref([]);
    const getSessions = () => {
        $api.get('http://localhost:8000/api/getSessionList/')
        .then((response) => {
            console.log(response.data.data)
            sessionList.value = response.data.data;
        })
        .catch((error) => {
            console.log(error);
        })  
    }   
    getSessions();
    
    const callSummariser = () => {
        $api.post('http://localhost:8000/api/summary/', {
            session_id: currentSessionID.value,
        })
        .then ((response) => {
            console.log(response.data.Summary);
            summary.value = response.data.Summary;
            
        })
        .catch((error) => {
            console.log(error);
        })
    }

    const createSession = () => {
        emptyError.value = false;
        if (form.input.client_fname === '' || form.input.client_lname === '' || form.input.session_Name === '') {
            emptyError.value = true;
            return;
        }

        $api.post('http://localhost:8000/api/createSession/', {
            fname: form.input.client_fname,
            lname: form.input.client_lname,
            session_Name: form.input.session_Name,
        })
        .then((response) => {
            console.log(response);
            if (response.status == 200) {
                isNewSession.value = false;
                form.input.client_fname = '';
                form.input.client_lname = '';
                form.input.session_Name = '';
            }
            getSessions();

        })
        .catch((error) => {
            creationError.value = true;
            setTimeout(() => {
                creationError.value = false;
            }, 3000);
            console.log("Error: ", error);
        })
    }

    const deleteSession = (id) => {
        $api.post('http://localhost:8000/api/deleteSession/', {
            session_id: id,
        })
        .then((response) => {
            getSessions();
            currentSessionID.value = null;
        })
        .catch((error) => {
            console.log(error);
        })
    }

    const updateLocalSessionView = (id) => {
        currentSessionID.value = id;
        sessionList.value.forEach(item => {
            if (item.id === id) {
                transcription.value = item.transcription;
                summary.value = item.summarisation;

            }
        });
        console.log(currentSessionID.value);
    }

    const toggleSessionForm = () => {
        isNewSession.value = !isNewSession.value;

        form.input.client_fname = '';
        form.input.client_lname = '';
        form.input.session_Name = '';
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
                        const blob = new Blob(fullRecording, {type: "audio/mp4"});
                        fullRecording = [];
                        //sendFullAudioRecording(blob)
                    }


                    chunkRecorder.ondataavailable = (event) => {
                        chunk.push(event.data);
                        const blob = new Blob(chunk, {type: "audio/mp4"});
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
    function enableMicrophone () {
        if (!recordingStatus) return;

        recordingEnabled.value = !recordingEnabled.value;

        if (recordingEnabled.value) {
            fullRecorder.start();
            chunkRecorder.start();
            

            intervalID = setInterval(() => {
                    chunkRecorder.stop();
                    chunkRecorder.start();
            }, 4000);

        } else {
            clearInterval(intervalID);
            fullRecorder.stop();
            chunkRecorder.stop();
        }

        console.log(recordingEnabled.value);
    }


    const request_Transcription = (chunkBlob) => {
        const formData = new FormData();
        formData.append("audio", chunkBlob);
        formData.append("session_id", currentSessionID.value);

        console.log("Requesting for ", currentSessionID.value);
        
        $api.post('http://localhost:8000/api/transcribe/', formData)
        .then((response) => {
            if (response.data.transcription != "") {
                console.log(response.data);
                transcription.value += response.data.transcription;
            }
        })
        .catch((error) => {
            console.log(error);
        })
    }

    const sendFullAudioRecording = (audioBlob) => {
        const fullAudio = new FormData();
        fullAudio.append("fullAudio", audioBlob);

        $api.post("http://localhost:8000/api/upload/recording/")
        .then ((response) => {
            console.log(response);
            //callSummariser();
        })
        .catch((error) => {
            console.log("Error", error);
        })
    }

</script>


<template>
    <div class="flex h-[calc(100%-61.5px)]">

        <div class="flex flex-col w-[230px] bg-[#444444] relative overflow-hidden">
            <div class="py-4 grow overflow-hidden">
                <div class="text-center font-bold text-[25px] underline">
                    <h1>Sessions</h1>
                </div>
                <div class="flex-grow px-2 max-h-full overflow-y-auto">
                    <div v-for="item in sessionList" class="flex items-center truncate text-[15px] px-2 py-1 transition cursor-pointer hover:bg-neutral-600">
                        <h2 class="truncate w-[60%]" @click="updateLocalSessionView(item.id)">{{ item.session_name }}</h2>
                        <div class="grow flex items-center justify-end">
                            <Icon @click="deleteSession(item.id)" size="20px" name="material-symbols-light:delete-outline"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="py-5 flex items-center gap-3 w-full cursor-pointer" @click="toggleSessionForm">
                <Icon size="35px" name="material-symbols:add"/>
                <p class="text-[20px]">New session</p>
            </div>
        </div>
        
        <!-- displays a popup to allow user to fill basic info such as client details and name for session, when user clicks new session-->
        <div v-if="isNewSession" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-full">
            <div class="p-5 bg-white text-black w-[300px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <Icon class="absolute right-0 top-0 mt-2 mr-2 cursor-pointer" size="20px" name="gridicons:cross" @click="toggleSessionForm"/>
                <h1 class="text-[20px] text-center">Enter client details</h1>
                <form class="w-full" @submit.prevent="createSession">
                    <label for="fname">First Name</label>
                    <input type="text" id="fname" v-model="form.input.client_fname" name="email" placeholder="First Name">

                    <label for="lname">Last Name</label>
                    <input type="text" id="lname" v-model="form.input.client_lname" name="lname" placeholder="Last Name">

                    <label for="session">Session Name (has to be unique)</label>
                    <input type="text" id="session" v-model="form.input.session_Name" name="session" placeholder="Session Name">

                    <p v-if="emptyError" class="text-center pt-3"><span>Please fill all fields</span></p>
                    <p v-if="creationError" class="text-center pt-3"><span>Please type a unique session name</span></p>

                    <div class="text-center pt-3">
                        <input type="submit" value="Submit" class="cursor-pointer">
                    </div>
                </form>
            </div>
        </div>

        <!-- Displays the transcriptions, summary and the functions under these panels -->
        <div v-if="currentSessionID == null " class="flex w-full items-center text-center">
            <p class="grow">Choose a session to get started</p>
        </div>
        <div v-else class="flex w-full">
            <div class="w-full">
                <div class="flex justify-center py-5 h-5/6 text-black">
                    <div class="w-full bg-white rounded-xl overflow-hidden mx-3">
                        <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Transcribed Text</h2>
                        <p class="h-[calc(100%-54px)] px-2 overflow-y-auto overflow-hidden">{{ transcription }}</p>
                    </div>

                    <div class="w-full bg-white rounded-xl overflow-auto mx-3">
                        <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Summary</h2>
                        <p class="h-[calc(100%-54px)] px-2 overflow-y-auto overflow-hidden">{{ summary }}</p>
                    </div>
                </div>
                    
                <div class="flex justify-center gap-3 text-[30px] mx-3">
                    <div class="flex items-center p-4 bg-[#222222] space-x-6 rounded-xl">
                        <Icon size="37px" class="cursor-pointer" name="fluent:mic-record-20-regular" @click="enableMicrophone"/>
                        <Icon size="37px" class="cursor-pointer" name="material-symbols:upload-file-outline" @click="toggleUploadMenu"/>
                    </div>
                    <div class="p-4 bg-[#222222] rounded-xl">
                        <button @click="callSummariser">Generate Statement</button>
                        
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- A menu will pop up to allow users to upload templates (hidden for now) -->
    <!--<div v-if="uploadMenu" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-dvh">
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
    </div> -->
    
</template>