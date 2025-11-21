import { Leaf, LogIn, LogOut, MapPin, ScanBarcode, Calendar, BookOpen } from "lucide-react";
import { Link, NavLink } from "react-router-dom";
import { auth, google } from "../lib/firebase";
import { signInWithPopup, signOut, onAuthStateChanged } from "firebase/auth";
import type { User } from "firebase/auth";
import React from "react";

export default function NavBar() {
  const [user, setUser] = React.useState<User | null>(auth.currentUser);
  React.useEffect(() => onAuthStateChanged(auth, setUser), []);

  const link = "flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-eco-100 transition";
  const active = "bg-eco-100 text-eco-800";

  return (
    <header className="border-b bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/50">
      <div className="container flex items-center justify-between py-3">
        <Link to="/" className="flex items-center gap-2 font-semibold text-eco-700">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-eco-600 text-white">
            <Leaf className="h-5 w-5" />
          </span>
          <span className="text-xl">Eco Hero</span>
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          <NavLink to="/rules" className={({isActive}) => `${link} ${isActive?active:""}`}><BookOpen className="h-4 w-4"/>Rules</NavLink>
          <NavLink to="/schedule" className={({isActive}) => `${link} ${isActive?active:""}`}><Calendar className="h-4 w-4"/>Schedule</NavLink>
          <NavLink to="/scanner" className={({isActive}) => `${link} ${isActive?active:""}`}><ScanBarcode className="h-4 w-4"/>Scanner</NavLink>
          <NavLink to="/bins" className={({isActive}) => `${link} ${isActive?active:""}`}><MapPin className="h-4 w-4"/>Nearby bins</NavLink>
          {user && (
            <NavLink to="/history" className={({isActive}) => `${link} ${isActive?active:""}`}>History</NavLink>
          )}
        </nav>
        <div className="flex items-center gap-2">
          {!user ? (
            <button className="btn" onClick={() => signInWithPopup(auth, google)}>
              <LogIn className="h-4 w-4"/> Sign in
            </button>
          ) : (
            <button className="btn" onClick={() => signOut(auth)}>
              <LogOut className="h-4 w-4"/> Sign out
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
