import {createApi} from "@reduxjs/toolkit/query/react";
import {baseQueryWithAuth} from "./baseQueryWithAuth";

export const reviewApi = createApi({
    reducerPath: 'reviewApi',
    baseQuery: baseQueryWithAuth,
    endpoints: (builder) => ({
        getBooks: builder.mutation<
            [{
                "id": number;
                "name": string;
                "description": string;
                "file_path": string;
            }]
            , void>({
            query: () => {
                return {
                    url: "/book/list",
                    method: "GET"
                }
            },
        }),
        createReview: builder.mutation<{
            "id": number;
            "content": string;
            "user_id": number;
            "book_id": number;
        }, { content: string, user_id: number, book_id: number }>({
            query: ({content, user_id, book_id}) => {
                return {
                    url: "/review/create",
                    method: "POST",
                    body: {content: content, user_id: user_id, book_id: book_id}
                }
            },
        }),
    }),
})

export const {useGetBooksMutation, useCreateReviewMutation} = reviewApi
