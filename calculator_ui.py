import tkinter as tk
import sys
from calculator import divide, average, first_element

BG       = "#1C1C1E"
COL_NUM  = "#2C2C2E"
COL_FUNC = "#3A3A3C"
COL_OP   = "#FF9500"
COL_EQ   = "#30D158"
FG       = "#FFFFFF"
FG_DIM   = "#8E8E93"

BTN_W = 76
BTN_H = 66
PAD   = 3


class CanvasButton:
    def __init__(self, parent, text, bg, fg, row, col, colspan=1, command=None):
        w = BTN_W * colspan + PAD * (colspan - 1)
        self.canvas = tk.Canvas(
            parent, width=w, height=BTN_H,
            bg=BG, highlightthickness=0, bd=0
        )
        self.canvas.grid(
            row=row, column=col, columnspan=colspan,
            padx=PAD, pady=PAD
        )
        self.bg = bg
        self.command = command
        self.w = w

        self.rect = self.canvas.create_rectangle(
            0, 0, w, BTN_H,
            fill=bg, outline="", width=0
        )
        font_size = 22 if len(text) == 1 else 18
        self.label = self.canvas.create_text(
            w // 2, BTN_H // 2,
            text=text, fill=fg,
            font=("Helvetica Neue", font_size, "bold")
        )

        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, e):
        r, g, b = (int(self.bg[i:i+2], 16) for i in (1, 3, 5))
        lighter = "#{:02X}{:02X}{:02X}".format(
            min(255, r + 40), min(255, g + 40), min(255, b + 40)
        )
        self.canvas.itemconfig(self.rect, fill=lighter)

    def _on_release(self, e):
        self.canvas.itemconfig(self.rect, fill=self.bg)
        if self.command:
            self.command()


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.resizable(False, False)
        self.window.configure(bg=BG)

        self.expr = ""
        self.just_evaled = False

        self._build_display()
        self._build_buttons()

    def _build_display(self):
        frame = tk.Frame(self.window, bg=BG)
        frame.grid(row=0, column=0, columnspan=4, sticky="ew",
                   padx=16, pady=(20, 8))

        self.sub_var = tk.StringVar(value="")
        tk.Label(
            frame, textvariable=self.sub_var,
            font=("Helvetica Neue", 13),
            bg=BG, fg=FG_DIM, anchor="e"
        ).pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        tk.Label(
            frame, textvariable=self.display_var,
            font=("Helvetica Neue", 48, "bold"),
            bg=BG, fg=FG, anchor="e"
        ).pack(fill="x")

    def _build_buttons(self):
        defs = [
            ("C",  COL_FUNC, 1, 0, 1),
            ("±",  COL_FUNC, 1, 1, 1),
            ("÷",  COL_OP,   1, 2, 1),
            ("×",  COL_OP,   1, 3, 1),
            ("7",  COL_NUM,  2, 0, 1),
            ("8",  COL_NUM,  2, 1, 1),
            ("9",  COL_NUM,  2, 2, 1),
            ("−",  COL_OP,   2, 3, 1),
            ("4",  COL_NUM,  3, 0, 1),
            ("5",  COL_NUM,  3, 1, 1),
            ("6",  COL_NUM,  3, 2, 1),
            ("+",  COL_OP,   3, 3, 1),
            ("1",  COL_NUM,  4, 0, 1),
            ("2",  COL_NUM,  4, 1, 1),
            ("3",  COL_NUM,  4, 2, 1),
            ("=",  COL_EQ,   4, 3, 1),
            ("0",  COL_NUM,  5, 0, 2),
            (".",  COL_NUM,  5, 2, 1),
            ("%",  COL_FUNC, 5, 3, 1),
        ]
        for (text, bg, row, col, colspan) in defs:
            CanvasButton(
                self.window, text, bg, FG,
                row, col, colspan,
                command=lambda t=text: self._press(t)
            )

    def _press(self, ch):
        if ch == "C":
            self.expr = ""
            self.just_evaled = False
            self.display_var.set("0")
            self.sub_var.set("")
            return

        is_op = ch in ("÷", "×", "−", "+")

        if ch == "=":
            if not self.expr:
                return

            safe = (self.expr
                    .replace("÷", "/")
                    .replace("×", "*")
                    .replace("−", "-"))

            # Direkt divide() aufrufen — kein try/except
            # ZeroDivisionError beendet die App hart
            if "/" in safe and safe.count("/") == 1:
                parts = safe.split("/")
                a = float(parts[0].strip())
                b = float(parts[1].strip())
                result = divide(a, b)  # crashed hier bei b=0
            else:
                result = eval(safe)

            result = round(result, 10)
            display = (str(int(result))
                       if isinstance(result, float) and result.is_integer()
                       else str(result))
            self.sub_var.set(self.expr + " =")
            self.display_var.set(display)
            self.expr = display
            self.just_evaled = True

            # sys.exit nach Ergebnis damit tkinter den Fehler nicht schluckt
            # Nur bei Division aktiv — Fehler propagiert nach oben
            return

        if ch == "±":
            if not self.expr:
                return
            self.expr = (self.expr[1:]
                         if self.expr.startswith("-")
                         else "-" + self.expr)
            self.display_var.set(self.expr)
            return

        if ch == "%":
            if not self.expr:
                return
            safe = (self.expr
                    .replace("÷", "/")
                    .replace("×", "*")
                    .replace("−", "-"))
            val = eval(safe)
            val = round(val / 100, 10)
            self.expr = (str(int(val))
                         if isinstance(val, float) and val.is_integer()
                         else str(val))
            self.display_var.set(self.expr)
            return

        if self.just_evaled and not is_op:
            self.expr = ""
            self.just_evaled = False
        self.just_evaled = False

        last = self.expr[-1:] if self.expr else ""
        if is_op and last in ("÷", "×", "−", "+"):
            self.expr = self.expr[:-1] + ch
        else:
            self.expr += ch

        self.display_var.set(self.expr)

    def run(self):
        # report_callback_exception überschreiben damit tkinter
        # den Fehler NICHT schluckt sondern die App wirklich beendet
        def crash_on_error(exc_type, exc_val, exc_tb):
            import traceback
            traceback.print_exception(exc_type, exc_val, exc_tb)
            sys.exit(1)

        self.window.report_callback_exception = crash_on_error
        self.window.mainloop()


if __name__ == "__main__":
    Calculator().run()