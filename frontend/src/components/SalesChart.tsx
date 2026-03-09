"use client";

import { Line, LineChart, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function SalesChart() {
  const data = [
    { month: "Jan", revenue: 32 },
    { month: "Feb", revenue: 45 },
    { month: "Mar", revenue: 43 },
    { month: "Apr", revenue: 60 },
    { month: "May", revenue: 55 },
    { month: "Jun", revenue: 78 }
  ];

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="revenue" stroke="#0f766e" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
