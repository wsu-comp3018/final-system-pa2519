<script setup>
    definePageMeta({
        middleware: function (to, from) {
            const token = useCookie('token');

            token.value = null;

            return navigateTo('/login')
        }
    })
</script>

<template></template>