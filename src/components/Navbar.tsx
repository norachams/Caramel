import { PanelLeft } from "lucide-react";

type NavbarProps = {
  onToggleSidebar: () => void;
};

function Navbar({ onToggleSidebar }: NavbarProps) {
  return (
    <header className="flex items-center justify-between px-4 md:px-6 py-3 border-b border-gray-200 bg-white">
      <button
        onClick={onToggleSidebar}
        className="p-2 rounded-md hover:bg-gray-100"
        aria-label="Toggle sidebar"
      >
        <PanelLeft size={18} className="text-[#654236]" />
      </button>
      <div />
    </header>
  );
}

export default Navbar;
