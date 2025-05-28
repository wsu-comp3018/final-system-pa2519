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

    const currentSelectStatement = ref('Select one to preview.')
    const showSelectedStatement = (statement_id) => {
        listOfStatements.value.forEach( item => {
            if (item.statement_id = statement_id) {
                currentSelectStatement.value = item.statement_content;
            }
        })
    }

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

        } else {
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
            
        </div> 

        <div class="flex justify-center gap-4 overflow-hidden mt-5">

            <div class="h-fit w-2/5 bg-[#454444]">
                <h1 class="text-center text-[28px] bg-[#222222]">Selected Statement</h1>
                <div class="px-5 py-2 h-[90%]">
                    <p class="text-[18px]">{{ currentSelectStatement }}</p>
                </div>
            </div>

        
            <div class="grow overflow-y-auto overflow-hidden">
                <div v-if="searchFilterList.length == 0" class="flex justify-center text-[20px]">
                    <p>Its empty here.</p>
                </div>
                <div v-for="item in searchFilterList">
                    <div class="flex mb-5 p-3 bg-[#454444] rounded-md">
                        <div>
                            <p class="text-[24px] hover:underline cursor-pointer" @click="showSelectedStatement(item.statement_id)">Statement for - {{ item.client_first_name }} {{ item.client_last_name }}</p>
                        </div>
                        <div class="grow self-end text-right">
                            <button class="bg-[#222222] rounded-sm px-4 py-1 text-[16px]" @click="redirectToStatement(item.statement_id)">Open</button>
                        </div>
                    </div>
                </div>
                
            </div>
            

        </div>
    </div>
</template>