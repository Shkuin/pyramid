import tkinter as tk
from tkinter import filedialog
import os
import shutil
import socket

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Форма заявки")
        self.set_fixed_window_size()

        self.photos = []  # Список для хранения выбранных фотографий

        self.create_widgets()

    def set_fixed_window_size(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.6)

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)

        self.root.update_idletasks()
        window_x = (screen_width - self.root.winfo_width()) // 2
        window_y = (screen_height - self.root.winfo_height()) // 2
        self.root.geometry(f"+{window_x}+{window_y}")

        self.root.focus_force()

    def create_widgets(self):
        fio_label = tk.Label(self.root, text="ФИО:")
        fio_label.pack(anchor="w", padx=10, pady=10)
        self.fio_entry = tk.Entry(self.root)
        self.fio_entry.pack(fill="x", padx=10)

        company_label = tk.Label(self.root, text="Наименование компании:")
        company_label.pack(anchor="w", padx=10, pady=10)
        self.company_entry = tk.Entry(self.root)
        self.company_entry.pack(fill="x", padx=10)

        cabinet_label = tk.Label(self.root, text="Кабинет:")
        cabinet_label.pack(anchor="w", padx=10, pady=10)
        self.cabinet_entry = tk.Entry(self.root)
        self.cabinet_entry.pack(fill="x", padx=10)

        description_label = tk.Label(self.root, text="Описание проблемы:")
        description_label.pack(anchor="w", padx=10, pady=10)
        self.description_text = tk.Text(self.root, height=5)
        self.description_text.pack(fill="both", padx=10)

        dates_label = tk.Label(self.root, text="Сроки (от и до):")
        dates_label.pack(anchor="w", padx=10, pady=10)
        self.dates_entry = tk.Entry(self.root)
        self.dates_entry.pack(fill="x", padx=10)

        self.add_photo_button = tk.Button(self.root, text="Добавить фото", command=self.attach_photo)
        self.add_photo_button.pack(padx=10, pady=10)

        self.submit_button = tk.Button(self.root, text="Сформировать заявку", command=self.create_request)
        self.submit_button.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="", fg="green", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

    def attach_photo(self):
        filenames = filedialog.askopenfilenames()
        for filename in filenames:
            self.photos.append(filename)

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    
    def create_request(self):
        fio = self.fio_entry.get()
        company = self.company_entry.get()
        cabinet = self.cabinet_entry.get()
        ip = self.get_ip_address()
        description = self.description_text.get("1.0", tk.END).strip()
        dates = self.dates_entry.get()

        if fio and company and cabinet and description:

            check_the_same_name = True
            number = 0
            while check_the_same_name:
                if number==0:
                    folder_name = company
                    folder_name += "(" + dates + ")"
                    folder_name = folder_name.replace(" ", "_")
                else:
                    folder_name = company
                    folder_name += ("(" + dates + ")")
                    folder_name += ("-" + str(number))
                    folder_name = folder_name.replace(" ", "_")

                folder_path = os.path.join(os.path.expanduser("~/Desktop"), folder_name)
                # Создание папки заявки на рабочем столе
                folder_path = os.path.join(os.path.expanduser("~/Desktop"), folder_name)
                try:
                    os.makedirs(folder_path, exist_ok=False)
                except FileExistsError:
                    number+=1
                else:
                    check_the_same_name = False

            # Создание текстового файла заявки
            file_path = os.path.join(folder_path, "Заявка.txt")
            with open(file_path, "w") as file:
                file.write(f"От: {fio}\nКабинет: {cabinet}\nIP: {ip}\n___________Описание___________\n")
                file.write(description)

            # Создание папки "Фото проблемы"
            photo_folder_path = os.path.join(folder_path, "Фото проблемы")
            os.makedirs(photo_folder_path)

            # Копирование выбранных фотографий в папку "Фото проблемы"
            for photo in self.photos:
                photo_name = os.path.basename(photo)
                destination_path = os.path.join(photo_folder_path, photo_name)
                shutil.copy(photo, destination_path)

            self.status_label.config(text="Ваша заявка успешно создана", fg="green")
            self.reset_form()
        else:
            self.status_label.config(text="Вы заполнили не все поля", fg="red")

    def reset_form(self):
        self.fio_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.cabinet_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.dates_entry.delete(0, tk.END)
        self.photos = []

    def run(self):
        self.root.mainloop()

app = Application()
app.run()
