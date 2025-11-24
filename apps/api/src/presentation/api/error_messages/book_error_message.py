# General error messages
BOOK_NOT_FOUND = "Book with the specified ID was not found."
BOOK_ACCESS_DENIED = "You do not have permission to access this book."
BOOK_FILE_NOT_FOUND = "File for this book was not found."
BOOK_COVER_NOT_FOUND = "Cover image for this book was not found."
BOOK_ALREADY_STARTED = "This book has already been started."
BOOK_ALREADY_COMPLETED = "This book has already been completed."

# Operation error messages
BOOK_CREATE_ERROR = "An error occurred while creating the book: {error}"
BOOK_UPDATE_ERROR = "An error occurred while updating the book: {error}"
BOOK_DELETE_ERROR = "An error occurred while deleting the book: {error}"
BOOK_BULK_DELETE_ERROR = "An error occurred while bulk deleting books: {error}"
BOOK_FETCH_ERROR = "An error occurred while fetching the book: {error}"
BOOK_COVER_FETCH_ERROR = "An error occurred while fetching the book cover image: {error}"
BOOK_FILE_FETCH_ERROR = "An error occurred while fetching the book file: {error}"
SIGNED_URL_GENERATION_ERROR = "An error occurred while generating the signed URL: {error}"

# Input validation error messages
BOOK_TITLE_REQUIRED = "Book title is required."
BOOK_TITLE_TOO_LONG = "Book title must be 100 characters or less."
BOOK_DESCRIPTION_TOO_LONG = "Book description must be 1000 characters or less."
BOOK_DATA_REQUIRED = "Book data is required."
BOOK_USER_ID_REQUIRED = "User ID is required."
BOOK_ID_INVALID_FORMAT = "Book ID format is invalid. Please specify a valid UUID."
