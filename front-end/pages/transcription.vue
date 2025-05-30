<style scoped>
    input[type="text"], input[type="password"], input[type="email"]{
        border-width: 2px;
        border-color: #6b7280;
        width: 100%;
        height: 40px;
        border: none;
        border-bottom: 2px solid;
        padding: 20px 0 20px 0;
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
            client_email: '',
        }
    })

    const sessionList = ref([]);
    const currentSessionID = ref(null);
    const currentSessionName = ref('');
    let newSession = ref(false);

    let uploadTemplatePopup = ref(false);
    const emptyError = ref(false);
    const creationError = ref(false);
    const transcription = ref("");
    const summaryPoints = ref([]);
    const { $api } = useNuxtApp();
    const hideSummary = ref(false);
    const generationButtonText = ref('Generate Statement');
    const summaryButtonText = ref('Summarise')
    const micColor = ref("white");


    const closePopups = (event) => {
        if (event.key === 'Escape') {
            newSession.value = false;
            uploadTemplatePopup.value = false;

            form.input.client_fname = '';
            form.input.client_lname = '';
            form.input.session_Name = '';
            form.input.client_email = '';

            file.value = [];
        }
    }

    onMounted(() => {
        document.addEventListener('keydown', closePopups);
    })
    
    const getSessions = () => {
        $api.get('http://localhost:8000/api/session-list/', {withCredentials: true})
        .then((response) => {
            sessionList.value = response.data.data;
        }) 
    }   
    getSessions();
    
    const callSummariser = () => {

        if (transcription.value === '') {
            summaryButtonText.value = 'No transcription available';
            setTimeout(() => {
                summaryButtonText.value = 'Summarise';
            }, 3000);
            return;
        }

        hideSummary.value = true;

        $api.post('http://localhost:8000/api/summary/', {
            session_id: currentSessionID.value,
        }, {withCredentials: true})
        .then ((response) => {
            if (response.data.summary) {
                summaryPoints.value = response.data.summary.match(/[^.!]+[.!]/g);
            }
            hideSummary.value = false;

            getSessions();
            
        })
        .catch((error) => {
            errorMessage.value = "An error occur during summarisation."
            displayErrorMessage();
            hideSummary.value = false;
        })
    }

    const callStatementGenerator = () => {
        generationButtonText.value = 'Generating...';

        if (transcription.value === '') {
            generationButtonText.value = 'No transcription available';
            setTimeout(() => {
                generationButtonText.value = 'Generate';
            }, 3000);
            return;
        }

        $api.post('http://localhost:8000/api/generate/', {
            session_id: currentSessionID.value,
        }, {withCredentials: true})
        .then (async (response) => {
            const id = response.data.statement_id
            if (!id) {
                generationButtonText.value = 'Generate Statement';
                return;
            }
            generationButtonText.value = 'Generate Statement';
            await navigateTo(`/review/${id}`)
        })
        .catch((error) => {
            generationButtonText.value = 'Generate Statement';
            errorMessage.value = "An error occur during generation."
            displayErrorMessage();
        })
    }

    const createSession = () => {
        emptyError.value = false;
        if (form.input.client_fname === '' || form.input.client_lname === '' || form.input.session_Name === '' || form.input.client_email === '') {
            emptyError.value = true;
            return;
        }

        $api.post('http://localhost:8000/api/create-session/', {
            fname: form.input.client_fname,
            lname: form.input.client_lname,
            session_name: form.input.session_Name,
            email: form.input.client_email,
        }, {withCredentials: true})
        .then((response) => {
            if (response.status == 200) {
                newSession.value = false;
                form.input.client_fname = '';
                form.input.client_lname = '';
                form.input.session_Name = '';
                form.input.client_email = '';
            }
            getSessions();

        })
        .catch((error) => {
            creationError.value = true;
            setTimeout(() => {
                creationError.value = false;
            }, 3000);
        })
    }

    const deleteSession = (id) => {
        $api.post('http://localhost:8000/api/delete-session/', {
            session_id: id,
        }, {withCredentials: true})
        .then((response) => {
            getSessions();
            currentSessionID.value = null;
        })
        .catch((error) => {
            errorMessage.value = "An error occur deleting statement."
            displayErrorMessage();
        })
    }

    const updateLocalSessionView = (id) => {
        currentSessionID.value = id;
        sessionList.value.forEach(item => {
            if (item.id === id) {
                if (item.transcription) {
                    transcription.value = item.transcription;
                } else {
                    transcription.value = "";
                }
                if (item.summary) {
                    summaryPoints.value = item.summary.match(/[^.!]+[.!]/g);
                } else {
                    summaryPoints.value = [];
                }
                currentSessionName.value = item.session_name;
            }
        });
    }


    const toggleMenus = (menuType) => {
        if (menuType === 'session') {
            newSession.value = !newSession.value;

            form.input.client_fname = '';
            form.input.client_lname = '';
            form.input.session_Name = '';
            form.input.client_email = '';

        } else if (menuType === 'templates') {
            uploadTemplatePopup.value = !uploadTemplatePopup.value;
        }
    }

    const errorMessage = ref('');
    const errorPopup = ref(false);
    const displayErrorMessage = () => {
        errorPopup.value = true;
        setTimeout(() => {
            errorPopup.value = false;
        }, 3000);
    }


    const inputFile = useTemplateRef('fileInput');
    const openFileInputWindow = () => {
        inputFile.value.click();
    }

    const file = ref(null);
    const getFile = (e) => {
        file.value = e.target.files[0];
    }

    const fileError = ref("");
    const templateSubmit = () => {
        fileError.value = "";

        if (!file.value) {
            fileError.value = "Upload a file to submit"
            return;
        }
        else {
            const formData = new FormData();
            formData.append('session_id', currentSessionID.value);
            if(file.value) {
                const file_name = file.value.name.split('.')[0];
                formData.append('file_name', file_name);
                formData.append('template', file.value);
            }

            $api.post("http://localhost:8000/api/upload-template/", formData, {withCredentials: true})
            .then((response) => {
                uploadTemplatePopup.value = false;
            })
            .catch((error) => {
                uploadTemplatePopup.value = false;
                errorMessage.value = "An error occur uploading the template."
                displayErrorMessage();      
            })
        }
    }

    // Functions to enable microphone and recording
    let recordingStatus = false;
    let recordingEnabled = ref(false);
    let fullRecording = [];
    let chunk = [];
    let fullRecorder = null;
    let chunkRecorder = null;
    const uploadRecordingPopup = ref(false);
    let fullRecordingBlob = null;

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
                        fullRecordingBlob = new Blob(fullRecording, {type: "audio/wav"});
                        fullRecording = [];
                        uploadRecordingPopup.value = true;
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
                    console.error('Error:', err);
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
            micColor.value = "red";

            intervalID = setInterval(() => {
                chunkRecorder.stop();
                chunkRecorder.start();
            }, 4000);

        } else {
            clearInterval(intervalID);
            fullRecorder.stop();
            chunkRecorder.stop();
            micColor.value = "white";
        }

    }

    // Function to get transcription from whisper
    const request_Transcription = (chunkBlob) => {
        const formData = new FormData();
        formData.append("audio", chunkBlob);
        formData.append("session_id", currentSessionID.value);
        
        $api.post('http://localhost:8000/api/transcribe/', formData, {withCredentials: true})
        .then((response) => {
            if (response.data.transcription != "") {
                transcription.value += response.data.transcription;
                getSessions();
            }
        })
        .catch((error) => {
            enableMicrophone();
            errorMessage.value = "An error occured during transcribing. Please try again."
            displayErrorMessage();
        })
    }

    const recordingName = reactive({
        name: '',
    })
    const confirmRecordingUpload = (answer) => {
        if (answer === 'Yes') {
            uploadRecordingPopup.value = false;
            sendFullAudioRecording(fullRecordingBlob);
        } else {
            uploadRecordingPopup.value = false;
            return;
        }
    }

    // Function to upload full audio recording to backend NOTE: IGNORE FOR NOW PLEASE.
    const sendFullAudioRecording = (audioBlob) => {
        const formData = new FormData();
        const filename = recordingName.name + '.wav';
        formData.append("fullRecording", audioBlob, filename);
        formData.append("session_id", currentSessionID.value);
        formData.append("audio_name", recordingName.name);

        $api.post("http://localhost:8000/api/upload-recording/", formData, {withCredentials: true})
        .then ((response) => {
            return;
        })
        .catch((error) => {
            errorMessage.value = "An error occur uploading the recording."
            displayErrorMessage();
        })
    }

</script>


<template>

    <div class="flex h-[calc(100%-61.5px)]">
        <!-- sidebar -->
        <div class="flex flex-col w-[230px] bg-[#222222] relative overflow-hidden">
            <div class="py-4 px-4 grow overflow-hidden">
                <div class="font-bold text-[22px] underline">
                    <h1>Your sessions</h1>
                </div>
                <div class="flex-grow max-h-full overflow-y-auto">
                    <div v-for="item in sessionList" class="flex items-center truncate text-[16px] py-1 transition cursor-pointer hover:bg-neutral-600">
                        <h2 class="truncate w-full" @click="updateLocalSessionView(item.id)">{{ item.session_name }}</h2>
                        <div class="grow flex items-center justify-end">
                            <Icon @click="deleteSession(item.id)" size="20px" name="material-symbols-light:delete-outline"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="py-5 px-3 flex items-center gap-3 w-full cursor-pointer" @click="toggleMenus('session')">
                <Icon size="35px" name="material-symbols:add"/>
                <p class="text-[20px]">New session</p>
            </div>
        </div>

        <!-- Displays the transcriptions, summary and the functions under these panels -->
        <div v-if="currentSessionID == null " class="flex grow items-center text-center">
            <p class="grow">Create or select a session to get started.</p>
        </div>
        <div v-else class="flex w-[calc(100%-230px)]">
            <div class="w-full h-[calc(100%-42px)]">
                <h1 class="ml-3 text-[28px] underline">Current session - {{ currentSessionName }}</h1>
                <div class="flex justify-center pb-5 h-5/6 text-black ">
                    <div class="w-full bg-white rounded-xl overflow-hidden mx-3">
                        <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Transcribed Text</h2>
                        <p class="h-[calc(100%-54px)] px-2 overflow-y-auto overflow-hidden">{{ transcription }}</p>
                    </div>

                    <div class="w-full bg-white rounded-xl overflow-auto mx-3">
                        <h2 class="text-center bg-[#222222] text-white p-3 text-[20px]">Summary</h2>
                        <div v-if="hideSummary" class="h-[calc(100%-54px)] flex items-center justify-center">
                            <p>Summarising please wait...</p>
                        </div>
                        <div class="h-[calc(100%-54px)] overflow-y-auto overflow-hidden pr-2">
                            <ul class="list-disc list-outside pl-6">
                                <li v-for="line in summaryPoints">{{ line }}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                    
                <div class="flex justify-center gap-3 text-[30px] mx-3">
                    <div class="flex items-center p-4 bg-[#222222] space-x-6 rounded-xl">
                        <Icon size="37px" class="cursor-pointer" :style="{color: micColor}" name="fluent:mic-record-20-regular" @click="enableMicrophone"/>
                        <Icon size="37px" class="cursor-pointer" name="material-symbols:upload-file-outline" @click="toggleMenus('templates')"/>
                    </div>
                    <div class="p-4 bg-[#222222] rounded-xl">
                        <button @click="callSummariser">{{ summaryButtonText }}</button>
                    </div>
                    <div class="p-4 bg-[#222222] rounded-xl">
                        <button @click="callStatementGenerator">{{ generationButtonText }}</button>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- displays a popup to allow user to fill basic info such as client details and name for session, when user clicks new session-->
    <div v-if="newSession" class="absolute z-10 bg-[rgba(0,0,0,0.8)] w-full h-dvh">
        <div class="p-5 bg-white text-black w-[300px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <Icon class="absolute right-0 top-0 mt-2 mr-2 cursor-pointer" size="20px" name="gridicons:cross" @click="toggleMenus('session')"/>
            <h1 class="text-[20px] text-center">Enter client details</h1>
            <form class="w-full" @submit.prevent="createSession">
                <label for="fname">First Name</label>
                <input type="text" id="fname" v-model="form.input.client_fname" name="email">

                <label for="lname">Last Name</label>
                <input type="text" id="lname" v-model="form.input.client_lname" name="lname">

                <label for="email">Email Address</label>
                <input type="email" id="email" v-model="form.input.client_email" name="email">

                <label for="session">Session Name (has to be unique)</label>
                <input type="text" id="session" v-model="form.input.session_Name" name="session">

                <p v-if="emptyError" class="text-center pt-3"><span>Please fill all fields</span></p>
                <p v-if="creationError" class="text-center pt-3"><span>Please type a unique session name</span></p>

                <div class="text-center pt-3">
                    <input type="submit" value="Submit" class="bg-[#222222] text-white hover:underline px-3 py-1 rounded-md cursor-pointer">
                </div>
            </form>
        </div>
    </div>

    <!-- A menu will pop up to allow users to upload templates (hidden for now) -->
    <div v-if="uploadTemplatePopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] text-white w-full h-dvh">
        <div class="p-5 bg-white text-black w-[300px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <Icon class="absolute right-0 top-0 mt-2 mr-2 cursor-pointer" size="20px" name="gridicons:cross" @click="toggleMenus('templates')"/>

            <h1 class="text-[18px]">Upload a template or select one from the dropdown</h1>
            <form method="post" @submit.prevent="templateSubmit">
                <input ref="fileInput" @change="getFile" type="file" name="template" id="template" class="hidden">
                <button type="button" class="text-white bg-[#444343] w-full py-2 rounded-sm" @click="openFileInputWindow">Upload</button>
                <span class="text-red-500">{{ fileError }}</span>
                <p class="pt-2">Chosen file: <span v-if="file != null">{{ file.name }}</span></p>
                <input type="submit" value="Submit" class="bg-[#222222] text-white hover:underline px-3 py-1 rounded-md cursor-pointer">
            </form>
        </div>
    </div>

    <div v-if="uploadRecordingPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] w-full h-dvh">
        <div class="p-5 bg-white text-black w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <Icon class="absolute right-0 top-0 mt-2 mr-2 cursor-pointer" size="20px" name="gridicons:cross" @click="confirmRecordingUpload('No')"/>
            <p>Do you want to upload this recording to the server? If so enter a name for this recording.</p>
            <input class="bg-white my-2" v-model="recordingName.name" type="text">
            <div class="flex justify-center gap-4 pt-3">
                <button class="bg-[#222222] text-white hover:underline px-3 py-1 rounded-md" @click="confirmRecordingUpload('Yes')">Confirm</button>
            </div>
        </div>
    </div>

    <div v-if="errorPopup" class="absolute z-10 bg-[rgba(0,0,0,0.8)] w-full h-full">
        <div class="p-5 text-white w-[400px] rounded-xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <p>{{ errorMessage }}</p>
        </div>
    </div>
    
</template>