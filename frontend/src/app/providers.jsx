import { useState, useEffect, createContext } from "react";
import {
  getCurrentUser,
  loginUser,
} from "../features/auth/services/authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      return currentUser;
    } catch (err) {
      setUser(null);
      return null;
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      await refreshUser();
      setLoading(false);
    };
    initializeAuth();
  }, []);

  const login = async (credentials) => {
    await loginUser(credentials);
    await refreshUser();
  };

  const logout = async () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}
