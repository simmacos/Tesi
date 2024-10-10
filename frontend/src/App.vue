<template>
  <div class="bg-background text-text min-h-screen">
    <div class="container mx-auto px-4 py-6">
      <AppHeader />
      <main class="max-w-8xl mx-auto">
        <LevelBar />
        <QuestBoard />
        <TaskManager />
        <HabitTracker />
      </main>
    </div>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import LevelBar from './components/LevelBar.vue'
import QuestBoard from './components/QuestBoard.vue'
import TaskManager from './components/TaskManager.vue'
import HabitTracker from './components/HabitTracker.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    LevelBar,
    QuestBoard,
    TaskManager,
    HabitTracker
  },
  mounted() {
    this.loadFont();
  },
  methods: {
    loadFont() {
      // Aggiungi preconnect links
      const preconnectGoogle = document.createElement('link');
      preconnectGoogle.rel = 'preconnect';
      preconnectGoogle.href = 'https://fonts.googleapis.com';
      document.head.appendChild(preconnectGoogle);

      const preconnectGstatic = document.createElement('link');
      preconnectGstatic.rel = 'preconnect';
      preconnectGstatic.href = 'https://fonts.gstatic.com';
      preconnectGstatic.crossOrigin = 'anonymous';
      document.head.appendChild(preconnectGstatic);

      // Carica il font
      const link = document.createElement('link');
      link.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap';
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }
  }
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

body {
  font-family: 'Roboto Slab', serif;
}

</style>
