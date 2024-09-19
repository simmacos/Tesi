<template>
    <div class="level-bar">
      <div class="main-level">
        <h2>Livello principale: {{ mainLevel }}</h2>
        <progress :value="mainExp" max="100"></progress>
      </div>
      <div class="skill-levels">
        <div v-for="skill in skills" :key="skill.name" class="skill">
          <h3>{{ skill.name }}</h3>
          <progress :value="skill.exp" max="100"></progress>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LevelBar',
    data() {
      return {
        mainLevel: 1,
        mainExp: 50,
        skills: [
          { name: 'Skill 1', exp: 30 },
          { name: 'Skill 2', exp: 60 },
          // ... altre skills
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  /* Stili per le barre di livello */
  </style>
  