import {createTheme, ThemeProvider} from "@mui/material";
import {Provider} from "react-redux";
import {store} from "./store/store";
import {RouterProvider} from "react-router-dom";
import {router} from "./router/Router";

function App() {
    const theme = createTheme();

    return (
        <Provider store={store}>
            <ThemeProvider theme={theme}>
                <RouterProvider router={router}/>
            </ThemeProvider>
        </Provider>
    );
}

export default App;
