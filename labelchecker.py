# IMPORT LIBRARIES
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from pandas import read_excel
import tkinter as tk
from tkinter import filedialog as fd

# IMPORT LOCAL PATH TO POPPLER
from local import PATH_TO_POPPLER

def read_data(path:str, nr_barcodes:int) -> list:
    """
    INPUTS:
    path: path to excel file with the codes
    nr_barcodes: the number of barcodes on a specific label

    OUTPUT:
    output: multilist of codes per label
    """
    try:
        df = read_excel(path, header=None)
        df_list = df.values.tolist()
        output = []
        for i in range(0, len(df_list), nr_barcodes):
            label_output = []
            for j in range(i, i+nr_barcodes):
                label_output.append(*df_list[j])
            output.append(label_output)

        return output

    except PermissionError:
        print("ERROR: Close the excel file")

class LabelReader():
    """
    Class that handles the reading of barcodes from the generated labels
    """
    def __init__(self, path) -> None:
        """
        INPUT:
        path: path to pdf with the generated labels
        """
        self.label_obj = convert_from_path(path, poppler_path=PATH_TO_POPPLER)
        self.nr_pages = len(self.label_obj)
    
    def get_barcodes_from_page(self, page_nr:int) -> list:
        """
        Reads barcodes from a specific page
        INPUT:
        page_nr: page number in the pdf document (can not be larger than the total number of pages)

        OUTPUT:
        list of strings that represents the values of the barcodes on that specific page
        """
        if page_nr <= self.nr_pages:
            decoded_objs = decode(self.label_obj[page_nr])
            return [obj.data.decode() for obj in decoded_objs]
        
        else:
            print("ERROR: page number exceeds number of pages")

def check_barcodes(codes:list, barcodes:list, page_nr:int) -> bool:
    if len(codes) == len(barcodes):
        if set(codes) != set(barcodes):
            wrong_barcodes = list(set(codes) - set(barcodes))
            print("\033[91mWRONG BARCODES ON PAGE {}: {}\033[0m".format(page_nr, wrong_barcodes))
            return True
    else:
        broken_barcodes = list(set(codes) - set(barcodes))
        print("\033[91mBROKEN BARCODES ON PAGE {}: {}\033[0m".format(page_nr, broken_barcodes))
        return True
    
    return False

def run_interface() -> tuple:
    window = tk.Tk()
    window.title("")
    
    global file_labels, file_data
    file_data = False
    file_labels = False
    qty = tk.StringVar()

    def select_data():
        filename = fd.askopenfilename(
            title="Select data file",
            initialdir="example",
            filetypes=(("Excel files", "*.xlsx"),)
        )
        global file_data
        if filename != "":
            file_data = filename
            file_data_label.config(text=filename[filename.rfind("/")+1:])

    def select_labels():
        filename = fd.askopenfilename(
            title="Select labels file",
            initialdir="example",
            filetypes=(("PDF files", "*.pdf"),)
        )
        global file_labels
        if filename != "":
            file_labels = filename
            file_labels_label.config(text=filename[filename.rfind("/")+1:])


    def run_checker():
        if file_labels and file_data and qty.get() != "":
            print("CHECKING STARTS! PLEASE WAIT AND SEE OUTPUT IN YOUR TERMINAL")
            codes = read_data(file_data, int(qty.get()))
            reader = LabelReader(file_labels)

            error = False
            for page in range(reader.nr_pages):
                error = check_barcodes(
                    codes[page],
                    reader.get_barcodes_from_page(page),
                    page
                )
            
            if not error:
                print("\033[92mSucces! No errors found!\033[0m")
                
            window.destroy()

    tk.Label(text="Label checker", font=("Calibri bold", 15)).pack()

    frame_data = tk.Frame(window, padx=25, pady=5)
    frame_data.pack(fill=tk.X)
    file_data_label = tk.Label(frame_data, text="No file selected", font=("Calibri", 12))
    tk.Button(frame_data, text="Select", command=select_data).pack(side=tk.LEFT)  
    file_data_label.pack(side=tk.LEFT)      

    frame_label = tk.Frame(window, padx=25, pady=5)
    frame_label.pack(fill=tk.X)
    file_labels_label = tk.Label(frame_label, text="No file selected", font=("Calibri", 12))
    tk.Button(frame_label, text="Select", command=select_labels).pack(side=tk.LEFT)
    file_labels_label.pack(side=tk.LEFT)

    frame_qty = tk.Frame(window, padx=25, pady=10)
    frame_qty.pack(fill=tk.X)
    tk.Label(frame_qty, text="Nr. barcodes:", font=("Calibri", 12)).pack(side=tk.LEFT)
    tk.Entry(frame_qty, textvariable=qty, width=3).pack(padx=3)

    tk.Button(window, text="RUN", command=run_checker).pack(pady=10)

    window.mainloop()

    return file_data, file_labels

    

def main():
    run_interface()

if __name__ == "__main__":
    main()
    