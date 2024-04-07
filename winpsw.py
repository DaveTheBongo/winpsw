""" winpsw.py
    Generates any quantity of any length passwords that include required character types
    Textbox displays 36 x 20 chrs
    Symbols are string.puncuation or Winpsw(symbols: str)
    TODO
    ?button for user to input acceptable symbols instead of arg
    ?button for user to save to file
    convert to exe
"""

import customtkinter as ctk
import secrets


def main():
    Winpsw("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~¼½¾±""")


class Winpsw(ctk.CTk):
    def __init__(self, symbols=None):
        super().__init__()
        self.geometry("400x640")
        self.resizable(False, False)
        self.title("Password Generator")
        self.eval("tk::PlaceWindow . center")  # Load center screen
        self.lowercase_chk = ctk.CTkCheckBox(self)
        self.lowercase_val = ctk.IntVar(value=True)  # True = check box
        self.lowercase = self.make_str([[97, 122]])  # equiv string.lowercase
        self.digits_chk = ctk.CTkCheckBox(self)
        self.digits_val = ctk.IntVar(value=True)
        self.digits = self.make_str([[48, 57]])  # equiv string.digits
        self.uppercase_chk = ctk.CTkCheckBox(self)
        self.uppercase_val = ctk.IntVar(value=True)
        self.uppercase = self.make_str([[65, 90]])  # equiv string.uppercase
        self.symbols_chk = ctk.CTkCheckBox(self)
        self.symbols_val = ctk.IntVar(value=True)
        if symbols and self.check_ascii(symbols):  # valid ascii symbols
            self.symbols = symbols  # use provided param
        else:
            self.symbols = self.make_str(
                [
                    [33, 47],
                    [58, 64],
                    [91, 96],
                    [123, 126],
                    [163],
                    [166],
                    [172],
                ]
            )  # equiv string.punctuation
        self.checkboxes = {
            "lowercase": [self.lowercase_chk, self.lowercase_val, self.lowercase],
            "digits": [self.digits_chk, self.digits_val, self.digits],
            "uppercase": [self.uppercase_chk, self.uppercase_val, self.uppercase],
            "symbols": [self.symbols_chk, self.symbols_val, self.symbols],
        }
        self.e_length = ctk.CTkEntry(self)
        self.e_quantity = ctk.CTkEntry(self)
        self.textbox = ctk.CTkTextbox(self)
        self.textbox_line = 1  # textbox does not show line 0 ???

        self.default_types = ["lowercase", "digits"]
        self.draw_widgets()
        self.mainloop()

    def make_str(self, str_range: list) -> str:
        """create str of ascii chrs"""
        return "".join(
            [
                chr(ch)
                for sublist in str_range
                for ch in range(sublist[0], sublist[~0] + 1)
            ]
        )

    def check_ascii(self, ascii_chrs):
        if not isinstance(ascii_chrs, str) or len(ascii_chrs) < 1:
            print("Invalid symbols")
            return False
        for a in ascii_chrs:
            if not a.isprintable():
                print(f"Invalid symbol: {a}")
                return False
        return True

    def widget(self, widget, t, *args) -> None:
        """Generate and place widet"""
        # Common args: app, widget, text, args
        blue_color = "#5da3d1"
        var_font = ("Tahoma", 14)
        fixed_font = ("Courier New", 16)
        *arg, x, y = args  # {widget defined}, relx, rely
        match widget:  # widget defined params required
            case "label":
                # global: none
                ref = ctk.CTkLabel(self, text=t, font=var_font)
            case "radio":
                # global: var=ctk.StringVar(value="x") (x=default)
                var, v = arg  # var, val
                ref = ctk.CTkRadioButton(self, text=t, variable=var, value=v)
            case "checkbox":
                # global: ref=ctk.IntVar(value=x), var=ctk.CTkCheckBox(self) (x=True/False)
                ref, var = arg  # name, var
                ref.configure(self, text=t, font=var_font, variable=var)
            case "button":
                # global: none
                c, w, r = arg  # action, width, radius
                ref = ctk.CTkButton(self, text=t, command=c, width=w, corner_radius=r)
            case "combo":
                # global: ref=ctk.CTkComboBox(self), var=ctk.StringVar(value="")
                ref, v, c, var, w, x1 = arg  # name, val, action, var, width, label_start
                lab = ctk.CTkLabel(self, text=t, font=var_font)
                lab.place(relx=x1, rely=y, anchor="nw")
                ref.configure(values=v, font=var_font, command=c, variable=var, width=w)
            case "entry":
                # global: ref=ctk.CTkEntry(self)
                ref, w, x1 = arg  # name, width, label_start
                lab = ctk.CTkLabel(self, text=t, font=var_font)
                lab.place(relx=x1, rely=y, anchor="nw")
                ref.configure(width=w, font=var_font, text_color=blue_color)
            case "textbox":
                # global: ref=ctk.CTkTextbox(self)
                ref, wr, w, h = arg  # name, wrap, width, height
                ref.configure(
                    self,
                    fg_color="transparent",
                    font=fixed_font,
                    text_color=blue_color,
                    wrap=wr,
                    width=w,
                    height=h,
                    corner_radius=5,
                )
        ref.place(relx=x, rely=y, anchor="nw")

    def draw_widgets(self) -> None:
        # relx and rely widget placement
        rx1, rx2, rx3, rx4 = 0.05, 0.28, 0.51, 0.74
        ry1, ry2, ry3, ry4 = 0.03, 0.08, 0.13, 0.18  # checkboxes
        ry5, ry6 = 0.24, 0.30  # entrys
        ry7 = 0.36  # button line
        ry8 = 0.41  # textbox

        self.widget("label", "Character types required:", rx1, ry1)
        for kv, ry in zip(self.checkboxes.items(), [ry1, ry2, ry3, ry4]):
            k, v = kv
            self.widget("checkbox", k, v[0], v[1], rx3, ry)
        self.widget("entry", "Password Length:", self.e_length, 80, rx1, rx3, ry5)
        self.widget("entry", "Password Quantity:", self.e_quantity, 80, rx1, rx3, ry6)
        self.widget("button", "Run", self.run, 80, 15, rx1, ry7)
        self.widget("button", "Copy", self.copy, 80, 15, rx2, ry7)
        self.widget("button", "Clear", self.clear, 80, 15, rx3, ry7)
        self.widget("button", "Exit", exit, 80, 15, rx4, ry7)
        self.widget("textbox", "", self.textbox, "none", 375, 375, rx1, ry8)

    def text_line(self, text: str) -> None:
        """appends text + \n to textbox"""
        count_lines = sum(1 for char in text if char == "\n") + 1
        self.textbox.configure(state="normal")
        self.textbox.insert(f"{self.textbox_line}.0", f"{text}\n")
        self.textbox.configure(state="disabled")
        self.textbox_line += count_lines

    def get_char_types(self) -> None:
        """set char_types for checkboxes or default if none set"""

        def set_default_types() -> int:
            """set chr_types to default_types"""
            qty = 0
            for k, v in self.checkboxes.items():
                if k in self.default_types:
                    self.chr_types[k] = True
                    v[0].toggle()  # cb_type
                    v[0].configure()
                    qty += 1
            return qty

        self.selection = ""  # reset for this run
        self.chr_types = {}
        for k, v in self.checkboxes.items():
            self.chr_types[k] = v[1].get()  # check_type
        qty_types = sum(v for k, v in self.chr_types.items())
        if not qty_types:  # if no checkboxes set use default
            qty_types = set_default_types()
        return qty_types

    def get_min_size(self, entry, qty: int) -> int:
        """return entry size or qty if not set, invalid or insufficient"""

        def valid_number(num: str) -> int:
            """return int >= 0"""
            return int(num) if num.isdigit() and int(num) > 0 else 0

        return max(valid_number(entry.get()), qty)

    def create_selection_str(self) -> str:
        """add each selection type to str"""
        for k, v in self.checkboxes.items():
            if self.chr_types[k]:
                self.selection += v[2]  # type

    def create_valid_password(self, length: int) -> str:
        """generate a password of size length including all required character types"""
        while True:
            # set reqd vals to false, then to true when found in psw
            sym: bool = not self.chr_types["symbols"]
            lc: bool = not self.chr_types["lowercase"]
            uc: bool = not self.chr_types["uppercase"]
            dig: bool = not self.chr_types["digits"]
            psw: str = "".join(secrets.choice(self.selection) for _ in range(length))
            # ensure psw contains the required types
            for char in psw:
                if not sym:
                    if char in self.symbols:
                        sym = True
                if not lc:
                    if char in self.lowercase:
                        lc = True
                if not uc:
                    if char in self.uppercase:
                        uc = True
                if not dig:
                    if char in self.digits:
                        dig = True
                if all([lc, dig, sym, uc]):
                    return psw

    def run(self) -> None:
        """validate input and generate password(s)"""
        qty_types = self.get_char_types()
        length = self.get_min_size(self.e_length, qty_types)
        quantity = self.get_min_size(self.e_quantity, 1)

        self.create_selection_str()

        for _ in range(quantity):
            self.text_line(f"{self.create_valid_password(length)}")

    def copy(self) -> None:
        """copies text in textbox to clipboard"""
        data = self.textbox.get(1.0, "end").strip("\n")
        self.clipboard_clear()
        self.clipboard_append(data)

    def clear(self) -> None:
        """delete text in textbox and reset line count"""
        self.textbox.configure(state="normal")
        self.textbox.delete(f"0.0", f"end")
        self.textbox.configure(state="disabled")
        self.textbox_line = 1


if __name__ == "__main__":
    main()
