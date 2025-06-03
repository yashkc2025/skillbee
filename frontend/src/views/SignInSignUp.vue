<template>
    <div class="body">
        <div class="container" :class="{ 'sign-up-mode': isSignUp }">
            <div class="forms-container">
                <div class="signin-signup">
                    <!-- Sign In Form -->
                    <div class="sign-in-form" v-if="!isSignUp">
                        <h2 class="title">Sign in <span>as {{ userType }} </span> </h2>
                        <div class="user-btn-box" v-if=!userType>
                            <button class="btn user-btn" @click="admin">Admin</button>
                            <button class="btn user-btn" @click="parent">Parent</button>
                            <button class="btn user-btn" @click="child">Independent Child</button>
                        </div>
                        <form v-if="userType" @submit.prevent="loginUser">
                            <div v-if="userType === 'Child'">
                                <div class="input-field">
                                    <i class="username-icon"></i>
                                    <input type="text" placeholder="Username" v-model="register.username" required />
                                </div>
                            </div>

                            <div v-if="userType === 'Parent'">
                                <div class="input-field">
                                    <i class="email_icon"></i>
                                    <input type="email" placeholder="Email" v-model="register.email" required />
                                </div>
                            </div>

                            <div class="input-field">
                                <i class="password-icon"></i>
                                <input type="password" placeholder="Password" v-model="login.password" required />
                            </div>
                            <button class="btn solid" type="submit">Login</button>
                        </form>

                        <div v-if="isForm" class="sign-in-form">
                            <p style="margin: 0; color: grey;">--------------------------------- &nbsp; or &nbsp;
                                ---------------------------------</p>
                            <h2 class="title">Sign in <span>as </span> </h2>
                            <div class="forms-btn">
                                <button class="btn" v-if="userType !== 'Admin'" @click="admin">Admin</button>
                                <button class="btn" v-if="userType !== 'Parent'" @click="parent">Parent</button>
                                <button class="btn" v-if="userType !== 'Child'" @click="child">Independent
                                    Child</button>
                            </div>
                        </div>

                    </div>

                    <!-- Sign Up Form -->
                    <div class="sign-up-form" v-else>
                        <h2 class="title">Sign up <span>as {{ userType }} </span> </h2>
                        <div class="user-btn-box" v-if=!userType>
                            <button class="btn user-btn" @click="parent">Parent</button>
                            <button class="btn user-btn" @click="child">Independent Child</button>
                        </div>
                        <form v-if="userType" @submit.prevent="registerUser">
                            <div class="input-field">
                                <font-awesome-icon :icon="['fas', 'user']" />
                                <input type="text" placeholder="Name" required>
                            </div>

                            <div class="input-field">
                                <i class="email-icon"></i>
                                <input type="email" placeholder="Email" v-model="register.email" required />
                            </div>

                            <div v-if="userType === 'Child'">
                                <div class="input-field">
                                    <i class="username_icon"></i>
                                    <input type="text" placeholder="Username" v-model="register.username" required />
                                </div>
                            </div>

                            <div class="input-field">
                                <i class="bx bx-lock"></i>
                                <input type="password" placeholder="Password" v-model="register.password" required />
                            </div>

                            <div v-if="userType === 'Child'">
                                <div class="input-field">
                                    <i class="calender-icon"></i>
                                    <input type="date" placeholder="Date of Birth" v-model="register.dob" required />
                                </div>
                            </div>
                            <div v-if="userType === 'Child'">
                                <div class="input-field">
                                    <i class="school-icon"></i>
                                    <input type="text" placeholder="School" v-model="register.school" required />
                                </div>
                            </div>
                            <button class="btn" type="submit">Register</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Slider -->
            <div class="slider-container">
                <div class="slide left-slide" v-if="!isSignUp">
                    <div class="content">
                        <h2 class="about-form">Hello, Welcome back!</h2>
                        <p class="about-btn">Don't have an account?</p>
                        <button class="btn transparent" @click="toggleMode">Sign up</button>
                    </div>
                </div>
                <div class="slide right-slide" v-else>
                    <div class="content">
                        <h2 class="about-form">Create an account!</h2>
                        <p class="about-btn">Already have an account?</p>
                        <button class="btn transparent" @click="toggleMode">Sign in</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'SignInSignUp',
    data() {
        return {
            isSignUp: false,
            isForm: false,
            userType: '',
            login: {
                username: '',
                email: '',
                password: ''
            },
            register: {
                name: '',
                username: '',
                email: '',
                password: '',
                dob: '',
                school: ''
            }
        }
    },
    methods: {
        toggleMode() {
            this.isSignUp = !this.isSignUp;
            this.userType = '';
            this.isForm = false;
            this.login = {
                username: '',
                email: '',
                password: ''
            };
            this.register = {
                name: '',
                username: '',
                email: '',
                password: '',
                dob: '',
                school: ''
            };
        },
        admin() {
            this.userType = 'Admin';
            this.isForm = true;
        },
        parent() {
            this.userType = 'Parent';
            this.isForm = true;
        },
        child() {
            this.userType = 'Child';
            this.isForm = true;
        },
        async loginUser() {
            if (this.userType === 'Parent' && this.login.email && this.login.password) {
                alert(`Logging in Parent: ${this.login.email}`);
            } else if (this.userType === 'Child' && this.login.username && this.login.password) {
                alert(`Logging in Child: ${this.login.username}`);
            } else if (this.userType === 'Admin' && this.login.username && this.login.password) {
                alert(`Logging in Admin: ${this.login.username}`);
            } else {
                alert('Please fill in all required fields.');
            }
        },
        async registerUser() {
            if (this.userType === 'Parent') {
                if (this.register.name && this.register.email && this.register.password) {
                    alert(`Registering Parent: Name=${this.register.name}, Email=${this.register.email}`);
                } else {
                    alert('Please fill all required fields for Parent.');
                }
            } else if (this.userType === 'Child') {
                if (
                    this.register.name &&
                    this.register.username &&
                    this.register.email &&
                    this.register.password &&
                    this.register.dob &&
                    this.register.school
                ) {
                    alert(`Registering Child: Name=${this.register.name}, Username=${this.register.username}, Email=${this.register.email}, DOB=${this.register.dob}, School=${this.register.school}`);
                } else {
                    alert('Please fill all required fields for Child.');
                }
            }
        }
    }
}

</script>

<style scoped>
.body {
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

:global(body) {
    background-color: rgba(255, 240, 240, 0.6);
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

.container {
    position: fixed;
    left: 20%;
    top: 10%;
    width: 60%;
    min-height: 80%;
    background: #f6f5f7;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 4%;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.forms-container {
    position: absolute;
    width: 50%;
    height: 100%;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.4s ease;
}

.signin-signup {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.sign-in-form,
.sign-up-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 auto;
}

form {
    border-radius: 10px;
    padding: 2rem;
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: -30px;
}

span {
    font-weight: 400;
}

.input-field {
    position: relative;
    width: 85%;
}

.input-field i {
    position: absolute;
    top: 12px;
    left: 10px;
    color: #acacac;
}

.input-field input {
    width: 100%;
    padding: 12px 12px 12px 36px;
    border: none;
    border-radius: 4px;
    background: #f0f0f0;
    outline: none;
    font-size: medium;
}

.btn {
    border: none;
    outline: none;
    border-radius: 20px;
    padding: 10px 40px;
    background-color: #ef476ec0;
    color: #fff;
    font-weight: bold;
    cursor: pointer;
    transition: 0.5s;
    font-size: medium;
}

.forms-btn {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
}

.user-btn-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 300px;
}

.user-btn {
    width: 80%;
}

.btn:hover {
    background-color: #ef476f;
    transform: scale(1.01);
}

.btn.transparent {
    background: transparent;
    border: 2px solid #fff;
    color: #fff;
}

.about-btn {
    font-size: small;
}

.about-form {
    font-size: xx-large;
}

.slider-container {
    position: absolute;
    width: 150%;
    height: 100%;
    top: 0;
    right: -100%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 1s ease-in-out;
    background-color: #ef476f;
    /* border-radius: 20%; */
}

.slide {
    color: #fff;
    border-radius: 10px;
    padding: 2rem;
    width: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.left-slide {
    position: absolute;
    left: 3%;
}

.right-slide {
    position: absolute;
    right: 3%;
}

.sign-up-mode .forms-container {
    left: 50%;
}

.sign-up-mode .slider-container {
    right: 50%;
}
</style>
