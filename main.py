class Book():
    def __init__(self,title,author,book_id,total_copies):
        self.title=title
        self.author=author
        self.book_id=book_id
        self.total_copies=total_copies
        self.available_copies=total_copies
class User():
    def __init__(self,name,user_id):
        self.name=name
        self.user_id=user_id
        self.borrowed_books=[]
class Library():
    def __init__(self):
        self.books=[]
        self.users=[]
    def add_book(self,book):
        self.books.append(book)
    def add_user(self,user):
        self.users.append(user)
    def search_by_title(self,title):
        for a in self.books:
            if a.title == title:
              return a
        else:
              return "Not found "
    def search_by_author(self,author):
        for a in self.books:
            if a.author == author:
                return a
        else:
            return "Not found "
    def borrow_book(self,title,user):
        book=self.search_by_title(title) 
        if book != "Not found ":
            if book.available_copies > 0:
                book.available_copies -= 1
                user.borrowed_books.append(book)
                return "Book borrowed successfully"
            else:
                return "No copies available"       
        else:
            return "Book not found"
    def return_book(self,title,user):
        book=self.search_by_title(title)
        if book != "Not found ":
            if book in user.borrowed_books:
                book.available_copies += 1
                user.borrowed_books.remove(book)
                return "Book returned successfully"
            else:
                return "User did not borrow this book"
        else:
            return "Book not found"
    
import streamlit as st

st.title("📚 Digital Library Management System")

# Session State Setup 
if 'library' not in st.session_state:
    st.session_state.library = Library()

if 'current_user' not in st.session_state:
    st.session_state.current_user = User(name="Test User", user_id=1)
# Sidebar for Navigation
st.sidebar.title("Navigation")
options = ["Add Book", "Search Book", "Borrow Book", "Return Book", "View Borrowed Books"]
choice = st.sidebar.selectbox("Choose an option", options)
if choice == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    book_id = st.number_input("Book ID", min_value=1, step=1)
    total_copies = st.number_input("Total Copies", min_value=1, step=1)
    if st.button("Add Book"):
        new_book = Book(title=title, author=author, book_id=book_id, total_copies=total_copies)
        st.session_state.library.add_book(new_book)
        st.success(f"Book '{title}' added successfully!")
elif choice == "Search Book":
    st.header("Search for a Book")
    search_title = st.text_input("Enter Book Title to Search")
    if st.button("Search"):
        result = st.session_state.library.search_by_title(search_title)
        if result != "Not found ":
            st.write(f"**Title:** {result.title}")
            st.write(f"**Author:** {result.author}")
            st.write(f"**Available Copies:** {result.available_copies}")
        else:
            st.error("Book not found!")
elif choice == "Borrow Book":
    st.header("Borrow a Book")
    borrow_title = st.text_input("Enter Book Title to Borrow")
    if st.button("Borrow"):
        message = st.session_state.library.borrow_book(borrow_title, st.session_state.current_user)
        if message == "Book borrowed successfully":
            st.success(message)
        else:
            st.error(message)
elif choice == "Return Book":
    st.header("Return a Book")
    return_title = st.text_input("Enter Book Title to Return")
    if st.button("Return"):
        message = st.session_state.library.return_book(return_title, st.session_state.current_user)
        if message == "Book returned successfully":
            st.success(message)
        else:
            st.error(message)
elif choice == "View Borrowed Books":
    st.header("Your Borrowed Books")
    if st.session_state.current_user.borrowed_books:
        for b in st.session_state.current_user.borrowed_books:
            st.write(f"- {b.title} by {b.author}")
    else:
        st.info("You have not borrowed any books yet.")
elif choice == "View All Books":
    st.header("All Books in Library")
    if st.session_state.library.books:
        for b in st.session_state.library.books:
            st.write(f"- {b.title} by {b.author} (Available: {b.available_copies}/{b.total_copies})")
    else:
        st.info("No books in the library yet.")
