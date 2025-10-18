import { useEffect, useMemo, useState } from "react";
import { Calendar, MoreVertical } from "lucide-react";

type ApiItem = {
  id: string;
  company: string;
  date: string;            
  predicted_label: string; 
  role?: string;
};

type Status = "submitted" | "interview" | "oa" | "rejected";

const LABEL_MAP: Record<string, Status> = {
  applied: "submitted",
  submitted: "submitted",
    "application received": "submitted",
  interview: "interview",
  oa: "oa",
  "online assessment": "oa",
  rejected: "rejected",
};

const API_BASE = process.env.REACT_APP_API_URL ?? "http://localhost:5050";

function toStatus(label?: string): Status | null {
  if (!label) return null;
  return LABEL_MAP[label.toLowerCase()] ?? null;
}

function Badge({ status }: { status: Status }) {
  const style: Record<Status, string> = {
    submitted: "bg-blue-100 text-blue-700",
    interview: "bg-emerald-100 text-emerald-700",
    oa: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    rejected: "bg-rose-100 text-rose-700",
  };
  const text: Record<Status, string> = {
    submitted: "Submitted",
    interview: "Interview",
    oa: "OA",
    rejected: "Rejected",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 text-xs font-medium rounded-md ${style[status]}`}>
      {text[status]}
    </span>
  );
}

function Card({ item, status }: { item: ApiItem; status: Status }) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-[#fbf8fb] p-4 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-[15px] font-semibold text-gray-800">{item.company || "Unknown"}</h3>
          <p className="text-sm text-gray-500">{item.role ?? "—"}</p>
        </div>
        <button className="p-1 rounded-md text-gray-500 hover:bg-gray-100">
          <MoreVertical size={16} />
        </button>
      </div>

      <div className="mt-4 flex items-center gap-2 text-sm text-gray-600">
        <Calendar size={16} className="shrink-0" />
        <span>{item.date}</span>
      </div>

      <div className="mt-3">
        <Badge status={status} />
      </div>
    </div>
  );
}

function Column({
  title,
  dotColor,
  items,
  leftBorder = false,
}: {
  title: string;
  dotColor: string;
  items: ApiItem[];
  leftBorder?: boolean;
}) {
  return (
    <div className={`space-y-4 ${leftBorder ? "md:border-l md:border-gray-200 md:pl-6" : ""}`}>
      {/* column header */}
      <div className="flex items-center gap-2">
        <span className={`inline-block h-2.5 w-2.5 rounded-full ${dotColor}`} />
        <h2 className="text-[15px] font-semibold text-[#654236]">
          {title} <span className="text-[#826751] font-normal">({items.length})</span>
        </h2>
      </div>

      {/* content */}
      {items.length === 0 ? (
        <div className="rounded-2xl border-2 border-dashed border-[#e5d9d1] text-[#826751] flex items-center justify-center h-40">
          No applications yet
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((it) => {
            const s = toStatus(it.predicted_label) ?? "submitted";
            return <Card key={it.id} item={it} status={s} />;
          })}
        </div>
      )}
    </div>
  );
}


export default function Tracker() {
  const [data, setData] = useState<ApiItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const r = await fetch(`${API_BASE}/tracker`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const json = await r.json();
        if (alive) setData(Array.isArray(json) ? json : []);
      } catch (e: any) {
        if (alive) setError(e?.message ?? "Failed to load");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const { submitted, interviewAndOA, rejected } = useMemo(() => {
    const submitted: ApiItem[] = [];
    const interviewAndOA: ApiItem[] = [];
    const rejected: ApiItem[] = [];
    for (const it of data) {
      const s = toStatus(it.predicted_label);
      if (s === "submitted") submitted.push(it);
      else if (s === "interview" || s === "oa") interviewAndOA.push(it);
      else if (s === "rejected") rejected.push(it);
    }
    return { submitted, interviewAndOA, rejected };
  }, [data]);


  return (
    <div className="w-full">
      {/* header always visible */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div>
            <h1 className="text-2xl font-semibold text-[#654236]">Job Tracker</h1>
            <p className="text-[#826751]">Track and manage your job applications</p>
          </div>
          {loading && <span className="text-sm text-gray-400">Loading…</span>}
          
        </div>
        <button className="inline-flex items-center gap-2 rounded-lg bg-[#DA7635] px-4 py-2 text-white hover:opacity-90">
          <span className="text-lg leading-none">＋</span> Add Application
        </button>
      </div>

      {/* columns always visible (with thin separators); cards render only if items exist) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <Column title="Submitted Applications" dotColor="bg-blue-500" items={submitted} />
        <Column title="Interviews & OA" dotColor="bg-emerald-500" items={interviewAndOA} leftBorder />
        <Column title="Rejected" dotColor="bg-rose-500" items={rejected} leftBorder />
      </div>
    </div>
  );
}
