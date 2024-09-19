<template>
    <div class="habit-tracker">
      <h2>Tracker Abitudini</h2>
      <ul>
        <li v-for="habit in habits" :key="habit.id">
          {{ habit.name }}
          <button @click="trackHabit(habit.id)">Fatto</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HabitTracker',
    data() {
      return {
        habits: [
          { id: 1, name: 'Meditazione mattutina' },
          { id: 2, name: 'Leggere 30 minuti' },
          // ... altre abitudini
        ]
      }
    },

  }
  </script>
  
  <style scoped>
  /* Stili per l'habit tracker */
  </style>
  