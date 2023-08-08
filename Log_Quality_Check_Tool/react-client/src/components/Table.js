import React, { useEffect, useState, useMemo, useCallback } from 'react'
import Details from './Details'
import useAxiosPrivate from '../hooks/useAxiosPrivate'
import { useNavigate, useLocation } from "react-router-dom"

const Table = () => {
    const [data, setData] = useState(undefined)
    const axiosPrivate = useAxiosPrivate();
    const nav = useNavigate();
    const location = useLocation();

    useEffect(() => {
        axiosPrivate.get('/getReports')
            .then(
                response => {
                    console.log(response)
                    setData(response.data)
                }
            )
            .catch((err) => {
                console.log(err);
                nav("/", { state: { from: location }, replace: true });
            })
    }, [])

    if (data === undefined) {
        return <>Still loading...</>;
    } else {
        return (
            <>
                <Details data={data} />
            </>
        )
    }
}

export default Table