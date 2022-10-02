<script setup>
import { ref } from 'vue';

import { Authenticator } from '@aws-amplify/ui-vue';
import '@aws-amplify/ui-vue/styles.css';
import { useRoute, useRouter } from "vue-router";
import { API } from 'aws-amplify';
const apiName = 'blackmagicapigw';

const $userEmail = ref(null);
const route = useRoute();
const router = useRouter();
const bandcampCode = route?.query?.bandcampCode;
const requestInit = {
    headers: { 'Content-Type': 'application/json' },
    response: true,
    queryStringParameters: {
        bandcampCode
    }
};
function getPresignedS3Url() {
    const getPath = `/api/users/${$userEmail.value.innerHTML}`;
    API.get(apiName, getPath, requestInit).then((response) => {
        const { mp3Url, mp3Name, userId } = response.data;
        const deletePath = `/api/mp3s/${userId}/${mp3Name}.mp3`;

        sendToDownload(encodeURIComponent(mp3Url), encodeURIComponent(deletePath));
    }).catch((error) => {
        console.error(error);
        router.push('/n0-down1oad-4-u');
    });
}
function sendToDownload(mp3Url, deletePath) {
    router.push(`/d0wnload-mvz1k?deletePath=${deletePath}&presignedS3Url=${mp3Url}`)
}
</script>
<template>
    <authenticator>
        <template v-slot="{ user, signOut }">
            <h1>Hey <span ref="$userEmail">{{ user.signInUserSession.idToken.payload.email }}</span>, click 'ACCESS
                DOWNLOAD' to get your download link.</h1>
            <button v-if="!$presignedS3Url" class="access-download" @click="getPresignedS3Url">Access
                Download</button>
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

.access-download {
    color: hsla(160, 100%, 37%, 1);
}

.access-download,
.no-downloads-for-you {
    margin: 1.3rem auto;
}

.sign-out {
    color: rgba(235, 235, 235, 0.64);
}
</style>
    