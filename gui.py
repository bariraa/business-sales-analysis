from tkinter import *
import os
from sales_analysis import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk 


m = Tk()
m.geometry("1000x600")
m.title("Business Sales Dashboard")
m.iconbitmap("images/icon.ico")

def show_frame(frame):
    frame.tkraise()


# Frames
frame_side = Frame(m, width=260, bg="#003972")
frame_side.pack(side="left", fill="y")

frame_main = Frame(m, bg="#ecf0f1")
frame_main.pack(side="right", fill="both", expand=True)

frame_upload = Frame(frame_main, bg="#ffffff")
frame_kpis = Frame(frame_main, bg="#ffffff")
frame_graphs = Frame(frame_main, bg="#ffffff")

for frame in (frame_upload, frame_kpis, frame_graphs):
    frame.place(relwidth=1, relheight=1)

show_frame(frame_upload)


# ------Side Panels------
Label(frame_side,text="Dashboard", font=('Calibri',15, "bold"), bg="#003972", fg="#ffffff",relief="flat", anchor="w").pack(pady=25)
Button(frame_side, text="📁  Upload Data", width=20, font=('Arial',11), bg="#003972", fg="#ffffff",relief="flat", anchor="w", command=lambda: show_frame(frame_upload)).pack(padx=5,pady=5)
Button(frame_side, text="📊  KPIs", width=20, font=('Arial',11), bg="#003972", fg="#ffffff", relief="flat", anchor="w", command=lambda: [show_frame(frame_kpis), display_kpis()]).pack(padx=5,pady=5)
Button(frame_side, text="📈  Graphs", width=20, font=('Arial',11), bg="#003972", fg="#ecf0f1", relief="flat", anchor="w",  command=lambda: [show_frame(frame_graphs), display_graph()]).pack(padx=5,pady=5)




# --------------upload page-----------------
df = None

def clear():
    global df
    df = None
    lbl.config(text="Dataset cleared!", fg="#F67206")


def upload():
    global df
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    file_name = os.path.basename(file_path)

    if not file_path:
        return
    try:
        df = load_data(file_path)
        df = clean_data(df)
        lbl.config(text=f"Dataset uploaded and cleaned successfully!\n📄 {file_name}",fg="green")

    except Exception as e:
        df = None
        lbl.config(text=f"Something went wrong:\n{e}",fg="red")


Label(frame_upload, text="Upload CSV File", font=("Arial", 14, "bold"),fg="#003972", bg="#ffffff").pack(pady=20)
Button(frame_upload, text="Select File",font=('Arial',11), command=upload, width=15,bg="#003972", fg="#ffffff").pack(pady=10)
lbl = Label(frame_upload,text="", bg="#ffffff", font=("Arial",12,"bold"))
lbl.pack(pady=20)

Label(frame_upload, text="Note:", font=("Arial", 14, 'bold'),fg="#003972",bg="#ffffff",justify="left",anchor="w").pack(fill="x", padx=10, pady=5)

required_columns = ['product', 'category', 'quantity', 'price', 'date', 'region']
Label(frame_upload, 
    text="The CSV File must contain these columns:\n-  " + "\n-  ".join(required_columns),
    font=("Calibri", 12), 
    fg="#003972", bg="#ffffff",
    justify="left",   
    anchor="w").pack(fill="x", padx=30, pady=5)

# -----------------KIPS Page---------------------
kpi_img = None  

def display_kpis():
    global kpi_img
    for widget in frame_kpis.winfo_children():
        widget.destroy()

    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        try:
            img = Image.open("images/notfound.png")
            img = img.resize((300, 300))
            kpi_img = ImageTk.PhotoImage(img)  
            label_img = Label(frame_kpis, image=kpi_img, bg="#ffffff")
            label_img.pack(pady=20)
        except Exception:
            pass

        Label(frame_kpis, text="⚠️ No valid dataset uploaded!", font=("Arial", 14), fg="red",bg="#ffffff").pack(pady=10)
        return 

    kpis = calculate_kpis(df)
    colors = ["#1D8CBC", "#9360C4", "#EAA226", "#13A633", "#F12020", "#3A3268", "#9A8DFF", "#49CCF0", "#976694"]
    Label(frame_kpis, text="📊 Key Performance Indicators", font=("Arial", 16, "bold"),bg="#ffffff", fg="#003972").pack(pady=20)
   
    frame_cards =  Frame(frame_kpis, bg='#ffffff')
    frame_cards.pack(fill="both", expand=True, padx=10, pady=10)
    row = 0
    col = 0
    for i,( key, value) in enumerate(kpis.items()):
        card = Frame(frame_cards, bg=colors[i], relief="raised", width=300, height=250)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
        Label(card, text=f"{key}:", font=("Arial", 12, "bold"), bg=colors[i], fg="#ffffff",justify="center").pack(pady=(50,0))
        Label(card, text=value, font=("Arial", 14), bg=colors[i],fg="#ffffff",anchor="center", justify="center").pack(pady=(10,20))
    
        col += 1
        if col == 3:
            col = 0
            row += 1

    for c in range(3):
        frame_cards.grid_columnconfigure(c, weight=1)
    for r in range(row+1):
        frame_cards.grid_rowconfigure(r, weight=1)

Button(frame_upload, text="Delete File",font=('Arial',11), command=clear, width=15,bg="#F60606", fg="#ffffff").pack(side="bottom",pady=50)    

# -------------Graph Page-------------   
graph_img = None

def display_graph():
    global graph_img
    for widget in frame_graphs.winfo_children():
        widget.destroy()

    # data not exist
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        try:
            img = Image.open("images/notfound.png")
            img = img.resize((300, 300))
            graph_img = ImageTk.PhotoImage(img)  
            label_img = Label(frame_graphs, image=graph_img, bg="#ffffff")
            label_img.pack(pady=20)
        except Exception:
            pass

        Label(frame_graphs, text="⚠️ No valid dataset uploaded!", font=("Arial", 14), fg="red",bg="#ffffff").pack(pady=10)
        return 

    # if data exist:
    Label(frame_graphs, text="📊 Graph Analysis", font=("Arial", 16, "bold"),
          bg="#ffffff", fg="#003972").pack(pady=20)

    graph_var = StringVar()
    graph_var.set("Select Graph")
    options = [
        "Sales Trend",
        "Monthly Sales Trend",
        "Yearly Sales Trend",
        "Product Sales",
        "Category Sales",
        "Region Sales"
    ]
    dropdown = OptionMenu(frame_graphs, graph_var, *options)
    dropdown.config(width=25)
    dropdown.pack(pady=10)

    Button(frame_graphs, text="Show Graph", font=("Arial", 11), bg="#003972",
           fg="white", width=15,
           command=lambda: show_selected_graph(frame_graphs,graph_var.get())
          ).pack(pady=10)



def show_selected_graph(parent_frame,choice):
    
    for widget in parent_frame.winfo_children():
        if isinstance(widget, Canvas):
            widget.destroy()
    try:
        if choice == "Sales Trend":
            fig = sales_trends(df)
        elif choice == "Monthly Sales Trend":
            fig = monthly_sales_trend(df)
        elif choice == "Yearly Sales Trend":
            fig = yearly_sales_trend(df)
        elif choice == "Product Sales":
            fig = product_sales(df)
        elif choice == "Category Sales":
            fig = category_sales(df)
        elif choice == "Region Sales":
            fig = region_sales(df)
        else:
            messagebox.showinfo("Info", "Please select a graph type")
            return
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error generating graph:\n{e}")


m.mainloop()


