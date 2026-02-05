import { useEffect, useState } from 'react';
import { SensorReading, Alert } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertTriangle, Droplets, Activity, Thermometer } from 'lucide-react';

export default function Dashboard() {
    const [readings, setReadings] = useState<SensorReading[]>([]);
    const [alerts, setAlerts] = useState<Alert[]>([]);

    const fetchData = async () => {
        try {
            // Direct API call - in production use Axios instance with Base URL
            const r = await fetch('http://localhost:8000/api/v1/sensors/?limit=50');
            const data = await r.json();
            setReadings(data.reverse()); // Show chronological

            const a = await fetch('http://localhost:8000/api/v1/alerts/');
            const alertData = await a.json();
            setAlerts(alertData);
        } catch (e) {
            console.error("Failed to fetch data", e);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, []);

    const latest = readings[readings.length - 1];

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <header className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">Water Quality Surveillance</h1>
                    <p className="text-slate-500">Real-time IoT Monitoring & Outbreak Prediction</p>
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm border border-slate-200">
                    <span className="text-sm text-slate-500 block">System Status</span>
                    <span className="flex items-center gap-2 text-green-600 font-semibold">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        Online
                    </span>
                </div>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <StatCard
                    title="Avg pH"
                    value={latest?.ph.toFixed(2) || "--"}
                    unit="pH"
                    icon={<Droplets size={20} className="text-blue-500" />}
                />
                <StatCard
                    title="Turbidity"
                    value={latest?.turbidity.toFixed(1) || "--"}
                    unit="NTU"
                    icon={<Activity size={20} className="text-amber-500" />}
                />
                <StatCard
                    title="Temperature"
                    value={latest?.temperature.toFixed(1) || "--"}
                    unit="°C"
                    icon={<Thermometer size={20} className="text-red-500" />}
                />
                <StatCard
                    title="Active Alerts"
                    value={alerts.length.toString()}
                    unit="High Risk"
                    icon={<AlertTriangle size={20} className="text-red-600" />}
                    color="bg-red-50"
                />
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Charts Section */}
                <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h2 className="text-lg font-semibold mb-4">Real-time Trends (pH & Turbidity)</h2>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={readings}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                                <XAxis dataKey="timestamp" tick={false} />
                                <YAxis yAxisId="left" domain={[0, 14]} />
                                <YAxis yAxisId="right" orientation="right" />
                                <Tooltip />
                                <Legend />
                                <Line yAxisId="left" type="monotone" dataKey="ph" stroke="#3b82f6" dot={false} strokeWidth={2} />
                                <Line yAxisId="right" type="monotone" dataKey="turbidity" stroke="#f59e0b" dot={false} strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Alerts Feed */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h2 className="text-lg font-semibold mb-4">Latest Alerts</h2>
                    <div className="space-y-4 max-h-[400px] overflow-auto">
                        {alerts.length === 0 ? (
                            <p className="text-slate-400 text-sm text-center py-10">No active alerts detected.</p>
                        ) : (
                            alerts.map((alert, idx) => (
                                <div key={idx} className="p-3 bg-red-50 border-l-4 border-red-500 rounded-r">
                                    <div className="flex justify-between">
                                        <span className="font-bold text-red-700">{alert.severity}</span>
                                        <span className="text-xs text-red-400">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                                    </div>
                                    <p className="text-sm text-slate-700 mt-1">{alert.message}</p>
                                    <div className="mt-2 text-xs font-mono bg-white/50 p-1 rounded inline-block">
                                        Risk Score: {alert.risk_score.toFixed(1)}%
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
}

const StatCard = ({ title, value, unit, icon, color = "bg-white" }: any) => (
    <div className={`${color} p-4 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4`}>
        <div className="p-3 bg-slate-100 rounded-lg">
            {icon}
        </div>
        <div>
            <p className="text-sm text-slate-500">{title}</p>
            <p className="text-2xl font-bold">{value} <span className="text-xs text-slate-400 font-normal">{unit}</span></p>
        </div>
    </div>
);
