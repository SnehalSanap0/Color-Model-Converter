import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import colorsys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from tkinter import font as tkfont

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    return colorsys.rgb_to_hsv(r, g, b)

# Function to convert HSV to RGB
def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

# Function to convert RGB to CMY
def rgb_to_cmy(r, g, b):
    c = 255 - r
    m = 255 - g
    y = 255 - b
    return c, m, y

# Function to convert CMY to RGB
def cmy_to_rgb(c, m, y):
    r = 255 - c
    g = 255 - m
    b = 255 - y
    return int(r), int(g), int(b)

# Function to update the display color based on RGB sliders
def update_color_from_rgb(*args):
    try:
        r = int(r_slider.get())
        g = int(g_slider.get())
        b = int(b_slider.get())
        
        # Set the color preview
        color_preview.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
        
        # Update RGB label
        rgb_label.configure(text=f"RGB: ({r}, {g}, {b})")
        
        # Convert RGB to HSV and CMY, then update the sliders
        h, s, v = rgb_to_hsv(r, g, b)
        h_slider.set(int(h * 360))
        s_slider.set(int(s * 100))
        v_slider.set(int(v * 100))
        
        c, m, y = rgb_to_cmy(r, g, b)
        c_slider.set(int(c))
        m_slider.set(int(m))
        y_slider.set(int(y))
    except Exception as e:
        print(f"Error in update_color_from_rgb: {e}")

# Function to update the display color based on HSV sliders
def update_color_from_hsv(*args):
    try:
        h = int(h_slider.get()) / 360.0
        s = int(s_slider.get()) / 100.0
        v = int(v_slider.get()) / 100.0
        
        # Convert HSV to RGB
        r, g, b = hsv_to_rgb(h, s, v)
        
        # Set the color preview
        color_preview.configure(bg=f'#{int(r):02x}{int(g):02x}{int(b):02x}')
        
        # Update RGB label
        rgb_label.configure(text=f"RGB: ({int(r)}, {int(g)}, {int(b)})")
        
        # Update the RGB sliders
        r_slider.set(int(r))
        g_slider.set(int(g))
        b_slider.set(int(b))

        # Update CMY sliders
        c, m, y = rgb_to_cmy(int(r), int(g), int(b))
        c_slider.set(int(c))
        m_slider.set(int(m))
        y_slider.set(int(y))
    except Exception as e:
        print(f"Error in update_color_from_hsv: {e}")

# Function to update the display color based on CMY sliders
def update_color_from_cmy(*args):
    try:
        c = int(c_slider.get())
        m = int(m_slider.get())
        y = int(y_slider.get())

        # Convert CMY to RGB
        r, g, b = cmy_to_rgb(c, m, y)

        # Set the color preview
        color_preview.configure(bg=f'#{r:02x}{g:02x}{b:02x}')

        # Update RGB label
        rgb_label.configure(text=f"RGB: ({r}, {g}, {b})")

        # Update the RGB sliders
        r_slider.set(r)
        g_slider.set(g)
        b_slider.set(b)

        # Update HSV sliders
        h, s, v = rgb_to_hsv(r, g, b)
        h_slider.set(int(h * 360))
        s_slider.set(int(s * 100))
        v_slider.set(int(v * 100))
    except Exception as e:
        print(f"Error in update_color_from_cmy: {e}")

# Function to open color chooser dialog
def choose_color():
    try:
        color = colorchooser.askcolor(title="Choose a color")
        if color[0]:  # Check if a color was chosen
            r, g, b = [int(x) for x in color[0]]
            # Update RGB sliders
            r_slider.set(r)
            g_slider.set(g)
            b_slider.set(b)
            # Update color preview directly
            color_preview.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
            # Update other sliders
            update_color_from_rgb()
    except Exception as e:
        print(f"Error in choose_color: {e}")

# Drawing functions
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw(event):
    global last_x, last_y
    if last_x and last_y:
        color = "white" if eraser_active.get() else color_preview.cget('bg')
        width = brush_size.get() * (2 if eraser_active.get() else 1)
        canvas.create_line(last_x, last_y, event.x, event.y, 
                         fill=color, width=width, 
                         capstyle=tk.ROUND, smooth=tk.TRUE)
    last_x, last_y = event.x, event.y

def stop_draw(event):
    global last_x, last_y
    last_x = last_y = None

# Function to clear the canvas
def clear_canvas():
    canvas.delete("all")

# Function to show information
def show_information():
    info_window = tk.Toplevel(root)
    info_window.title("Color Models Information")
    info_window.geometry("600x400")
    title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=11)
    bold_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

    info_pages = [
        # Page 1 - Hardware-Oriented Color Models & RGB
        """Hardware-Oriented Color Models

1. RGB (Red, Green, Blue):

• Definition:

    - The RGB color model is an additive color model in which red, green, and blue light are combined in various ways to reproduce a broad array of colors.

• Technical Detail:
    
    - It is called "additive" because the more light you add, the closer you get to white. If no light is added (R=0, G=0, B=0), the result is black.

• Applications:

    - RGB is primarily used in digital displays, such as CRT (Cathode Ray Tube) monitors, LCD (Liquid Crystal Displays), and projectors.
    - Each pixel on a display device contains red, green, and blue sub-pixels that can vary in intensity (ranging from 0 to 255), creating over 16.7 million color combinations (256^3).

• Example:

    - (255, 0, 0) represents pure red.
    - (0, 255, 0) represents pure green.
    - (0, 0, 255) represents pure blue.
    - (255, 255, 255) represents white, where all colors of light are present at full intensity.""",

        # Page 2 - YIQ
"""
2. YIQ (Luminance and Chrominance):

• Definition:

    - YIQ is used in the NTSC color TV system, which separates image information into luminance (Y) and chrominance (IQ) components.

• Technical Detail:

    - The Y component represents the brightness or grayscale information.
    - The I and Q components represent the color information (chrominance), allowing for color to be overlaid onto the luminance data. This separation helps TV systems to be backward compatible with older black-and-white televisions.

• Applications:

    - This model is mostly used in analog TV broadcasting. It provides efficient transmission of color information while preserving the luminance signal for black-and-white viewers.""",
"""
3. CMY (Cyan, Magenta, Yellow):

• Definition:

    - The CMY color model is a subtractive color model used in color printing. The inks subtract light from white paper by absorbing specific wavelengths of light and reflecting others.

• Technical Detail:

    - In subtractive models, white light (composed of all visible wavelengths) is assumed to be the starting point.
    - Cyan ink absorbs red light but reflects blue and green.
    - Magenta ink absorbs green light but reflects red and blue.
    - Yellow ink absorbs blue light but reflects red and green.
    - Combining these inks allows printers to produce a wide range of colors.

• Applications:

    - Used in inkjet printers, color photocopiers, and various printing processes. However, CMY cannot produce deep blacks, which leads to the introduction of the CMYK model.""",
"""
4. CMYK (Cyan, Magenta, Yellow, Key/Black):

• Definition:

    - CMYK adds a black ink (K stands for "Key" or black) to the CMY model to produce rich blacks and save on colored ink.
    
• Technical Detail:

    - In theory, combining cyan, magenta, and yellow should produce black, but due to ink impurities, the result is often muddy brown. To solve this issue, black ink is added.
    - The K component allows for the accurate production of shadows and sharp contrasts.
    - Using black ink also reduces printing costs since black ink is cheaper than using equal amounts of cyan, magenta, and yellow.
    
• Applications:

    - Used extensively in professional printing, especially when printing documents with large areas of black, such as text-heavy documents or dark images.""",
    
"""User-Oriented Color Models

1. HSV (Hue, Saturation, Value):

• Definition:

    - The HSV model is a more intuitive representation of colors, designed to match how humans perceive and describe colors.
    
• Technical Detail:

    - Hue (H): - Refers to the actual color and is measured as a degree on a color wheel from 0° to 360°. 0° = Red, 120° = Green, 240° = Blue.
    - Saturation (S): - Indicates how "pure" the color is, with 100% being full color and 0% being a shade of gray.
    - Value (V): - Represents the brightness or intensity of the color, where 0% is black and 100% is the brightest possible version of the color.

• Applications:

    - Commonly used in image editing software (like Photoshop) and in color selection interfaces.""",
"""
2. HSB (Hue, Saturation, Brightness):

• Definition:

    - HSB is a variant of HSV, where the third component is called brightness instead of value.
        
• Technical Detail:

    - Brightness here refers to how much light the color emits or reflects. It allows for finer control over the appearance of colors in situations where light plays a significant role in visual perception.
        
• Applications:

    - HSB is often used in graphics and design software for color correction and color balance.""",
    
"""3. HLS (Hue, Lightness, Saturation):

• Definition:

    - HLS is similar to HSV but uses lightness instead of value or brightness. Lightness controls the mixture of white and black with the pure color (hue).

• Technical Detail:

    - Lightness ranges from 0% (black) to 50% (pure color) to 100% (white).
    - Saturation defines how vivid or dull the color is.
        
• Applications:

    - Used in color management systems and in some design tools for web and UI design.""",
        
"""Additive vs. Subtractive Color Mixing

1. Additive Color Mixing:

• Definition:

    - Additive color mixing refers to combining colored light to produce new colors. This is used in screens and displays.
        
• Technical Detail:

    - When red, green, and blue lights are combined at full intensity, they produce white light.
    - Lowering the intensity of one or more of these lights can produce different shades.

• Applications:

    - Used in displays, projectors, and any technology that emits light.""",
        
"""2. Subtractive Color Mixing:

• Definition:

    - Subtractive color mixing is used when pigments (like ink) are combined. This process removes (or subtracts) certain wavelengths from white light.
        
• Technical Detail:

    - Cyan ink absorbs red light and reflects blue and green, magenta absorbs green and reflects blue and red, and yellow absorbs blue and reflects red and green.
    - Black is created by combining all three subtractive primaries (cyan, magenta, yellow).
        
• Applications:

    - Used in printing, photography, and painting.""",

"""Challenges in Color Reproduction

• Monitors vs. Printers:

    - RGB monitors and CMYK printers have different color gamuts, meaning they can display and print different ranges of colors. This makes color matching between a screen and a printed copy difficult.
    - Color profiles (like ICC profiles) are often used to ensure that what you see on the screen matches what is printed.
        
• Chromaticity Diagram:

    - A chromaticity diagram maps out visible colors, allowing engineers to compare the gamuts of different devices (like a monitor vs. a printer). It helps in analyzing and optimizing color reproduction."""      
    ]

    
    current_page = tk.IntVar(value=0)

    # Create scrollbar
    scrollbar = ttk.Scrollbar(info_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    info_text = tk.Text(info_window, wrap=tk.WORD, width=70, height=20, 
                       font=body_font, yscrollcommand=scrollbar.set)
    info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Configure the scrollbar
    scrollbar.config(command=info_text.yview)
    
    # Configure text tags
    info_text.tag_configure("title", font=title_font)
    info_text.tag_configure("bold", font=bold_font)
    info_text.tag_configure("indent", lmargin1=20, lmargin2=20)
    info_text.tag_configure("indent2", lmargin1=40, lmargin2=40)
    
    def insert_formatted_text(text):
        info_text.delete(1.0, tk.END)
        lines = text.split('\n')
        
        for line in lines:
            stripped_line = line.strip()
            
            # Apply formatting based on content
            if stripped_line.startswith('Hardware-Oriented') or \
               stripped_line.startswith('User-Oriented') or \
               stripped_line.startswith('Additive vs.'):
                info_text.insert(tk.END, line + '\n', "title")
            
            elif stripped_line.startswith(('1.', '2.', '3.', '4.')):
                info_text.insert(tk.END, line + '\n', "bold")
            
            elif stripped_line.startswith('•'):
                info_text.insert(tk.END, line + '\n', ("bold", "indent"))
            
            elif stripped_line.startswith('-'):
                info_text.insert(tk.END, line + '\n', "indent2")
            
            else:
                info_text.insert(tk.END, line + '\n')
    
    # Insert the initial text with formatting
    insert_formatted_text(info_pages[0])
    info_text.config(state=tk.DISABLED)

    def next_page():
        page = current_page.get()
        if page < len(info_pages) - 1:
            page += 1
            current_page.set(page)
            info_text.config(state=tk.NORMAL)
            insert_formatted_text(info_pages[page])
            info_text.config(state=tk.DISABLED)
        
        if page == len(info_pages) - 1:
            next_button.config(state=tk.DISABLED)
        prev_button.config(state=tk.NORMAL)

    def prev_page():
        page = current_page.get()
        if page > 0:
            page -= 1
            current_page.set(page)
            info_text.config(state=tk.NORMAL)
            insert_formatted_text(info_pages[page])
            info_text.config(state=tk.DISABLED)
        
        if page == 0:
            prev_button.config(state=tk.DISABLED)
        next_button.config(state=tk.NORMAL)

    button_frame = ttk.Frame(info_window)
    button_frame.pack(pady=5)

    prev_button = ttk.Button(button_frame, text="Previous", command=prev_page, state=tk.DISABLED)
    prev_button.pack(side=tk.LEFT, padx=5)

    next_button = ttk.Button(button_frame, text="Next", command=next_page)
    next_button.pack(side=tk.LEFT, padx=5)
# New function for the quiz
def take_quiz():
    quiz_window = tk.Toplevel(root)
    quiz_window.title("Take Quiz")
    # Set the quiz window to stay on top
    quiz_window.transient(root)
    quiz_window.grab_set()
    
    # Configure window size and position
    window_width = 400
    window_height = 300
    screen_width = quiz_window.winfo_screenwidth()
    screen_height = quiz_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    quiz_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # List of questions and answers
    questions = [
        {
            "question": "Which color model is used for printing?",
            "options": ["RGB", "HSV", "CMYK"],
            "answer": "CMYK"
        },
        {
            "question": "What color model is commonly used for screens?",
            "options": ["CMYK", "HSV", "RGB"],
            "answer": "RGB"
        },
        {
            "question": "What does CMYK stand for?",
            "options": ["Cyan, Magenta, Yellow, Key", "Cyan, Magenta, Yellow, Kelp", "Cyan, Magenta, Yellow, Knight"],
            "answer": "Cyan, Magenta, Yellow, Key"
        },
        {
            "question": "Which color model is used for web design?",
            "options": ["CMYK", "RGB", "HSB"],
            "answer": "RGB"
        },
        {
            "question": "What is the full form of HSV?",
            "options": ["Hue, Saturation, Value", "Hue, Saturation, Vividness", "Hue, Saturation, Visibility"],
            "answer": "Hue, Saturation, Value"
        }
    ]

    correct_answers = 0
    current_question = 0
    
    # Create main frame for quiz content
    quiz_frame = ttk.Frame(quiz_window, padding="20")
    quiz_frame.pack(fill=tk.BOTH, expand=True)

    # Question label with proper styling
    question_text = tk.StringVar()
    question_label = ttk.Label(quiz_frame, textvariable=question_text, wraplength=350, justify=tk.LEFT)
    question_label.pack(pady=(0, 20))

    # Options frame
    options_frame = ttk.Frame(quiz_frame)
    options_frame.pack(fill=tk.BOTH, expand=True)
    
    answer_var = tk.StringVar(value="")
    option_buttons = []

    # Create Radiobuttons for options
    for i in range(3):
        option_button = ttk.Radiobutton(options_frame, variable=answer_var, value="")
        option_button.pack(pady=5, anchor="w")
        option_buttons.append(option_button)

    def show_question():
        nonlocal current_question
        # Clear previous selection
        answer_var.set("")
        # Update question text
        question_text.set(f"Question {current_question + 1}: {questions[current_question]['question']}")
        # Update options
        for i, option in enumerate(questions[current_question]["options"]):
            option_buttons[i].config(text=option, value=option)

    def check_answer():
        nonlocal correct_answers, current_question
        selected_answer = answer_var.get()
        
        if not selected_answer:
            messagebox.showwarning("Warning", "Please select an answer!", parent=quiz_window)
            return
            
        if selected_answer == questions[current_question]["answer"]:
            correct_answers += 2
            messagebox.showinfo("Result", "Correct!", parent=quiz_window)
        else:
            messagebox.showinfo("Result", 
                              f"Incorrect. The correct answer is {questions[current_question]['answer']}.", 
                              parent=quiz_window)
        
        current_question += 1
        if current_question < len(questions):
            show_question()
        else:
            show_result()

    def show_result():
        total_marks = len(questions) * 2
        messagebox.showinfo("Quiz Result", 
                          f"You scored {correct_answers} out of {total_marks} marks.", 
                          parent=quiz_window)
        quiz_window.destroy()

    # Submit button
    submit_button = ttk.Button(quiz_frame, text="Submit", command=check_answer)
    submit_button.pack(pady=20)

    # Show the first question
    show_question()

# Global variables for color cube
azimuth = 0
elevation = 20
prev_x = 0
prev_y = 0

# Function to show color cube
def show_color_cube():
    cube_window = tk.Toplevel(root)
    cube_window.title("RGB Color Cube")
    
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    canvas = FigureCanvasTkAgg(fig, master=cube_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    
    def update_color_cube():
        global azimuth, elevation
        ax.cla()
        r = np.linspace(0, 255, 16)
        g = np.linspace(0, 255, 16)
        b = np.linspace(0, 255, 16)
        R, G, B = np.meshgrid(r, g, b)
        R_flat, G_flat, B_flat = R.flatten(), G.flatten(), B.flatten()
        colors = np.zeros((R_flat.shape[0], 4))
        colors[:, 0] = R_flat / 255
        colors[:, 1] = G_flat / 255
        colors[:, 2] = B_flat / 255
        colors[:, 3] = 1
        ax.scatter(R_flat, G_flat, B_flat, c=colors, marker='o', alpha=0.5)
        selected_r, selected_g, selected_b = int(r_slider.get()), int(g_slider.get()), int(b_slider.get())
        ax.scatter(selected_r, selected_g, selected_b, color='black', s=100)
        ax.set_xlabel('Red Channel')
        ax.set_ylabel('Green Channel')
        ax.set_zlabel('Blue Channel')
        ax.set_title('RGB Color Cube')
        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.set_zlim(0, 255)
        ax.view_init(elev=elevation, azim=azimuth)
        canvas.draw()
    
    def on_mouse_press(event):
        global prev_x, prev_y
        prev_x, prev_y = event.x, event.y
    
    def on_mouse_drag(event):
        global azimuth, elevation, prev_x, prev_y
        dx, dy = event.x - prev_x, event.y - prev_y
        azimuth += dx
        elevation += dy
        azimuth %= 360
        elevation = max(min(elevation, 90), -90)
        update_color_cube()
        prev_x, prev_y = event.x, event.y
    
    canvas_widget.bind('<ButtonPress-1>', on_mouse_press)
    canvas_widget.bind('<B1-Motion>', on_mouse_drag)
    update_color_cube()

# Create main window
root = tk.Tk()
root.title("Color Model Tool")
root.geometry("1200x800")
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure grid weights
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Variables
brush_size = tk.IntVar(value=5)
eraser_active = tk.BooleanVar(value=False)
last_x = None
last_y = None

# Create color preview frame with a border
color_preview_container = ttk.Frame(main_frame, borderwidth=2, relief="solid")
color_preview_container.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")
color_preview = tk.Frame(color_preview_container, width=200, height=100, bg="black")
color_preview.pack(padx=2, pady=2, fill="both", expand=True)

# RGB label
rgb_label = ttk.Label(main_frame, text="RGB: (0, 0, 0)")
rgb_label.grid(row=1, column=0, sticky="w")

# Button frame for quiz, cube, and information buttons
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=1, column=1, columnspan=2, sticky="e")

# Quiz button
quiz_button = ttk.Button(button_frame, text="Take Quiz", command=take_quiz)
quiz_button.pack(side=tk.LEFT, padx=5)

# Color Cube button
color_cube_button = ttk.Button(button_frame, text="Show Color Cube", command=show_color_cube)
color_cube_button.pack(side=tk.LEFT, padx=5)

# Information button
info_button = ttk.Button(button_frame, text="Color Information", command=show_information)
info_button.pack(side=tk.LEFT, padx=5)

# Sliders frame
sliders_frame = ttk.Frame(main_frame)
sliders_frame.grid(row=2, column=0, columnspan=3, pady=10)

# RGB Sliders
ttk.Label(sliders_frame, text="RGB:").grid(row=0, column=0, sticky="w")
r_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_rgb)
g_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_rgb)
b_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_rgb)

ttk.Label(sliders_frame, text="R:").grid(row=1, column=0)
r_slider.grid(row=1, column=1)
ttk.Label(sliders_frame, text="G:").grid(row=2, column=0)
g_slider.grid(row=2, column=1)
ttk.Label(sliders_frame, text="B:").grid(row=3, column=0)
b_slider.grid(row=3, column=1)

# HSV Sliders
ttk.Label(sliders_frame, text="HSV:").grid(row=0, column=2, sticky="w")
h_slider = tk.Scale(sliders_frame, from_=0, to=360, orient="horizontal", command=update_color_from_hsv)
s_slider = tk.Scale(sliders_frame, from_=0, to=100, orient="horizontal", command=update_color_from_hsv)
# HSV Sliders (continued)
v_slider = tk.Scale(sliders_frame, from_=0, to=100, orient="horizontal", command=update_color_from_hsv)

ttk.Label(sliders_frame, text="H:").grid(row=1, column=2)
h_slider.grid(row=1, column=3)
ttk.Label(sliders_frame, text="S:").grid(row=2, column=2)
s_slider.grid(row=2, column=3)
ttk.Label(sliders_frame, text="V:").grid(row=3, column=2)
v_slider.grid(row=3, column=3)

# CMY Sliders
ttk.Label(sliders_frame, text="CMY:").grid(row=0, column=4, sticky="w")
c_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_cmy)
m_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_cmy)
y_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", command=update_color_from_cmy)

ttk.Label(sliders_frame, text="C:").grid(row=1, column=4)
c_slider.grid(row=1, column=5)
ttk.Label(sliders_frame, text="M:").grid(row=2, column=4)
m_slider.grid(row=2, column=5)
ttk.Label(sliders_frame, text="Y:").grid(row=3, column=4)
y_slider.grid(row=3, column=5)

# Color chooser button
choose_button = ttk.Button(main_frame, text="Choose Color", command=choose_color)
choose_button.grid(row=3, column=0, pady=5)

# Drawing controls frame
controls_frame = ttk.LabelFrame(main_frame, text="Drawing Controls")
controls_frame.grid(row=3, column=1, columnspan=2, pady=5, sticky="ew")

# Brush size control
ttk.Label(controls_frame, text="Brush Size:").pack(side=tk.LEFT, padx=5)
brush_size_scale = ttk.Scale(controls_frame, from_=1, to=20, orient="horizontal", 
                            variable=brush_size)
brush_size_scale.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

# Eraser toggle
eraser_check = ttk.Checkbutton(controls_frame, text="Eraser", variable=eraser_active)
eraser_check.pack(side=tk.LEFT, padx=5)

# Canvas
canvas = tk.Canvas(main_frame, bg="white", width=800, height=400)
canvas.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)

# Canvas bindings
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# Bottom buttons frame
bottom_button_frame = ttk.Frame(main_frame)
bottom_button_frame.grid(row=5, column=0, columnspan=3, pady=5)

# Clear canvas button
clear_button = ttk.Button(bottom_button_frame, text="Clear Canvas", command=clear_canvas)
clear_button.pack(side=tk.LEFT, padx=5)

# Configure row weights for expansion
main_frame.grid_rowconfigure(4, weight=1)

# Start the application
root.mainloop()
