<template>
  <section class="mb-4 bg-accent bg-opacity-20 shadow-lg rounded-lg p-3 border-2 border-secondary relative">
    <div class="flex justify-between items-center mb-2">
      <h2 class="text-lg font-bold text-primary">Quest Giornaliere</h2>
      <button @click="refreshQuests" 
              class="bg-primary text-background rounded-full w-8 h-8 flex items-center justify-center hover:bg-secondary transition-colors duration-200"
              :class="{ 'animate-spin': isLoading }">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
    <div class="flex space-x-2">
      <div v-for="quest in quests" :key="quest.id" 
           class="flex-1 bg-background rounded-lg p-2 border border-secondary cursor-pointer transition-all duration-300 hover:bg-accent hover:bg-opacity-10"
           @click="showQuestDetails(quest)">
        <div class="flex items-start">
          <input 
            type="checkbox" 
            :checked="quest.completed" 
            @change="toggleQuest(quest.id)"
            @click.stop
            class="form-checkbox h-4 w-4 text-primary rounded border-secondary focus:ring-primary mr-2 mt-1"
          >
          <div class="flex-grow">
            <div class="flex justify-between items-start mb-1">
              <p class="text-sm font-medium text-text line-clamp-2 mr-2">{{ quest.title }}</p>
              <span class="text-xs font-semibold whitespace-nowrap" :class="difficultyColor(quest.difficulty)">
                {{ getDifficultyLabel(quest.difficulty) }}
              </span>
            </div>
            <div class="flex justify-end">
              <span class="text-xs text-secondary font-semibold">{{ quest.skill }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quest Details Dialog -->
    <div v-if="selectedQuest" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-background rounded-lg p-4 w-80 border-4 border-secondary retro-shadow">
        <h3 class="text-lg font-bold text-primary mb-2">{{ selectedQuest.title }}</h3>
        <p class="text-sm text-text mb-3">{{ selectedQuest.description }}</p>
        <div class="flex justify-between items-center mb-3">
          <span class="text-xs font-semibold" :class="difficultyColor(selectedQuest.difficulty)">
            {{ getDifficultyLabel(selectedQuest.difficulty) }}
          </span>
          <span class="text-xs text-secondary font-semibold">{{ selectedQuest.skill }}</span>
        </div>
        <div class="flex justify-end">
          <button @click="selectedQuest = null" class="bg-primary text-background rounded px-4 py-2 hover:bg-secondary transition-colors duration-200">Close</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import { config } from '@/config';

export default {
  name: 'QuestBoard',
  data() {
    return {
      quests: [],
      selectedQuest: null,
      habits: [],
      goals: [],
      isLoading: false
    }
  },
  mounted() {
    this.loadGoals();
    this.fetchHabits();
    this.fetchQuests();
    window.addEventListener('storage', this.handleStorageChange);
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.handleStorageChange);
  },
  methods: {
    loadGoals() {
      const savedGoals = localStorage.getItem('userGoals');
      if (savedGoals) {
        this.goals = JSON.parse(savedGoals);
      }
    },
    handleStorageChange(event) {
      if (event.key === 'userGoals') {
        this.loadGoals();
      }
    },
    async fetchHabits() {
      try {
        const response = await axios.get('/api/habits');
        this.habits = response.data.map(habit => habit.titolo);
      } catch (error) {
        console.error('Error fetching habits:', error);
      }
    },
    async fetchQuests() {
      this.isLoading = true;
      try {
        const response = await axios.get(`/api/get_latest_quests/${config.username}`);
        this.quests = response.data.quests;
        
        if (this.quests.length < 3) {
          await this.generateNewQuests(3 - this.quests.length);
        }
      } catch (error) {
        console.error('Error fetching quests:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
        }
      } finally {
        this.isLoading = false;
      }
    },
    async generateNewQuests(count) {
      try {
        const response = await axios.post('/api/generate_quests', {
          habits: this.habits,
          goals: this.goals,
          count: count
        });
        const generatedQuests = response.data.quests;
        
        console.log('Generated quests:', generatedQuests);

        const formattedQuests = generatedQuests.map(quest => ({
          title: quest.title,
          description: quest.description,
          difficulty: this.convertDifficultyToNumber(quest.difficulty),
          skill: quest.skill
        }));

        console.log('Formatted quests:', formattedQuests);

        const saveResponse = await axios.post('/api/save_generated_quests', {
          user_id: config.username,
          quests: formattedQuests
        });
        
        // Aggiorna this.quests con le nuove quest generate
        this.quests = saveResponse.data.quests;
      } catch (error) {
        console.error('Error generating new quests:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
        }
      }
    },
    async toggleQuest(id) {
      try {
        const quest = this.quests.find(q => q.id === id);
        if (quest) {
          const response = await axios.post(`/api/toggle_quest/${quest.id}`);
          quest.completed = response.data.completata;
          console.log(response.data.message);
        }
      } catch (error) {
        console.error('Error toggling quest:', error);
      }
    },
    difficultyColor(difficulty) {
      switch (this.getDifficultyLabel(difficulty)) {
        case 'EASY': return 'text-green-600';
        case 'MEDIUM': return 'text-yellow-600';
        case 'HARD': return 'text-red-600';
        default: return 'text-gray-600';
      }
    },
    getDifficultyLabel(difficulty) {
      if (typeof difficulty === 'number') {
        if (difficulty <= 10) return 'EASY';
        if (difficulty <= 20) return 'MEDIUM';
        return 'HARD';
      }
      return difficulty.toUpperCase();
    },
    convertDifficultyToNumber(difficulty) {
      switch (difficulty.toLowerCase()) {
        case 'easy': return 10;
        case 'medium': return 20;
        case 'hard': return 30;
        default: return 10;
      }
    },
    async refreshQuests() {
      this.isLoading = true;
      try {
        await this.generateNewQuests(3);
      } catch (error) {
        console.error('Error refreshing quests:', error);
      } finally {
        this.isLoading = false;
      }
    },
    showQuestDetails(quest) {
      this.selectedQuest = quest;
    }
  }
}
</script>
<style scoped>
.form-checkbox {
  appearance: none;
  -webkit-appearance: none;
  border: 2px solid #D2691E;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
}

.form-checkbox:checked {
  background-color: #8B4513;
  border-color: #8B4513;
}

.form-checkbox:checked::before {
  content: '\2714';
  display: block;
  text-align: center;
  color: #FFF8DC;
  font-size: 12px;
  line-height: 12px;
}

.form-checkbox:focus {
  box-shadow: 0 0 0 2px rgba(210, 105, 30, 0.5);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.retro-shadow {
  box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.3);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
