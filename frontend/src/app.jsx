import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./auth/authContext";

import Layout from "./layout/layout";
import Home from "./home/home";
import Login from "./login/login";
import Dashboard from "./dashboard/dashboard";
import Barcode from "./barcode/barcode";
import Search from "./search/search";
import LocalRules from "./localRules/localRules";
import History from "./history/history";

function RequireAuth({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default function App() {
  return (
    <Layout>
      <Routes>
        {/* Public Access */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* User-Protected Access */}
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />
        <Route
          path="/features/barcode"
          element={
            <RequireAuth>
              <Barcode />
            </RequireAuth>
          }
        />
        <Route
          path="/features/search"
          element={
            <RequireAuth>
              <Search />
            </RequireAuth>
          }
        />
        <Route
          path="/features/local-rules"
          element={
            <RequireAuth>
              <LocalRules />
            </RequireAuth>
          }
        />
        <Route
          path="/features/history"
          element={
            <RequireAuth>
              <History />
            </RequireAuth>
          }
        />

        {/* Backup */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}