
import tkinter as tk

root = tk.Tk()
root.title("Keyboard Input Test")
root.geometry("450x200")

label = tk.Label(
    root,
    text="Click the box and type Hello",
    font=("Arial", 12)
)
label.pack(pady=15)

entry = tk.Entry(root, font=("Arial", 16))
entry.pack(padx=20, fill="x")
entry.focus_force()

button = tk.Button(
    root,
    text="Test Input",
    command=lambda: label.config(
        text="You typed: " + entry.get()
    )
)
button.pack(pady=15)

root.mainloop()