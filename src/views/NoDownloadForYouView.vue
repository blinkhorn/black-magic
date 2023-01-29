<script setup>
import { Authenticator } from '@aws-amplify/ui-vue';
import '@aws-amplify/ui-vue/styles.css';
</script>
<template>
    <authenticator>
        <template v-slot="{ user, signOut }">

            <h1 class="no-downloads-for-you">No downloads are available for your account, {{
                    user.signInUserSession.idToken.payload.email
            }}. Did you already use your bandcamp
                code?</h1>
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

.no-downloads-for-you {
    margin: 1.3rem auto;
}

.sign-out {
    color: rgba(235, 235, 235, 0.64);
}
</style>
        