import {
    createBrowserRouter,
} from "react-router-dom";
import {Auth} from "../pages/auth/Auth";
import {Authorized} from "../pages/authorized/Authorized";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Auth/>,
    },
    {
        path: "/authorized",
        element: <Authorized/>,
    },
        {
        path: "/hello",
        element: <div>Hello world!</div>,
    },
]);
