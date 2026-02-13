'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AuthForm } from '@/components/auth/AuthForm';
import { authApi } from '@/lib/api/auth';
import { Button } from '@/components/ui/Button';

export default function SignupPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSignup = async (credentials: { email: string; password: string }) => {
    console.log("handleSignup called", credentials);
    setIsLoading(true);
    setError(null);

    try {
      const response = await authApi.signup(credentials);

      if (response.success && (response.token || response.access_token)) {
        // Store the token (prefer access_token from backend API)
        const token = response.access_token || response.token;
        if (token) {
          await authApi.setAuthToken(token);
        }

        // Extract user ID from the response if available
        // The backend register endpoint should return user data including the ID
        if (response.id) {
          localStorage.setItem('user_id', response.id);
        } else if (response.user && response.user.id) {
          localStorage.setItem('user_id', response.user.id);
        } else if (response.access_token) {
          // Extract user ID from the JWT token (in the 'sub' field)
          try {
            const tokenPayload = response.access_token.split('.')[1];
            const decodedPayload = atob(tokenPayload);
            const parsedPayload = JSON.parse(decodedPayload);
            if (parsedPayload.sub) {
              localStorage.setItem('user_id', parsedPayload.sub);
            }
          } catch (error) {
            console.error('Error decoding JWT token:', error);
          }
        }

        // Redirect to dashboard
        router.push('/dashboard');
        router.refresh(); // Refresh to update the UI context
      } else {
        setError(response.error || 'Failed to create account. Please try again.');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during signup');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">Todo App</h1>
          <Link href="/">
            <Button variant="outline">Home</Button>
          </Link>
        </div>
      </header>

      <main className="grow flex items-center justify-center p-4">
        <AuthForm
          type="signup"
          onSubmit={handleSignup}
          isLoading={isLoading}
          error={error ?? undefined}
        />
      </main>

      <footer className="py-6 text-center text-sm text-gray-500">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}