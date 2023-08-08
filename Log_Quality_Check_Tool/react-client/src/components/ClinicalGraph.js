import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';


const ClinicalGraph = ( {rows, colors} ) => {
    const distinct_sites = new Set(rows.map(row => row["site"]));
    const sites = [...distinct_sites]
    const indices = [...Array(sites.length).keys()].map(i => i.toString());
    const [isCheckAll, setIsCheckAll] = useState(true);
    const [isCheck, setIsCheck] = useState(indices);
    const [expand, setExpand] = useState(false);
    const [lines, setLines] = useState([]);
    const chart_data = [
        {
            name: '4-25-2022',
            "University Medical Center of NOLA": 0,
            "Medical University South Carolina": 0,
            "Medstar Health": 0,
            "Wake Forest Baptist Health": 0,
            "University Medical Center of NOLA Children": 0,
            "Masschusetts General Health": 0,
            "University of Alabama Brimingham": 0,
            "Medical University South Carolina Children": 0,
            "Bridgeport Hospital": 0,
            "University of Alabama Brimingham-Emergency Dept": 0,
            "Massachusetts General Hospital": 0
        },
    ];

    if (rows.length > 0) {
        const point = { ...chart_data[chart_data.length - 1] }
        const prev_date = new Date(rows[0]['acquired_end_time'])
        let prev_month = prev_date.getMonth() + 1;
        let prev_year = prev_date.getFullYear()
        point["name"] = prev_month + "-25-" + prev_year
        rows.forEach(row => {
            const date = new Date(row['acquired_end_time'])
            const month = date.getMonth() + 1;
            const year = date.getFullYear()
            if (month === prev_month && year === prev_year) {
                if (row['site'] in point) {
                    point[row['site']] += row['image_collection_number']
                } else {
                    point[row['site']] = row['image_collection_number']
                }
            } else {
                const new_point = { ...point }
                chart_data.push(new_point)
                for (let i = prev_month + 1; i < month; ++i) {
                    const new_point = { ...point }
                    new_point['name'] = i + "-25-" + year
                    chart_data.push(new_point)
                }
                point['name'] = month + "-25-" + year
                if (row['site'] in point) {
                    point[row['site']] += row['image_collection_number']
                } else {
                    point[row['site']] = row['image_collection_number']
                }
                prev_month = month
                prev_year = year
            }
        });
        const new_point = { ...point }
        chart_data.push(new_point)
    }

    const showCheckboxes = () => {
        setExpand(old => !old)
    }

    const handleClick = e => {
        const { id, checked } = e.target;
        setIsCheck([...isCheck, id]);
        if (!checked) {
            setIsCheck(isCheck.filter(item => item !== id));
        }
    };

    const handleSelectAll = e => {
        setIsCheckAll(!isCheckAll);
        setIsCheck(indices);
        if (isCheckAll) {
            setIsCheck([]);
        }
    };

    useEffect(() => {
        const new_lines = isCheck.map((checked, index) => {
            const site = sites[parseInt(checked)]
            return <Line key={index} type="monotone" dataKey={site} stroke={colors[index]} activeDot={{ r: 8 }} />
        })
        setLines(new_lines);
    }, [isCheck]);

    const catalog = sites.map((site, index) => {
        return <label key={index}>
            <input key={index} id={index} type="checkbox" onChange={handleClick} checked={isCheck.includes(index.toString())} />{' '}
            {site}
        </label>
    });

    return (
        <>
            <h2 className='mt-3 d-inline'>Clinical Data </h2><Link to="/details"> (see details)</Link>
            <div className="multiselect m-4">
                <div className="selectBox" onClick={showCheckboxes}>
                    <select>
                        <option>Choose sites to show</option>
                    </select>
                    <div className="overSelect"></div>
                </div>
                {expand ?
                    (<div id="checkboxes">
                        <label>
                            <input type="checkbox" checked={isCheckAll} onChange={handleSelectAll} />{' '}
                            Toggle All
                        </label>
                        {catalog}
                    </div>) : ''}
            </div>
            <LineChart
                width={600}
                height={600}
                data={chart_data}
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

export default ClinicalGraph