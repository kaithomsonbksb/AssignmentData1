import customtkinter as ctk

next_id = 1
lock_temp = True


class RunLog:
    def __init__(self):
        self.runs = {}
        self.terrain = {}
        self.duration = {}

    def add_run(self, run_id, distance, terrain, duration):
        if run_id in self.runs:
            raise ValueError(f"Run ID {run_id} already exists.")
        self.runs[run_id] = {
            "distance": distance,
            "terrain": terrain,
            "duration": duration,
        }
        if terrain not in self.terrain:
            self.terrain[terrain] = []
        self.terrain[terrain].append(run_id)
        if duration not in self.duration:
            self.duration[duration] = []
        self.duration[duration].append(run_id)

    def search_runs(self, terrain=None, duration=None):
        results = []
        for run_id, run in self.runs.items():
            if (terrain is None or run["terrain"] == terrain) and (
                duration is None or run["duration"] == duration
            ):
                results.append((run_id, run["distance"]))
        return results

    def delete_run(self, run_id):
        if run_id not in self.runs:
            raise ValueError(f"Run ID {run_id} does not exist.")
        run = self.runs.pop(run_id)
        self.terrain[run["terrain"]].remove(run_id)
        self.duration[run["duration"]].remove(run_id)
        if not self.terrain[run["terrain"]]:
            del self.terrain[run["terrain"]]
        if not self.duration[run["duration"]]:
            del self.duration[run["duration"]]
        return f"Run {run_id} removed: {run['distance']} km"


log = RunLog()


def gui_update_next_id():
    if lock_temp.get():
        global next_id
        entry_id.configure(state="normal")
        entry_id.delete(0, "end")
        entry_id.insert(0, str(next_id))
        entry_id.configure(state="readonly")
    else:
        entry_id.configure(state="normal")
        entry_id.delete(0, "end")


def gui_add_run():
    global next_id
    try:
        rid = int(entry_id.get())
        distance = entry_distance.get()
        terrain = entry_terrain.get()
        duration = entry_duration.get()
        log.add_run(rid, distance, terrain, duration)
        output.configure(text=f"Added run {rid}")
        next_id += 1
        gui_update_next_id()
        gui_update_terrain_dropdown()
    except Exception as e:
        output.configure(text=str(e))


def gui_search_runs():
    terrain = entry_terrain.get() or None
    duration = entry_duration.get() or None
    results = log.search_runs(terrain, duration)
    if results:
        output.configure(text="\n".join([f"{rid}: {dist} km" for rid, dist in results]))
    else:
        output.configure(text="No results found.")


def gui_delete_run():
    global next_id
    try:
        rid = int(entry_id.get())
        msg = log.delete_run(rid)
        output.configure(text=msg)
        if log.runs:
            max_id = max(log.runs.keys())
            next_id = max_id + 1
        else:
            next_id = 1
        gui_update_next_id()
        gui_update_terrain_dropdown()
    except Exception as e:
        output.configure(text=str(e))


def gui_edit_run():
    try:
        rid = int(entry_id.get())
        if rid not in log.runs:
            output.configure(text=f"Run ID {rid} does not exist.")
            return
        distance = entry_distance.get()
        terrain = entry_terrain.get()
        duration = entry_duration.get()
        log.runs[rid]["distance"] = distance
        log.runs[rid]["terrain"] = terrain
        log.runs[rid]["duration"] = duration
        output.configure(text=f"Run {rid} updated.")
        gui_update_terrain_dropdown()
    except Exception as e:
        output.configure(text=str(e))


def gui_update_terrain_dropdown():
    terrains = list(log.terrain.keys())
    entry_terrain.configure(values=terrains)


def gui_open_cycle_window():
    cycle_win = ctk.CTkToplevel(root)
    cycle_win.title("Cycle Through Runs")
    cycle_win.geometry("500x300")

    runs = list(log.runs.items())
    if not runs:
        msg = ctk.CTkLabel(cycle_win, text="No runs available.")
        msg.pack(pady=20)
        return

    idx = [0]

    def show_run():
        rid, r = runs[idx[0]]
        run_label.configure(
            text=f"ID: {rid}\nTerrain: {r['terrain']}\nDuration: {r['duration']}\n\n{r['distance']} km"
        )

    def next_run():
        idx[0] = (idx[0] + 1) % len(runs)
        show_run()

    def prev_run():
        idx[0] = (idx[0] - 1) % len(runs)
        show_run()

    run_label = ctk.CTkLabel(cycle_win, text="", wraplength=450, justify="left")
    run_label.pack(pady=20)

    btn_prev = ctk.CTkButton(cycle_win, text="Previous", command=prev_run)
    btn_prev.pack(side="left", padx=40, pady=10)
    btn_next = ctk.CTkButton(cycle_win, text="Next", command=next_run)
    btn_next.pack(side="right", padx=40, pady=10)

    show_run()


def gui_toggle_lock_temp():
    gui_update_next_id()


# GUI Setup
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Run Log")
root.geometry("600x800")

lock_temp = ctk.BooleanVar(value=True)

entry_id = ctk.CTkEntry(root, placeholder_text="Run ID", width=400, height=40)
entry_id.pack(padx=20, pady=10)
entry_distance = ctk.CTkEntry(
    root, placeholder_text="Distance (km)", width=400, height=40
)
entry_distance.pack(padx=20, pady=10)
entry_terrain = ctk.CTkComboBox(root, values=["Terrain"], width=400, height=40)
entry_terrain.pack(padx=20, pady=10)
entry_duration = ctk.CTkComboBox(
    root, values=["Short", "Medium", "Long"], width=400, height=40
)
entry_duration.pack(padx=20, pady=10)

gui_update_next_id()
gui_update_terrain_dropdown()

btn_add = ctk.CTkButton(root, text="Add Run", command=gui_add_run, width=200, height=40)
btn_add.pack(padx=20, pady=10)
btn_search = ctk.CTkButton(
    root, text="Search Runs", command=gui_search_runs, width=200, height=40
)
btn_search.pack(padx=20, pady=10)
btn_delete = ctk.CTkButton(
    root, text="Delete Run", command=gui_delete_run, width=200, height=40
)
btn_delete.pack(padx=20, pady=10)
btn_edit = ctk.CTkButton(root, text="Edit Run", command=gui_edit_run, width=200, height=40)
btn_edit.pack(padx=20, pady=10)
btn_cycle = ctk.CTkButton(
    root, text="Cycle Runs", command=gui_open_cycle_window, width=200, height=40
)
btn_cycle.pack(padx=20, pady=10)
lock_checkbox = ctk.CTkCheckBox(
    root, text="Lock", variable=lock_temp, command=gui_toggle_lock_temp
)
lock_checkbox.pack(padx=20, pady=(0, 10), anchor="w")

output = ctk.CTkLabel(
    root, text="", wraplength=500, justify="left", width=500, height=100
)
output.pack(padx=20, pady=20)

root.mainloop()
