<template>
    <header>
      <h1>Nome App</h1>
      <div class="user-info">
        <span>{{ username }}</span>
        <button @click="openSettings">Impostazioni</button>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    name: 'AppHeader',
    data() {
      return {
        username: 'NomeUtente'
      }
    },
    methods: {
      openSettings() {
        // Logica per aprire le impostazioni
      }
    }
  }
  </script>
  
  <style scoped>
  /* Stili per l'header */
  </style>
  