import {fetchBaseQuery} from '@reduxjs/toolkit/query'
import type {
    BaseQueryFn,
    FetchArgs,
    FetchBaseQueryError,
} from '@reduxjs/toolkit/query'
import {RootState} from "./store";

const baseQuery = fetchBaseQuery({baseUrl: '/'})
export const baseQueryWithAuth: BaseQueryFn<
    FetchArgs,
    unknown,
    FetchBaseQueryError
> = async (args, api, extraOptions) => {
    const state: RootState = api.getState() as RootState
    const token = state?.auth?.token

    const result = await baseQuery({...args, headers: {"Authorization": `Bearer ${token}`}}, api, extraOptions)
    return result
}
