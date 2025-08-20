import tkinter as tk
from tkinter import ttk, messagebox

class BankersGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banker's Algorithm - GUI (Python)")
        self.geometry("950x700")
        self.resizable(True, True)

        # Defaults (a common textbook example)
        self.default_allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        self.default_max = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]
        self.default_available = [3, 3, 2]

        self._build_controls()
        self._load_defaults()

    def _build_controls(self):
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=8, pady=6)

        ttk.Label(control_frame, text="Processes (n):").grid(row=0, column=0, sticky="w")
        self.n_var = tk.IntVar(value=5)
        n_spin = ttk.Spinbox(control_frame, from_=1, to=20, textvariable=self.n_var, width=5, command=self._rebuild_tables)
        n_spin.grid(row=0, column=1, sticky="w", padx=4)

        ttk.Label(control_frame, text="Resource types (m):").grid(row=0, column=2, sticky="w")
        self.m_var = tk.IntVar(value=3)
        m_spin = ttk.Spinbox(control_frame, from_=1, to=10, textvariable=self.m_var, width=5, command=self._rebuild_tables)
        m_spin.grid(row=0, column=3, sticky="w", padx=4)

        load_btn = ttk.Button(control_frame, text="Load Sample Data", command=self._load_defaults)
        load_btn.grid(row=0, column=4, padx=8)

        build_btn = ttk.Button(control_frame, text="Rebuild Tables", command=self._rebuild_tables)
        build_btn.grid(row=0, column=5, padx=8)

        # Matrices Frame
        matrices = ttk.Frame(self)
        matrices.pack(fill="both", expand=False, padx=8, pady=6)

        # Allocation table
        alloc_frame = ttk.LabelFrame(matrices, text="Allocation Matrix")
        alloc_frame.grid(row=0, column=0, padx=6, pady=6, sticky="n")
        self.alloc_entries = []
        self.alloc_frame = alloc_frame

        # Max table
        max_frame = ttk.LabelFrame(matrices, text="Max Matrix")
        max_frame.grid(row=0, column=1, padx=6, pady=6, sticky="n")
        self.max_entries = []
        self.max_frame = max_frame

        # Available vector
        avail_frame = ttk.LabelFrame(matrices, text="Available Vector")
        avail_frame.grid(row=0, column=2, padx=6, pady=6, sticky="n")
        self.available_entries = []
        self.available_frame = avail_frame

        # Lower controls: compute and request
        lower = ttk.Frame(self)
        lower.pack(fill="both", expand=True, padx=8, pady=6)

        btn_frame = ttk.Frame(lower)
        btn_frame.pack(fill="x", pady=4)

        ttk.Button(btn_frame, text="Compute Need & Safety", command=self.compute_safety).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Show Need Matrix", command=self.show_need).pack(side="left", padx=6)

        # Request controls
        request_frame = ttk.LabelFrame(lower, text="Resource Request")
        request_frame.pack(fill="x", pady=6)

        ttk.Label(request_frame, text="Process index (0..n-1):").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.request_pid = tk.IntVar(value=1)
        ttk.Entry(request_frame, textvariable=self.request_pid, width=6).grid(row=0, column=1, sticky="w", padx=4)

        ttk.Label(request_frame, text="Request vector (space separated):").grid(row=0, column=2, sticky="w", padx=4)
        self.request_vec = tk.StringVar(value="1 0 2")
        ttk.Entry(request_frame, textvariable=self.request_vec, width=24).grid(row=0, column=3, sticky="w", padx=4)

        ttk.Button(request_frame, text="Try Request", command=self.handle_request).grid(row=0, column=4, padx=6)

        # Output box
        out_frame = ttk.LabelFrame(lower, text="Output")
        out_frame.pack(fill="both", expand=True, pady=6)
        self.output = tk.Text(out_frame, height=15, wrap="word")
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # Initialize table widgets
        self._rebuild_tables()

    def _clear_frame_children(self, frame):
        for c in frame.winfo_children():
            c.destroy()

    def _rebuild_tables(self):
        n = self.n_var.get()
        m = self.m_var.get()
        # Rebuild allocation table
        self._clear_frame_children(self.alloc_frame)
        self.alloc_entries = []
        ttk.Label(self.alloc_frame, text="P\\R").grid(row=0, column=0, padx=2, pady=2)
        for j in range(m):
            ttk.Label(self.alloc_frame, text=f"R{j}").grid(row=0, column=j+1, padx=4)
        for i in range(n):
            ttk.Label(self.alloc_frame, text=f"P{i}").grid(row=i+1, column=0, padx=2)
            row_entries = []
            for j in range(m):
                e = ttk.Entry(self.alloc_frame, width=5)
                e.grid(row=i+1, column=j+1, padx=2, pady=1)
                e.insert(0, "0")
                row_entries.append(e)
            self.alloc_entries.append(row_entries)

        # Rebuild max table
        self._clear_frame_children(self.max_frame)
        self.max_entries = []
        ttk.Label(self.max_frame, text="P\\R").grid(row=0, column=0, padx=2, pady=2)
        for j in range(m):
            ttk.Label(self.max_frame, text=f"R{j}").grid(row=0, column=j+1, padx=4)
        for i in range(n):
            ttk.Label(self.max_frame, text=f"P{i}").grid(row=i+1, column=0, padx=2)
            row_entries = []
            for j in range(m):
                e = ttk.Entry(self.max_frame, width=5)
                e.grid(row=i+1, column=j+1, padx=2, pady=1)
                e.insert(0, "0")
                row_entries.append(e)
            self.max_entries.append(row_entries)

        # Rebuild available vector
        self._clear_frame_children(self.available_frame)
        self.available_entries = []
        ttk.Label(self.available_frame, text="R").grid(row=0, column=0)
        for j in range(m):
            ttk.Label(self.available_frame, text=f"R{j}").grid(row=0, column=j+1, padx=4)
            e = ttk.Entry(self.available_frame, width=5)
            e.grid(row=1, column=j+1, padx=2, pady=1)
            e.insert(0, "0")
            self.available_entries.append(e)

    def _load_defaults(self):
        n = len(self.default_allocation)
        m = len(self.default_available)
        self.n_var.set(n)
        self.m_var.set(m)
        self._rebuild_tables()

        # Populate allocation
        for i in range(n):
            for j in range(m):
                self.alloc_entries[i][j].delete(0, tk.END)
                self.alloc_entries[i][j].insert(0, str(self.default_allocation[i][j]))
        # Populate max
        for i in range(n):
            for j in range(m):
                self.max_entries[i][j].delete(0, tk.END)
                self.max_entries[i][j].insert(0, str(self.default_max[i][j]))
        # Populate available
        for j in range(m):
            self.available_entries[j].delete(0, tk.END)
            self.available_entries[j].insert(0, str(self.default_available[j]))

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Loaded sample data (classic textbook example).\n")

    def _read_matrices(self):
        try:
            n = self.n_var.get()
            m = self.m_var.get()
            alloc = [[int(self.alloc_entries[i][j].get()) for j in range(m)] for i in range(n)]
            mx = [[int(self.max_entries[i][j].get()) for j in range(m)] for i in range(n)]
            avail = [int(self.available_entries[j].get()) for j in range(m)]
            return alloc, mx, avail
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid numeric entries: {e}")
            return None

    def compute_need(self, alloc, mx):
        n = len(alloc)
        m = len(alloc[0])
        need = [[mx[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
        return need

    def safety_algorithm(self, alloc, mx, avail):
        n = len(alloc)
        m = len(avail)
        need = self.compute_need(alloc, mx)

        work = avail.copy()
        finish = [False] * n
        safe_seq = []

        changed = True
        while changed:
            changed = False
            for i in range(n):
                if not finish[i]:
                    # check if need[i] <= work
                    if all(need[i][j] <= work[j] for j in range(m)):
                        # can allocate, simulate finishing
                        for j in range(m):
                            work[j] += alloc[i][j]
                        finish[i] = True
                        safe_seq.append(i)
                        changed = True
        is_safe = all(finish)
        return is_safe, safe_seq, need, work

    def compute_safety(self):
        data = self._read_matrices()
        if not data:
            return
        alloc, mx, avail = data
        is_safe, safe_seq, need, final_work = self.safety_algorithm(alloc, mx, avail)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Need matrix:\n")
        for i, row in enumerate(need):
            self.output.insert(tk.END, f"P{i}: {row}\n")
        self.output.insert(tk.END, "\n")
        if is_safe:
            self.output.insert(tk.END, f"System is in a SAFE state.\nSafe sequence: {['P'+str(x) for x in safe_seq]}\n")
        else:
            self.output.insert(tk.END, "System is in an UNSAFE state. No safe sequence found.\n")
        self.output.insert(tk.END, f"\nFinal Work (available after running sequence): {final_work}\n")

    def show_need(self):
        data = self._read_matrices()
        if not data:
            return
        alloc, mx, avail = data
        need = self.compute_need(alloc, mx)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "Need matrix:\n")
        for i, row in enumerate(need):
            self.output.insert(tk.END, f"P{i}: {row}\n")

    def handle_request(self):
        data = self._read_matrices()
        if not data:
            return
        alloc, mx, avail = data
        n = len(alloc)
        m = len(avail)

        try:
            pid = int(self.request_pid.get())
            req_list = list(map(int, self.request_vec.get().strip().split()))
            if pid < 0 or pid >= n:
                raise ValueError("Process index out of range")
            if len(req_list) != m:
                raise ValueError("Request vector length must equal number of resources (m).")
        except Exception as e:
            messagebox.showerror("Request Error", f"Invalid request input: {e}")
            return

        # Banker's request algorithm:
        need = self.compute_need(alloc, mx)
        # 1. If request > need -> error
        if any(req_list[j] > need[pid][j] for j in range(m)):
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Request {req_list} exceeds process P{pid}'s need {need[pid]}. Denied.\n")
            return

        # 2. If request > available -> cannot grant now
        if any(req_list[j] > avail[j] for j in range(m)):
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Request {req_list} cannot be granted right now. Resources not available: Available={avail}\n")
            return

        # 3. Pretend to allocate and check safety
        # make deep copies to simulate
        import copy
        alloc_sim = copy.deepcopy(alloc)
        avail_sim = avail.copy()
        mx_sim = copy.deepcopy(mx)

        for j in range(m):
            alloc_sim[pid][j] += req_list[j]
            avail_sim[j] -= req_list[j]

        is_safe, safe_seq, need_sim, final_work = self.safety_algorithm(alloc_sim, mx_sim, avail_sim)
        self.output.delete(1.0, tk.END)
        if is_safe:
            self.output.insert(tk.END, f"After granting request {req_list} to P{pid}, the system is SAFE.\n")
            self.output.insert(tk.END, f"Safe sequence would be: {['P'+str(x) for x in safe_seq]}\n")
            self.output.insert(tk.END, f"New Available after granting: {avail_sim}\n")
            # Optionally commit simulated allocation into GUI (ask user)
            if messagebox.askyesno("Commit Allocation?", "The request can be granted and leaves the system safe.\nDo you want to commit this allocation to the current matrices in the GUI?"):
                for j in range(m):
                    self.alloc_entries[pid][j].delete(0, tk.END)
                    self.alloc_entries[pid][j].insert(0, str(alloc_sim[pid][j]))
                    self.available_entries[j].delete(0, tk.END)
                    self.available_entries[j].insert(0, str(avail_sim[j]))
                self.output.insert(tk.END, "Committed allocation and updated Available vector in GUI.\n")
        else:
            self.output.insert(tk.END, f"After granting request {req_list} to P{pid}, the system would be UNSAFE.\nRequest DENIED by Banker.\n")

if __name__ == "__main__":
    app = BankersGUI()
    app.mainloop()
