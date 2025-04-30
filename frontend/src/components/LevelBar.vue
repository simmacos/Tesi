<template>
  <section class="mb-8 bg-accent bg-opacity-20 shadow-lg rounded-lg p-6 border-2 border-secondary">
    <!-- Barra di livello principale -->
    <div class="mb-6">
      <div class="flex justify-between items-center mb-2">
        <span class="text-2xl font-bold text-primary">Level {{ mainLevel }}</span>
        <span class="text-xl text-text">{{ mainExp }} / {{ mainExpNeeded }} XP</span>
      </div>
      <div class="w-full bg-background rounded-full h-5 border-2 border-primary relative group">
        <div 
          class="bg-primary h-full rounded-full transition-all duration-500 ease-out"
          :style="{ width: `${mainProgressPercentage}%` }"
        ></div>
        <span class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          XP Totali: {{ totalMainExp }}
        </span>
      </div>
    </div>

    <!-- Barre delle skill -->
    <div class="grid grid-cols-3 gap-4">
      <div v-for="skill in skills" :key="skill.name" class="skill-bar">
        <div class="flex items-center justify-between mb-1">
          <span class="font-semibold text-text text-sm">{{ skill.name }}</span>
          <span class="text-xs text-text">Lv. {{ skill.level }}</span>
        </div>
        <div class="w-full bg-background rounded-full h-3 border border-secondary relative group">
          <div 
            class="bg-secondary h-full rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${skill.progressPercentage}%` }"
          ></div>
          <span class="absolute inset-0 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            {{ skill.exp }} / {{ skill.expNeeded }} XP
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import { config } from '@/config.js';

export default {
  name: 'LevelBar',
  data() {
    return {
      mainExp: 0,
      totalMainExp: 0,
      mainLevel: 1,
      mainExpNeeded: 100,
      mainProgressPercentage: 0,
      skills: [
        { name: 'CULTURE', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
        { name: 'SPORT', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
        { name: 'WELLBEING', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
        { name: 'PRODUCTIVITY', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
        { name: 'CREATIVITY', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
        { name: 'SOCIAL', exp: 0, totalExp: 0, level: 1, expNeeded: 100, progressPercentage: 0 },
      ]
    }
  },
  mounted() {
    this.fetchUserData();
    this.startPolling();
  },
  beforeUnmount() {
    this.stopPolling();
  },
  methods: {
    calculateLevel(totalExp) {
      return Math.floor((totalExp / 100) ** (2/3)) + 1;
    },
    calculateExpNeeded(level) {
      const rawExpNeeded = Math.ceil(100 * (level ** 1.5));
      return Math.ceil(rawExpNeeded / 10) * 10; // Arrotonda al multiplo di 10 più vicino
    },
    calculateExpForCurrentLevel(totalExp) {
      const level = this.calculateLevel(totalExp);
      const expForPreviousLevel = this.calculateExpNeeded(level - 1);
      return totalExp - expForPreviousLevel;
    },
    updateSkillData(skill) {
      skill.totalExp = Math.max(0, parseInt(skill.totalExp) || 0);
      skill.level = this.calculateLevel(skill.totalExp);
      skill.expNeeded = this.calculateExpNeeded(skill.level);
      skill.exp = this.calculateExpForCurrentLevel(skill.totalExp);
      skill.progressPercentage = Math.min(100, Math.max(0, (skill.exp / skill.expNeeded) * 100));
      console.log(`Updated ${skill.name}: Level ${skill.level}, XP ${skill.exp}/${skill.expNeeded}, Total XP ${skill.totalExp}`);
    },
    async fetchUserData() {
      try {
        const [generalResponse, skillResponse] = await Promise.all([
          axios.get(`/api/user/${config.username}/general_xp`),
          axios.get(`/api/user/${config.username}/skill_xp`)
        ]);

        console.log('General XP:', generalResponse.data);
        console.log('Skill XP:', skillResponse.data);

        this.totalMainExp = Math.max(0, parseInt(generalResponse.data.general_xp) || 0);
        this.mainLevel = this.calculateLevel(this.totalMainExp);
        this.mainExpNeeded = this.calculateExpNeeded(this.mainLevel);
        this.mainExp = this.calculateExpForCurrentLevel(this.totalMainExp);
        this.mainProgressPercentage = Math.min(100, Math.max(0, (this.mainExp / this.mainExpNeeded) * 100));

        const skillData = skillResponse.data;
        this.skills.forEach(skill => {
          const skillName = skill.name.toLowerCase();
          skill.totalExp = Math.max(0, parseInt(skillData[`${skillName}_xp`]) || 0);
          this.updateSkillData(skill);
        });
      } catch (error) {
        console.error('Error fetching user XP data:', error);
      }
    },
    startPolling() {
      this.pollingInterval = setInterval(() => {
        this.fetchUserData();
      }, 5000); // Poll every 5 seconds
    },
    stopPolling() {
      clearInterval(this.pollingInterval);
    }
  }
}
</script>

<style scoped>
.skill-bar:hover .bg-secondary {
  filter: brightness(110%);
  box-shadow: 0 0 8px rgba(210, 105, 30, 0.6);
}

.group:hover .bg-primary,
.group:hover .bg-secondary {
  filter: brightness(90%);
}
</style>
