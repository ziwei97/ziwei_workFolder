import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';


const ExampleThing = ({data}) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        width={500}
        height={400}
        data={data}
        margin={{
          top: 15,
          right: 30,
          left: 15,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="file_count" fill="#3b780c" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default ExampleThing;
