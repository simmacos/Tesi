<template>
  <header class="mb-8 bg-accent bg-opacity-20 shadow-lg rounded-lg p-4 border-2 border-secondary">
    <div class="flex justify-between items-center">
      <button @click="openSettings" class="text-primary hover:text-secondary transition-colors duration-300">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </button>
      <h1 class="text-4xl font-bold text-primary" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">Retro Task Manager</h1>
      <div class="text-text font-semibold">{{ username }}</div>
    </div>

    <!-- Settings Dialog -->
    <div v-if="showSettings" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-background rounded-lg p-6 w-96 border-4 border-secondary retro-shadow">
        <h2 class="text-2xl font-bold text-primary mb-4">Settings</h2>
        
        <div class="mb-4">
          <label for="description" class="block text-text font-medium mb-2">About You</label>
          <textarea 
            id="description" 
            v-model="userDescription" 
            rows="3" 
            class="w-full px-3 py-2 text-text bg-accent bg-opacity-10 rounded border border-secondary focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Describe yourself..."
          ></textarea>
        </div>

        <div class="mb-4">
          <label class="block text-text font-medium mb-2">Your Goals</label>
          <div v-for="(goal, index) in goals" :key="index" class="flex mb-2">
            <input 
              v-model="goals[index]" 
              type="text" 
              class="flex-grow px-3 py-2 text-text bg-accent bg-opacity-10 rounded-l border border-secondary focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter a goal..."
            >
            <button @click="removeGoal(index)" class="px-3 py-2 bg-red-500 text-white rounded-r hover:bg-red-600 transition-colors duration-300">
              X
            </button>
          </div>
          <button @click="addGoal" class="w-full px-3 py-2 bg-primary text-background rounded hover:bg-secondary transition-colors duration-300">
            Add Goal
          </button>
        </div>

        <div class="flex justify-end">
          <button @click="saveSettings" class="px-4 py-2 bg-primary text-background rounded hover:bg-secondary transition-colors duration-300 mr-2">
            Save
          </button>
          <button @click="closeSettings" class="px-4 py-2 bg-gray-300 text-text rounded hover:bg-gray-400 transition-colors duration-300">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { config } from '@/config';

export default {
  name: 'AppHeader',
  data() {
    return {
      username: config.username,
      showSettings: false,
      userDescription: '',
      goals: ['']
    }
  },
  mounted() {
    this.loadSettings();
  },
  methods: {
    openSettings() {
      this.showSettings = true;
    },
    closeSettings() {
      this.showSettings = false;
    },
    addGoal() {
      this.goals.push('');
    },
    removeGoal(index) {
      this.goals.splice(index, 1);
    },
    saveSettings() {
      localStorage.setItem('userDescription', this.userDescription);
      localStorage.setItem('userGoals', JSON.stringify(this.goals.filter(goal => goal.trim() !== '')));
      this.closeSettings();
    },
    loadSettings() {
      const savedDescription = localStorage.getItem('userDescription');
      const savedGoals = localStorage.getItem('userGoals');
      
      if (savedDescription) {
        this.userDescription = savedDescription;
      }
      
      if (savedGoals) {
        this.goals = JSON.parse(savedGoals);
      }
    }
  }
}
</script>

<style scoped>
.retro-shadow {
  box-shadow: 4px 4px 0px rgba(0, 0, 0, 0.2);
}
</style>
