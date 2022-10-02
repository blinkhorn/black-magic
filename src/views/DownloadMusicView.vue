<script setup>
import { Authenticator } from '@aws-amplify/ui-vue';
import '@aws-amplify/ui-vue/styles.css';
import { useRoute } from "vue-router";
import { API } from 'aws-amplify';
const apiName = 'blackmagicapigw';
const requestInit = {
    headers: { 'Content-Type': 'application/json' },
    response: true,
};

const route = useRoute();
const deletePath = decodeURIComponent(route?.query?.deletePath);
const presignedS3Url = decodeURIComponent(route?.query?.presignedS3Url);
function removeMp3FromS3() {
    API.del(apiName, deletePath, requestInit)
        .then(() => {
            // do nothing
        }).catch((error) => {
            console.error(error);
        });
}
</script>
<template>
    <authenticator>
        <template v-slot="{ signOut }">
            <h1>Click "DOWNLOAD" to download your music. Once you click 'DOWNLOAD,'
                you have 6
                minutes to download your music from the page that opens.</h1>
            <a target="_blank" rel="noopener noreferrer" v-bind:href="presignedS3Url"><button class="go-to-download"
                    @click="removeMp3FromS3">Download</button></a>
            <button class="sign-out" @click="signOut">Sign Out</button>
        </template>
    </authenticator>
</template>
<style scoped>
h1,
button {
    font-family: helvetica, san-serif;
    font-weight: 300;
    font-size: calc(1rem + 0.7vw);
    border-radius: 0.25rem;
    text-align: center;
}

h1 {
    width: 70vw;
}

button {
    text-transform: uppercase;
    cursor: pointer;
    border: 0;
    box-shadow: none;
    padding: 0.1em;
    background-color: #282828;
}

.go-to-download {
    color: hsla(160, 100%, 37%, 1);
    margin: 1.3rem auto;
}

.sign-out {
    color: rgba(235, 235, 235, 0.64);
}
</style>
    