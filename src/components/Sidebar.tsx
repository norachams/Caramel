import { Briefcase, ListChecks, Mail, Target, FileText, Coffee, GraduationCap } from "lucide-react";

const navItems = [
  { name: "Job Tracker", icon: <Briefcase size={18} />, active: true },
  { name: "To-Do List", icon: <ListChecks size={18} /> },
  { name: "Cold Emailing", icon: <Mail size={18} /> },
  { name: "Dream Job", icon: <Target size={18} /> },
  { name: "Written Apps", icon: <FileText size={18} /> },
  { name: "Coffee Chats", icon: <Coffee size={18} /> },
  { name: "Interview Prep", icon: <GraduationCap size={18} /> },
];

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 h-screen bg-[#FBFAF8] border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="flex items-center gap-2 p-6">
        <div className="bg-[#EB7C36] p-2 rounded-lg">
          <Briefcase size={20} color="white" />
        </div>
        <h1 className="text-lg font-semibold text-gray-800">Caramel</h1>
      </div>

      {/* Section title */}
      <p className="text-xs font-medium text-gray-500 px-6 mb-2">Job Hunt Tools</p>

      {/* Nav links */}
      <nav className="flex flex-col">
        {navItems.map((item) => (
          <button
            key={item.name}
            className={`flex items-center gap-3 px-6 py-2 text-sm text-gray-800 hover:bg-gray-100 transition rounded-md ${
              item.active ? "bg-gray-100 font-medium" : ""
            }`}
          >
            {item.icon}
            <span>{item.name}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
