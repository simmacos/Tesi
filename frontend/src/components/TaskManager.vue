<template>
    <div class="task-manager">
      <h2>Gestione Task</h2>
      <form @submit.prevent="addTask">
        <input v-model="newTask" placeholder="Nuovo task">
        <button type="submit">Aggiungi</button>
      </form>
      <ul>
        <li v-for="task in tasks" :key="task.id">
          {{ task.description }}
          <button @click="completeTask(task.id)">Completa</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TaskManager',
    data() {
      return {
        newTask: '',
        tasks: [
          { id: 1, description: 'Completare il progetto' },
          { id: 2, description: 'Fare la spesa' },
          // ... altri task
        ]
      }
    },

  }
  </script>
  
  <style scoped>
  /* Stili per il task manager */
  </style>
  