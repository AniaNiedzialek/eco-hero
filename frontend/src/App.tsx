// App.tsx
import { Routes, Route, Link } from "react-router-dom";
import NavBar from "./components/NavBar";
import RulesPage from "./pages/Rules";
import SchedulePage from "./pages/Schedule";
import ScannerPage from "./pages/Scanner";
import BinsPage from "./pages/Bins";

export default function App() {
  return (
    // NOTE: subtle site-wide bg helps every page, not just the hero
    <div className="min-h-dvh flex flex-col bg-gradient-to-b from-white to-eco-50">
      <NavBar />

      {/* main is now flex-1 only; the hero below controls its own height */}
      <main className="flex-1">
        <Routes>
          <Route
            index
            element={
              // ===== Full-bleed hero that fills the viewport =====
              <section className="relative overflow-hidden">
                {/* background gradient for the hero */}
                <div className="absolute inset-0 -z-10 bg-gradient-to-b from-eco-50 via-white to-eco-100" />

                {/* soft decorative blobs (purely visual) */}
                <div className="pointer-events-none absolute -top-24 -left-24 h-80 w-80 rounded-full bg-eco-300/20 blur-3xl" />
                <div className="pointer-events-none absolute -bottom-28 -right-28 h-96 w-96 rounded-full bg-emerald-300/20 blur-3xl" />

                <div className="container">
                  <div
                    className="
                      grid lg:grid-cols-2 gap-10 lg:gap-16 items-center
                      min-h-[85dvh] py-16 lg:py-24
                    "
                  >
                    {/* Left: headline + CTAs */}
                    <div>
                      <h1 className="text-5xl lg:text-6xl font-extrabold text-eco-700 leading-tight">
                        Recycle smarter. <br />
                        Be your neighborhood’s{" "}
                        <span className="text-eco-400 italic">Eco Hero</span>!
                      </h1>

                      <p className="mt-5 text-lg text-slate-600 max-w-prose">
                        Welcome to the EcoHero app! Here you can look up recycling rules, check pickup schedules, scan
                        barcodes, and find nearby bins, all in one place!
                      </p>

                      <div className="mt-8 flex flex-wrap gap-4">
                        <Link to="/bins" className="btn px-6 py-3 text-base border-eco-500 bg-transparent text-eco-700 hover:bg-eco-300">
                          Check rules
                        </Link>
                        <Link to="/bins" className="btn px-6 py-3 text-base border-eco-500 bg-transparent text-eco-700 hover:bg-eco-300">
                          Find bins
                        </Link>
                      </div>

                      {/* Small feature strip to anchor the hero */}
                      <div className="mt-10">
                        <div className="text-sm font-semibold text-eco-600 uppercase">
                        <p>Features</p>
                        </div>
                        </div>

                      <div className="mt-5 grid grid-cols-3 gap-6 max-w-xl text-sm text-slate-700">
                        <div className="rounded-xl bg-white/70 backdrop-blur p-4 shadow-sm">
                          City rules by ZIP
                          <p className="text-slate-500 text-xs mt-1">Check how to recycle locally!</p>
                        </div>
                        <div className="rounded-xl bg-white/70 backdrop-blur p-4 shadow-sm">
                          Barcode scanner
                          <p className="text-slate-500 text-xs mt-1">Browse specific guidance after scanning!</p>
                        </div>
                        <div className="rounded-xl bg-white/70 backdrop-blur p-4 shadow-sm">
                          Pickup reminders
                          <p className="text-slate-500 text-xs mt-1">Set yourself for a success!</p>
                        </div>
                      </div>
                    </div>

                    {/* Right: taller image card */}
                    <div className="rounded-2xl bg-white/70 backdrop-blur p-4 shadow-xl">
                      <img
                        src="https://images.unsplash.com/photo-1528323273322-d81458248d40?q=80&w=1200&auto=format&fit=crop"
                        alt="recycling"
                        className="
                          rounded-xl object-cover
                          aspect-[4/3] w-full
                          lg:aspect-auto lg:h-[32rem]
                        "
                      />
                    </div>
                  </div>
                </div>
              </section>
            }
          />

          {/* Other routes unchanged */}
          <Route path="/rules" element={<RulesPage />} />
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/scanner" element={<ScannerPage />} />
          <Route path="/bins" element={<BinsPage />} />
        </Routes>
      </main>

      <footer className="border-t py-6">
        <div className="container text-sm text-slate-500">
          © {new Date().getFullYear()} Eco Hero 
        </div>
      </footer>
    </div>
  );
}
