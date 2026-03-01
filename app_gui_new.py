import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

MODEL_PATH = "eq_model_bundle_new.pkl"

# Load model
def load_model():
    if not os.path.exists(MODEL_PATH):
        # Only show messagebox if tkinter is available
        try:
            messagebox.showerror("Error", f"Model not found: {MODEL_PATH}")
        except:
            pass
        return None
    return joblib.load(MODEL_PATH)

model = None  # Will be initialized in main()

# -----------------------------------------------------------------------

def get_strength_category(mag):
    if mag < 3.0:
        return "WEAK", "green"
    elif mag < 4.5:
        return "MODERATE", "yellow"
    elif mag < 6.0:
        return "STRONG", "orange"
    else:
        return "SEVERE", "red"

def plot_gauge(mag):
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Draw colored sectors
    ax.barh(1, width=np.pi/6, left=np.pi*0/6, color="green")
    ax.barh(1, width=np.pi/6, left=np.pi*1/6, color="yellow")
    ax.barh(1, width=np.pi/6, left=np.pi*2/6, color="orange")
    ax.barh(1, width=np.pi/6, left=np.pi*3/6, color="red")

    # Needle
    angle = (mag / 10) * np.pi
    ax.arrow(angle, 0, 0, 1, width=0.02, color="black")

    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title(f"Predicted Magnitude: {mag:.2f}", fontsize=16)
    plt.show()

# -----------------------------------------------------------------------

def predict_output():
    try:
        values = [float(entry.get()) for entry in entries]
    except ValueError:
        messagebox.showerror("Error", "Please enter numeric values only")
        return

    X = np.array([values])
    mag = model.predict(X)[0]

    strength, color = get_strength_category(mag)
    probability = round(min(max(mag / 10, 0), 1), 3)

    output_mag.config(text=f"Predicted Magnitude: {mag:.2f}")
    output_strength.config(text=f"Strength: {strength}", fg=color)
    output_prob.config(text=f"Strong Probability: {probability}")

    if strength == "WEAK":
        summary = "Intensity: Very Light\nDamage: None\nImpact: Minimal"
    elif strength == "MODERATE":
        summary = "Intensity: Light\nDamage: Low\nImpact: Minimal"
    elif strength == "STRONG":
        summary = "Intensity: Moderate\nDamage: Noticeable\nImpact: Medium"
    else:
        summary = "Intensity: Severe\nDamage: High\nImpact: Significant"

    output_summary.config(text=f"Earthquake Summary:\n{summary}")

    plot_gauge(mag)

def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)
    output_mag.config(text="")
    output_strength.config(text="")
    output_prob.config(text="")
    output_summary.config(text="")

# -----------------------------------------------------------------------

def main():
    global model, root, entries, output_mag, output_strength, output_prob, output_summary, btn_frame, predict_btn, clear_btn
    
    model = load_model()
    
    root = tk.Tk()
    root.title("Earthquake Predictor")
    root.geometry("600x650")
    root.configure(bg="white")

    title = tk.Label(root, text="Earthquake Predictor",
                     font=("Arial", 20, "bold"), bg="white")
    title.pack(pady=10)

    sub = tk.Label(root, text="Enter the input features:",
                   font=("Arial", 14), bg="white")
    sub.pack()

    frame = tk.Frame(root, bg="white")
    frame.pack()

    fields = ["Longitude", "Latitude", "Depth", "HD", "PS", "SAR Coherence", "Displacement"]
    entries = []

    for f in fields:
        lbl = tk.Label(frame, text=f, font=("Arial", 12), bg="white")
        lbl.grid(row=fields.index(f), column=0, pady=8, padx=5)

        ent = tk.Entry(frame, font=("Arial", 12), width=20)
        ent.grid(row=fields.index(f), column=1)
        entries.append(ent)

    # OUTPUT AREA
    output_mag = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="white")
    output_mag.pack(pady=10)

    output_strength = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="white")
    output_strength.pack()

    output_prob = tk.Label(root, text="", font=("Arial", 14), bg="white")
    output_prob.pack()

    output_summary = tk.Label(root, text="", font=("Arial", 14), bg="white")
    output_summary.pack(pady=10)

    # BUTTONS
    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(pady=20)

    predict_btn = tk.Button(btn_frame, text="Predict", font=("Arial", 12, "bold"),
                            width=10, command=predict_output)
    predict_btn.grid(row=0, column=0, padx=10)

    clear_btn = tk.Button(btn_frame, text="Clear", font=("Arial", 12, "bold"),
                          width=10, command=clear_fields)
    clear_btn.grid(row=0, column=1, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()