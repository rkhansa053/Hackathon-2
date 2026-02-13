import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export function Input({ className = '', error, ...props }: InputProps) {
  const errorClass = error ? 'border-red-500 ring-1 ring-red-500' : '';

  return (
    <div className="relative">
      <input
        {...props}
        className={`appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
          errorClass
        } ${className}`}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}