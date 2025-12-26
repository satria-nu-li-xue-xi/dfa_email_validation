import tkinter as tk
from graphviz import Digraph
from PIL import Image, ImageTk
from src.email_dfa import EmailDFAWithCounter, EmailDFAExpandedStates

zoom_factor = 1.0

def visualize_dfa(email, validator, filename):
    states_path = []
    state = validator.dfa.start_state
    states_path.append(state)
    for ch in email:
        if (state, ch) in validator.dfa.transition:
            state = validator.dfa.transition[(state, ch)]
            states_path.append(state)

    dot = Digraph()
    dot.attr(size="12,9", dpi="200", fontsize="16")
    for i in range(len(states_path)-1):
        dot.edge(states_path[i], states_path[i+1], label=email[i])
    dot.render(filename, format="png", cleanup=True)
    return f"{filename}.png"

def update_images(email):
    validator1 = EmailDFAWithCounter()
    validator2 = EmailDFAExpandedStates()

    result1 = "VALID" if validator1.validate(email) else "INVALID"
    result2 = "VALID" if validator2.validate(email) else "INVALID"
    label_result.config(text=f"WithCounter: {result1}\nExpandedStates: {result2}")

    img1_path = visualize_dfa(email, validator1, "dfa_counter")
    img2_path = visualize_dfa(email, validator2, "dfa_expanded")

    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    w1, h1 = img1.size
    w2, h2 = img2.size
    img1 = img1.resize((int(w1*zoom_factor), int(h1*zoom_factor)))
    img2 = img2.resize((int(w2*zoom_factor), int(h2*zoom_factor)))

    img1_tk = ImageTk.PhotoImage(img1)
    img2_tk = ImageTk.PhotoImage(img2)

    canvas1.create_image(0, 0, anchor="nw", image=img1_tk)
    canvas1.image = img1_tk
    canvas1.config(scrollregion=canvas1.bbox("all"))

    canvas2.create_image(0, 0, anchor="nw", image=img2_tk)
    canvas2.image = img2_tk
    canvas2.config(scrollregion=canvas2.bbox("all"))

def validate_email():
    email = entry.get()
    update_images(email)

def zoom_in():
    global zoom_factor
    zoom_factor += 0.2
    validate_email()

def zoom_out():
    global zoom_factor
    if zoom_factor > 0.4:
        zoom_factor -= 0.2
    validate_email()

# Setup GUI
root = tk.Tk()
root.title("DFA Email Validation")

tk.Label(root, text="Masukkan Email:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)
tk.Button(frame_buttons, text="Validasi", command=validate_email).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Zoom In (+)", command=zoom_in).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Zoom Out (-)", command=zoom_out).pack(side="left", padx=5)

label_result = tk.Label(root, text="Hasil: -")
label_result.pack(pady=10)

# Frame untuk dua canvas bersebelahan
frame_canvases = tk.Frame(root)
frame_canvases.pack(fill="both", expand=True)

# Canvas kiri (WithCounter)
frame_left = tk.Frame(frame_canvases)
frame_left.pack(side="left", fill="both", expand=True)
tk.Label(frame_left, text="DFA WithCounter").pack()
canvas1 = tk.Canvas(frame_left, width=600, height=500)
scroll_x1 = tk.Scrollbar(frame_left, orient="horizontal", command=canvas1.xview)
scroll_y1 = tk.Scrollbar(frame_left, orient="vertical", command=canvas1.yview)
canvas1.configure(xscrollcommand=scroll_x1.set, yscrollcommand=scroll_y1.set)
canvas1.pack(side="left", fill="both", expand=True)
scroll_x1.pack(side="bottom", fill="x")
scroll_y1.pack(side="right", fill="y")

# Canvas kanan (ExpandedStates)
frame_right = tk.Frame(frame_canvases)
frame_right.pack(side="right", fill="both", expand=True)
tk.Label(frame_right, text="DFA ExpandedStates").pack()
canvas2 = tk.Canvas(frame_right, width=600, height=500)
scroll_x2 = tk.Scrollbar(frame_right, orient="horizontal", command=canvas2.xview)
scroll_y2 = tk.Scrollbar(frame_right, orient="vertical", command=canvas2.yview)
canvas2.configure(xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)
canvas2.pack(side="left", fill="both", expand=True)
scroll_x2.pack(side="bottom", fill="x")
scroll_y2.pack(side="right", fill="y")

root.mainloop()