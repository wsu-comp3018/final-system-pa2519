<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const message = ref('');

onMounted(async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/example/');
  message.value = response.data.message;
});
</script>