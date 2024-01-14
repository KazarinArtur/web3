import {createSlice} from '@reduxjs/toolkit'
import type {PayloadAction} from '@reduxjs/toolkit'

enum Roles {
    user = "user",
    admin = "admin"
}


export interface AuthState {
    token: string | null;
    isAuthorized: boolean;
    role: Roles | null;
    userId: number;
}

const initialState: AuthState = {
    token: null,
    isAuthorized: false,
    role: null,
    userId: 0,
}

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setToken: (state, action: PayloadAction<string>) => {
            state.token = action.payload
            state.isAuthorized = true
        },
        invalidateToken: (state) => {
            state.token = null
            state.isAuthorized = false
            state.role = null
        },
        setRole: (state, action: PayloadAction<Roles>) => {
            state.role = action.payload
        },
        setUserId: (state, action: PayloadAction<number>) => {
            state.userId = action.payload
        },
    },
})

export const {setToken, invalidateToken, setRole, setUserId} = authSlice.actions

export default authSlice.reducer
