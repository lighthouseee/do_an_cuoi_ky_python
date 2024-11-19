from CRUD.CRUD import read_csv_data, create_data, update_data, delete_data, paginate_data
from Tool.tool import sort_data, search_data, filter_data, filter_depression_risk
import pandas as pd

CSV_FILE = "cleaned_and_predicted_data.csv"

def main():
    # Tải dữ liệu ban đầu
    data = pd.DataFrame(read_csv_data())
    while True:
        print("\nMenu:")
        print("1. Xem dữ liệu")
        print("2. Thêm dữ liệu")
        print("3. Cập nhật dữ liệu")
        print("4. Xóa dữ liệu")
        print("5. Sắp xếp dữ liệu")
        print("6. Tìm kiếm dữ liệu")
        print("7. Lọc dữ liệu")
        print("8. Lọc rủi ro trầm cảm cao")
        print("9. Thoát")
        choice = input("Chọn thao tác: ").strip()

        if choice == "1":
            page_size = int(input("Nhập số dòng mỗi trang: "))
            paginate_data(data, page_size)

        elif choice == "2":
            new_entry = {col: input(f"Nhập {col}: ").strip() for col in data.columns}
            create_data(data.to_dict("records"), new_entry)
            print("Thêm dữ liệu thành công!")

        elif choice == "3":
            target_name = input("Nhập tên cần cập nhật: ").strip()
            updated_entry = {col: input(f"Nhập {col} mới (hoặc Enter để bỏ qua): ").strip() for col in data.columns}
            updated_entry = {k: v for k, v in updated_entry.items() if v}
            if update_data(data.to_dict("records"), target_name, updated_entry):
                print("Cập nhật thành công!")
            else:
                print("Không tìm thấy dữ liệu!")

        elif choice == "4":
            target_names = input("Nhập tên cần xóa (phân cách bằng dấu phẩy): ").split(", ")
            if delete_data(data.to_dict("records"), target_names):
                print("Xóa thành công!")
            else:
                print("Không tìm thấy dữ liệu để xóa!")

        elif choice == "5":  # Sắp xếp dữ liệu
            sorted_data = sort_data(data)
            print("Dữ liệu sau khi sắp xếp:")
            page_size = int(input("Nhập số dòng mỗi trang: "))
            paginate_data(sorted_data, page_size)

        elif choice == "6":  # Tìm kiếm dữ liệu
            search_result = search_data(data)
            print("Kết quả tìm kiếm:")
            page_size = int(input("Nhập số dòng mỗi trang: "))
            paginate_data(search_result, page_size)

        elif choice == "7":  # Lọc dữ liệu theo điều kiện
            filtered_data = filter_data(data)
            print("Kết quả lọc dữ liệu:")
            page_size = int(input("Nhập số dòng mỗi trang: "))
            paginate_data(filtered_data, page_size)

        elif choice == "8":  # Lọc theo nguy cơ trầm cảm cao
            risk_data = filter_depression_risk(data)
            print("Dữ liệu lọc theo nguy cơ trầm cảm cao:")
            page_size = int(input("Nhập số dòng mỗi trang: "))
            paginate_data(risk_data, page_size)

        elif choice == "9":
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()