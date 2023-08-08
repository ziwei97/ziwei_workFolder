import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';

const DeviceGraph = ({ rows, colors }) => {
    const distinct_sites = new Set(rows.map(row => {
        return row["site"] + "-" + row['device_number']
    }));
    const sites = [...distinct_sites]
    const [check, setCheck] = useState("All");
    const [expand, setExpand] = useState(false);
    const [lines, setLines] = useState([]);
    const chart_data = {}
    const default_data = [
        {
            name: '5-25-2022',
            "fatal_error": 0,
            "critical_error": 0,
            "ignore_error": 0,
        },
    ];

    sites.forEach(site => {
        chart_data[site] = [...default_data]
    })
    chart_data["All"] = [...default_data]

    if (rows.length > 0) {
        rows.forEach(row => {
            const date = new Date(row['acquired_end_time'])
            const month = date.getMonth() + 1;
            const year = date.getFullYear();
            const site = row['site'] + "-" + row['device_number']
            let error_data = chart_data[site];
            let point = error_data[error_data.length - 1] // get last data
            let past_date = new Date(point['name'])
            if (month === past_date.getMonth() + 1 && year === past_date.getFullYear()) {
                point["fatal_error"] += row['fatal_error']
                point["critical_error"] += row['critical_error']
                point["ignore_error"] += row['ignore_error']
            } else {
                for (let i = past_date.getMonth() + 2; i < month; ++i) {
                    const new_point = { ...point }
                    new_point['name'] = i + "-25-" + year
                    error_data.push(new_point)
                }
                const new_point = { ...point }
                new_point['name'] = month + "-25-" + year
                new_point["fatal_error"] += row['fatal_error']
                new_point["critical_error"] += row['critical_error']
                new_point["ignore_error"] += row['ignore_error']
                error_data.push(new_point)
            }
            let error_all = chart_data["All"];
            let point_all = error_all[error_all.length - 1] // get last data
            let past_all = new Date(point_all['name'])
            if (month === past_all.getMonth() + 1 && year === past_all.getFullYear()) {
                point_all["fatal_error"] += row['fatal_error']
                point_all["critical_error"] += row['critical_error']
                point_all["ignore_error"] += row['ignore_error']
            } else {
                for (let i = past_all.getMonth() + 2; i < month; ++i) {
                    const new_point = { ...point_all }
                    new_point['name'] = i + "-25-" + year
                    error_all.push(new_point)
                }
                const new_point = { ...point_all }
                new_point['name'] = month + "-25-" + year
                new_point["fatal_error"] += row['fatal_error']
                new_point["critical_error"] += row['critical_error']
                new_point["ignore_error"] += row['ignore_error']
                error_all.push(new_point)
            }
        });
    }

    const showCheckboxes = () => {
        setExpand(old => !old)
    }

    const handleClick = e => {
        const { id, checked } = e.target;
        setCheck(id);
    };

    useEffect(() => {
        const new_lines = [
            <Line key={0} type="monotone" dataKey={"fatal_error"} stroke={colors[0]} activeDot={{ r: 8 }} />,
            <Line key={1} type="monotone" dataKey={"critical_error"} stroke={colors[1]} activeDot={{ r: 8 }} />,
            <Line key={2} type="monotone" dataKey={"ignore_error"} stroke={colors[2]} activeDot={{ r: 8 }} />,
        ]
        setLines(new_lines);
    }, [check]);

    const catalog = sites.map((site, index) => {
        return <label key={index}>
            <input key={index} id={site} type="checkbox" onChange={handleClick} checked={check === site} />{' '}
            {site}
        </label>
    });

    return (
        <>
            <h2 className='mt-3 d-inline'>Device Data </h2><Link to="/details"> (see details)</Link>
            <div className="multiselect m-4">
                <div className="selectBox" onClick={showCheckboxes}>
                    <select>
                        <option>Choose devices to show</option>
                    </select>
                    <div className="overSelect"></div>
                </div>
                {expand ?
                    (<div id="checkboxes">
                        <label>
                            <input type="checkbox" id={"All"} checked={check === "All"} onChange={handleClick} />{' '}
                            Show Total
                        </label>
                        {catalog}
                    </div>) : ''}
            </div>

            <LineChart
                width={600}
                height={600}
                data={chart_data[check]}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                {lines}
            </LineChart>
        </>

    )
}

export default DeviceGraph