import React, { useState } from 'react';
import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase'; 
import { signInWithCredential, GoogleAuthProvider } from 'firebase/auth';


const Login: React.FC = () => {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  const responseMessage = async (response: CredentialResponse) => {
    if (response.credential) {
      try {
        setSubmitting(true);
        const credential = GoogleAuthProvider.credential(response.credential);
        await signInWithCredential(auth, credential);
        navigate('/tracker');
      } catch (error) {
        console.error('Firebase sign-in failed:', error);
      } finally {
        setSubmitting(false);
      }
    } else {
      console.error('Google credential is missing');
    }
  };

  const errorMessage = () => {
    console.error('Google Login Failed');
  };

  return (
    <div className="min-h-screen w-full grid grid-cols-1 md:grid-cols-2">
      <section className="relative hidden md:flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#F5E0CF] via-[#EAC5A9] to-[#DFA880]" />
        <div className="relative max-w-xl px-10">
          <div className="flex items-center justify-center md:justify-start mb-6">
             <div className="p-2 rounded-lg">
            <img src="/newlogo.png" alt="Your Logo" className="h-12 mx-auto"/>
        </div>
            <h1 className="text-5xl font-semibold text-[#654236]">Caramel</h1>
          </div>

          <p className="text-[#654236]/80 text-lg md:text-xl mb-10">
            Your sweet companion for job hunting success 
          </p>

          {/* feature bullets */}
          <ul className="space-y-6 text-[#654236]">
            <li className="flex items-center gap-4">
              <span className="grid h-10 w-10 place-items-center rounded-full bg-white/70">
                {/* calendar */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="4" width="18" height="18" rx="3" stroke="#1f1f1f" strokeWidth="1.6"/>
                  <path d="M16 2v4M8 2v4M3 10h18" stroke="#1f1f1f" strokeWidth="1.6" strokeLinecap="round"/>
                </svg>
              </span>
              <span className="text-[15px]">Track applications effortlessly</span>
            </li>
            <li className="flex items-center gap-4">
              <span className="grid h-10 w-10 place-items-center rounded-full bg-white/70">
                {/* clock icon */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="9" stroke="#1f1f1f" strokeWidth="1.6"/>
                  <path d="M12 7v5l3 2" stroke="#1f1f1f" strokeWidth="1.6" strokeLinecap="round"/>
                </svg>
              </span>
              <span className="text-[15px]">Never miss an interview</span>
            </li>
            <li className="flex items-center gap-4">
              <span className="grid h-10 w-10 place-items-center rounded-full bg-white/70">
                {/* lightning icon */}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="#1f1f1f">
                  <path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/>
                </svg>
              </span>
              <span className="text-[15px]">Land your dream job faster</span>
            </li>
          </ul>
        </div>
      </section>

      {/* Right: sign-in stack */}
      <section className="flex items-center justify-center bg-white">
        <div className="w-full max-w-md px-6 py-12">
          <h2 className="text-3xl font-semibold text-center text-[#654236]">Welcome back</h2>
          <p className="mt-2 text-center text-[#826751]">
            Sign in to continue your job search journey 
          </p>

          {/* Google button */}
          <div className={`w-full mt-6 flex justify-center ${submitting ? 'opacity-60 pointer-events-none' : ''}`}>
            <GoogleLogin
              onSuccess={responseMessage}
              onError={errorMessage}
              useOneTap
              theme="outline"
              size="large"
              text="continue_with"
              shape="rectangular"
              logo_alignment="left"
              width="100%"  
            />
          </div>

          {/* divider */}
          <div className="my-6 flex items-center gap-4">
            <div className="h-px flex-1 bg-gray-200" />
            <span className="text-xs text-[#826751]">Or continue with email</span>
            <div className="h-px flex-1 bg-gray-200" />
          </div>

          {/* email / password placeholders only google works for now */}
          <div className="space-y-4">
            <input
              type="email"
              placeholder="Email address"
              className="w-full rounded-lg border border-gray-200 px-4 py-2.5 text-[15px] outline-none focus:border-gray-300"
              disabled
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full rounded-lg border border-gray-200 px-4 py-2.5 text-[15px] outline-none focus:border-gray-300"
              disabled
            />
            <div className="flex items-center justify-between text-sm">
              <label className="inline-flex items-center gap-2 text-[#826751]">
                <input type="checkbox" className="h-4 w-4 rounded border-gray-300" disabled />
                Remember me
              </label>
              <button type="button" className="text-[#DA7635] hover:underline" disabled>
                Forgot password?
              </button>
            </div>
            <button
              type="button"
              className="w-full rounded-lg bg-[#DA7635] text-white py-2.5 font-medium cursor-not-allowed opacity-80"
              title="Use Google above to sign in"
              disabled
            >
              Sign in
            </button>
          </div>

          <p className="mt-6 text-center text-sm text-[#826751]">
            Don&apos;t have an account?{' '}
            <span className="text-[#DA7635] hover:underline cursor-not-allowed" title="Use Google above">
              Sign up for free
            </span>
          </p>

         
        </div>
      </section>
    </div>
  );
};

export default Login;
