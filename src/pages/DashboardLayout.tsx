import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { motion } from "framer-motion";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

const SIDEBAR_OPEN = 256; 
const EASE = [0.22, 1, 0.36, 1] as const;

function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen flex bg-[#FBFAF8] ">
      <motion.aside
        className="overflow-hidden border-r border-gray-200 bg-white"
        initial={false}
        animate={{ width: sidebarOpen ? SIDEBAR_OPEN : 0 }}
        transition={{ duration: 0.28, ease: EASE }}
      >
        <div className="w-64 h-full">
          <Sidebar />
        </div>
      </motion.aside>

      <motion.div
        className="flex-1 flex flex-col min-w-0"
        initial={false}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.28, ease: EASE }}
      >
        <Navbar
          onToggleSidebar={() => setSidebarOpen((s) => !s)}
         
        />
        <main className="flex-1 p-6 md:p-8">
          <Outlet />
        </main>
      </motion.div>
    </div>
  );
}

export default DashboardLayout;
