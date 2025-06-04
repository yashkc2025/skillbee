<script setup lang="ts">
import { ref, computed } from "vue";

// Types
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
}

// Reactive state
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

// Computed properties
const signInUserTypes = computed(() => ["Admin", "Parent", "Child"]);
const signUpUserTypes = computed(() => ["Parent", "Child"]);

const alternativeUserTypes = computed(() => {
  const allTypes = ["Admin", "Parent", "Child"];
  return allTypes.filter((type) => type !== selectedUserType.value);
});

const loginFormFields = computed((): FormField[] => {
  const fields: FormField[] = [];

  if (selectedUserType.value === "Child" || selectedUserType.value === "Admin") {
    fields.push({
      name: "username",
      type: "text",
      placeholder: "Username",
      icon: "user",
      required: true,
    });
  }

  if (selectedUserType.value === "Parent") {
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
      icon: "user",
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

// Methods
const getIconClass = (icon: string): string => {
  const iconMap: Record<string, string> = {
    user: "fas fa-user",
    envelope: "fas fa-envelope",
    lock: "fas fa-lock",
    calendar: "fas fa-calendar",
    "graduation-cap": "fas fa-graduation-cap",
  };
  return iconMap[icon] || "fas fa-user";
};

const toggleAuthMode = () => {
  isSignUp.value = !isSignUp.value;
  resetForm();
};

const resetForm = () => {
  selectedUserType.value = "";
  showAlternativeTypes.value = false;

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
      return !!(email && password);
    case "Child":
    case "Admin":
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

const handleLogin = () => {
  if (!validateLoginData()) {
    alert("Please fill in all required fields.");
    return;
  }

  const { username, email } = loginData.value;
  const identifier = selectedUserType.value === "Parent" ? email : username;

  alert(`Logging in ${selectedUserType.value}: ${identifier}`);
  // Here you would typically make an API call for authentication
};

const handleRegister = () => {
  if (!validateRegisterData()) {
    alert(`Please fill all required fields for ${selectedUserType.value}.`);
    return;
  }

  const data = registerData.value;
  let message = `Registering ${selectedUserType.value}: Name=${data.name}`;

  if (selectedUserType.value === "Child") {
    message += `, Username=${data.username}, Email=${data.email}, DOB=${data.dob}, School=${data.school}`;
  } else {
    message += `, Email=${data.email}`;
  }

  alert(message);
  // Here you would typically make an API call for registration
};
</script>

<template>
  <div class="auth-wrapper">
    <div class="auth-container" :class="{ 'sign-up-mode': isSignUp }">
      <!-- Forms Section -->
      <div class="forms-container">
        <div class="form-content">
          <!-- Sign In Form -->
          <div v-if="!isSignUp" class="auth-form">
            <h2 class="form-title">
              Select a user to login
              <span v-if="selectedUserType">as {{ selectedUserType }}</span>
            </h2>

            <!-- User Type Selection -->
            <div v-if="!selectedUserType" class="user-type-selector">
              <button v-for="userType in signInUserTypes" :key="userType" class="btn user-type-btn"
                @click="handleUserTypeSelection(userType)">
                {{ userType === "Child" ? "Independent Child" : userType }}
              </button>
            </div>

            <!-- Login Form -->
            <form v-if="selectedUserType" @submit.prevent="handleLogin" class="user-form">
              <div v-for="field in loginFormFields" :key="field.name" class="form-field">
                <i :class="getIconClass(field.icon)"></i>
                <input :type="field.type" :placeholder="field.placeholder" :value="loginData[field.name]"
                  :required="field.required" @input="updateLoginData(field.name, $event.target.value)" />
              </div>

              <button class="btn btn-primary" type="submit">Login</button>
            </form>

            <!-- Alternative User Types -->
            <div v-if="selectedUserType && showAlternativeTypes" class="alternative-types">
              <p class="divider">
                --------------------------------- &nbsp; or &nbsp;
                ---------------------------------
              </p>
              <h3 class="alternative-title">Sign in as</h3>
              <div class="alternative-buttons">
                <button v-for="userType in alternativeUserTypes" :key="userType" class="btn btn-secondary"
                  @click="handleUserTypeSelection(userType)">
                  {{ userType === "Child" ? "Independent Child" : userType }}
                </button>
              </div>
            </div>
          </div>

          <!-- Sign Up Form -->
          <div v-else class="auth-form">
            <h2 class="form-title">
              Sign up
              <span v-if="selectedUserType">as {{ selectedUserType }}</span>
            </h2>

            <!-- User Type Selection -->
            <div v-if="!selectedUserType" class="user-type-selector">
              <button v-for="userType in signUpUserTypes" :key="userType" class="btn user-type-btn"
                @click="handleUserTypeSelection(userType)">
                {{ userType === "Child" ? "Independent Child" : userType }}
              </button>
            </div>

            <!-- Register Form -->
            <form v-if="selectedUserType" @submit.prevent="handleRegister" class="user-form">
              <div v-for="field in registerFormFields" :key="field.name" class="form-field">
                <i :class="getIconClass(field.icon)"></i>
                <input :type="field.type" :placeholder="field.placeholder" :value="registerData[field.name]"
                  :required="field.required" @input="updateRegisterData(field.name, $event.target.value)" />
              </div>

              <button class="btn btn-primary" type="submit">Register</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Slider Section -->
      <div class="slider-container">
        <div class="slide" :class="isSignUp ? 'slide-right' : 'slide-left'">
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

<style scoped>
h2 {
  font-family: "VAGRoundedNext", sans-serif;
  font-weight: 700;
}

/* Base Styles */
.auth-wrapper {
  background-color: var(--color-background);
  min-height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-container {
  width: 60%;
  min-height: 80vh;
  background-color: var(--color-background);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 2rem;
  border: 1px solid #e6e6e6;
  box-shadow: 0 8px 32px #e6e6e6;
  position: relative;
}

/* Forms Container */
.forms-container {
  position: absolute;
  width: 50%;
  height: 100%;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.form-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

/* Auth Form */
.auth-form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.form-title {
  font-size: 2rem;
  color: #333;
  margin: 0;
  text-align: center;
}

.form-title span {
  font-weight: 400;
  color: #666;
}

/* User Type Selector */
.user-type-selector {
  display: flex;
  flex-direction: column;
  gap: var(--size-sm);
  width: 100%;
  max-width: 300px;
}

.user-type-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: #ef476ec0;
  color: #fff;
}

/* Form */
.user-form {
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Form Field */
.form-field {
  position: relative;
  width: 100%;
}

.form-field i {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  color: #acacac;
  z-index: 1;
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

/* Buttons */
.btn {
  border: none;
  outline: none;
  border-radius: var(--border-radius);
  padding: var(--size-xs);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  text-transform: capitalize;
}

.btn-primary {
  background: linear-gradient(135deg, #ef476f, #f78fa7);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #d63384, #ef476f);
  transform: translateY(-2px);
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

.btn-transparent {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.btn-transparent:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}

.user-type-btn:hover {
  background-color: #ef476f;
  transform: scale(1.01);
}

/* Alternative Types */
.alternative-types {
  width: 100%;
  max-width: 400px;
  margin-top: 2rem;
  text-align: center;
}

.divider {
  margin: 1rem 0;
  color: #999;
  font-size: 0.9rem;
}

.alternative-title {
  font-size: 1.2rem;
  color: #333;
  margin: 1rem 0;
}

.alternative-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Slider */
.slider-container {
  position: absolute;
  width: 150%;
  height: 100%;
  top: 0;
  right: -100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: linear-gradient(135deg, #ef476f, #f78fa7);
  overflow: hidden;
}

.slide {
  position: absolute;
  color: white;
  text-align: center;
  padding: 2rem;
  width: 300px;
}

.slide-left {
  left: 10%;
}

.slide-right {
  right: 10%;
}

.slide-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.slide-title {
  font-size: 2.5rem;
  margin: 0;
  font-weight: 300;
}

.slide-text {
  font-size: 1rem;
  margin: 0;
  opacity: 0.9;
}

/* Sign Up Mode */
.sign-up-mode .forms-container {
  left: 50%;
}

.sign-up-mode .slider-container {
  right: 50%;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .auth-container {
    width: 80%;
  }
}

@media (max-width: 768px) {
  .auth-container {
    width: 95%;
    min-height: 90vh;
    flex-direction: column;
  }

  .forms-container {
    position: relative;
    width: 100%;
    height: auto;
    left: 0;
  }

  .slider-container {
    position: relative;
    width: 100%;
    height: 200px;
    right: 0;
    background: linear-gradient(45deg, #ef476f, #f78fa7);
  }

  .slide {
    position: relative;
    left: auto;
    right: auto;
  }

  .sign-up-mode .forms-container {
    left: 0;
  }

  .sign-up-mode .slider-container {
    right: 0;
  }
}

@media (max-width: 480px) {
  .auth-container {
    width: 100%;
    min-height: 100vh;
    border-radius: 0;
  }

  .form-content {
    padding: 1rem;
  }

  .slide-title {
    font-size: 2rem;
  }
}
</style>
