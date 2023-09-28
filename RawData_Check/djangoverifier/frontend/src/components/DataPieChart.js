import React, { useState } from 'react';
import { PieChart, Pie, Sector, ResponsiveContainer } from 'recharts';

// const data = [
//   { name: 'Patient_207-001', total_img: 96, Raw_MSI: 80, Pseudocolor_generation_intermediate_output: 4, Pseudocolor: 4 },
//   { name: 'Patient_207-005', total_img: 286, Raw_MSI: 240, Pseudocolor_generation_intermediate_output: 12, Pseudocolor: 12 },
// ];

const DataPieChart = ({ data }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  const onPieEnter = (_, index) => {
    setActiveIndex(index);
  };

  const renderActiveShape = (props) => {
    const RADIAN = Math.PI / 180;
    const { cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent, total_img } = props;
    const sin = Math.sin(-RADIAN * midAngle);
    const cos = Math.cos(-RADIAN * midAngle);
    const sx = cx + (outerRadius + 10) * cos;
    const sy = cy + (outerRadius + 10) * sin;
    const mx = cx + (outerRadius + 30) * cos;
    const my = cy + (outerRadius + 30) * sin;
    const ex = mx + (cos >= 0 ? 1 : -1) * 50;
    const ey = my + (sin >= 0 ? 1 : -1) * 50;
    const textAnchor = cos >= 0 ? 'start' : 'end';
    // console.log(payload);
    const sectorFill = payload.Pseudocolor === 0 || payload.Raw_MSI === 0 || payload.Pseudocolor * 20 !== payload.Raw_MSI ? '#fc0f3f' : fill;



    return (
      <g>
        <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
          {payload.name}
        </text>
        <Sector
          cx={cx}
          cy={cy}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
          startAngle={startAngle}
          endAngle={endAngle}
          fill={sectorFill}
        />
        <Sector
          cx={cx}
          cy={cy}
          startAngle={startAngle}
          endAngle={endAngle}
          innerRadius={outerRadius + 6}
          outerRadius={outerRadius + 10}
          fill={sectorFill}
        />
        <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none" />
        <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
        <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor} fill="#333">{`Total Images: ${total_img} (${(percent * 100).toFixed(2)}%)`}</text>
        <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={15} textAnchor={textAnchor} fill="#999" fontSize={13}>
          {`Pseudocolor: ${payload.Pseudocolor ? payload.Pseudocolor : "missing"}`}
        </text>
        <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={30} textAnchor={textAnchor} fill="#999" fontSize={13}>
          {`CJA: ${payload.CJA ? payload.CJA : "missing"}`}
        </text>
        <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={45} textAnchor={textAnchor} fill="#999" fontSize={13}>
          {`Raw_MSI: ${payload.Raw_MSI ? payload.Raw_MSI : "missing"}`}
        </text>
        <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={60} textAnchor={textAnchor} fill="#999" fontSize={13}>
          {`Pseudocolor_intermediate_output: ${payload.Pseudocolor_generation_intermediate_output? payload.Pseudocolor_generation_intermediate_output : "missing"}`}        
        </text>
      </g>
    );
  };

  return (
    <ResponsiveContainer width={1000} height={500}>
      <PieChart width={1000} height={500}>
        <Pie
          activeIndex={activeIndex}
          activeShape={renderActiveShape}
          data={data}
          cx="50%"
          cy="45%"
          innerRadius={80}
          outerRadius={120}
          fill='#38870b'
          dataKey="total_img"
          onMouseEnter={onPieEnter}
        />
      </PieChart>
    </ResponsiveContainer>
    
  );
};

export default DataPieChart;
