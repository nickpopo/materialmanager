import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from src.gui import MaterialManagerApp
from sqlite3 import Error

class TestMaterialManagerApp(unittest.TestCase):
    def setUp(self):
        # Создаем корневой элемент Tkinter и инициализируем приложение
        self.root = tk.Tk()
        self.app = MaterialManagerApp(self.root)
    
    def tearDown(self):
        # Закрываем окно после каждого теста
        self.root.destroy()

    @patch('src.gui.create_connection')
    @patch('src.gui.create_tables')
    def test_initialization(self, mock_create_tables, mock_create_connection):
        # Проверяем, что создается соединение с базой данных и вызывается создание таблиц
        mock_create_connection.assert_called_once()
        mock_create_tables.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    @patch('sqlite3.connect')
    def test_login_invalid_credentials(self, mock_connect, mock_showerror):
        # Мокируем поведение базы данных
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # Заполняем поля ввода и нажимаем кнопку "Login"
        self.app.username_entry.insert(0, "wrong_user")
        self.app.password_entry.insert(0, "wrong_pass")
        self.app.login()

        # Проверяем, что было показано сообщение об ошибке
        mock_showerror.assert_called_once_with("Error", "Invalid credentials")

    @patch('tkinter.messagebox.showinfo')
    @patch('sqlite3.connect')
    def test_register_user_success(self, mock_connect, mock_showinfo):
        # Мокируем поведение базы данных
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Заполняем поля ввода и вызываем регистрацию
        self.app.username_entry.insert(0, "new_user")
        self.app.password_entry.insert(0, "new_pass")
        self.app.register()

        # Проверяем, что пользователь успешно зарегистрирован
        mock_showinfo.assert_called_once_with("Success", "User registered successfully")
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, password) VALUES (?, ?)", ("new_user", "new_pass"))

    @patch('tkinter.messagebox.showerror')
    @patch('sqlite3.connect')
    def test_register_user_already_exists(self, mock_connect, mock_showerror):
        # Мокируем поведение базы данных, чтобы выбросить ошибку
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Error("Username already exists")

        # Заполняем поля ввода и вызываем регистрацию
        self.app.username_entry.insert(0, "existing_user")
        self.app.password_entry.insert(0, "existing_pass")
        self.app.register()

        # Проверяем, что показывается ошибка о существующем пользователе
        mock_showerror.assert_called_once_with("Error", "Username already exists")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.simpledialog.askinteger')
    def test_add_material(self, mock_askinteger, mock_askstring, mock_showinfo):
        # Мокируем ввод данных пользователем
        mock_askstring.side_effect = ["Material A", "123456"]
        mock_askinteger.return_value = 10

        # Запускаем добавление материала
        self.app.add_material()

        # Проверяем, что добавление материала произошло корректно
        mock_showinfo.assert_called_once_with("Success", "Material added successfully")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.simpledialog.askinteger')
    @patch('tkinter.ttk.Treeview.selection')
    def test_update_material(self, mock_selection, mock_askstring, mock_askinteger, mock_showinfo):
        # Мокируем выбор и ввод данных пользователем
        mock_selection.return_value = ["mock_item"]
        mock_askstring.side_effect = ["Material A Updated", "654321"]
        mock_askinteger.return_value = 20

        # Запускаем обновление материала
        self.app.update_material()

        # Проверяем, что обновление материала произошло корректно
        mock_showinfo.assert_called_once_with("Success", "Material updated successfully")

    @patch('tkinter.messagebox.showwarning')
    @patch('tkinter.ttk.Treeview.selection')
    def test_update_material_no_selection(self, mock_selection, mock_showwarning):
        # Мокируем отсутствие выбора материала пользователем
        mock_selection.return_value = []

        # Запускаем обновление материала
        self.app.update_material()

        # Проверяем, что было показано предупреждение
        mock_showwarning.assert_called_once_with("Warning", "Select a material to update")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.ttk.Treeview.selection')
    def test_delete_material(self, mock_selection, mock_showinfo):
        # Мокируем выбор материала пользователем
        mock_selection.return_value = ["mock_item"]

        # Запускаем удаление материала
        self.app.delete_material()

        # Проверяем, что удаление материала произошло корректно
        mock_showinfo.assert_called_once_with("Success", "Material deleted successfully")

    @patch('tkinter.messagebox.showwarning')
    @patch('tkinter.ttk.Treeview.selection')
    def test_delete_material_no_selection(self, mock_selection, mock_showwarning):
        # Мокируем отсутствие выбора материала пользователем
        mock_selection.return_value = []

        # Запускаем удаление материала
        self.app.delete_material()

        # Проверяем, что было показано предупреждение
        mock_showwarning.assert_called_once_with("Warning", "Select a material to delete")

    @patch('tkinter.messagebox.showinfo')
    @patch('src.report.export_to_excel')
    def test_export_to_excel(self, mock_export_to_excel, mock_showinfo):
        # Проверяем, что при вызове экспорта в Excel вызывается соответствующая функция
        self.app.view_inventory_report()
        mock_export_to_excel.assert_called_once()

if __name__ == "__main__":
    unittest.main()
