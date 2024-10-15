<script setup>
import {ref, onMounted} from 'vue';

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

  <div class="w-full min-h-screen flex flex-col items-center bg-gray-800">
    <div class="flex flex-col w-full sm:w-1/2 md:w-2/3 lg:w-2/3 xl:w-5/12 space-y-4">
      <h1 class="text-green-400 text-4xl mb-5">Список задач</h1>
      <div v-if="error" class="error">{{ error }}</div>
      <ul v-else-if="tasks.length">
        <li v-for="task in tasks" :key="task.id" class="text-green-400 text-2xl mb-5">
          <div>
            <h4 class="text-green-400 text-2xl mb-1">{{ task.name }}</h4>
            <p class="text-white-400 text-xs">ID: {{ task.id }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="text-red-400 text-xl mb-5">Задачи не найдены</p>
    </div>
  </div>
</template>

<style scoped>
.error {
  color: red;
}
</style>