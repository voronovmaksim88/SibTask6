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
      const errorData = await response.json().catch(() => null);
      // noinspection ExceptionCaughtLocallyJS
      throw new Error(errorData?.detail || `HTTP error! status: ${response.status}`);
    }
    tasks.value = await response.json();
  } catch (e) {
    console.error('Error fetching tasks:', e);
    error.value = e.message || 'Произошла ошибка при получении данных';
  }
}

onMounted(fetchTasks);
</script>

<template>
  <div class="w-full min-h-screen flex flex-col items-center bg-gray-800">
    <div class="flex flex-col w-full sm:w-1/2 md:w-2/3 lg:w-2/3 xl:w-3/12 space-y-4">
      <h1 class="text-green-400 text-4xl mb-5">Список задач</h1>
      <div class="flex flex-row gap-2">
        <input
            class="w-1/2 rounded-md"
            type="text"
            placeholder="новая задача"
        />
        <button class="btn btn-p">Добавить</button>
      </div>

      <div v-if="error" class="text-red-500 text-xl mb-5">{{ error }}</div>
      <ul v-else-if="tasks.length">
        <li v-for="task in tasks" :key="task.id" class="mb-5">
          <div class="border border-gray-300 rounded-md p-3">
            <h4 class="text-green-400 text-2xl mb-1">{{ task.name }}</h4>
            <p class="text-gray-400 text-xs">ID: {{ task.id }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="text-yellow-400 text-xl mb-5">Задачи не найдены</p>
    </div>
  </div>
</template>
