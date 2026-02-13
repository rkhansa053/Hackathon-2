export interface User {
  id: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuthUser extends User {
  token: string;
}