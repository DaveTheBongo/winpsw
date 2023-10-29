""" winpsw.py
    Generates a quantity of passwords including required character types
    TODO
    ?buttons for users to input chr_types, eg acceptable symbols ?save to file
"""
import customtkinter as ctk
import secrets


def make_str(str_range: list) -> str:
    return "".join(
        [chr(ch) for sublist in str_range for ch in range(sublist[0], sublist[-1] + 1)]
    )


symbols = make_str([[33, 47], [58, 64], [91, 96], [123, 126], [163], [166], [172]])
lowercase = make_str([[97, 122]])
uppercase = make_str([[65, 90]])
digits = make_str([[48, 57]])

app = ctk.CTk()
app.geometry("400x600")
app.resizable(False, False)
app.title("Password Generator")
app.eval("tk::PlaceWindow . center")
check_lowercase = ctk.IntVar(value=True)
cb_lowercase = ctk.CTkCheckBox(app)
check_digits = ctk.IntVar(value=True)
cb_digits = ctk.CTkCheckBox(app)
check_uppercase = ctk.IntVar(value=True)
cb_uppercase = ctk.CTkCheckBox(app)
check_symbols = ctk.IntVar(value=True)
cb_symbols = ctk.CTkCheckBox(app)
e_length = ctk.CTkEntry(app)
e_quantity = ctk.CTkEntry(app)
textbox = ctk.CTkTextbox(app)
textbox_output_line = 1


def main():
    run_app()


def run_app() -> None:
    myfont = ("Tahoma", 14)
    textcol = "#5da3d1"

    rx1 = 0.05
    rx2 = 0.53
    ry1 = 0.05
    ry2 = 0.10
    ry3 = 0.15
    ry4 = 0.20
    ry5 = 0.27
    ry6 = 0.34
    rx3 = 0.28
    rx4 = 0.51
    rx5 = 0.845
    ry7 = 0.41
    ry8 = 0.45

    l_cb = ctk.CTkLabel(
        app, text="Types of character required:", font=myfont, width=30, anchor="w"
    )

    l_cb.place(relx=rx1, rely=ry1, anchor="w")
    cb_lowercase.configure(
        app,
        font=myfont,
        text="Lowercase",
        variable=check_lowercase,
    )
    cb_lowercase.place(relx=rx2, rely=ry1, anchor="w")

    cb_digits.configure(
        app,
        font=myfont,
        text="Digits",
        variable=check_digits,
    )
    cb_digits.place(relx=rx2, rely=ry2, anchor="w")

    cb_uppercase.configure(
        app,
        font=myfont,
        text="Uppercase",
        variable=check_uppercase,
    )
    cb_uppercase.place(relx=rx2, rely=ry3, anchor="w")

    cb_symbols.configure(
        app,
        font=myfont,
        text="Symbols",
        variable=check_symbols,
    )
    cb_symbols.place(relx=rx2, rely=ry4, anchor="w")

    l_length = ctk.CTkLabel(
        app, text="Length of password:", font=myfont, width=100, anchor="w"
    )
    l_length.place(relx=rx1, rely=ry5, anchor="w")
    e_length.configure(width=80, font=myfont, text_color=textcol)
    e_length.place(relx=rx4, rely=ry5, anchor="w")

    l_quantity = ctk.CTkLabel(
        app, text="Number of passwords:", font=myfont, width=100, anchor="w"
    )
    l_quantity.place(relx=rx1, rely=ry6, anchor="w")
    e_quantity.configure(width=80, font=myfont, text_color=textcol)
    e_quantity.place(relx=rx4, rely=ry6, anchor="w")

    b_run = ctk.CTkButton(app, text="Run", command=run, width=80, corner_radius=5)
    b_run.place(relx=rx1, rely=ry7, anchor="w")

    b_copy = ctk.CTkButton(app, text="Copy", command=copy, width=80, corner_radius=5)
    b_copy.place(relx=rx3, rely=ry7, anchor="w")

    b_run = ctk.CTkButton(app, text="Clear", command=clear, width=80, corner_radius=5)
    b_run.place(relx=rx4, rely=ry7, anchor="w")

    b_exit = ctk.CTkButton(app, text="Exit", command=exit, width=80, corner_radius=5)
    b_exit.place(relx=rx5, rely=ry7, anchor="center")

    textbox.configure(
        state="disabled",
        fg_color="transparent",
        font=("Courier New", 16),
        text_color=textcol,
        wrap="none",
        width=360,
        height=308,
        corner_radius=5,
    )
    textbox.place(relx=rx1, rely=ry8, anchor="nw")

    app.mainloop()


def text_line(text: str) -> None:
    """appends text + \n to textbox"""
    global textbox_output_line
    num_lines = sum(1 for char in text if char == "\n") + 1
    textbox.configure(state="normal")
    textbox.insert(f"{textbox_output_line}.0", f"{text}\n")
    textbox.configure(state="disabled")
    textbox_output_line += num_lines
    return


def isvalid(digit: str) -> int:
    """check digit and return int > 0 or None"""
    if not digit.isdigit():
        return None
    if int(digit) < 1:
        return None
    return int(digit)


def create_selection_str(chr_types: dict) -> str:
    """add each selection type to str"""
    selection = ""
    if chr_types["symbols"]:
        selection += symbols
    if chr_types["lowercase"]:
        selection += lowercase
    if chr_types["uppercase"]:
        selection += uppercase
    if chr_types["digits"]:
        selection += digits
    return selection


def run() -> None:
    """validate input and generate password(s)"""
    chr_types: dict = {}
    chr_types["symbols"] = check_symbols.get()
    chr_types["lowercase"] = check_lowercase.get()
    chr_types["uppercase"] = check_uppercase.get()
    chr_types["digits"] = check_digits.get()
    qty_types = sum(v for k, v in chr_types.items())

    if qty_types == 0:
        cb_lowercase.toggle()
        cb_lowercase.configure()
        chr_types["lowercase"] = True
        qty_types += 1
        cb_digits.toggle()
        cb_digits.configure()
        chr_types["digits"] = True
        qty_types += 1
        text_line(f"Selection set to lowercase & digits")

    length = isvalid(e_length.get())
    if not length or length < qty_types:
        length = qty_types
        text_line(f"Length set to {qty_types}")

    quantity = isvalid(e_quantity.get())
    if not quantity:
        quantity = 1
        text_line(f"Number set to 1")

    selection = create_selection_str(chr_types)

    for _ in range(quantity):
        text_line(f"{valid_password(selection, chr_types, length)}")


def valid_password(selection: str, chr_types: dict, length: int) -> str:
    """generate a password of size length including all required character types"""
    while True:
        sym: bool = not chr_types["symbols"]
        lc: bool = not chr_types["lowercase"]
        uc: bool = not chr_types["uppercase"]
        dig: bool = not chr_types["digits"]
        psw: str = "".join(secrets.choice(selection) for _ in range(length))
        # ensure psw contains the required types
        for char in psw:
            if not sym:
                if char in symbols:
                    sym = True
            if not lc:
                if char in lowercase:
                    lc = True
            if not uc:
                if char in uppercase:
                    uc = True
            if not dig:
                if char in digits:
                    dig = True
            if all([lc, dig, sym, uc]):
                return psw


def clear() -> None:
    """delete text in textbox and reset line count"""
    global textbox_output_line
    textbox.configure(state="normal")
    textbox.delete(f"0.0", f"end")
    textbox.configure(state="disabled")
    textbox_output_line = 1
    return


def copy() -> None:
    """copies text in textbox to clipboard"""
    data = textbox.get(1.0, "end").strip("\n")
    app.clipboard_clear()
    app.clipboard_append(data)
    return


if __name__ == "__main__":
    main()
