<template>
  <section>
    <h1 class="tilt">black</h1>
    <h1>magic</h1>
  </section>
</template>

<style scoped>
section {
  width: 80vw;
  display: grid;
  margin: auto;
  grid-template-columns: auto 1fr 1fr 1fr 0.5fr;
  grid-template-rows: auto 1fr 1fr auto auto;
  grid-gap: 1rem;
}

section h1:nth-child(1) {
  grid-column: 1 / 4;
  color: hsla(160, 100%, 37%, 1);
}

section h1:nth-child(2) {
  grid-column: 3 / 4;
  grid-row: 2 / 5;
  justify-self: end;
  margin-top: -10px;
  margin-right: -10px;
}

h1 {
  text-transform: uppercase;
  font-family: helvetica, san-serif;
  font-weight: 300;
  font-size: calc(1.1rem + 1.8vw);
}

.tilt {
  text-align: center;
  transform: rotate(-45deg);
}

@media (min-width: 1024px) {
  section {
    width: 50vw;
  }
}
</style>
