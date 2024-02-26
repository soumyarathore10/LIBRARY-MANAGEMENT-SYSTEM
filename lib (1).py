import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x400")

        
        self.root.configure(bg='#F0EAE1')

        self.create_database()

        self.title_label = tk.Label(root, text="Library Management System", font=("Helvetica", 16), bg='#825F45', fg='#F0EAE1')
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")

        
        self.input_frame = tk.Frame(root, bg='#F0EAE1')
        self.input_frame.grid(row=1, column=0, rowspan=10, padx=20, pady=10, sticky="nsew")

        self.book_id_label = tk.Label(self.input_frame, text="Book ID:", bg='#F0EAE1' ,fg='black')
        self.book_id_label.grid(row=0, column=0, sticky="e", pady=5)
        self.book_id_entry = tk.Entry(self.input_frame)
        self.book_id_entry.grid(row=0, column=1, pady=5)

        self.book_label = tk.Label(self.input_frame, text="Book Title:",  bg='#F0EAE1',fg='black')
        self.book_label.grid(row=1, column=0, sticky="e", pady=5)
        self.book_entry = tk.Entry(self.input_frame)
        self.book_entry.grid(row=1, column=1, pady=5)

        self.author_label = tk.Label(self.input_frame, text="Author:",  bg='#F0EAE1', fg='black')
        self.author_label.grid(row=2, column=0, sticky="e", pady=5)
        self.author_entry = tk.Entry(self.input_frame)
        self.author_entry.grid(row=2, column=1, pady=5)

        self.status_label = tk.Label(self.input_frame, text="Status:",  bg='#F0EAE1', fg='black')
        self.status_label.grid(row=3, column=0, sticky="e", pady=5)
        self.status_entry = tk.Entry(self.input_frame)
        self.status_entry.grid(row=3, column=1, pady=5)

        self.card_id_label = tk.Label(self.input_frame, text="Card ID:",  bg='#F0EAE1', fg='black')
        self.card_id_label.grid(row=4, column=0, sticky="e", pady=5)
        self.card_id_entry = tk.Entry(self.input_frame)
        self.card_id_entry.grid(row=4, column=1, pady=5)

        self.add_button = tk.Button(self.input_frame, text="Add Book", command=self.add_book, width=15, bg='#D08C60', fg='#F0EAE1')
        self.add_button.grid(row=5, column=0, pady=10, columnspan=2)

        self.issue_button = tk.Button(self.input_frame, text="Issue Book", command=self.issue_book, width=15, bg='#D08C60', fg='#F0EAE1')
        self.issue_button.grid(row=6, column=0, pady=10, columnspan=2)

        self.return_button = tk.Button(self.input_frame, text="Return Book", command=self.return_book, width=15, bg='#D08C60', fg='#F0EAE1')
        self.return_button.grid(row=7, column=0, pady=10, columnspan=2)

       
        self.tree = ttk.Treeview(root, columns=("Book ID", "Title", "Author", "Status", "Card ID"), show='headings')
        self.tree.grid(row=1, column=1, rowspan=10, columnspan=4, padx=10, pady=10, sticky="nsew")

        
        self.tree.tag_configure("evenrow", background='#F0EAE1')
        self.tree.tag_configure("oddrow", background='#F0EAE1')

        
        self.tree.heading("Book ID", text="Book ID", anchor="center")
        self.tree.heading("Title", text="Title", anchor="center")
        self.tree.heading("Author", text="Author", anchor="center")
        self.tree.heading("Status", text="Status", anchor="center")
        self.tree.heading("Card ID", text="Card ID", anchor="center")

        
        self.tree.column("Book ID", anchor="center", width=50)
        self.tree.column("Title", anchor="center", width=150)
        self.tree.column("Author", anchor="center", width=100)
        self.tree.column("Status", anchor="center", width=80)
        self.tree.column("Card ID", anchor="center", width=80)

        self.display_books()

        
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def create_database(self):
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                status TEXT,
                card_id INTEGER
            )
            """
        )
        self.conn.commit()

    def add_book(self):
        book_id = self.book_id_entry.get()
        title = self.book_entry.get()
        author = self.author_entry.get()
        status = self.status_entry.get()
        card_id = self.card_id_entry.get()

        if book_id and title and author and status and card_id:
            self.cursor.execute(
                "INSERT INTO books (id, title, author, status, card_id) VALUES (?, ?, ?, ?, ?)",
                (book_id, title, author, status, card_id)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_entries()
            self.display_books()
        else:
            messagebox.showerror("Error", "Please enter all book details.")

    def issue_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item, 'values')[0]
            self.cursor.execute("UPDATE books SET status='Not Available' WHERE id=?", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", f"Book {book_id} issued successfully!")
            self.display_books()
        else:
            messagebox.showerror("Error", "Please select a book to issue.")

    def return_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item, 'values')[0]
            self.cursor.execute("UPDATE books SET status='Available' WHERE id=?", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", f"Book {book_id} returned successfully!")
            self.display_books()
        else:
            messagebox.showerror("Error", "Please select a book to return.")

    def display_books(self):
        # Clear existing entries in the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        for i, book in enumerate(books):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=book, tags=(tag,))

    def clear_entries(self):
        self.book_id_entry.delete(0, tk.END)
        self.book_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.card_id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()





