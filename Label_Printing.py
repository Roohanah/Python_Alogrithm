import win32print

def print_label(label_file):
    printer_name = win32print.GetDefaultPrinter()
    win32print.SetDefaultPrinter(printer_name)
    win32print.StartDocPrinter(printer_name, 1, ("label", None, "RAW"))
    win32print.StartPagePrinter(printer_name)
    with open(label_file, "rb") as f:
        data = f.read()
    win32print.WritePrinter(printer_name, data)
    win32print.EndPagePrinter(printer_name)
    win32print.EndDocPrinter(printer_name)

print_label("label.pdf")
