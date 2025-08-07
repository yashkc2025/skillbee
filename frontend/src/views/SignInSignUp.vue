<template>
    <div class="body">
        <div class="container" :class="{ 'sign-up-mode': isSignUp }">
            <div class="forms-container">
                <div class="signin-signup">
                    <!-- Sign In Form -->
                    <div class="sign-in-form">
                        <h2 class="title ft-head-1">{{ selectedUserType ? "Selected" : "Select" }} a user to login
                            <span v-if="selectedUserType">as {{ selectedUserType }} </span>
                        </h2>

                        <!-- User Type Selection Buttons -->
                        <div class="user-btn-box" v-if="!selectedUserType">
                            <button v-for="userType in signInUserTypes" :key="userType" class="btn user-btn"
                                @click="handleUserTypeSelection(userType)">
                                {{ userType }}
                            </button>
                        </div>

                        <!-- SignIn Form -->
                        <form v-if="selectedUserType" @submit.prevent="handleLogin">
                            <div v-for="field in loginFormFields" :key="field.name" class="form-field">
                                <i :class="getIconClass(field.icon)"></i>
                                <input
                                    :type="field.name === 'password' ? (showPassword ? 'text' : 'password') : field.type"
                                    :placeholder="field.placeholder" :value="loginData[field.name]"
                                    :required="field.required"
                                    @input="updateLoginData(field.name, $event.target.value)" />

                                <button v-if="field.name === 'password'" type="button" @click="togglePasswordVisibility"
                                    class="eye-toggle-btn">
                                    <i :class='showPassword ? "bi bi-eye" : "bi bi-eye-slash"'></i>
                                </button>
                            </div>
                            <button class="btn btn-primary" type="submit">Login</button>
                            <p class="error" v-if="errorMessage">error: {{ errorMessage }}</p>
                        </form>

                        <!-- Alternative User Types -->
                        <div v-if="selectedUserType && showAlternativeTypes" class="alternative-btn">
                            <p class="divider">------------ &nbsp; or &nbsp; ------------</p>
                            <h3 class="alternative-title">Sign in <span>as </span> </h3>
                            <div class="alternative-btns">
                                <button v-for="userType in alternativeUserTypes" :key="userType"
                                    class="btn btn-secondary" @click="handleUserTypeSelection(userType)">
                                    {{ userType }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Sign Up Form -->
                    <div class="sign-up-form">
                        <h2 class="title ft-head-1">Sign up <span>as
                                {{ selectedUserType === "Child" ? "Independent Child" : selectedUserType }} </span>
                        </h2>

                        <!-- User Selection Buttons -->
                        <div class="user-btn-box" v-if="!selectedUserType">
                            <button v-for="userType in signUpUserTypes" :key="userType" class="btn user-btn"
                                @click="handleUserTypeSelection(userType)">
                                {{ userType === "Child" ? "Independent Child" : userType }}
                            </button>
                        </div>

                        <!-- Signup Form -->
                        <form v-if="selectedUserType" @submit.prevent="handleRegister">
                            <div v-for="field in registerFormFields" :key="field.name" class="form-field">
                                <i :class="getIconClass(field.icon)"></i>
                                <input
                                    :type="field.name === 'password' ? (showPassword ? 'text' : 'password') : field.type"
                                    :placeholder="field.placeholder" :value="registerData[field.name]"
                                    :required="field.required"
                                    @input="updateRegisterData(field.name, $event.target.value)"
                                    v-if="field.name !== 'dob'" />
                                <input v-if="field.name === 'dob'" type="date" :placeholder="field.placeholder"
                                    :value="registerData[field.name]" :required="field.required" :min="minDate"
                                    :max="maxDate" @input="updateRegisterData(field.name, $event.target.value)" />
                                <button v-if="field.name === 'password'" type="button" @click="togglePasswordVisibility"
                                    class="eye-toggle-btn">
                                    <i :class='showPassword ? "bi bi-eye" : "bi bi-eye-slash"'></i>
                                </button>
                            </div>
                            <button class="btn btn-primary" type="submit">Register</button>
                            <p class="error" v-if="errorMessage">error: {{ errorMessage }}</p>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Slider -->
            <div class="slider-container">
                <div class="slide" :class="isSignUp ? 'right-slide' : 'left-slide'">
                    <div class="slide-content">
                        <h2 class="slide-title">{{ slideTitle }}</h2>
                        <p class="slide-text">{{ slideText }}</p>
                        <button class="btn btn-transparent" @click="toggleAuthMode">
                            {{ buttonText }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { base_url } from "../router";

interface UserData {
    username?: string;
    email?: string;
    password?: string;
    name?: string;
    dob?: string;
    school?: string;
}
type UserType = "Admin" | "Parent" | "Child" | "";
interface FormField {
    name: string;
    type: string;
    placeholder: string;
    icon: string;
    required: boolean;
    min?: string;
    max?: string;
}
// Reactive state
const showPassword = ref(false);
const isSignUp = ref(false);
const selectedUserType = ref<UserType>("");
const showAlternativeTypes = ref(false);
const loginData = ref<UserData>({
    username: "",
    email: "",
    password: "",
});
const registerData = ref<UserData>({
    name: "",
    username: "",
    email: "",
    password: "",
    dob: "",
    school: "",
});

const signInUserTypes = computed(() => ["Admin", "Parent", "Child"]);
const signUpUserTypes = computed(() => ["Parent", "Child"]);
const alternativeUserTypes = computed(() => {
    const allTypes = ["Admin", "Parent", "Child"];
    return allTypes.filter((type) => type !== selectedUserType.value);
});
const loginFormFields = computed((): FormField[] => {
    const fields: FormField[] = [];
    if (selectedUserType.value === "Child") {
        fields.push({
            name: "username",
            type: "text",
            placeholder: "Username",
            icon: "@",
            required: true,
        });
    }
    if (selectedUserType.value === "Parent" || selectedUserType.value === "Admin") {
        fields.push({
            name: "email",
            type: "email",
            placeholder: "Email",
            icon: "envelope",
            required: true,
        });
    }
    fields.push({
        name: "password",
        type: "password",
        placeholder: "Password",
        icon: "lock",
        required: true,
    });
    return fields;
});
const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0');
const dd = String(today.getDate()).padStart(2, '0');


const maxDate = `${yyyy - 8}-${mm}-${dd}`;
const minDate = `${yyyy - 14}-${mm}-${dd}`;

const registerFormFields = computed((): FormField[] => {
    const fields: FormField[] = [];
    fields.push({
        name: "name",
        type: "text",
        placeholder: "Name",
        icon: "user",
        required: true,
    });
    if (selectedUserType.value === "Child") {
        fields.push({
            name: "username",
            type: "text",
            placeholder: "Username",
            icon: "@",
            required: true,
        });
    }
    fields.push({
        name: "email",
        type: "email",
        placeholder: "Email",
        icon: "envelope",
        required: true,
    });
    fields.push({
        name: "password",
        type: "password",
        placeholder: "Password",
        icon: "lock",
        required: true,
    });
    if (selectedUserType.value === "Child") {
        fields.push(
            {
                name: "dob",
                type: "date",
                placeholder: "Date of Birth",
                icon: "calendar",
                required: true,
                min: minDate,
                max: maxDate
            },
            {
                name: "school",
                type: "text",
                placeholder: "School",
                icon: "graduation-cap",
                required: true,
            }
        );
    }
    return fields;
});
const slideTitle = computed(() => {
    return isSignUp.value ? "Create an account!" : "Hello, Welcome back!";
});
const slideText = computed(() => {
    return isSignUp.value ? "Already have an account?" : "Don't have an account?";
});
const buttonText = computed(() => {
    return isSignUp.value ? "Sign in" : "Sign up";
});

const getIconClass = (icon: string): string => {
    const iconMap: Record<string, string> = {
        user: "bi bi-person",
        "@": "bi bi-at",
        envelope: "bi bi-envelope",
        lock: "bi bi-lock",
        calendar: "bi bi-calendar",
        "graduation-cap": "bi bi-mortarboard",
    };
    return iconMap[icon];
};
const toggleAuthMode = () => {
    isSignUp.value = !isSignUp.value;
    resetForm();
};

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const resetForm = () => {
    selectedUserType.value = "";
    showAlternativeTypes.value = false;
    errorMessage.value = '';
    loginData.value = {
        username: "",
        email: "",
        password: "",
    };
    registerData.value = {
        name: "",
        username: "",
        email: "",
        password: "",
        dob: "",
        school: "",
    };
};
const handleUserTypeSelection = (userType: UserType) => {
    selectedUserType.value = userType;
    showAlternativeTypes.value = true;
    errorMessage.value = '';
    loginData.value = {
        username: "",
        email: "",
        password: "",
    };
    registerData.value = {
        name: "",
        username: "",
        email: "",
        password: "",
        dob: "",
        school: "",
    };

};
const updateLoginData = (field: string, value: string) => {
    loginData.value = {
        ...loginData.value,
        [field]: value,
    };
};
const updateRegisterData = (field: string, value: string) => {
    registerData.value = {
        ...registerData.value,
        [field]: value,
    };
};
const validateLoginData = (): boolean => {
    const { username, email, password } = loginData.value;
    switch (selectedUserType.value) {
        case "Parent":
        case "Admin":
            return !!(email && password);
        case "Child":
            return !!(username && password);
        default:
            return false;
    }
};
const validateRegisterData = (): boolean => {
    const { name, username, email, password, dob, school } = registerData.value;
    switch (selectedUserType.value) {
        case "Parent":
            return !!(name && email && password);
        case "Child":
            return !!(name && username && email && password && dob && school);
        default:
            return false;
    }
};

const errorMessage = ref<string>('');
const showError = (message: string) => {
    errorMessage.value = message;

    setTimeout(() => {
        errorMessage.value = '';
    }, 5000);
};

// let base_url = 'http://127.0.0.1:5000/'

// const setCookie = (name: string, value: string, days = 1) => {
//     const expires = new Date();
//     expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
//     document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
// };

import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogin = async () => {
    if (!validateLoginData()) {
        showError("Please fill in all required fields.");
        return;
    }
    const { username, email, password } = loginData.value;
    const identifier = selectedUserType.value === "Child" ? username : email;

    let url = '';
    let payload: Record<string, any> = {};

    if (selectedUserType.value === "Parent") {
        url = base_url + '/auth/parent_login';
        payload = {
            email,
            password,
        };
    } else if (selectedUserType.value === "Child") {
        url = base_url + '/auth/children_login';
        payload = {
            username: username,
            password,
        };
    } else if (selectedUserType.value === "Admin") {
        url = base_url + '/auth/admin_login';
        payload = {
            email: email,
            password,
        };
    } else {
        showError("Invalid user type.");
        return;
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload),
            credentials: 'include'
        });

        const result = await response.json();

        if (!response.ok) {
            showError(`Login failed: ${result.error || "Unknown error"}`);
            return;
        }

        const token = result.session?.token;
        const userId = result.user?.id;

        if (!token || !userId) {
            showError("Invalid response from server");
            return;
        }

        localStorage.setItem("authToken", token);

        switch (selectedUserType.value) {
            case "Admin":
                router.push({ name: 'admin_dashboard' });
                break;
            case "Parent":
                router.push({ name: 'parent_dashboard' });
                break;
            case "Child":
                router.push({ name: 'child_dashboard' });
                break;
            default:
                showError("Unknown user type");
        }
        resetForm();
    } catch (error) {
        console.error("Login Error:", error);
        showError("Something went wrong. Please try again.");
    }

};
const handleRegister = async () => {
    if (!validateRegisterData()) {
        showError(`Please fill all required fields for ${selectedUserType.value}.`);
        return;
    }
    const data = registerData.value;
    // let message = `Registering ${selectedUserType.value}: Name=${data.name}`;
    // if (selectedUserType.value === "Child") {
    //     message += `, Username=${data.username}, Email=${data.email}, DOB=${data.dob}, School=${data.school}`;
    // } else {
    //     message += `, Email=${data.email}`;
    // }

    let url = '';
    let payload = {};

    if (selectedUserType.value === "Parent") {
        url = base_url + '/auth/parent_register';
        payload = {
            name: data.name,
            email: data.email,
            password: data.password,
        };
    } else if (selectedUserType.value === "Child") {
        url = base_url + '/auth/children_register';
        payload = {
            name: data.name,
            email: data.email,
            username: data.username,
            password: data.password,
            dob: data.dob,
            school: data.school,
        };
    } else {
        showError("Invalid user type selected.");
        return;
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (!response.ok) {
            showError(`Error: ${result.error || "Registration failed"}`);
            return;
        }

        if (selectedUserType.value === "Child") {
            loginData.value.username = data.username!;
        } else {
            loginData.value.email = data.email!;
        }
        loginData.value.password = data.password!;

        await handleLogin();
    } catch (error) {
        console.error("Registration Error:", error);
        showError("Something went wrong. Please try again.");
    }

};
</script>

<style scoped>
.body {
    background-color: var(--color-background);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    padding: 0;
}

.container {
    position: relative;
    width: 800px;
    height: 550px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-background);
    overflow: hidden;
    border-radius: 2rem;
    border: 1px solid #e6e6e6;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.forms-container {
    position: absolute;
    width: 150%;
    height: 100%;
    left: -100%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.signin-signup {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem;
}

.sign-in-form,
.sign-up-form {
    position: absolute;
    width: 33%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.sign-in-form {
    right: 0;
}

.sign-up-form {
    left: 0;
}

.title {
    font-size: 2rem;
    color: #333;
    margin: 0;
    text-align: center;
}

.alternative-btn {
    text-align: center;
}

.divider {
    color: #999;
    font-size: 0.9rem;
}

.alternative-title {
    font-size: 1.2rem;
    color: #333;
    margin: 1rem 0;
}

form {
    width: 100%;
    max-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.error {
    color: red;
    font-size: small;
    text-align: center;
    animation: fadeInOut 5s ease forwards;
}

@keyframes fadeInOut {
    0% {
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.title span {
    font-weight: 400;
    color: #666;
}

.form-field {
    position: relative;
    width: 100%;
}

.form-field i {
    position: absolute;
    top: 50%;
    left: 12px;
    color: #acacac;
    transform: translateY(-50%);
    z-index: 1;
}

.eye-toggle-btn {
    border: none;
    border-radius: 0 8px 8px 0;
    background: none;
    position: absolute;
    font-size: medium;
    right: 0;
    cursor: pointer;
    padding: 20px 15px 20px 25px;
}


.form-field input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: none;
    border-radius: 8px;
    background: #f0f0f0;
    outline: none;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.form-field input:focus {
    background: #e8e8e8;
    box-shadow: 0 0 0 2px rgba(239, 71, 111, 0.2);
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

.btn:hover {
    background-color: #ef476f;
    transform: scale(1.01);
}

.btn-primary {
    background: linear-gradient(135deg, #ef476f, #f78fa7);
    color: white;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #d63384, #ef476f);
    box-shadow: 0 4px 12px rgba(239, 71, 111, 0.3);
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
    transform: translateY(-2px);
}

.alternative-btns {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    flex-wrap: wrap;
}

.user-btn-box {
    display: flex;
    flex-direction: column;
    gap: var(--size-sm);
    width: 60%;
}

.btn-box-signup {
    width: 138%;
}

.user-btn {
    width: 100%;
    padding: 0.75rem 1rem;
    background-color: #ef476ec0;
    color: #fff;
}


.btn-transparent {
    background: transparent;
    border: 2px solid #fff;
    color: #fff;
    width: 50%;
    min-width: 120px;
}

.btn-transparent:hover {
    background: #ef476e5a;
    transform: scale(1.02);
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
    right: -100%;
    display: flex;
    align-items: center;
    transition: all 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    background: linear-gradient(135deg, #ef476f, #f78fa7);
}

.slide {
    position: absolute;
    color: #fff;
    padding: 2rem;
    width: 30%;
}

.left-slide {
    left: 0;
}

.right-slide {
    right: 0;
}

.slide-content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.slide-title {
    font-size: 2.5rem;
    margin: 0;
    font-weight: 600;
}

.slide-text {
    font-size: 1rem;
    margin: 0;
    opacity: 0.9;
}

.sign-up-mode .forms-container {
    left: 50%;
}

.sign-up-mode .slider-container {
    right: 50%;
}


@media screen and (min-width: 550px) and (max-width: 799px) {
    .container {
        border-radius: 2rem;
        width: 90%;
    }

    .btn-transparent {
        width: 68%;
        min-width: 150px;
    }

    .title {
        font-size: 1.8rem;
    }

    form {
        width: 90%;
    }

    .slide-title {
        font-size: 2.2rem;
    }
}

@media screen and (min-width: 450px) and (max-width: 550px) {
    .container {
        width: 90%;
        border-radius: 2rem 2rem;
    }

    .btn-transparent {
        width: 145px;
    }

    .right-slide {
        right: 15px;
    }

    .sign-in-form,
    .sign-up-form {
        gap: 0.8rem;
    }

    .form-field input {
        padding: 0.6rem 0.8rem 0.6rem 2.2rem;
    }

    form {
        gap: 0.8rem;
        width: 90%;
    }

    .title {
        font-size: 1.5rem;
    }
}

@media screen and (max-width: 450px) {
    .container {
        width: 90%;
        height: 98vh;
        max-height: 620px;
    }

    .forms-container {
        width: 200%;
        height: 75%;
        bottom: 0;
    }

    .signin-signup {
        width: 90%;
    }

    .sign-in-form,
    .sign-up-form {
        width: 50%;
        gap: 1rem;
    }

    .title {
        font-size: 1.5rem;
    }

    form {
        gap: 0.6rem;
        padding-bottom: 15px;
    }

    .form-field input {
        padding: 0.6rem 0.8rem 0.6rem 2.2rem;
    }

    .slider-container {
        width: 200%;
        height: 25%;
        right: -100%;
        top: 0;
    }

    .left-slide {
        left: 0;
    }

    .right-slide {
        right: 0;
    }

    .slide {
        width: 50%;
        bottom: -25px;
    }

    .slide-content {
        gap: 0.6rem;
    }

    .slide-title {
        font-size: 1.7rem;
    }

    .slide-text {
        font-size: 0.8rem;
    }

    .btn-transparent {
        padding: 10px 10px;
    }

    .sign-up-mode .forms-container {
        left: 0;
    }

    .sign-up-mode .slider-container {
        right: 0;
    }
}
</style>
