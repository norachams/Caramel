// import React from 'react';
// import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
// import { useNavigate } from 'react-router-dom';
// import { auth } from '../firebase'; 
// import { signInWithCredential, GoogleAuthProvider } from 'firebase/auth';

// const Login: React.FC = () => {
//   const navigate = useNavigate();

//   const responseMessage = async (response: CredentialResponse) => {
//     if (response.credential) {
//       const credential = GoogleAuthProvider.credential(response.credential);
//       try {
//         await signInWithCredential(auth, credential);
//         navigate('/tracker');
//       } catch (error) {
//         console.error('Firebase sign-in failed:', error);
//       }
//     } else {
//       console.error('Google credential is missing');
//     }
//   };

//   const errorMessage = () => {
//     console.error('Google Login Failed');
//   };

//   return (
//     <div className="min-h-screen flex flex-col items-center bg-gray-400">
//       <h2 className="text-5xl font-semibold mt-12 mb-20 text-center leading-tight">
//         Automatically track your job applications
//       </h2>
//       <div className="flex flex-col justify-center items-center w-1/2 bg-white p-10 rounded-lg shadow-lg">
//         <h2 className='text-2xl font-semibold'>
//           Log In With Google
//         </h2>
//         <p className="text-gray-600 text-center mb-12">
//           Keep all your job applications organized and accessible in one place.
//         </p>
//         <div className="flex justify-center mb-8 scale-150">
//           <GoogleLogin onSuccess={responseMessage} onError={errorMessage} />
//         </div>
//         <p className="text-center text-gray-500 mt-4">
//           By signing in, you agree to our <a href="#" className="text-blue-500">Terms of Service</a> and <a href="#" className="text-blue-500">Privacy Policy</a>.
//         </p>
//       </div>
//     </div>
//   );
// };

// export default Login;

// src/components/Login.tsx
import React from 'react';
import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase'; 
import { signInWithCredential, GoogleAuthProvider } from 'firebase/auth';


const Login: React.FC = () => {
  const navigate = useNavigate();

  const responseMessage = async (response: CredentialResponse) => {
    if (response.credential) {
      const credential = GoogleAuthProvider.credential(response.credential);
      try {
        await signInWithCredential(auth, credential);
        navigate('/tracker');
      } catch (error) {
        console.error('Firebase sign-in failed:', error);
      }
    } else {
      console.error('Google credential is missing');
    }
  };

  const errorMessage = () => {
    console.error('Google Login Failed');
  };

  return (
    <div className="flex min-h-screen">
      {/* Left half (desktop) */}
      <div className="hidden md:flex w-1/2 bg-[#738290] justify-center items-center">
        <div className="text-white text-center px-8 space-y-4">
          {/* Placeholder logo */}
          <div>
            <img src="/logo.png" alt="Your Logo" className="h-12 mx-auto"/>
          </div>
          <h1 className="text-4xl font-bold">JobJourney</h1>
          <p className="text-lg">Automatically track your job applications</p>
        </div>
      </div>

      {/* Right half (form) */}
      <div className="flex flex-1 bg-[#FFFCF7] justify-center items-center p-8">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-10 space-y-6">
          {/* Logo again (mobile) */}
          <div className="md:hidden flex justify-center">
            <img src="/logo-placeholder.png" alt="Your Logo" className="h-10"/>
          </div>

          <h2 className="text-2xl font-semibold text-[#738290] text-center">
            Welcome Back!
          </h2>
          <p className="text-center text-gray-500">
            Log in to continue your journey
          </p>

          <div className="flex justify-center">
            <GoogleLogin
              onSuccess={responseMessage}
              onError={errorMessage}
              useOneTap
            />
          </div>

          <p className="text-center text-sm text-gray-400">
            By signing in, you agree to our{' '}
            <a href="#" className="text-[#A1B5D8] hover:underline">Terms of Service</a>{' '}
            and{' '}
            <a href="#" className="text-[#A1B5D8] hover:underline">Privacy Policy</a>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
