<script setup>
import router from '@/router';
import { API } from 'aws-amplify';
import { ref } from 'vue';


const apiName = 'blackmagicapigwproduction';
const getInit = {
    headers: { 'Content-Type': 'application/json' },
    response: true,
};
const bandcampCode = ref('');
function verifyCode() {
    const getPath = `/api/codes/${bandcampCode.value}`;
    API.get(apiName, getPath, getInit)
        .then((response) => {
            const code = response.data[0].code;
            router.push(`/@cce$s-downl0ad?bandcampCode=${code}`)
        })
        .catch((error) => {
            console.log(error);
        });
}
</script>
<template>
    <label>Code from Bandcamp</label>
    <input v-model="bandcampCode" placeholder="ENTER CODE">
    <button @click="verifyCode">Redeem Code</button>
</template>
<style scoped>
label,
input,
button {
    font-family: helvetica, san-serif;
    font-weight: 300;
    font-size: calc(1rem + 0.7vw);
    border-radius: 0.25rem;
}

label,
button {
    text-transform: uppercase;
}

button {
    margin: 1.3rem auto;
    cursor: pointer;
    color: hsla(160, 100%, 37%, 1);
    background-color: #282828;
    border: 0;
    box-shadow: none;
    padding: 0.1em;
}
</style>
    