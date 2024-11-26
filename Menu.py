import tkinter as tk
from tkinter import ttk, messagebox
from crud.CRUD import read_csv_data, paginate_data, create_data, update_data
import pandas as pd

CSV_FILE = "cleaned_and_predicted_data.csv"

VALID_VALUES = {
    "Smoking Status": ["Non-smoker", "Former", "Current"],
    "Physical Activity Level": ["Sedentary", "Moderate", "Active"],
    "Employment Status": ["Employed", "Unemployed"],
    "Alcohol Consumption": ["Low", "Moderate", "High"],
    "Dietary Habits": ["Healthy", "Moderate", "Unhealthy"],
    "Sleep Patterns": ["Poor", "Good", "Fair"],
    "History of Mental Illness": ["Yes", "No"],
    "History of Substance Abuse": ["Yes", "No"],
    "Family History of Depression": ["Yes", "No"],
    "Chronic Medical Conditions": ["Yes", "No"],
    "Marital Status": ["Single", "Married", "Divorced", "Widowed"],
    "Education Level": ["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree", "PhD"],
    "Depression Risk": ["Low", "Medium", "High", "Very High"]
}

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý dữ liệu")
        self.root.geometry("1200x600")

        # Đọc dữ liệu từ file CSV
        self.data = read_csv_data()
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1

        # Khung Treeview và thanh cuộn
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=list(self.data.columns), show="headings", height=20)
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scroll.set)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Menu chức năng
        self.menu_frame = ttk.Frame(root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Button(self.menu_frame, text="Xem dữ liệu", command=self.view_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Thêm dữ liệu", command=self.add_new_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Tìm kiếm dữ liệu", command=self.open_search_window).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Cập nhật dữ liệu", command=self.update_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Thoát", command=root.quit).pack(side=tk.RIGHT, padx=10)

        # Điều hướng trang
        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.prev_button = ttk.Button(self.nav_frame, text="Trang trước", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.page_entry = ttk.Entry(self.nav_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=5)

        self.goto_button = ttk.Button(self.nav_frame, text="Đi tới trang", command=self.goto_page)
        self.goto_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.nav_frame, text="Trang sau", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.pagination_label = ttk.Label(root, text="Trang: 1/1", font=("Arial", 10))
        self.pagination_label.pack(side=tk.BOTTOM, pady=5)

        self.update_treeview()

    def update_treeview(self):
        try:
            page_data, self.total_pages = paginate_data(self.data, self.page_size, self.current_page)
            for row in self.tree.get_children():
                self.tree.delete(row)
            for _, row in page_data.iterrows():
                self.tree.insert("", tk.END, values=list(row))
            self.pagination_label.config(text=f"Trang: {self.current_page}/{self.total_pages}")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def view_data(self):
        def set_page_size():
            try:
                page_size = int(entry.get())
                if page_size <= 0:
                    raise ValueError("Số dòng mỗi trang phải lớn hơn 0.")
                self.page_size = page_size
                self.current_page = 1
                self.update_treeview()
                view_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Số dòng mỗi trang phải là số nguyên dương.")

        view_window = tk.Toplevel(self.root)
        view_window.title("Xem dữ liệu")
        view_window.geometry("300x150")

        ttk.Label(view_window, text="Nhập số dòng mỗi trang:").pack(pady=10)
        entry = ttk.Entry(view_window)
        entry.pack(pady=5)

        ttk.Button(view_window, text="Xác nhận", command=set_page_size).pack(pady=10)

    def add_new_data(self):
        def save_data():
            new_data = {}
            errors = []
            for col, widget in widgets.items():
                value = widget.get().strip()
                if col == "Age":
                    if not value.isdigit() or not (0 <= int(value) <= 120):
                        errors.append(f"Trường '{col}' phải là số từ 0 đến 120.")
                    else:
                        new_data[col] = int(value)
                elif col == "Income":
                    if not value.replace('.', '', 1).isdigit() or float(value) < 0:
                        errors.append(f"Trường '{col}' phải là số không âm.")
                    else:
                        new_data[col] = float(value)
                elif col in VALID_VALUES and value not in VALID_VALUES[col]:
                    errors.append(f"Trường '{col}' phải thuộc {VALID_VALUES[col]}.")
                else:
                    new_data[col] = value

            if errors:
                messagebox.showerror("Lỗi nhập liệu", "\n".join(errors))
                return

            self.data = create_data(self.data, new_data)
            self.current_page = 1
            self.update_treeview()
            messagebox.showinfo("Thành công", "Dữ liệu mới đã được thêm.")
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm dữ liệu mới")
        add_window.geometry("600x600")

        widgets = {}
        for i, col in enumerate(self.data.columns):
            ttk.Label(add_window, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            if col in VALID_VALUES:
                widget = ttk.Combobox(add_window, values=VALID_VALUES[col], state="readonly")
                widget.grid(row=i, column=1, padx=10, pady=5)
            else:
                widget = ttk.Entry(add_window, width=30)
                widget.grid(row=i, column=1, padx=10, pady=5)
            widgets[col] = widget

        ttk.Button(add_window, text="Lưu", command=save_data).grid(row=len(self.data.columns), column=0, columnspan=2, pady=10)

    def search_records(self, column, value):
        if column not in self.data.columns:
            messagebox.showerror("Lỗi", f"Cột '{column}' không tồn tại.")
            return pd.DataFrame()
        return self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]

    def open_search_window(self):
        """
        Mở cửa sổ tìm kiếm để người dùng tìm theo bất kỳ cột nào.
        """
        def perform_search():
            column = column_combobox.get()
            value = value_entry.get().strip()
            if not column or not value:
                messagebox.showerror("Lỗi", "Vui lòng chọn cột và nhập giá trị cần tìm.")
                return
            results = self.search_records(column, value)
            if results.empty:
                messagebox.showinfo("Kết quả", "Không tìm thấy bản ghi nào phù hợp.")
            else:
                for row in results_tree.get_children():
                    results_tree.delete(row)
                for idx, row in results.iterrows():
                    results_tree.insert("", tk.END, values=list(row), tags=(idx,))
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} bản ghi.")

        # Cửa sổ tìm kiếm
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm dữ liệu")
        search_window.geometry("800x500")

        ttk.Label(search_window, text="Chọn cột để tìm kiếm:").pack(pady=5)
        column_combobox = ttk.Combobox(search_window, values=list(self.data.columns), state="readonly")
        column_combobox.pack(pady=5)

        ttk.Label(search_window, text="Nhập giá trị cần tìm:").pack(pady=5)
        value_entry = ttk.Entry(search_window, width=30)
        value_entry.pack(pady=5)

        ttk.Button(search_window, text="Tìm kiếm", command=perform_search).pack(pady=10)

        # Frame chứa Treeview và thanh cuộn
        results_frame = ttk.Frame(search_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview hiển thị kết quả tìm kiếm
        results_tree = ttk.Treeview(results_frame, columns=list(self.data.columns), show="headings", height=15)
        for col in self.data.columns:
            results_tree.heading(col, text=col)
            results_tree.column(col, width=100, anchor=tk.CENTER)

        results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thanh cuộn dọc cho Treeview
        v_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Thanh cuộn ngang cho Treeview
        h_scroll = ttk.Scrollbar(search_window, orient=tk.HORIZONTAL, command=results_tree.xview)
        results_tree.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    def update_data(self):
        def find_records():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên để tìm kiếm.")
                return
            results = self.search_records("Name", name)
            if results.empty:
                messagebox.showinfo("Kết quả", "Không tìm thấy bản ghi nào phù hợp.")
            else:
                for row in results_tree.get_children():
                    results_tree.delete(row)
                for idx, row in results.iterrows():
                    results_tree.insert("", tk.END, values=list(row), tags=(idx,))

        def select_record(event):
            selected_item = results_tree.selection()
            if not selected_item:
                return
            record_index = int(results_tree.item(selected_item)["tags"][0])
            open_update_window(record_index)

        def open_update_window(record_index):
            update_window = tk.Toplevel(self.root)
            update_window.title("Cập nhật dữ liệu")
            update_window.geometry("600x600")
            record_data = self.data.loc[record_index]
            widgets = {}
            for i, col in enumerate(self.data.columns):
                ttk.Label(update_window, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
                if col in VALID_VALUES:
                    widget = ttk.Combobox(update_window, values=VALID_VALUES[col], state="readonly")
                    widget.set(record_data[col])
                    widget.grid(row=i, column=1, padx=10, pady=5)
                else:
                    widget = ttk.Entry(update_window, width=30)
                    widget.insert(0, str(record_data[col]))
                    widget.grid(row=i, column=1, padx=10, pady=5)
                widgets[col] = widget

            def save_changes():
                updated_entry = {}
                errors = []
                for col, widget in widgets.items():
                    value = widget.get().strip()
                    if col == "Age":
                        if not value.isdigit() or not (0 <= int(value) <= 120):
                            errors.append(f"Trường '{col}' phải là số từ 0 đến 120.")
                        else:
                            updated_entry[col] = int(value)
                    elif col == "Income":
                        if not value.replace('.', '', 1).isdigit() or float(value) < 0:
                            errors.append(f"Trường '{col}' phải là số không âm.")
                        else:
                            updated_entry[col] = float(value)
                    elif col in VALID_VALUES and value not in VALID_VALUES[col]:
                        errors.append(f"Trường '{col}' phải thuộc {VALID_VALUES[col]}.")
                    else:
                        updated_entry[col] = value

                if errors:
                    messagebox.showerror("Lỗi nhập liệu", "\n".join(errors))
                    return

                for col, value in updated_entry.items():
                    if pd.api.types.is_numeric_dtype(self.data[col]):
                        self.data.at[record_index, col] = pd.to_numeric(value, errors="coerce")
                    else:
                        self.data.at[record_index, col] = value

                self.data.to_csv(CSV_FILE, index=False)
                self.update_treeview()
                messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công.")
                update_window.destroy()
                search_window.destroy()

            ttk.Button(update_window, text="Lưu", command=save_changes).grid(row=len(self.data.columns), column=0, columnspan=2, pady=10)

        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm và chọn bản ghi")
        search_window.geometry("800x400")

        ttk.Label(search_window, text="Nhập tên để tìm kiếm:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(search_window, width=30)
        name_entry.pack(padx=10, pady=5)

        ttk.Button(search_window, text="Tìm kiếm", command=find_records).pack(pady=10)

        results_frame = ttk.Frame(search_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        results_tree = ttk.Treeview(results_frame, columns=list(self.data.columns), show="headings", height=10)
        for col in self.data.columns:
            results_tree.heading(col, text=col)
            results_tree.column(col, width=100, anchor=tk.CENTER)

        results_tree.pack(fill=tk.BOTH, expand=True)
        results_tree.bind("<Double-1>", select_record)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_treeview()
        else:
            messagebox.showinfo("Thông báo", "Đây là trang cuối cùng.")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_treeview()
        else:
            messagebox.showinfo("Thông báo", "Đây là trang đầu tiên.")

    def goto_page(self):
        try:
            page = int(self.page_entry.get())
            if page < 1 or page > self.total_pages:
                raise ValueError("Trang không hợp lệ.")
            self.current_page = page
            self.update_treeview()
        except ValueError:
            messagebox.showerror("Lỗi", "Số trang phải là số nguyên hợp lệ trong khoảng.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
