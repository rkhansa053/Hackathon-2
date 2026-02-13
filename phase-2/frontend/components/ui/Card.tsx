import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className = '', children, ...props }: CardProps) {
  return (
    <div
      {...props}
      className={`bg-white overflow-hidden shadow rounded-lg ${className}`}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardHeader({ className = '', children, ...props }: CardHeaderProps) {
  return (
    <div {...props} className={`px-4 py-5 sm:px-6 ${className}`}>
      {children}
    </div>
  );
}

interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardBody({ className = '', children, ...props }: CardBodyProps) {
  return (
    <div {...props} className={`px-4 py-5 sm:p-6 ${className}`}>
      {children}
    </div>
  );
}

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardFooter({ className = '', children, ...props }: CardFooterProps) {
  return (
    <div {...props} className={`bg-gray-50 px-4 py-4 sm:px-6 ${className}`}>
      {children}
    </div>
  );
}