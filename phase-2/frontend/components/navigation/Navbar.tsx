'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { betterAuthClient } from '@/lib/auth/better-auth-client';
import { Button } from '../ui/Button';

export default function Navbar() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = await betterAuthClient.isAuthenticated();
      setIsLoggedIn(authenticated);
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const handleLogout = async () => {
    try {
      await betterAuthClient.logout();
      setIsLoggedIn(false);
      router.push('/');
      router.refresh();
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  if (isLoading) {
    return null; // Don't render navbar while checking auth status
  }

  return (
    <nav className="bg-indigo-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="shrink-0">
              <Link href="/" className="text-white text-xl font-bold">
                Todo App
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  href="/"
                  className="text-white hover:bg-indigo-700 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Home
                </Link>
                {isLoggedIn && (
                  <>
                    <Link
                      href="/dashboard"
                      className="text-white hover:bg-indigo-700 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      Dashboard
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            {isLoggedIn ? (
              <div className="ml-4 flex items-center md:ml-6 space-x-3">
                <Button onClick={handleLogout} variant="outline">
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex space-x-3">
                <Link href="/signin">
                  <Button variant="outline">Sign In</Button>
                </Link>
                <Link href="/signup">
                  <Button>Sign Up</Button>
                </Link>
              </div>
            )}
          </div>
          {/* Mobile menu button */}
          <div className="-mr-2 flex md:hidden">
            <button
              type="button"
              className="bg-indigo-600 inline-flex items-center justify-center p-2 rounded-md text-indigo-200 hover:text-white hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu, show/hide based on menu state */}
      <div className="md:hidden hidden" id="mobile-menu">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            href="/"
            className="text-white hover:bg-indigo-700 block px-3 py-2 rounded-md text-base font-medium"
          >
            Home
          </Link>
          {isLoggedIn && (
            <Link
              href="/dashboard"
              className="text-white hover:bg-indigo-700 block px-3 py-2 rounded-md text-base font-medium"
            >
              Dashboard
            </Link>
          )}
          <div className="mt-2 space-y-2">
            {isLoggedIn ? (
              <Button
                onClick={handleLogout}
                variant="outline"
                className="w-full justify-center"
              >
                Logout
              </Button>
            ) : (
              <>
                <Link href="/signin">
                  <Button variant="outline" className="w-full">
                    Sign In
                  </Button>
                </Link>
                <Link href="/signup">
                  <Button className="w-full">Sign Up</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}