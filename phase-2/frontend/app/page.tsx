import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import Navbar from '@/components/navigation/Navbar';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100 flex flex-col">
      <Navbar />

      <main className="grow flex items-center justify-center p-4">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
              Manage your tasks efficiently
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              A simple and secure todo application to organize your daily tasks
            </p>
          </div>

          <div className="mt-8">
            <Link href="/signup" className="w-full">
              <Button className="w-full">
                Get Started
              </Button>
            </Link>

            <div className="mt-4 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <Link href="/signin" className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign in
              </Link>
            </div>
          </div>
        </div>
      </main>

      <footer className="py-6 text-center text-sm text-gray-500">
        <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
      </footer>
    </div>
  );
}
