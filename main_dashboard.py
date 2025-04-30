import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

def clean_dataset(file_path):
    df = pd.read_excel(file_path)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

        if "date" in col:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass

    if not os.path.exists("cleaned_data"):
        os.makedirs("cleaned_data")

    df.to_csv("cleaned_data/cleaned_output.csv", index=False)
    return df

def generate_charts(df):
    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    for col in df.columns:
        plt.figure(figsize=(8, 4))
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col].plot(kind="hist", bins=20, color="skyblue", edgecolor="black")
            plt.title(f"Histogram of {col}")
        else:
            value_counts = df[col].value_counts().head(10)
            value_counts.plot(kind="bar", color="orange", edgecolor="black")
            plt.title(f"Top Categories in {col}")
        plt.tight_layout()
        plt.savefig(f"graphs/{col}.png")
        plt.close()

def load_images():
    return [f for f in os.listdir("graphs") if f.endswith(".png")]

def show_image(index):
    image_path = os.path.join("graphs", images[index])
    image = Image.open(image_path)
    image = image.resize((700, 400))
    img_display = ImageTk.PhotoImage(image)

    img_label.config(image=img_display)
    img_label.image = img_display
    window.title(f"Graph Viewer - {images[index]}")

def next_image():
    global current_index
    current_index = (current_index + 1) % len(images)
    show_image(current_index)

def prev_image():
    global current_index
    current_index = (current_index - 1) % len(images)
    show_image(current_index)

# Step 1: File picker
file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])
if not file_path:
    print("No file selected.")
    exit()

# Step 2: Clean + Analyze
df = clean_dataset(file_path)
generate_charts(df)

# Step 3: GUI
window = tk.Tk()
window.geometry("800x550")
window.title("Graph Viewer")

img_label = Label(window)
img_label.pack(pady=20)

btn_frame = tk.Frame(window)
btn_frame.pack()

Button(btn_frame, text="Previous", command=prev_image, width=15).pack(side="left", padx=20)
Button(btn_frame, text="Next", command=next_image, width=15).pack(side="right", padx=20)

images = load_images()
current_index = 0

if images:
    show_image(current_index)
else:
    img_label.config(text="No charts found.")

window.mainloop()
