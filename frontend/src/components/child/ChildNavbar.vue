<script setup lang="ts">
import sitemap from "../../router/sitemap.json";

const navOptions = [
  {
    label: "🏠 Dashboard",
    link: sitemap.child_app.dashboard,
  },
  {
    label: "📚 Curriculum",
    link: sitemap.child_app.curriculum.curriculums,
  },
  {
    label: "🏅 Achievements",
    link: sitemap.child_app.achievements,
  },
  {
    label: "⚙️ Settings",
    link: sitemap.child_app.settings,
  },
];
</script>

<template>
  <div class="navbar box-shadow kid-navbar">
    <section class="logo-parent">
      <img src="/logo.png" alt="Kid App Logo" />
    </section>
    <section class="items-parent">
      <a :href="n.link" class="nav-items" v-for="n in navOptions" :key="n.label" tabindex="0">
        {{ n.label }}
      </a>
      <a class="danger" href="/" tabindex="0">🚪 Logout</a>
    </section>
  </div>
</template>

<style scoped>
.navbar.kid-navbar {
  padding: var(--size-xs) var(--size-lg);
  display: flex;
  flex-direction: row;
  background: #fff3e0;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(211, 210, 210, 0.455);
}

.items-parent {
  display: flex;
  flex-direction: row;
  align-items: center;
}

a.nav-items {
  color: #4a148c;
  padding: 5px 18px;
  font-family: "VAGRoundedNext";
  font-weight: bold;
  transition: background 0.2s, color 0.2s, transform 0.15s;
  cursor: pointer;
  display: flex;
  align-items: center;
  text-decoration: none;
}

a.nav-items:hover,
a.nav-items:focus {
  color: #d84315;
  transform: scale(1.02);
}

a.danger {
  color: #e53935;
  padding: 5px 18px;
  font-family: "VAGRoundedNext";
  font-weight: bold;
  transition: background 0.2s, color 0.2s, transform 0.15s;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  text-decoration: none;
}

a.danger:hover,
a.danger:focus {
  color: #b71c1c;
  transform: scale(1.02);
}

.logo-parent {
  display: flex;
  justify-content: center;
  align-items: center;
}

img {
  width: 90px;
  padding: var(--size-2xs) var(--size-xs);
  /* border-radius: 50%; */
  /* background: #fffde7; */
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.10);
  /* border: 2px solid #ffb300; */
  transition: transform 0.2s;
}

/* img:hover {transform: scale(1.08) rotate(-6deg);
  box-shadow: 0 4px 16px rgba(255, 193, 7, 0.18);
} */
</style>
