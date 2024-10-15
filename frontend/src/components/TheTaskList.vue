<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  apiUrl: {
    type: String,
    required: true
  }
});

const tasks = ref([]);
const error = ref('');

async function fetchTasks() {
  try {
    const response = await fetch(`${props.apiUrl}/tasks/`);
    if (!response.ok) {
      throw new Error('Ошибка при получении данных');
    }
    const data = await response.json();
    tasks.value = data;
  } catch (e) {
    error.value = e.message;
  }
}

onMounted(fetchTasks);
</script>

<template>
  <div class="bg-blue-500 text-white p-4">
    Hello, Tailwind CSS in Vue!
  </div>
  <div>
    <h2>Список задач</h2>
    <div v-if="error" class="error">{{ error }}</div>
    <ul v-else-if="tasks.length">
      <li v-for="task in tasks" :key="task.id">
        ID: {{ task.id }} - Название: {{ task.name }}
      </li>
    </ul>
    <p v-else>Задачи не найдены</p>
  </div>
</template>

<style scoped>
.error {
  color: red;
}
</style>