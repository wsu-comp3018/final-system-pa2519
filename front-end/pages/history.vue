<script setup>
    definePageMeta({
        layout: 'logged-in'
    })

    const items = ref([{
        session_title: 'sample',
    },
    {
        session_title: 'sample-2'
    }])

    const listOfStatements = ref([]);
    const searchFilterList = ref([]);
    const filterList = ref([]);
    const resultList = ref([]);
    const query = ref('');
    const caseTypes = ref([]);
    const filterListOpen = ref(false);
    
    const { $api } = useNuxtApp();

    const getStatementHistory = () => {
        $api.get('http://localhost:8000/api/statement-list', {withCredentials: true})
        .then((response) => {
            console.log(response);
            listOfStatements.value = response.data.list;
            searchFilterList.value = response.data.list;
            resultList.value = response.data.list;
        })
        .catch((error) => {
            console.log(error);
        })
    }
    getStatementHistory();

    const redirectToStatement = (statement_id) => {
        return navigateTo(`/review/${statement_id}`)
    }

    // const openFilterList = () => {
    //     filterListOpen.value = !filterListOpen.value;
    // }

    // const filterCases = () => {
    //     filterList.value = [];
    //     if (caseTypes.value.length > 0) {
    //         if (searchFilterList.value.length > 0) {

    //             caseTypes.value.forEach( type => {
    //                 searchFilterList.value.forEach( list_Item => {

    //                     if (list_Item.case_type == type) {
    //                         filterList.value.push(list_Item);
    //                     }

    //                 })
    //             })

    //             resultList.value = filterList.value.slice();
    //         } 
    //     } else {
    //         if (query.value === '') {
    //             resultList.value = listOfStatements.value.slice();
    //         } else {
    //             resultList.value = searchFilterList.value.slice();
    //         }
    //     }

    // }

    const search = () => {
        // at the beginning, check for filter if set, then filter array
        if (query.value !== '') {
            searchFilterList.value = [];
            listOfStatements.value.forEach( item => {
                let fullName = (item.client_first_name + ' ' + item.client_last_name).toLowerCase();
                if (fullName.includes(query.value.toLowerCase())) {
                    searchFilterList.value.push(item);
                }
            })
            
            //filterCases();

        } else {
            //filterCases(); // check if there is filters enabled
            searchFilterList.value = listOfStatements.value;
        }
    }

</script>

<template>


    <div class="h-full w-[1100px] mx-auto my-5 overflow-hidden">
        <div class="flex relative items-center">
            <Icon class="absolute left-2" size="22px" name="material-symbols:search"/>
            <input v-model="query" type="search" id="search" name="search" placeholder="Search" autocomplete="off"
            class="h-[40px] rounded-[10px] indent-[35px] bg-[#444444] outline-none w-2/6" @input="search">
            
            <!-- <div class="ml-3">
                <button class="px-2 py-1 text-[20px] text-center hover:underline outline-none" @click="openFilterList" @keydown.esc="openFilterList">Filter</button>
                <div v-if="filterListOpen" class="absolute bg-[#222222] p-3 w-[15%]">
                    <div>
                        <div>
                            <h1>Case Type</h1>
                            <p class="indent-5">
                                <input type="checkbox" value="Insurance" name="Insurance" id="Insurance" v-model="caseTypes"> <label for="Insurance">Insurance</label>
                            </p>
                            <p class="indent-5">
                                <input type="checkbox" value="Fraud" name="Fraud" id="Fraud" v-model="caseTypes"> <label for="Fraud">Fraud</label>
                            </p>
                        </div>
                        <div class="text-center mt-3">
                            <button class="text-center" @click="filterCases">Done</button>
                        </div>
                    </div>
                </div>
            </div> -->
        </div> 

        <div class="flex justify-center gap-4 overflow-hidden mt-5">

            <div class="h-fit w-2/5 bg-gray-500">
                <h1 class="text-center text-[25px] bg-gray-800">Selected Statement</h1>
                <div class="px-5 py-2 h-[90%] overflow-y-auto">
                    <p class="text-[30px] underline">John Smith [REF: 10465]</p>
                    <p class="text-[20px]">
                        Case against his worksite manager, claims negligence. Can't work any more due to constant
                        migraines since accident, seeking insurance settlement. 
                    </p>
                </div>
            </div>

        
            <div class="grow overflow-y-auto overflow-hidden">
                <div v-if="searchFilterList.length == 0" class="flex justify-center text-[20px]">
                    <p>Its empty here.</p>
                </div>
                <!-- <div v-for="item in searchFilterList">
                    <div class="flex mb-5 p-2 bg-gray-500">
                        <div>
                            <p class="text-[25px]">Statement for - {{ item.client_first_name }} {{ item.client_last_name }}</p>
                        </div>
                        <div class="grow self-end text-right">
                            <button class="bg-gray-800 px-4 py-1 text-[16px]" @click="redirectToStatement(item.statement_id)">Open</button>
                        </div>
                    </div>
                </div> -->
                <div v-for="item in items">
                    <div class="flex mb-5 p-2 bg-gray-500">
                        <div>
                            <p class="text-[25px]">Statement for - {{ item.session_title }}</p>
                        </div>
                        <div class="grow self-end text-right">
                            <button class="bg-gray-800 px-4 py-1 text-[16px]">Open</button>
                        </div>
                    </div>
                </div>
                
            </div>
            

        </div>
    </div>
</template>