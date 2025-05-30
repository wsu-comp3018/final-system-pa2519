<script setup>
    definePageMeta({
        middleware: function (to, from) {
            const route = useRoute();
            return navigateTo('/transcription')
        }
    })
</script>

<template>

</template>