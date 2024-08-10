import pandas as pd
from datetime import datetime
from tkinter import filedialog, messagebox
import os

def export_to_excel(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM materials")
    rows = cur.fetchall()

    if not rows:
        messagebox.showinfo("Export to Excel", "No materials found.")
        return

    df = pd.DataFrame(rows, columns=["ID", "Name", "Barcode", "Quantity", "Unit"])

    # Генерация имени файла по умолчанию с текущей датой и временем
    now = datetime.now()
    default_filename = f"materials_report_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Save as",
        initialfile=default_filename
    )

    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Export to Excel", f"Report exported to {file_path}")
        
        # Открытие файла после экспорта
        try:
            os.startfile(file_path)
        except AttributeError:
            os.system(f"open '{file_path}'")  # для macOS и Linux
