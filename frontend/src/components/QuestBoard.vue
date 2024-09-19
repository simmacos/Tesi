<template>
    <div class="quest-board">
      <h2>Quest Giornaliere</h2>
      <ul>
        <li v-for="quest in quests" :key="quest.id">
          {{ quest.description }}
          <button @click="completeQuest(quest.id)">Completa</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuestBoard',
    data() {
      return {
        quests: [
          { id: 1, description: 'Completa 3 task' },
          { id: 2, description: 'Fai 30 minuti di esercizio' },
          // ... altre quest
        ]
      }
    },

  }
  </script>
  
  <style scoped>
  /* Stili per la quest board */
  </style>
  