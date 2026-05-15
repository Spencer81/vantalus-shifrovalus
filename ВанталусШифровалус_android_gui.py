import tkinter as tk
from tkinter import scrolledtext, messagebox
import jnius

# --- Android clipboard via JNIus ---
def copy_to_clipboard(text):
    try:
        PythonActivity = jnius.autoclass('org.kivy.android.PythonActivity')
        Context = jnius.autoclass('android.content.Context')
        activity = PythonActivity.mActivity
        clipboard = activity.getSystemService(Context.CLIPBOARD_SERVICE)
        ClipData = jnius.autoclass('android.content.ClipData')
        clip = ClipData.newPlainText("text", text)
        clipboard.setPrimaryClip(clip)
    except Exception as e:
        raise Exception(f"Ошибка копирования: {e}")

def paste_from_clipboard():
    try:
        PythonActivity = jnius.autoclass('org.kivy.android.PythonActivity')
        Context = jnius.autoclass('android.content.Context')
        activity = PythonActivity.mActivity
        clipboard = activity.getSystemService(Context.CLIPBOARD_SERVICE)
        clip = clipboard.getPrimaryClip()
        if clip and clip.getItemCount() > 0:
            return clip.getItemAt(0).getText().toString()
        return ""
    except Exception as e:
        raise Exception(f"Ошибка вставки: {e}")

# --- Cipher table ---
REPLACE_TABLE = {
    'А': '丹', 'Б': '石', 'В': '归', 'Г': '厂', 'Д': '亼',
    'Е': '仨', 'Ё': '仨̈', 'Ж': '米', 'З': 'З', 'И': '认',
    'Й': '认̆', 'К': '长', 'Л': '几', 'М': '从', 'Н': '廾',
    'О': '口', 'П': '冂', 'Р': '尸', 'С': '匚', 'Т': '丁',
    'У': '丫', 'Ф': '中', 'Х': '乂', 'Ц': '凵', 'Ч': '丩',
    'Ш': '山', 'Щ': '山', 'Ъ': 'Ꙏ', 'Ы': 'ꙎI', 'Ь': 'Ꙏ',
    'Э': '彐', 'Ю': '仰', 'Я': '牙'
}

def encrypt(text: str) -> str:
    return ''.join(REPLACE_TABLE.get(ch.upper(), ch) for ch in text)

# --- GUI callbacks ---
def do_encrypt(in_widget, out_widget):
    txt = in_widget.get("1.0", tk.END).rstrip('\n')
    if not txt:
        messagebox.showinfo("Инфо", "Введите текст в верхнем поле.")
        return
    out_widget.delete("1.0", tk.END)
    out_widget.insert(tk.END, encrypt(txt))

def paste_from_clipboard_gui(in_widget):
    try:
        text = paste_from_clipboard()
        if text:
            in_widget.insert(tk.INSERT, text)
        else:
            messagebox.showwarning("Внимание", "Буфер обмена пуст.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось вставить:\n{e}")

def copy_result_to_clipboard_gui(out_widget):
    text = out_widget.get("1.0", tk.END).rstrip('\n')
    if text:
        try:
            copy_to_clipboard(text)
            messagebox.showinfo("Успех", "Скопировано в буфер.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать:\n{e}")
    else:
        messagebox.showwarning("Внимание", "Нечего копировать.")

def clear_all(in_widget, out_widget):
    in_widget.delete("1.0", tk.END)
    out_widget.delete("1.0", tk.END)

# --- Main window ---
def main():
    root = tk.Tk()
    root.title("归丹廾丁丹几丫匚-山认中尸口归丹几丫匚")
    root.geometry("750x600")

    tk.Label(root, text="🔽 Исходный текст (русский):", font=("Arial", 10, "bold")).pack(pady=(10,0))
    text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Courier", 12))
    text_input.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Кнопки в ряд
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    btn_encrypt = tk.Button(btn_frame, text="Зашифровать", command=lambda: do_encrypt(text_input, text_output),
                            bg="#4CAF50", fg="white", padx=6, pady=2)
    btn_encrypt.pack(side=tk.LEFT, padx=3)

    btn_paste = tk.Button(btn_frame, text="Вставить", command=lambda: paste_from_clipboard_gui(text_input),
                          padx=6, pady=2)
    btn_paste.pack(side=tk.LEFT, padx=3)

    btn_copy = tk.Button(btn_frame, text="Скопировать", command=lambda: copy_result_to_clipboard_gui(text_output),
                         bg="#2196F3", fg="white", padx=6, pady=2)
    btn_copy.pack(side=tk.LEFT, padx=3)

    btn_clear = tk.Button(btn_frame, text="Очистить", command=lambda: clear_all(text_input, text_output),
                          padx=6, pady=2)
    btn_clear.pack(side=tk.LEFT, padx=3)

    tk.Label(root, text="🔼 Зашифрованный текст:", font=("Arial", 10, "bold")).pack(pady=(10,0))
    text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Courier", 12))
    text_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
