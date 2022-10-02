<script setup>
import { RouterLink, RouterView } from "vue-router";
import TheHeader from "./components/TheHeader.vue";
</script>
  
<template>
  <header>
    <div class="wrapper">
      <TheHeader />

      <nav>
        <RouterLink class="nav-link" to="/">
          <span>H</span>
          <span>o</span>
          <span>m</span>
          <span>e</span>
        </RouterLink>
        <RouterLink class="nav-link" to="/redeem-code">
          <span>R</span>
          <span>e</span>
          <span>d</span>
          <span>e</span>
          <span>e</span>
          <span>m</span>
          <span> </span>
          <span>C</span>
          <span>o</span>
          <span>d</span>
          <span>e</span>
        </RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
  
<style scoped>

header {
  line-height: 1.5;
  margin-bottom: 1rem;
}

nav .nav-link:nth-child(1) {
  grid-column: 11;
  grid-row: 1;
  display: grid;
  grid-template-rows: repeat(12, 1fr);
}

nav .nav-link:nth-child(2) {
  grid-column: 12;
  grid-row: 1;
  display: grid;
  grid-template-rows: repeat(12, 1fr);
}

nav .nav-link:nth-child(3) {
  grid-column: 13;
  grid-row: 1;
  display: grid;
  grid-template-rows: repeat(12, 1fr);
}

nav {
  text-align: center;
  display: grid;
  grid-template-columns: repeat(16, 1fr);
  width: 100%;
  margin-top: 1rem;
  text-transform: uppercase;
  font-family: helvetica, san-serif;
  font-weight: 300;
  font-size: calc(0.7rem + 1.1vw);
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

@media (min-width: 1024px) {

  header {
    display: flex;
    place-items: center;
  }

  nav {
    text-align: center;
    margin-left: -1rem;
    font-size: calc(0.5rem + 1.1vw);

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
  