<template>
  <AppHeader></AppHeader>
  <LevelBar></LevelBar>
  <QuestBoard></QuestBoard>
  <TaskManager></TaskManager>
  <HabitTracker></HabitTracker>
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
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
