import React from 'react'
import { useLocation, Navigate, Outlet } from 'react-router-dom'
import useAuth from '../hooks/useAuth'

const RequireAuth = () => {
    const { auth, setAuth } = useAuth();
    const location = useLocation();
    return (
        auth.access_token ? <Outlet />
        : <Navigate to="/" state ={{ from: location }} replace />
    )
}

export default RequireAuth