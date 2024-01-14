import {RootState} from "../../store/store";
import {useSelector} from "react-redux";
import {useNavigate} from "react-router-dom";
import {ChangeEvent, useEffect, useState} from "react";
import {
    Box,
    Button, Container,
    FormControl,
    InputLabel,
    MenuItem,
    Select, SelectChangeEvent, TextField
} from "@mui/material";
import {useCreateReviewMutation, useGetBooksMutation} from "../../store/reviewApi";

export const Authorized = () => {
    const token = useSelector((state: RootState) => state.auth.token)
    const userId = useSelector((state: RootState) => state.auth.userId)
    const [createReview] = useCreateReviewMutation()
    const [getBooks, getBooksResult] = useGetBooksMutation()

    const [book, setBook] = useState({
        id: 0,
        name: '',
        file_path: ''
    });
    const [reviewContent, setReviewContent] = useState('');

    const navigate = useNavigate()

    const handleBookNameChange = (event: SelectChangeEvent) => {
        setBook(book => ({
            ...book,
            name: event.target.value as string
        }));
    };

    const handleBookInfoChange = (event: any) => {
        setBook(book => ({
            ...book,
            id: event.currentTarget.dataset.id as number,
            file_path: event.currentTarget.dataset.filePath as string
        }));
    };

    const handleBookDownload = () => {
        const PDFUrl = "http://127.0.0.1:8000/book/download/" + book.file_path;
        const link = document.createElement("a");
        link.href = PDFUrl;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const handleTextInputChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setReviewContent(event.target.value as string);
    };

    useEffect(() => {
        if (!token) {
            navigate("/")
        } else {
            getBooks()
        }
    }, [token, getBooks, navigate])

    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    minHeight: "100vh"
                }}
            >
                <FormControl fullWidth>
                    <InputLabel>Books</InputLabel>
                    <Select
                        value={book.name}
                        label="Books"
                        onChange={handleBookNameChange}
                    >
                        {getBooksResult.data?.map(({id, name, file_path}, index) => (
                            <MenuItem key={index} value={name} data-id={id} data-file-path={file_path}
                                      onClick={handleBookInfoChange}>
                                {name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <Button onClick={handleBookDownload}>Download book</Button>
                <TextField
                    margin="normal"
                    fullWidth
                    label="Review"
                    name="Review"
                    value={reviewContent}
                    autoFocus
                    onChange={handleTextInputChange}
                />
                <Button onClick={() => createReview({content: reviewContent, user_id: userId, book_id: book.id})}>Post
                    review</Button>
            </Box>
        </Container>
    );
}
