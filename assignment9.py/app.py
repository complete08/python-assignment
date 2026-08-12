
import tkinter as tk
from tkinter import messagebox
import scraper


class BookBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Browser")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Keep the full unfiltered list here so Search can filter it
        # without needing to re-scrape the site every time.
        self.all_books = []

        self._build_widgets()

    def _build_widgets(self):
        # --- Title label ---
        title_label = tk.Label(
            self.root, text="Books to Scrape", font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(10, 5))

        # --- Search bar (bonus) ---
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5, fill="x", padx=10)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        # Pressing Enter in the search box also triggers a search
        self.search_entry.bind("<Return>", lambda event: self.search_books())

        search_button = tk.Button(search_frame, text="Search", command=self.search_books)
        search_button.pack(side="left")

        # --- Load Books button ---
        load_button = tk.Button(
            self.root, text="Load Books", command=self.load_books,
            bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold")
        )
        load_button.pack(pady=5)

        # --- Listbox with Scrollbar ---
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10)
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.listbox.yview)

        # --- Count label ---
        self.count_label = tk.Label(self.root, text="Total: 0 books loaded")
        self.count_label.pack(pady=(0, 10))

    def load_books(self):
        """Fetches books from the scraper and populates the Listbox."""
        self.count_label.config(text="Loading...")
        self.root.update_idletasks()  # refresh UI so "Loading..." actually shows

        books = scraper.get_books()

        if not books:
            messagebox.showwarning(
                "No Data", "Could not load books. Check your internet connection."
            )
            self.count_label.config(text="Total: 0 books loaded")
            return

        self.all_books = books
        self._populate_listbox(self.all_books)

    def search_books(self):
        """Filters the currently loaded books by the search term."""
        term = self.search_entry.get().strip().lower()

        if not self.all_books:
            messagebox.showinfo("No Data", "Load books first before searching.")
            return

        if term == "":
            filtered = self.all_books
        else:
            filtered = [b for b in self.all_books if term in b["title"].lower()]

        self._populate_listbox(filtered)

    def _populate_listbox(self, books):
        """Clears the Listbox and fills it with the given list of book dicts."""
        self.listbox.delete(0, tk.END)

        for book in books:
            self.listbox.insert(tk.END, f"{book['title']} — {book['price']}")

        self.count_label.config(text=f"Total: {len(books)} books loaded")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookBrowserApp(root)
    root.mainloop()