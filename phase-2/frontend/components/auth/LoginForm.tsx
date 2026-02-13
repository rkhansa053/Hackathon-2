// LoginForm is essentially a simpler version of AuthForm for just sign in
// We'll just export a specialized version of AuthForm for sign in
import { AuthForm } from './AuthForm';

interface LoginFormProps {
  onSubmit: (credentials: { email: string; password: string }) => void;
  isLoading?: boolean;
  error?: string;
}

export function LoginForm({ onSubmit, isLoading, error }: LoginFormProps) {
  return (
    <AuthForm
      type="signin"
      onSubmit={onSubmit}
      isLoading={isLoading}
      error={error}
    />
  );
}