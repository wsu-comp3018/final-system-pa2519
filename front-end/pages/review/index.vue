<script setup>
    definePageMeta({
        middleware: function (to, from) {
            const route = useRoute();
            console.log("CALLED")
            return navigateTo('/transcription')
        }
    })
</script>

<template>

</template>