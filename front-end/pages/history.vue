<script setup>
    const items = ref([
        {
            interviewee_fname: "John",
            interviewee_lname: "Smith",
            case_type: "Insurance",
            date_opened: "24/05/2025",
        }, {
            interviewee_fname: "Abby",
            interviewee_lname: "Miller",
            case_type: "Fraud",
            date_opened: "12/03/2025",
        }, {
            interviewee_fname: "Jake",
            interviewee_lname: "Brookes",
            case_type: "Insurance",
            date_opened: "31/01/2025"
        }
    ])

    const searchFilterList = ref(items.value);
    const filterList = ref([]);
    const resultList = ref(items.value);
    const query = ref('');
    const caseTypes = ref([]);
    const filterListOpen = ref(false);

    function openFilterList() {
        filterListOpen.value = !filterListOpen.value;
    }

    function filterCases() {
        filterList.value = [];
        if (caseTypes.value.length > 0) {
            if (searchFilterList.value.length > 0) {

                caseTypes.value.forEach( type => {
                    searchFilterList.value.forEach( list_Item => {

                        if (list_Item.case_type == type) {
                            filterList.value.push(list_Item);
                        }

                    })
                })

                resultList.value = filterList.value.slice();
            } 
        } else {
            if (query.value === '') {
                resultList.value = items.value.slice();
            } else {
                resultList.value = searchFilterList.value.slice();
            }
        }

    }

    function search() {
        // at the beginning, check for filter if set, then filter array
        if (query.value !== '') {
            searchFilterList.value = [];
            items.value.forEach( item => {
                let fullName = (item.interviewee_fname + ' ' + item.interviewee_lname).toLowerCase();
                if (fullName.includes(query.value.toLowerCase())) {
                    searchFilterList.value.push(item);
                }
            })
            
            filterCases();

        } else {
            filterCases(); // check if there is filters enabled
        }
    }
</script>

<template>


    <div class="h-full w-[1100px] mx-auto my-5 overflow-hidden">
        <div class="flex relative items-center">
            <Icon class="absolute left-2" size="22px" name="material-symbols:search"/>
            <input v-model="query" type="search" id="search" name="search" placeholder="Search" autocomplete="off"
            class="h-[40px] rounded-[10px] indent-[35px] bg-[#444444] outline-none w-2/6" @input="search">
            
            <div class="ml-3">
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
            </div>
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
                <div v-if="resultList.length == 0" class="flex justify-center text-[20px]">
                    <p>Its empty here.</p>
                </div>
                <div v-for="item in resultList">
                    <div class="flex mb-5 p-2 bg-gray-500">
                        <div>
                            <p class="text-[25px]">{{ item.interviewee_fname }} {{ item.interviewee_lname }}</p>
                            <p class="text-[20px]">{{ item.case_type }}</p>
                        </div>
                        <div class="grow self-end text-right">
                            <button class="bg-gray-800 px-4 py-1 text-[16px]"><NuxtLink>Open</NuxtLink></button>
                        </div>
                    </div>
                </div>
                
            </div>
            

        </div>
    </div>
</template>