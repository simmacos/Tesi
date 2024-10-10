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
    // Aggiungi i link per preconnect e preload dinamicamente
    this.addFontLinks();
  },
  methods: {
    addFontLinks() {
      const head = document.head;
      
      const preconnectGoogle = document.createElement('link');
      preconnectGoogle.rel = 'preconnect';
      preconnectGoogle.href = 'https://fonts.googleapis.com';
      head.appendChild(preconnectGoogle);

      const preconnectGstatic = document.createElement('link');
      preconnectGstatic.rel = 'preconnect';
      preconnectGstatic.href = 'https://fonts.gstatic.com';
      preconnectGstatic.crossOrigin = 'anonymous';
      head.appendChild(preconnectGstatic);

      const fontPreload = document.createElement('link');
      fontPreload.rel = 'preload';
      fontPreload.as = 'style';
      fontPreload.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap';
      head.appendChild(fontPreload);

      const fontStylesheet = document.createElement('link');
      fontStylesheet.rel = 'stylesheet';
      fontStylesheet.href = 'https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap';
      head.appendChild(fontStylesheet);
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

/* Aggiungi questa regola per utilizzare font-display: swap */
@font-face {
  font-family: 'Roboto Slab';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/robotoslab/v24/BngbUXZYTXPIvIBgJJSb6s3BzlRRfKOFbvjojISmb2Rm.woff2) format('woff2');
}

@font-face {
  font-family: 'Roboto Slab';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/robotoslab/v24/BngbUXZYTXPIvIBgJJSb6s3BzlRRfKOFbvjoa4Omb2Rm.woff2) format('woff2');
}
</style>
