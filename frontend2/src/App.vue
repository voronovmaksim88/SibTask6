<script setup>
import TaskList from './components/TheTaskList.vue';
</script>

<template>
  <TaskList :apiUrl="'http://localhost:8000'" />
</template>
