import React, { useMemo, useState, useCallback, useEffect } from 'react'
import { useTable, useGlobalFilter, useFilters, useSortBy, useAsyncDebounce } from 'react-table'
import ReportCell from "./ReportCell"
import ImageCell from "./ImageCell"
import Summary from './Summary'
import Filter from './Filter'
import './Table.css'
import useAuth from '../hooks/useAuth'
import ImportLocal from './ImportLocal'

const Details = ({ data }) => {
    const column = useMemo(() => data.col, [data])
    const row = useMemo(() => data.row, [data])
    const { auth, setAuth } = useAuth();

    const customFilter = useCallback(
        (rows, ids, query) => {
            const start_date = query['start']
            const end_date = query['end']
            const site = query['site']
            return rows.filter(row => {
                const acquire_start = new Date(row.values["acquired_start_time"])
                const acquire_end = new Date(row.values["acquired_end_time"])
                let left_ok = true;
                let right_ok = true;
                if (start_date) {
                    left_ok = left_ok && (start_date <= acquire_start)
                    right_ok = right_ok && (start_date <= acquire_end)
                }
                if (end_date) {
                    left_ok = left_ok && (acquire_start <= end_date)
                    right_ok = right_ok && (acquire_end <= end_date)
                }
                if (site === "") {
                    return left_ok || right_ok
                } else {
                    return row.values['site'] === site && (left_ok || right_ok)
                }
            })
        },
        []
    );

    const tableInstance = useTable({
        columns: column,
        data: row,
        globalFilter: customFilter,
    }, useFilters, useGlobalFilter, useSortBy)

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        state,
        setGlobalFilter,
        sortedFlatRows,
        getToggleHideAllColumnsProps,
        allColumns,
        visibleColumns,
    } = tableInstance

    const sites = useMemo(() => new Set(rows.map(row => row["values"]["site"])), []);


    return (
        <>
            {auth.roles === "admin" ? <ImportLocal /> : null}
            <Filter setGlobalFilter={setGlobalFilter} sites={sites} />
            <Summary rows={rows} />
            <table {...getTableProps()}>
                <thead>
                    {headerGroups.map((headerGroup, index) => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {
                                headerGroup.headers.map(column => (
                                    <th {...column.getHeaderProps()}>
                                        <div>
                                            {column.render('Header')}
                                        </div>
                                    </th>
                                ))
                            }
                        </tr>
                    ))
                    }
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map((row) => {
                        prepareRow(row)
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map(cell => {
                                    if (cell['column']['Header'] == 'report') {
                                        return <td><ReportCell {...cell.getCellProps()} cell={cell} /></td>
                                    } else if (cell['column']['Header'] == 'image_quality') {
                                        return <td><ImageCell {...cell.getCellProps()} cell={cell} /></td>
                                    } else {
                                        return <td {...cell.getCellProps()} className="content">
                                            {cell.render('Cell')}
                                        </td>
                                    }

                                })}
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </>
    )
}

export default Details