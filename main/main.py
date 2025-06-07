import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox


@dataclass
class PanelData:
    width: float
    length: float
    quantity: int
    area: float
    handles: float
    double_sided: bool


class PanelCalculator:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Panel Calculator")

        self.total_area = 0.0
        self.total_width = 0.0
        self.total_length = 0.0
        self.total_double_sided = 0.0
        self.quantity = 1

        self.font_large = ("Helvetica", 17)

        self.build_ui()

    def build_ui(self) -> None:
        tk.Label(self.root, text="Panel width (mm):", font=self.font_large).pack(pady=10)
        self.entry_width = tk.Entry(self.root, font=self.font_large)
        self.entry_width.pack(pady=5)
        self.width_var = tk.IntVar(value=0)
        tk.Checkbutton(self.root, text="Add to handles", variable=self.width_var, font=self.font_large).pack(pady=5)

        tk.Label(self.root, text="Panel length (mm):", font=self.font_large).pack(pady=10)
        self.entry_length = tk.Entry(self.root, font=self.font_large)
        self.entry_length.pack(pady=5)
        self.length_var = tk.IntVar(value=0)
        tk.Checkbutton(self.root, text="Add to handles", variable=self.length_var, font=self.font_large).pack(pady=5)

        self.double_sided_var = tk.IntVar(value=0)
        tk.Checkbutton(
            self.root,
            text="Double-sided panel (50% price per m²)",
            variable=self.double_sided_var,
            font=self.font_large,
        ).pack(pady=5)

        frame_quantity = tk.Frame(self.root)
        frame_quantity.pack(pady=15)
        tk.Button(frame_quantity, text="-", command=self.decrease_quantity, font=self.font_large, width=3).pack(
            side=tk.LEFT, padx=10
        )
        self.label_quantity = tk.Label(frame_quantity, text=f"Quantity: {self.quantity}", font=self.font_large)
        self.label_quantity.pack(side=tk.LEFT)
        tk.Button(frame_quantity, text="+", command=self.increase_quantity, font=self.font_large, width=3).pack(
            side=tk.LEFT, padx=10
        )

        tk.Button(self.root, text="Add panel", command=self.add_rectangle, font=self.font_large).pack(pady=15)

        tk.Label(self.root, text="Price per m²:", font=self.font_large).pack(pady=10)
        self.entry_price = tk.Entry(self.root, font=self.font_large)
        self.entry_price.pack(pady=5)

        tk.Label(self.root, text="Price per handle:", font=self.font_large).pack(pady=10)
        self.entry_handle_price = tk.Entry(self.root, font=self.font_large)
        self.entry_handle_price.pack(pady=5)

        tk.Label(self.root, text="Panel table:", font=self.font_large).pack(pady=10)
        self.table_text = tk.Text(self.root, height=10, width=75, font=("Helvetica", 13))
        self.table_text.pack(pady=10)

        tk.Button(self.root, text="Finish calculation", command=self.finish_calculation, font=self.font_large).pack(
            pady=15
        )

    def increase_quantity(self) -> None:
        self.quantity += 1
        self.label_quantity.config(text=f"Quantity: {self.quantity}")

    def decrease_quantity(self) -> None:
        if self.quantity > 1:
            self.quantity -= 1
            self.label_quantity.config(text=f"Quantity: {self.quantity}")

    def add_rectangle(self) -> None:
        try:
            width = float(self.entry_width.get())
            length = float(self.entry_length.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return

        width_m = width / 1000
        length_m = length / 1000
        area_m2 = width_m * length_m * self.quantity
        handles = 0.0

        if self.width_var.get() == 1:
            self.total_width += width_m * self.quantity
            handles += width_m * self.quantity
        if self.length_var.get() == 1:
            self.total_length += length_m * self.quantity
            handles += length_m * self.quantity

        if self.double_sided_var.get() == 1:
            self.total_double_sided += area_m2 * 0.5

        panel = PanelData(width, length, self.quantity, area_m2, handles, self.double_sided_var.get() == 1)

        messagebox.showinfo(
            "Panel Area",
            f"The area of the panel {width} mm x {length} mm in quantity {self.quantity} is: {area_m2:.4f} m²",
        )

        self.total_area += area_m2
        self.add_to_table(panel)

        self.entry_width.delete(0, tk.END)
        self.entry_length.delete(0, tk.END)
        self.width_var.set(0)
        self.length_var.set(0)
        self.double_sided_var.set(0)
        self.quantity = 1
        self.label_quantity.config(text=f"Quantity: {self.quantity}")

    def add_to_table(self, panel: PanelData) -> None:
        double_sided_text = "Yes" if panel.double_sided else "No"
        self.table_text.insert(
            tk.END,
            f"{panel.width} mm x {panel.length} mm | Quantity: {panel.quantity} | "
            f"Area: {panel.area:.4f} m² | Handles: {panel.handles:.4f} m | Double-sided: {double_sided_text}\n",
        )
        self.table_text.see(tk.END)

    def finish_calculation(self) -> None:
        total_handles = self.total_width + self.total_length

        try:
            price_m2 = float(self.entry_price.get())
            price_handle = float(self.entry_handle_price.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price input. Please enter numeric values.")
            return

        base_price = price_m2 * self.total_area
        handle_price = total_handles * price_handle
        double_sided_price = self.total_double_sided * price_m2
        total = base_price + handle_price + double_sided_price

        messagebox.showinfo(
            "Summary",
            f"Total area: {self.total_area:.4f} m²\n"
            f"Total handles: {total_handles:.4f} m\n"
            f"Base price: {base_price:.2f} zł\n"
            f"Handles price: {handle_price:.2f} zł\n"
            f"Double-sided additional price: {double_sided_price:.2f} zł\n"
            f"Total price: {total:.2f} zł",
        )
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PanelCalculator(root)
    root.mainloop()
