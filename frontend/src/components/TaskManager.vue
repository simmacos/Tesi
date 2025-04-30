<template>
  <section class="mb-4 bg-accent bg-opacity-20 shadow-lg rounded-lg p-4 border-2 border-secondary">
    <h2 class="text-lg font-bold text-primary mb-3">Daily tasks</h2>
    
    <!-- Barra di creazione task -->
    <div class="flex items-center bg-background rounded-lg p-2 border border-secondary mb-3">
      <input 
        v-model="newTask.titolo" 
        @keyup.enter="addTask"
        placeholder="New Task" 
        class="w-1/4 bg-transparent border-none focus:outline-none text-text placeholder-text placeholder-opacity-50 mr-2"
      >
      <input 
        v-model="newTask.descrizione" 
        placeholder="Description" 
        class="flex-grow bg-transparent border-none focus:outline-none text-text placeholder-text placeholder-opacity-50 mr-2"
      >
      <select 
        v-model="newTask.difficolta_xp" 
        class="bg-transparent border border-secondary rounded px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-primary mr-2"
      >
        <option :value="10">Easy</option>
        <option :value="20">Medium</option>
        <option :value="30">Hard</option>
      </select>
      <select 
        v-model="newTask.skill" 
        class="bg-transparent border border-secondary rounded px-2 py-1 text-sm text-text focus:outline-none focus:ring-1 focus:ring-primary mr-2"
      >
        <option value="GENERAL">GEN</option>
        <option value="CULTURE">CULT</option>
        <option value="SPORT">SPORT</option>
        <option value="WELLBEING">WELL</option>
        <option value="PRODUCTIVITY">PROD</option>
        <option value="CREATIVITY">CREA</option>
        <option value="SOCIAL">SOC</option>
      </select>
      <button @click="addTask" class="bg-primary text-background rounded-full w-8 h-8 flex items-center justify-center hover:bg-secondary transition-colors duration-200">
        ➤
      </button>
    </div>
    
    <!-- Lista delle task -->
    <TransitionGroup name="task-list" tag="div" class="space-y-2">
      <div v-for="task in sortedTasks" :key="task.id" 
           class="bg-background rounded-lg p-2 border border-secondary min-h-[64px] flex items-start transition-all duration-300 group hover:bg-accent hover:bg-opacity-10 relative"
           :class="{ 'opacity-50': task.completata }">
        <input 
          type="checkbox" 
          :checked="task.completata" 
          @change="toggleTask(task)"
          class="form-checkbox h-4 w-4 text-primary rounded border-secondary focus:ring-primary mr-2 mt-1"
        >
        <div class="flex-grow overflow-hidden">
          <div class="flex justify-between items-start mb-1">
            <div class="overflow-hidden">
              <p class="text-sm font-medium text-text truncate">{{ task.titolo }}</p>
              <p class="text-xs text-gray-500 break-words">{{ task.descrizione }}</p>
            </div>
            <span class="text-xs font-semibold whitespace-nowrap ml-2 transition-opacity duration-300 group-hover:opacity-0" :class="difficultyColor(task.difficolta_xp)">
              {{ getDifficultyLabel(task.difficolta_xp) }}
            </span>
          </div>
          <div class="flex justify-end">
            <span class="text-xs font-semibold transition-opacity duration-300 group-hover:opacity-0" :class="skillColor(task.skill)">{{ task.skill }}</span>
          </div>
        </div>
        <button @click="confirmDeleteTask(task)" 
                class="absolute top-0 bottom-0 right-2 my-auto w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 retro-shadow">
          <span class="retro-x">×</span>
        </button>
      </div>
    </TransitionGroup>

    <!-- Dialog di conferma eliminazione -->
    <div v-if="showDeleteConfirmDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-background rounded-lg p-4 w-80 border-4 border-secondary retro-shadow">
        <h3 class="text-lg font-bold text-primary mb-3">Confirm Deletion</h3>
        <p class="mb-4">Are you sure you want to delete this task?</p>
        <div class="flex justify-end">
          <button @click="deleteTask" class="bg-red-500 text-white rounded px-4 py-2 mr-2 hover:bg-red-600 transition-colors duration-200 retro-shadow">Delete</button>
          <button @click="cancelDelete" class="bg-gray-300 text-text rounded px-4 py-2 hover:bg-gray-400 transition-colors duration-200 retro-shadow">Cancel</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';
import { config } from '@/config.js';

export default {
  name: 'TaskManager',
  setup() {
    const newTask = ref({
      titolo: '',
      descrizione: '',
      difficolta_xp: 10,
      skill: 'GENERAL',
      utenti: config.username
    });

    const tasks = ref([]);
    const showDeleteConfirmDialog = ref(false);
    const taskToDelete = ref(null);

    const sortedTasks = computed(() => {
      return [...tasks.value].sort((a, b) => {
        if (a.completata === b.completata) return 0;
        return a.completata ? 1 : -1;
      });
    });

    const fetchTasks = async () => {
      try {
        const response = await axios.get('/api/tasks');
        tasks.value = response.data;
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    const addTask = async () => {
      if (newTask.value.titolo.trim()) {
        try {
          await axios.post('/api/add_task', newTask.value);
          await fetchTasks();
          newTask.value = {
            titolo: '',
            descrizione: '',
            difficolta_xp: 10,
            skill: 'GENERAL',
            utenti: config.username
          };
        } catch (error) {
          console.error('Error adding task:', error);
        }
      }
    };

    const toggleTask = async (task) => {
      try {
        if (task.completata) {
          await axios.post(`/api/uncomplete_task/${task.id}`);
        } else {
          await axios.post(`/api/complete_task/${task.id}`);
        }
        task.completata = !task.completata;
      } catch (error) {
        console.error('Error toggling task:', error);
      }
    };

    const confirmDeleteTask = (task) => {
      taskToDelete.value = task;
      showDeleteConfirmDialog.value = true;
    };

    const deleteTask = async () => {
      if (taskToDelete.value) {
        try {
          await axios.delete(`/api/delete_task/${taskToDelete.value.id}`);
          tasks.value = tasks.value.filter(t => t.id !== taskToDelete.value.id);
          showDeleteConfirmDialog.value = false;
          taskToDelete.value = null;
        } catch (error) {
          console.error('Error deleting task:', error);
        }
      }
    };

    const cancelDelete = () => {
      showDeleteConfirmDialog.value = false;
      taskToDelete.value = null;
    };

    const difficultyColor = (difficolta_xp) => {
      switch (difficolta_xp) {
        case 10: return 'text-green-600';
        case 20: return 'text-yellow-600';
        case 30: return 'text-red-600';
        default: return 'text-gray-600';
      }
    };

    const skillColor = (skill) => {
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
    };

    const getDifficultyLabel = (difficolta_xp) => {
      switch (difficolta_xp) {
        case 10: return 'EASY';
        case 20: return 'MEDIUM';
        case 30: return 'HARD';
        default: return 'UNKNOWN';
      }
    };

    return {
      newTask,
      tasks,
      sortedTasks,
      showDeleteConfirmDialog,
      taskToDelete,
      fetchTasks,
      addTask,
      toggleTask,
      confirmDeleteTask,
      deleteTask,
      cancelDelete,
      difficultyColor,
      skillColor,
      getDifficultyLabel
    };
  },
  mounted() {
    this.fetchTasks();
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

.task-list-move,
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.5s ease;
}

.task-list-enter-from,
.task-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.task-list-leave-active {
  position: absolute;
}

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%238B4513'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
</style>
