<template>
  <section class="mb-4 bg-accent bg-opacity-20 shadow-lg rounded-lg p-4 border-2 border-secondary">
    <div class="flex justify-between items-center mb-3">
      <h2 class="text-lg font-bold text-primary">Habit Tracker</h2>
      <button @click="openAddHabitDialog" class="bg-primary text-background rounded-full w-8 h-8 flex items-center justify-center hover:bg-secondary transition-colors duration-200">
        +
      </button>
    </div>
    
    <div v-if="habits.length === 0" class="text-center text-gray-500">
      No habits for today.
    </div>
    <div v-else class="grid grid-cols-2 gap-3">
      <div v-for="habit in habits" :key="habit.id" 
           class="bg-background rounded-lg p-2 border border-secondary relative group transition-all duration-300 hover:bg-accent hover:bg-opacity-10">
        <div class="flex items-start">
          <input 
            type="checkbox" 
            :checked="habit.completata" 
            @change="toggleHabit(habit)"
            class="form-checkbox h-4 w-4 text-primary rounded border-secondary focus:ring-primary mr-2 mt-1"
          >
          <div class="flex-grow">
            <div class="flex justify-between items-start mb-1">
              <span class="font-medium text-text text-sm">{{ habit.titolo }}</span>
              <span class="text-xs font-semibold transition-opacity duration-300 group-hover:opacity-0" :class="difficultyColor(habit.difficolta_xp)">
                {{ getDifficultyLabel(habit.difficolta_xp) }}
              </span>
            </div>
            <p v-if="habit.descrizione" class="text-xs text-gray-500 break-words">{{ habit.descrizione }}</p>
            <div class="flex justify-end mt-1">
              <span class="text-xs text-secondary font-semibold transition-opacity duration-300 group-hover:opacity-0" :class="skillColor(habit.skill)">{{ habit.skill }}</span>
            </div>
          </div>
        </div>
        <button @click="confirmDeleteHabit(habit)" 
                class="absolute top-0 bottom-0 right-2 my-auto w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 retro-shadow">
          <span class="retro-x">×</span>
        </button>
      </div>
    </div>

    <!-- Dialog per aggiungere una nuova abitudine -->
    <div v-if="showAddHabitDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-background rounded-lg p-4 w-80">
        <h3 class="text-lg font-bold text-primary mb-3">Add New Habit</h3>
        <input v-model="newHabit.titolo" placeholder="Habit Name" class="w-full mb-2 p-2 border border-secondary rounded">
        <input v-model="newHabit.descrizione" placeholder="Description (optional)" class="w-full mb-2 p-2 border border-secondary rounded">
        <select v-model="newHabit.difficolta_xp" class="w-full mb-2 p-2 border border-secondary rounded">
          <option :value="10">Easy</option>
          <option :value="20">Medium</option>
          <option :value="30">Hard</option>
        </select>
        <select v-model="newHabit.skill" class="w-full mb-2 p-2 border border-secondary rounded">
          <option value="GENERAL">GEN</option>
          <option value="CULTURE">CULT</option>
          <option value="SPORT">SPORT</option>
          <option value="WELLBEING">WELL</option>
          <option value="PRODUCTIVITY">PROD</option>
          <option value="CREATIVITY">CREA</option>
          <option value="SOCIAL">SOC</option>
        </select>
        <div class="mb-2">
          <p class="mb-1">Repeat on:</p>
          <div class="flex justify-between">
            <label v-for="(day, index) in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']" :key="index" class="flex items-center">
              <input type="checkbox" v-model="selectedDays[index]" class="mr-1">
              {{ day }}
            </label>
          </div>
        </div>
        <div class="flex justify-end">
          <button @click="addHabit" class="bg-primary text-background rounded px-4 py-2 mr-2 hover:bg-secondary transition-colors duration-200">Add</button>
          <button @click="closeAddHabitDialog" class="bg-gray-300 text-text rounded px-4 py-2 hover:bg-gray-400 transition-colors duration-200">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Dialog di conferma eliminazione -->
    <div v-if="showDeleteConfirmDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-background rounded-lg p-4 w-80 border-4 border-secondary retro-shadow">
        <h3 class="text-lg font-bold text-primary mb-3">Confirm Deletion</h3>
        <p class="mb-4">Are you sure you want to delete this habit?</p>
        <div class="flex justify-end">
          <button @click="deleteHabit" class="bg-red-500 text-white rounded px-4 py-2 mr-2 hover:bg-red-600 transition-colors duration-200 retro-shadow">Delete</button>
          <button @click="cancelDelete" class="bg-gray-300 text-text rounded px-4 py-2 hover:bg-gray-400 transition-colors duration-200 retro-shadow">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import { config } from '@/config.js';

export default {
  name: 'HabitTracker',
  data() {
    return {
      habits: [],
      showAddHabitDialog: false,
      showDeleteConfirmDialog: false,
      habitToDelete: null,
      newHabit: {
        titolo: '',
        descrizione: '',
        difficolta_xp: 10,
        skill: 'GENERAL',
        giorni_ripetizione: '1111111',
        utenti: config.username
      },
      selectedDays: [true, true, true, true, true, true, true]
    }
  },
  mounted() {
    this.fetchHabits();
  },
  methods: {
    async fetchHabits() {
      try {
        const response = await axios.get('/api/habits');
        console.log('Habits response:', response.data);
        if (Array.isArray(response.data)) {
          this.habits = response.data;
        } else {
          console.error('Unexpected response format:', response.data);
          this.habits = [];
        }
      } catch (error) {
        console.error('Error fetching habits:', error);
        this.habits = [];
      }
    },
    openAddHabitDialog() {
      this.showAddHabitDialog = true;
    },
    closeAddHabitDialog() {
      this.showAddHabitDialog = false;
      this.resetNewHabit();
    },
    resetNewHabit() {
      this.newHabit = {
        titolo: '',
        descrizione: '',
        difficolta_xp: 10,
        skill: 'GENERAL',
        giorni_ripetizione: '1111111',
        utenti: config.username
      };
      this.selectedDays = [true, true, true, true, true, true, true];
    },
    async addHabit() {
      if (this.newHabit.titolo.trim()) {
        this.newHabit.giorni_ripetizione = this.selectedDays.map(day => day ? '1' : '0').join('');
        try {
          const response = await axios.post('/api/add_habit', this.newHabit);
          console.log('Habit added:', response.data);
          await this.fetchHabits();
          this.closeAddHabitDialog();
        } catch (error) {
          console.error('Error adding habit:', error.response ? error.response.data : error.message);
        }
      }
    },
    async toggleHabit(habit) {
      try {
        const response = await axios.post(`/api/toggle_habit/${habit.id}`);
        console.log('Habit toggled:', response.data);
        habit.completata = !habit.completata;
      } catch (error) {
        console.error('Error toggling habit:', error);
      }
    },
    difficultyColor(difficolta_xp) {
      switch (difficolta_xp) {
        case 10: return 'text-green-600';
        case 20: return 'text-yellow-600';
        case 30: return 'text-red-600';
        default: return 'text-gray-600';
      }
    },
    getDifficultyLabel(difficolta_xp) {
      switch (difficolta_xp) {
        case 10: return 'EASY';
        case 20: return 'MEDIUM';
        case 30: return 'HARD';
        default: return 'UNKNOWN';
      }
    },
    skillColor(skill) {
      switch (skill) {
        case 'GENERAL': return 'text-gray-600';
        case 'CULTURE': return 'text-blue-600';
        case 'SPORT': return 'text-green-600';
        case 'WELLBEING': return 'text-yellow-600';
        case 'PRODUCTIVITY': return 'text-purple-600';
        case 'CREATIVITY': return 'text-pink-600';
        case 'SOCIAL': return 'text-indigo-600';
        default: return 'text-gray-600';
      }
    },
    confirmDeleteHabit(habit) {
      this.habitToDelete = habit;
      this.showDeleteConfirmDialog = true;
    },
    async deleteHabit() {
      if (this.habitToDelete) {
        try {
          await axios.delete(`/api/delete_habit/${this.habitToDelete.id}`);
          this.habits = this.habits.filter(h => h.id !== this.habitToDelete.id);
          this.showDeleteConfirmDialog = false;
          this.habitToDelete = null;
        } catch (error) {
          console.error('Error deleting habit:', error);
        }
      }
    },
    cancelDelete() {
      this.showDeleteConfirmDialog = false;
      this.habitToDelete = null;
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

.retro-shadow {
  box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.3);
}

.retro-x {
  font-size: 20px;
  line-height: 1;
  font-weight: bold;
  text-shadow: 1px 1px 0px rgba(0, 0, 0, 0.3);
}

.group:hover .retro-shadow {
  box-shadow: 2px 2px 0px rgba(0, 0, 0, 0.3);
  transform: translate(1px, 1px);
}
</style>
