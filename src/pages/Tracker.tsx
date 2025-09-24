import React, { useEffect, useState } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../firebase';

// main React component that fetches and displays the classified data on the frontend.

interface Classification {
  email_id: string;
  subject: string; 
  classification: string;
  company: string; 
  confidence?: number | null;
}

const Tracker: React.FC = () => {
  // get the current authenticated user using Firebase authentication
  const [user] = useAuthState(auth);
  // state to store the fetched classifications data
  const [classifications, setClassifications] = useState<Classification[]>([]);
  // state to handle any errors during the fetch process
  const [error, setError] = useState<string | null>(null);
  // state to handle the loading state while data is being fetched
  const [loading, setLoading] = useState<boolean>(true);
  // state to store the last updated timestamp
  const [lastUpdated, setLastUpdated] = useState<string>('');

  useEffect(() => {
    const fetchClassifications = async () => {
      setLoading(true);
      setError(null);

      try {
        
        const apiServer = 'http://127.0.0.1:5050/tracker';
        const response = await fetch(apiServer);

        if (!response.ok) {
          throw new Error(`HTTP Error. Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Fetched Classifications:', data);
        setClassifications(data || []);
        // Set the last updated time
        const now = new Date();
        const formattedDate = now.toLocaleString('en-GB', {
          day: '2-digit',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
        });
        setLastUpdated(formattedDate);
      } catch (error) {
        console.error('Error fetching classifications:', error);
        setError('Error fetching classifications.');
      } finally {
        setLoading(false);
      }
    };

    fetchClassifications();
  }, []);

  return (
    <div className="min-h-screen bg-[#FFFCF7] p-8">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold mb-8">Welcome, {user?.displayName || 'Guest'}</h1>
        <div className="flex flex-col md:flex-row justify-between mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md mb-4 md:mb-0 md:mr-4">
            <h2 className="text-xl font-semibold mb-4">Last Updated:</h2>
            <p className="text-gray-600">{lastUpdated || 'Not updated yet'}</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md md:ml-4 pr-32">
            <h2 className="text-xl font-semibold mb-4">Stats</h2>
            {loading ? (
              <p>Loading classifications...</p>
            ) : error ? (
              <p>Error: {error}</p>
            ) : (
              <>
                <p className="text-blue-600">Submitted: {classifications.filter(c => c.classification === 'Application Received').length}</p>
                <p className="text-red-600">Rejected: {classifications.filter(c => c.classification === 'Rejected').length}</p>
                <p className="text-green-600">Interview: {classifications.filter(c => c.classification === 'Interview').length}</p>
                <p className="text-gray-600">Total: {classifications.length}</p>
              </>
            )}
          </div>
        </div>
        <div className="flex flex-col md:flex-row justify-between">
          <div className="bg-white p-6 rounded-lg shadow-md mb-4 md:mb-0 md:mr-4 flex-1">
            <h2 className="text-xl text-blue-600 font-semibold mb-4">Applications Submitted</h2>
            <div className="space-y-2">
              {classifications.filter(c => c.classification === 'Application Received').map(c => (
                <div key={c.email_id} className="bg-gray-200 rounded-lg py-2 px-4">
                  {c.company || c.subject || 'Unknown company'}
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md mb-4 md:mb-0 md:ml-4 flex-1">
            <h2 className="text-xl text-red-600 font-semibold mb-4">Rejected</h2>
            <div className="space-y-2">
              {classifications.filter(c => c.classification === 'Rejected').map(c => (
                <div key={c.email_id} className="bg-gray-200 rounded-lg py-2 px-4">
                  {c.company || c.subject || 'Unknown company'}
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md md:ml-4 flex-1">
            <h2 className="text-xl text-green-600 font-semibold mb-4">Interview</h2>
            <div className="space-y-2">
              {classifications.filter(c => c.classification === 'Interview').map(c => (
                <div key={c.email_id} className="bg-[#C2D8B9] rounded-lg py-2 px-4">
                  {c.company || c.subject || 'Unknown company'}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tracker;
