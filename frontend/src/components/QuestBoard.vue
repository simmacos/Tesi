<template>
  <section class="mb-4 bg-accent bg-opacity-20 shadow-lg rounded-lg p-3 border-2 border-secondary">
    <h2 class="text-lg font-bold text-primary mb-2">Quest Giornaliere</h2>
    <div class="flex space-x-2">
      <div v-for="quest in quests" :key="quest.id" class="flex-1 bg-background rounded-lg p-2 border border-secondary">
        <div class="flex items-start">
          <input 
            type="checkbox" 
            :checked="quest.completed" 
            @change="toggleQuest(quest.id)"
            class="form-checkbox h-4 w-4 text-primary rounded border-secondary focus:ring-primary mr-2 mt-1"
          >
          <div class="flex-grow">
            <div class="flex justify-between items-start mb-1">
              <p class="text-sm font-medium text-text line-clamp-2 mr-2">{{ quest.description }}</p>
              <span class="text-xs font-semibold whitespace-nowrap" :class="difficultyColor(quest.difficulty)">
                {{ quest.difficulty.toUpperCase() }}
              </span>
            </div>
            <div class="flex justify-end">
              <span class="text-xs text-secondary font-semibold">{{ quest.category }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'QuestBoard',
  data() {
    return {
      quests: [
        { id: 1, description: 'Leggi un capitolo di un libro', difficulty: 'easy', category: 'CULT', completed: false },
        { id: 2, description: 'Fai 30 minuti di esercizio', difficulty: 'medium', category: 'FIT', completed: false },
        { id: 3, description: 'Completa un progetto creativo', difficulty: 'hard', category: 'ART', completed: false },
      ]
    }
  },
  methods: {
    toggleQuest(id) {
      const quest = this.quests.find(q => q.id === id);
      if (quest) {
        quest.completed = !quest.completed;
      }
    },
    difficultyColor(difficulty) {
      switch (difficulty) {
        case 'easy': return 'text-green-600';
        case 'medium': return 'text-yellow-600';
        case 'hard': return 'text-red-600';
        default: return 'text-gray-600';
      }
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
</style>
