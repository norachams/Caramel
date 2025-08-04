// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';


// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBGlDYpKUHKsd9hHRp7VAaYBbhY-AhlHgk",
  authDomain: "job-tracker-426605.firebaseapp.com",
  projectId: "job-tracker-426605",
  storageBucket: "job-tracker-426605.appspot.com",
  messagingSenderId: "878123970204",
  appId: "1:878123970204:web:313d156728be6a8d12c759",
  measurementId: "G-Z9FPBFB569"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

export { auth, GoogleAuthProvider, signInWithPopup };