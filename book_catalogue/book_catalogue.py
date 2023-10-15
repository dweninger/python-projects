import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk
import json

class BookCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Catalog")
        self.root.geometry("800x600")

        self.lists = ["Reading", "Want to Read", "Read"]

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Create tabs for Search, Reading, 
        # Want to Read, and Read
        self.search_tab = self.create_tab(
            "Search")
        self.reading_tab = self.create_tab(
            "Reading")
        self.want_to_read_tab = self.create_tab(
            "Want to Read")
        self.read_tab = self.create_tab(
            "Read")

        # Create dictionaries to map books to respective lists
        self.reading_list = {}
        self.want_to_read_list = {}
        self.read_list = {}

        # Create list to store book information
        self.books = []

        # Create buttons and labels for Search tab
        self.search_label = ttk.Label(
            self.search_tab, text="Search for a book:")
        self.search_label.grid(
            row=0, column=0, padx=10, 
            pady=5, sticky="w")
        self.search_entry = ttk.Entry(self.search_tab)
        self.search_entry.grid(
            row=0, column=1, padx=10, 
            pady=5, sticky="w")
        self.search_button = ttk.Button(
            self.search_tab, text="Search", 
            command=self.search_book)
        self.search_button.grid(
            row=0, column=2, padx=10, 
            pady=5, sticky="w")

        # Create a Frame for the search results
        search_tree_frame = ttk.Frame(self.search_tab)
        search_tree_frame.grid(
            row=1, column=0, columnspan=3, 
            padx=10, pady=5, sticky="nsew")

        # Create a style for the treeview to adjust row height
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=100)

        self.tree = ttk.Treeview(
            search_tree_frame, 
            columns=("Title", "Author"), 
            style="Custom.Treeview")
        self.tree.heading("#1", text="Title")
        self.tree.heading("#2", text="Author")
        self.tree.column("#1", width=300)

        y_scrollbar = ttk.Scrollbar(
            search_tree_frame, orient="vertical", 
            command=self.tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=y_scrollbar.set)

        self.tree.pack(expand=True, fill="both")

        # Create Combobox for list selection
        self.list_selection = ttk.Combobox(
            self.search_tab, values=self.lists)
        self.list_selection.set(self.lists[0])
        self.list_selection.grid(
            row=2, column=0, padx=10, 
            pady=5, sticky="w")
        self.add_button = ttk.Button(
            self.search_tab, text="Add to List", 
            command=self.add_to_list)
        self.add_button.grid(
            row=2, column=1, padx=10, 
            pady=5, sticky="w")

        self.search_tab.grid_columnconfigure(
            0, weight=1)
        self.search_tab.grid_rowconfigure(
            1, weight=1)

        # Create Reading, Want to Read, and Read listboxes
        self.reading_tree = self.create_tree(
            self.reading_tab, ["Title", "Author"])
        self.want_to_read_tree = self.create_tree(
            self.want_to_read_tab, ["Title", "Author"])
        self.read_tree = self.create_tree(
            self.read_tab, ["Title", "Author"])

        # Create Delete buttons
        self.create_delete_button(
            self.reading_tab, "Reading")
        self.create_delete_button(
            self.want_to_read_tab, "Want to Read")
        self.create_delete_button(
            self.read_tab, "Read")

        # Create "Move to" widgets for each list tab
        self.create_move_to_widgets(
            self.reading_tab, "Reading")
        self.create_move_to_widgets(
            self.want_to_read_tab, "Want to Read")
        self.create_move_to_widgets(
            self.read_tab, "Read")

        # Create menu bar
        self.create_menu()

        # Create list to store references to image objects
        self.image_references = []

    def create_tab(self, name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=name)
        return tab

    def create_tree(self, frame, columns):
        tree = ttk.Treeview(
            frame, columns=columns, 
            style="Custom.Treeview")
        tree.heading('#0', text="")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=300, anchor='w')
        tree.grid(
            row=0, column=0, columnspan=3, 
            padx=16, pady=10,  sticky="nsew")
        
        y_scrollbar = ttk.Scrollbar(
            frame, orient="vertical", 
            command=tree.yview)
        y_scrollbar.grid(row=0, column=2, sticky="nse")
        tree.config(yscrollcommand=y_scrollbar.set)
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return tree

    def create_delete_button(self, frame, list_name):
        delete_button = ttk.Button(
            frame, text="Delete", 
            command=lambda: self.delete_from_list(
                list_name))
        delete_button.grid(
            row=1, column=0, padx=10, 
            pady=5, sticky="w")

    def create_move_to_widgets(self, frame, list_name):
        move_label = ttk.Label(
            frame, text="Move book to:")
        move_label.grid(
            row=2, column=0, padx=10, 
            pady=5, sticky="w")

        move_to_list_var = tk.StringVar()
        move_to_list_var.set(self.lists[0])
        move_to_list_dropdown = ttk.Combobox(
            frame, textvariable=move_to_list_var, 
            values=[x for x in self.lists 
                    if x != list_name])
        move_to_list_dropdown.grid(
            row=2, column=1, padx=10, 
            pady=5, sticky="w")
        
        move_to_button = ttk.Button(
            frame, text="Move to", 
            command=lambda ln=list_name, 
            var=move_to_list_var: self.move_book(
                ln, var))
        move_to_button.grid(
            row=2, column=2, padx=10, 
            pady=5, sticky="w")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create a File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(
            label="File", menu=file_menu)
        file_menu.add_command(
            label="Import", command=self.import_lists)
        file_menu.add_command(
            label="Export", command=self.export_lists)

    def search_book(self):
        book_title = self.search_entry.get()
        if book_title:
            self.clear_tree(self.tree)
            # Use the Google Books API to search for books
            url = (f"https://www.googleapis.com/books/"
                   f"v1/volumes?q={book_title}")

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get(
                        "items", []):
                        volume_info = item.get(
                            "volumeInfo", {})
                        title = volume_info.get(
                            "title", "No Title")
                        authors = volume_info.get(
                            "authors", ["No Author"])
                        author = ", ".join(authors)
                        self.books.append(
                            (title, author))

                        # Get the image link
                        image_links = volume_info.get(
                            "imageLinks", {})
                        thumbnail = image_links.get(
                            "thumbnail", "")

                        if thumbnail:
                            img = Image.open(
                                requests.get(
                                    thumbnail, 
                                    stream=True).raw)
                            img = img.resize((50, 75))
                            img = ImageTk.PhotoImage(img)

                            item = self.tree.insert(
                                "", "end", 
                                values=(title, author), 
                                image=img)
                # Store thumbnail link in item's tag
                            self.tree.item(
                                item, tag=thumbnail)
                # Save a reference to image to 
                # prevent it from being garbage collected
                            self.image_references.append(
                                img)
                else:
                    print("Error: Unable to retrieve "
                          "book data from the API.")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def add_to_list(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            title = item["values"][0]
            author = item["values"][1]
            thumbnail = item["tags"][0]
            selected_list = self.list_selection.get()

            # Store book in selected list
            lists = {
                "Reading": self.reading_list,
                "Want to Read": self.want_to_read_list,
                "Read": self.read_list
            }

            if selected_list in lists:
                lists[selected_list][(
                    title, author)] = thumbnail

                # Update Treeview in respective tab
                treeviews = {
                    "Reading": self.reading_tree,
                    "Want to Read": self.want_to_read_tree,
                    "Read": self.read_tree
                }

                treeview = treeviews.get(selected_list)
                if thumbnail:
                    img = Image.open(
                        requests.get(
                            thumbnail, 
                            stream=True).raw)
                    img = img.resize((50, 75))
                    img = ImageTk.PhotoImage(img)

                    item = treeview.insert(
                        "", "end", values=(title, author), 
                        image=img)
                    # Store thumbnail link in tag
                    treeview.item(item, tag=thumbnail)
                    # Save reference to image
                    self.image_references.append(img)

    def delete_from_list(self, list_name):
        selected_item = self.get_selected_item(list_name)
        if selected_item:
            title, author, thumbnail_link = selected_item
            lists = {
                "Reading": self.reading_list,
                "Want to Read": self.want_to_read_list,
                "Read": self.read_list
            }
            if list_name in lists:
                del lists[list_name][(title, author)]

            # Update the Treeview in the respective tab
            treeviews = {
                "Reading": self.reading_tree,
                "Want to Read": self.want_to_read_tree,
                "Read": self.read_tree
            }

            treeview = treeviews.get(list_name)
            if treeview:
                selected_item_id = self.find_item_id(
                    treeview, title, author)
                if selected_item_id:
                    treeview.delete(selected_item_id)

    def move_book(self, current_list_name, move_to_var):
        selected_item = self.get_selected_item(
            current_list_name)  
        if selected_item:
            title, author, thumbnail_link = selected_item

            lists = {
                "Reading": self.reading_list,
                "Want to Read": self.want_to_read_list,
                "Read": self.read_list
            }

            current_list = lists[current_list_name]
            move_to_list_name = move_to_var.get()
            move_to_list = lists[move_to_list_name]

            if (title, author) in current_list:
                del current_list[(title, author)]
                move_to_list[
                    (title, author)] = thumbnail_link

                # Update Treeviews in respective tabs
                treeviews = {
                    "Reading": self.reading_tree,
                    "Want to Read": self.want_to_read_tree,
                    "Read": self.read_tree
                }

                current_tree = treeviews.get(
                    current_list_name)
                move_to_tree = treeviews.get(
                    move_to_list_name)

                if current_tree and move_to_tree:
                    selected_item_id = self.find_item_id(
                        current_tree, title, author)
                    if selected_item_id:
                        current_tree.delete(
                            selected_item_id)
                    if thumbnail_link:
                        img = Image.open(
                            requests.get(
                                thumbnail_link, 
                                stream=True).raw)
                        img = img.resize((50, 75))
                        img = ImageTk.PhotoImage(img)

                        item = move_to_tree.insert(
                            "", "end", 
                            values=(title, author), 
                            image=img)
                        # Store thumbnail link in tag
                        move_to_tree.item(
                            item, tag=thumbnail_link)
                        self.image_references.append(img)

    def get_selected_item(self, list_name):
        if list_name == "Reading":
            selected_item_id = (
                self.reading_tree.selection())
        elif list_name == "Want to Read":
            selected_item_id = (
                self.want_to_read_tree.selection())
        elif list_name == "Read":
            selected_item_id = (
                self.read_tree.selection())
        else:
            return None

        if selected_item_id:
            item = self.get_item_by_id(
                list_name, selected_item_id)
            thumbnail_link = self.get_thumbnail_link(
                list_name, selected_item_id)
            return item[0], item[1], thumbnail_link
        return None
    
    def get_thumbnail_link(self, list_name, item_id):
        tree = None

        if list_name == "Reading":
            tree = self.reading_tree
        elif list_name == "Want to Read":
            tree = self.want_to_read_tree
        elif list_name == "Read":
            tree = self.read_tree

        if tree:
            return tree.item(item_id)["tags"][0]
        return None

    def get_item_by_id(self, list_name, item_id):
        if list_name == "Reading":
            return self.reading_tree.item(
                item_id)["values"]
        elif list_name == "Want to Read":
            return self.want_to_read_tree.item(
                item_id)["values"]
        elif list_name == "Read":
            return self.read_tree.item(
                item_id)["values"]
        else:
            return None

    def find_item_id(self, tree, title, author):
        for item_id in tree.get_children():
            item = tree.item(item_id)
            if item["values"][0] == title and item[
                "values"][1] == author:
                return item_id
        return None

    def import_lists(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".json", 
            filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    self.reading_list = {}
                    self.want_to_read_list = {}
                    self.read_list = {}
                    for key, book_list in data.items():
                        for book_info in book_list:
                            title, author = book_info[0]
                            thumbnail = book_info[1]
                            if key == "Reading":
                                self.reading_list[
                                    (title, author)
                                    ] = thumbnail
                            elif key == "Want to Read":
                                self.want_to_read_list[
                                    (title, author)
                                    ] = thumbnail
                            elif key == "Read":
                                self.read_list[
                                    (title, author)
                                    ] = thumbnail

                # Update Treeviews with imported data
                self.update_tree(
                    self.reading_tree, 
                    self.reading_list)
                self.update_tree(
                    self.want_to_read_tree, 
                    self.want_to_read_list)
                self.update_tree(
                    self.read_tree, 
                    self.read_list)
            except Exception as e:
                print(f"Error: Unable to import data - {e}")

    def export_lists(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", 
            filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                data = {
                    "Reading": list(
                        self.reading_list.items()),
                    "Want to Read": list(
                        self.want_to_read_list.items()),
                    "Read": list(self.read_list.items()),
                    
                }
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
            except Exception as e:
                print(f"Error: Unable to export data - {e}")

    def update_tree(self, tree, book_list):
        self.clear_tree(tree)
        for book_data in book_list:
            title, author = book_data
            thumbnail = book_list[book_data]
            if thumbnail:
                img = Image.open(requests.get(
                    thumbnail, stream=True).raw)
                img = img.resize((50, 75))
                img = ImageTk.PhotoImage(img)

                item = tree.insert(
                    "", "end", 
                    values=(title, author), 
                    image=img)
                
                tree.item(item, tag=thumbnail)
                self.image_references.append(img)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookCatalogApp(root)
    root.mainloop()
