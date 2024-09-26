<template>
  <section class="mb-8 bg-accent bg-opacity-20 shadow-lg rounded-lg p-6 border-2 border-secondary">
    <!-- Barra di livello principale -->
    <div class="mb-6">
      <div class="flex justify-between items-center mb-2">
        <span class="text-2xl font-bold text-primary">Livello {{ mainLevel }}</span>
        <span class="text-xl text-text">{{ mainExp }} / {{ mainExpNeeded }} XP</span>
      </div>
      <div class="w-full bg-background rounded-full h-5 border-2 border-primary">
        <div 
          class="bg-primary h-full rounded-full transition-all duration-500 ease-out"
          :style="{ width: `${(mainExp / mainExpNeeded) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Barre delle skill -->
    <div class="grid grid-cols-3 gap-4">
      <div v-for="skill in skills" :key="skill.name" class="skill-bar">
        <div class="flex items-center justify-between mb-1">
          <span class="font-semibold text-text text-sm">{{ skill.name }}</span>
          <span class="text-xs text-text">Lv. {{ skill.level }}</span>
        </div>
        <div class="w-full bg-background rounded-full h-3 border border-secondary">
          <div 
            class="bg-secondary h-full rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${(skill.exp / skill.expNeeded) * 100}%` }"
          ></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'LevelBar',
  data() {
    return {
      mainLevel: 5,
      mainExp: 1250,
      mainExpNeeded: 2000,
      skills: [
        { name: 'CULT', level: 3, exp: 75, expNeeded: 100 },
        { name: 'ART', level: 2, exp: 50, expNeeded: 100 },
        { name: 'FIT', level: 4, exp: 90, expNeeded: 100 },
        { name: 'SOC', level: 1, exp: 25, expNeeded: 100 },
        { name: 'WELL', level: 3, exp: 60, expNeeded: 100 },
        { name: 'HOUS', level: 2, exp: 40, expNeeded: 100 },
      ]
    }
  }
}
</script>

<style scoped>
.skill-bar:hover .bg-secondary {
  filter: brightness(110%);
  box-shadow: 0 0 8px rgba(210, 105, 30, 0.6);
}
</style>
