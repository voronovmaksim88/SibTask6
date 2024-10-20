<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  apiUrl: {
    type: String,
    required: true
  }
})

const tasks = ref([])
const error = ref('')
const new_task_name = ref('')
const selectedTaskId = ref(null)

async function fetchTasks() {
  try {
    const response = await fetch(`${props.apiUrl}/tasks/`)
    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      // noinspection ExceptionCaughtLocallyJS
      throw new Error(errorData?.detail || `HTTP error! status: ${response.status}`)
    }
    tasks.value = await response.json()
  } catch (e) {
    console.error('Error fetching tasks:', e)
    error.value = e.message || 'Произошла ошибка при получении данных'
  }
}

async function addTask() {
  if (!new_task_name.value.trim()) {
    error.value = 'Имя задачи не может быть пустым'
    return
  }

  try {
    const response = await fetch(`${props.apiUrl}/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: new_task_name.value })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      // noinspection ExceptionCaughtLocallyJS
      throw new Error(errorData?.detail || `HTTP error! status: ${response.status}`)
    }

    const newTask = await response.json()
    tasks.value.push(newTask)
    new_task_name.value = ''
    error.value = ''
  } catch (e) {
    console.error('Error adding task:', e)
    error.value = e.message || 'Произошла ошибка при добавлении задачи'
  }
}

function selectTask(taskId) {
  selectedTaskId.value = selectedTaskId.value === taskId ? null : taskId
}

async function deleteTask(taskId) {
  try {
    const response = await fetch(`${props.apiUrl}/tasks/${taskId}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      // noinspection ExceptionCaughtLocallyJS
      throw new Error(errorData?.detail || `HTTP error! status: ${response.status}`)
    }

    // Удаляем задачу из локального списка
    tasks.value = tasks.value.filter(task => task.id !== taskId)
    selectedTaskId.value = null // Сбрасываем выбор
    error.value = ''
  } catch (e) {
    console.error('Error deleting task:', e)
    error.value = e.message || 'Произошла ошибка при удалении задачи'
  }
}

onMounted(fetchTasks)
</script>

<template>
  <div class="w-full min-h-screen flex flex-col items-center bg-gray-800">
    <div class="flex flex-col w-full sm:w-1/2 md:w-2/3 lg:w-2/3 xl:w-6/12 space-y-4">
      <h1 class="text-green-400 text-4xl mb-5">Список задач</h1>
      <div class="flex items-center justify-between">
        <input
          class="w-1/2 rounded-md px-2 py-1"
          type="text"
          placeholder="новая задача"
          v-model="new_task_name"
        />
        <button @click="addTask" class="btn btn-p">Добавить</button>
      </div>

      <div v-if="error" class="text-red-500 text-xl mb-5">{{ error }}</div>
      <ul v-else-if="tasks.length">
        <li v-for="task in tasks" :key="task.id" class="mb-5">
          <div
            @click="selectTask(task.id)"
            class="border rounded-md p-3 cursor-pointer transition-all duration-200"
            :class="[
              selectedTaskId === task.id ? 'border-green-400 border-4' : 'border-gray-300 border',
              'hover:border-green-400'
            ]"
          >
            <h4 class="text-green-400 text-2xl mb-1">{{ task.name }}</h4>
            <div v-if="selectedTaskId === task.id" class="flex items-center justify-between">
              <p  class="text-gray-400 text-xs">id: {{ task.id }}</p>
              <button @click="deleteTask(task.id)" class="btn btn-p">Удалить</button>
            </div>
          </div>
        </li>
      </ul>
      <p v-else class="text-yellow-400 text-xl mb-5">Задачи не найдены</p>
    </div>
  </div>
</template>