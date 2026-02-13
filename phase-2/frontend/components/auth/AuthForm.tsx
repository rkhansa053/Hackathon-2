'use client';

import React, { useState } from 'react';
import { validateEmail, validatePassword, validateSignupForm, validateSigninForm } from '@/lib/utils/validation';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

interface AuthFormProps {
  type: 'signup' | 'signin';
  onSubmit: (credentials: { email: string; password: string }) => void;
  isLoading?: boolean;
  error?: string;
}

export function AuthForm({ type, onSubmit, isLoading = false, error }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string; confirmPassword?: string }>({});

  const handleSubmit = (e: React.FormEvent) => {
    console.log("handleSubmit called", { type, email, password, confirmPassword });
    e.preventDefault();

    // Validate form
    let formErrors = {};
    if (type === 'signup') {
      // For signup, validate email, password, and confirm password
      const signupValidation = validateSignupForm(email, password);
      const confirmPasswordError = password !== confirmPassword ? 'Passwords do not match' : undefined;

      formErrors = {
        ...signupValidation.errors.reduce((acc, error, index) => ({ ...acc, [index]: error }), {}),
        confirmPassword: confirmPasswordError
      };

      console.log("Signup validation:", signupValidation, confirmPasswordError);

      if (!signupValidation.isValid || confirmPasswordError) {
        console.log("Validation failed:", formErrors);
        setErrors(formErrors as any);
        return;
      }
    } else {
      // For signin, validate email and password
      const signinValidation = validateSigninForm(email, password);
      formErrors = signinValidation.errors.reduce((acc, error, index) => ({ ...acc, [index]: error }), {});

      console.log("Signin validation:", signinValidation);

      if (!signinValidation.isValid) {
        console.log("Signin validation failed:", formErrors);
        setErrors(formErrors as any);
        return;
      }
    }

    // Clear previous errors
    setErrors({});

    console.log("Submitting form with credentials:", { email, password });

    // Submit form
    onSubmit({ email, password });
  };

  const title = type === 'signup' ? 'Create Account' : 'Sign In';
  const buttonText = type === 'signup' ? 'Sign Up' : 'Sign In';
  const toggleText = type === 'signup'
    ? 'Already have an account? Sign in'
    : "Don't have an account? Sign up";

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {title}
          </h2>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <Input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={errors.email}
                aria-label="Email address"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            <div>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={errors.password}
                aria-label="Password"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {type === 'signup' && (
              <div>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="current-password"
                  required
                  placeholder="Confirm Password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  error={errors.confirmPassword}
                  aria-label="Confirm Password"
                />
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
                )}
              </div>
            )}
          </div>

          <div>
            <Button
              type="submit"
              className="w-full"
              loading={isLoading}
              disabled={isLoading}
            >
              {buttonText}
            </Button>
          </div>

          <div className="text-center text-sm text-gray-600">
            {toggleText}
          </div>
        </form>
      </div>
    </div>
  );
}