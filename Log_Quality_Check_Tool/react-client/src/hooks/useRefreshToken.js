import React from 'react'
import axios from 'axios';
import useAuth from './useAuth'

const useRefreshToken = () => {
    const { auth, setAuth } = useAuth();

    const refresh = async () => {
        const refresh_token = localStorage.getItem('refresh_token')
        const response = await axios.post("/refresh", {}, {
            withCredentials: true,
            headers: { 
                Authorization: 'Bearer ' + refresh_token
            },
        });
        setAuth(prev => {
            return {...prev, access_token: response.data.access_token, roles: response.data.roles}
        })
        return response.data.access_token;
    }
    return refresh;
}

export default useRefreshToken