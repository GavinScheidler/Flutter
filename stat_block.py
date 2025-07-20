import tkinter as tk
from tkinter import ttk, messagebox

class CharacterCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flutter Character Creator")
        self.geometry("450x450")
        self.resizable(True, True) # Allow resizing
        self.configure(bg="#1e1e1e")
        # Attempting to change the icon
        try:
            self.iconbitmap('icon.ico')
        except tk.TclError:
            print("Warning: Could not load 'icon.ico'. Make sure the file exists and is a valid .ico file.")
            # Fallback for other OS or if .ico isn't preferred
            # You might try:
            # self.iconphoto(True, tk.PhotoImage(file='icon.png'))
            # self.photo_icon = tk.PhotoImage(file='icon.png') # Keep a reference to prevent garbage collection
            # self.iconphoto(True, self.photo_icon)

        # --- Predefined Features Data ---
        self.PREDEFINED_FEATURES = {
            "Veteran": {
                "stat_increase": ["Might", "Agility"],
                "description": "A veteran has seen combat before, and has the scars and knowledge of a life led in combat. Veterans come from diverse backgrounds, from bandits to town guards to once renowned heroes who have now faded into obscurity. No matter the source, veterans are proficient combat specialists.\n\n- Every attack deals an additional damage.\n- Survey Action: 1 Round, choose a creature, you learn the value of one statistic of your choosing, a random weakness or resistance, or the information of one action you have seen them perform.\n- Block Action: X Stamina, choosing an amount of stamina to expend, you gain temporary health equal to the stamina expended. This block goes away at the end of your next turn."
            },
            "Knave": {
                "stat_increase": "Agility",
                "description": "A Knave is a trickster, who often makes their life’s earnings swindling people and can be found in all walks of life. From the humble street pick-pocket to a crook whispering in a king's ear. Knaves are remarkably skilled in quiet movement, theft, and avoiding the victims of their exploits. Knaves are not necessarily evil, but are looked down on by more honest folk.\n\n- When attacking an opponent who is unaware of your presence, or who you’re flanking, deal double damage.\n- Annoy Action: 1 Round, choose a creature, you distract them with loud noises, pocket sand, or other distracting stimulus. Force the creature to turn towards you until the start of your next turn.\n- Hide Action: X Stamina, hide from those around, any creature with Mind lower than the stamina you expended to hide cannot target you with any action. This lasts until the start of your next turn. Any action that would affect another creature alerts them to your position removes the benefit of this action until you attempt to hide again."
            },
            "Scholar": {
                "stat_increase": "Mind",
                "description": "Scholars are almost always found in high society. Clustered to the ultra wealthy, these people come from nobility and have been given the privilege of a life surrounded by books, scrolls, and academia. Some scholars flee into the wilderness to research without supervision, and occasionally accept pupils from smaller villages, but the surroundings eventually degrade the quality of the research done, and lead more interested youth to pursue a life of a scribe to higher born people.\n\n- You gain a new derived stat, Mana. Mana is calculated by 3*Mind. Mana is restored during daily preparations.\n- Sparks: 1 Stamina X Mana, choose a creature within 15 spaces, they take X magic damage.\n- Research Action: 1 Workday, 100-Mind % chance to discover a new piece of lore related to what you are researching. Requires access to a library or populated town.",
                "special": {"derived_stat": "Mana"}
            },
            "Charlatan": {
                "stat_increase": "Will",
                "description": "Charlatans are similar to knaves, except they invest more in the mind over the body of theft. Charlatans will often be seen as loan sharks, gang leaders, or cheats. However, Charlatans are most successful in the open as diplomats. Tricky contracts and deals have bankrupted more kingdoms and ruined more lives than even the most influential cheat. Mind games and battles of will are a Charlatans bread and butter, and they naturally gravitate towards leading those with lower wills.\n\n- Your grit restores at the beginning of every round.\n- Belittle Action: 2 Stamina X Grit, choose a creature within range. If the creature can understand a language you speak, you shout harassments at it. Reduce their Grit by X. Once a creature has zero grit, this attack lowers the target’s will by half of X, while they are reduced to zero will, the creature obeys your commands and ignores other creature’s commands or pleas.\n- Inspire Action: 2 Stamina X Grit, choose a creature within range, restore the creature’s Grit. Any Grit exceeding their maximum is kept as temporary Grit."
            },
            "Wanderer": {
                "stat_increase": ["Might", "Agility", "Mind", "Will"],
                "description": "Wanderers have shirked the burdens of society and left to indulge in their own whims and wiles. Wanderers come from all walks of life, though tragedy of some form seems to hang over near all of them. It is said that any soul who lacks a place in the world finds a family in the groups of others who have left the world behind. A special language that transcends boundaries of land or life is known by all, and is said to be the root of most other languages, based on how quickly everyone seems to pick it up.\n\n- You learn the language “Primordial” and can leave hidden messages with it, only noticeable to others who know this language.\n- Aid Action: 1 Round, restore a value equal to your Will to a number of creatures equal to your Mind within 15 spaces to any derived stat of your choosing.\n- Steal Action: X Stamina, choose a creature within 5 spaces of you and a base stat. The target’s base stat is reduced and your base stat is improved by half of X. The target's base stat can not be reduced below 1. This effect lasts until the beginning of your next turn.",
                "special": {"language": "Primordial"}
            }
        }

        # --- Core Character Variables ---
        self.total_points = 8
        self.base_stats = {"Might": 1, "Agility": 1, "Mind": 1, "Will": 1}
        self.current_points = self.total_points
        self.stat_vars = {}
        self.frames = {}
        self.player_name = tk.StringVar()
        self.features = []
        self.stat_display_labels = {}
        self.language_entries = []
        self.language_label = None

        # --- Derived stat variables ---
        self.health_max_var = tk.IntVar()
        self.health_current = tk.IntVar()
        self.stamina_max_var = tk.IntVar()
        self.stamina_current = tk.IntVar()
        self.grit_max_var = tk.IntVar()
        self.grit_current = tk.IntVar()

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("Health.Horizontal.TProgressbar", troughcolor="#444444", background="#e63946", thickness=20)
        self.style.configure("Stamina.Horizontal.TProgressbar", troughcolor="#444444", background="#4cc9f0", thickness=20)
        self.style.configure("Grit.Horizontal.TProgressbar", troughcolor="#444444", background="#ffbe0b", thickness=20)
        self.style.configure("Mana.Horizontal.TProgressbar", troughcolor="#444444", background="#9a48d6", thickness=20)
        self.style.configure("TLabel", foreground="white", background="#1e1e1e", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="white", background="#1e1e1e")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold", "underline"), foreground="white", background="#1e1e1e")
        self.style.configure("Stat.TLabel", font=("Segoe UI", 12, "bold"), foreground="white", background="#1e1e1e")
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("TCombobox", font=("Segoe UI", 10))
        self.style.configure("TMenubutton", font=("Segoe UI", 10))

        self.show_stat_allocation_screen()

    def show_stat_allocation_screen(self):
        self.geometry("450x450")
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.frames["stat_alloc"] = frame

        ttk.Label(frame, text="Allocate Your Stats", style="Header.TLabel").pack(pady=10)
        self.point_label = ttk.Label(frame, text=f"Points Left: {self.current_points}", style="Stat.TLabel")
        self.point_label.pack(pady=5)

        for stat in self.base_stats:
            row = ttk.Frame(frame, style="TFrame")
            row.pack(pady=6, fill="x")
            ttk.Label(row, text=f"{stat}:", style="Stat.TLabel", width=12).pack(side="left")
            ttk.Button(row, text="-", width=3, command=lambda s=stat: self.modify_stat(s, -1)).pack(side="left", padx=(0, 5))
            self.stat_vars[stat] = tk.IntVar(value=self.base_stats[stat])
            ttk.Label(row, textvariable=self.stat_vars[stat], style="Stat.TLabel", width=3, anchor="center").pack(side="left")
            ttk.Button(row, text="+", width=3, command=lambda s=stat: self.modify_stat(s, 1)).pack(side="left", padx=(5, 0))

        ttk.Button(frame, text="Confirm", command=self.confirm_stats).pack(pady=20)

    def modify_stat(self, stat, delta):
        current = self.stat_vars[stat].get()
        if delta == 1 and self.current_points > 0:
            self.stat_vars[stat].set(current + 1)
            self.current_points -= 1
        elif delta == -1 and current > 1:
            self.stat_vars[stat].set(current - 1)
            self.current_points += 1
        self.point_label.config(text=f"Points Left: {self.current_points}")

    def confirm_stats(self):
        if self.current_points > 0:
            messagebox.showwarning("Unspent Points", "Please allocate all stat points before proceeding.")
            return
        for stat in self.base_stats:
            self.base_stats[stat] = self.stat_vars[stat].get()
        self.frames["stat_alloc"].destroy()
        self.show_stat_block_screen()

    def show_stat_block_screen(self):
        self.geometry("1100x800")
        # This top-level frame is packed into the main window, which is fine.
        frame = ttk.Frame(self, padding=20, style="TFrame")
        frame.pack(fill="both", expand=True)
        self.frames["stat_block"] = frame

        # --- Configure the grid layout for the 'frame' widget ---
        # This frame will use grid to manage its children (left_frame and right_frame).
        frame.grid_columnconfigure(1, weight=1)  # Make the right column (features) expand
        frame.grid_rowconfigure(0, weight=1)     # Make the row expand vertically

        # --- Create and place child frames using ONLY .grid() ---
        left_frame = ttk.Frame(frame, style="TFrame")
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 20))  # Use .grid(), NOT .pack()

        right_frame = ttk.Frame(frame, style="TFrame")
        right_frame.grid(row=0, column=1, sticky="nsew") # Use .grid(), NOT .pack()

        # --- LEFT SIDE: Stats and Bars ---
        self.setup_left_panel(left_frame)

        # --- RIGHT SIDE: Features panel ---
        self.setup_right_panel(right_frame)

    def setup_left_panel(self, parent_frame):
        player_name_frame = ttk.Frame(parent_frame, style="TFrame")
        player_name_frame.pack(pady=10, fill="x")
        ttk.Label(player_name_frame, text="Player Name:", style="Header.TLabel").pack(side="left", padx=(0, 10))
        self.player_name_entry = ttk.Entry(player_name_frame, textvariable=self.player_name, font=("Segoe UI", 12))
        self.player_name_entry.pack(side="left", fill="x", expand=True)

        for stat in self.base_stats:
            row = ttk.Frame(parent_frame, style="TFrame")
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=f"{stat}:", style="Stat.TLabel", width=12).pack(side="left")
            stat_label = ttk.Label(row, text=str(self.base_stats[stat]), style="Stat.TLabel")
            stat_label.pack(side="left")
            self.stat_display_labels[stat] = stat_label

        self.health_max_var.set(self.base_stats["Might"] * 3)
        self.health_current.set(self.health_max_var.get())
        self.stamina_max_var.set(self.base_stats["Agility"])
        self.stamina_current.set(self.stamina_max_var.get())
        self.grit_max_var.set(self.base_stats["Will"] * 2)
        self.grit_current.set(self.grit_max_var.get())

        self.bars_frame = ttk.Frame(parent_frame, style="TFrame")
        self.bars_frame.pack(fill="x", pady=8)
        self.health_progress_bar = self.add_bar(self.bars_frame, "Health", self.health_current, self.health_max_var, "Health.Horizontal.TProgressbar")
        self.stamina_progress_bar = self.add_bar(self.bars_frame, "Stamina", self.stamina_current, self.stamina_max_var, "Stamina.Horizontal.TProgressbar")
        self.grit_progress_bar = self.add_bar(self.bars_frame, "Grit", self.grit_current, self.grit_max_var, "Grit.Horizontal.TProgressbar")

        self.language_label = ttk.Label(parent_frame, text=f"\nLanguages (up to {1 + (self.base_stats['Mind'] - 1) // 3}):", style="Stat.TLabel")
        self.language_label.pack(pady=(15, 5))
        self.language_entries_frame = ttk.Frame(parent_frame, style="TFrame")
        self.language_entries_frame.pack(fill="x")
        self.create_language_entries()
        
        # Language Override Section
        override_lang_frame = ttk.Frame(parent_frame)
        override_lang_frame.pack(fill="x", pady=(10, 5))
        ttk.Label(override_lang_frame, text="Override, add language:", style="TLabel").pack(side="left")
        self.override_lang_entry = ttk.Entry(override_lang_frame, font=("Segoe UI", 10))
        self.override_lang_entry.pack(side="left", fill="x", expand=True, padx=(5,0))
        ttk.Button(override_lang_frame, text="Add", command=self.add_override_language).pack(side="left", padx=(5,0))


    def add_bar(self, parent, label, current_var, max_var, style_name):
        bar_frame = ttk.Frame(parent, style="TFrame")
        bar_frame.pack(fill="x", pady=6)
        ttk.Label(bar_frame, text=f"{label}:", style="Stat.TLabel", width=12).pack(side="left")
        progress = ttk.Progressbar(bar_frame, style=style_name, maximum=max_var.get(), variable=current_var, length=200)
        progress.pack(side="left", padx=5)
        ttk.Label(bar_frame, textvariable=current_var, style="Stat.TLabel", width=4, anchor="center").pack(side="left")
        ttk.Button(bar_frame, text="-", width=2, command=lambda: current_var.set(max(current_var.get() - 1, 0))).pack(side="left", padx=2)
        ttk.Button(bar_frame, text="+", width=2, command=lambda: current_var.set(min(current_var.get() + 1, max_var.get()))).pack(side="left", padx=2)
        ttk.Button(bar_frame, text="Reset", command=lambda: current_var.set(max_var.get())).pack(side="left", padx=2)
        return progress

    def setup_right_panel(self, parent_frame):
        # --- Predefined Features ---
        ttk.Label(parent_frame, text="Add Predefined Feature", style="SubHeader.TLabel").grid(row=0, column=0, sticky="w", pady=(10,5), columnspan=2)
        
        predefined_frame = ttk.Frame(parent_frame, style="TFrame")
        predefined_frame.grid(row=1, column=0, sticky="ew", columnspan=2)
        
        self.feature_combobox = ttk.Combobox(predefined_frame, values=list(self.PREDEFINED_FEATURES.keys()), state="readonly", width=30)
        self.feature_combobox.pack(side="left", padx=(0,10))
        self.feature_combobox.bind("<<ComboboxSelected>>", self.populate_feature_fields)

        self.predefined_stat_var = tk.StringVar()
        self.predefined_stat_menu = ttk.OptionMenu(predefined_frame, self.predefined_stat_var, "")
        self.predefined_stat_menu.config(state="disabled")
        self.predefined_stat_menu.pack(side="left", padx=10)
        
        ttk.Button(predefined_frame, text="Add Selected Feature", command=self.add_predefined_feature).pack(side="left", padx=10)

        # --- Custom Features ---
        ttk.Separator(parent_frame, orient='horizontal').grid(row=2, column=0, sticky="ew", pady=20, columnspan=2)
        ttk.Label(parent_frame, text="Add Custom Feature", style="SubHeader.TLabel").grid(row=3, column=0, sticky="w", pady=5, columnspan=2)
        
        custom_frame = ttk.Frame(parent_frame, style="TFrame")
        custom_frame.grid(row=4, column=0, sticky="nsew", columnspan=2)
        custom_frame.columnconfigure(1, weight=1)
        
        ttk.Label(custom_frame, text="Name:", style="Stat.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.custom_feature_name_var = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.custom_feature_name_var).grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(custom_frame, text="Stat Increase:", style="Stat.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.custom_feature_stat_var = tk.StringVar(value="Might")
        stat_choices = ["Might", "Agility", "Mind", "Will", "None"]
        ttk.OptionMenu(custom_frame, self.custom_feature_stat_var, "Might", *stat_choices).grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(custom_frame, text="Description:", style="Stat.TLabel").grid(row=2, column=0, sticky="nw", padx=5, pady=3)
        self.custom_feature_desc_text = tk.Text(custom_frame, height=4, width=30)
        self.custom_feature_desc_text.grid(row=2, column=1, sticky="ew", padx=5, pady=3)
        
        ttk.Button(custom_frame, text="Add Custom Feature", command=self.add_custom_feature).grid(row=3, column=1, sticky="e", pady=10, padx=5)

        # --- Feature List ---
        ttk.Separator(parent_frame, orient='horizontal').grid(row=5, column=0, sticky="ew", pady=20, columnspan=2)
        
        list_header_frame = ttk.Frame(parent_frame, style="TFrame")
        list_header_frame.grid(row=6, column=0, sticky="ew", columnspan=2)
        ttk.Label(list_header_frame, text="Added Features", style="SubHeader.TLabel").pack(side="left", pady=5)
        
        self.feature_tree = ttk.Treeview(parent_frame, columns=("Feature", "Bonus"), show="headings")
        self.feature_tree.heading("Feature", text="Feature Name")
        self.feature_tree.heading("Bonus", text="Stat Bonus")
        self.feature_tree.column("Feature", width=250)
        self.feature_tree.column("Bonus", width=100, anchor="center")
        self.feature_tree.grid(row=7, column=0, sticky="nsew", columnspan=2)
        parent_frame.rowconfigure(7, weight=1)
        
        # Add the remove button
        ttk.Button(parent_frame, text="Remove Selected Feature", command=self.remove_feature).grid(row=8, column=0, columnspan=2, pady=10)
        
        # Bind double-click event
        self.feature_tree.bind("<Double-1>", self.show_feature_description)

    def populate_feature_fields(self, event=None):
        selected_feature_name = self.feature_combobox.get()
        feature_data = self.PREDEFINED_FEATURES.get(selected_feature_name)
        if not feature_data: return

        # Handle stat increase options
        stat_increase = feature_data['stat_increase']
        menu = self.predefined_stat_menu["menu"]
        menu.delete(0, "end")

        if isinstance(stat_increase, list):
            for stat_choice in stat_increase:
                menu.add_command(label=stat_choice, command=lambda v=stat_choice: self.predefined_stat_var.set(v))
            self.predefined_stat_var.set(stat_increase[0])
            self.predefined_stat_menu.config(state="normal")
        else:
            menu.add_command(label=stat_increase, command=lambda v=stat_increase: self.predefined_stat_var.set(v))
            self.predefined_stat_var.set(stat_increase)
            self.predefined_stat_menu.config(state="disabled")

    def _add_feature_logic(self, name, stat, desc):
        """Shared logic for adding any feature. Returns True on success, False on failure."""
        # Prevent adding duplicate features (case-insensitive)
        existing_names = [f['Name'].lower() for f in self.features]
        if name.lower() in existing_names:
            messagebox.showwarning("Duplicate Feature", f"The feature '{name}' has already been added.")
            return False

        feature_to_add = {"Name": name, "Stat": stat, "Description": desc}
        self.features.append(feature_to_add)

        if stat in self.base_stats:
            self.base_stats[stat] += 1
            
        # Handle special rules for predefined features
        if name in self.PREDEFINED_FEATURES:
            feature_data = self.PREDEFINED_FEATURES[name]
            if 'special' in feature_data:
                special = feature_data['special']
                if special.get('derived_stat') == 'Mana' and not hasattr(self, 'mana_max_var'):
                    self.add_mana_bar()
                if special.get('language'):
                    self.add_language_programmatically(special['language'])
        
        self.update_displayed_stats()
        bonus_text = f"+1 {stat}" if stat != "None" else "N/A"
        self.feature_tree.insert("", "end", values=(name, bonus_text))
        return True

    def add_predefined_feature(self):
        name = self.feature_combobox.get()
        stat = self.predefined_stat_var.get()
        if not name or not stat:
            messagebox.showwarning("Input Error", "Please select a feature and a stat.")
            return

        desc = self.PREDEFINED_FEATURES[name]['description']
        self._add_feature_logic(name, stat, desc)
        
    def add_custom_feature(self):
        name = self.custom_feature_name_var.get().strip()
        stat = self.custom_feature_stat_var.get()
        desc = self.custom_feature_desc_text.get("1.0", "end").strip()

        if not name:
            messagebox.showwarning("Input Error", "Custom feature name cannot be empty.")
            return
        
        # Only clear fields if the feature was added successfully
        if self._add_feature_logic(name, stat, desc):
            # Clear custom fields
            self.custom_feature_name_var.set("")
            self.custom_feature_stat_var.set("Might")
            self.custom_feature_desc_text.delete("1.0", "end")

    def remove_feature(self):
        """Removes the selected feature from the tree and character."""
        selection = self.feature_tree.selection()
        if not selection:
            messagebox.showinfo("Information", "Please select a feature to remove.")
            return

        selected_item = self.feature_tree.item(selection[0])
        feature_name = selected_item['values'][0]

        # Find the feature in the master list
        feature_to_remove = next((f for f in self.features if f['Name'] == feature_name), None)

        if feature_to_remove:
            # Revert stat increase
            stat = feature_to_remove['Stat']
            if stat in self.base_stats:
                self.base_stats[stat] -= 1

            # Handle special rule reversals
            if feature_name == "Scholar":
                # Remove mana bar if it exists
                if hasattr(self, 'mana_progress_bar'):
                    self.mana_progress_bar.master.destroy()
                    del self.mana_max_var
                    del self.mana_current
                    del self.mana_progress_bar
            
            # Remove from master list BEFORE updating stats, so special languages get removed
            self.features.remove(feature_to_remove)
            
            # Remove from treeview
            self.feature_tree.delete(selection[0])
            
            # Update all displays
            self.update_displayed_stats()

    def show_feature_description(self, event):
        selection = self.feature_tree.selection()
        if not selection: return

        selected_item = self.feature_tree.item(selection[0])
        feature_name = selected_item['values'][0]

        found_feature = next((f for f in self.features if f['Name'] == feature_name), None)

        if found_feature:
            title = f"Feature: {found_feature['Name']}"
            bonus = f"+1 {found_feature['Stat']}" if found_feature['Stat'] != "None" else "No Stat Increase"
            message = f"Stat Increase: {bonus}\n\nDescription:\n{found_feature['Description']}"
            messagebox.showinfo(title, message)

    def add_mana_bar(self):
        self.mana_max_var = tk.IntVar(value=self.base_stats["Mind"] * 3)
        self.mana_current = tk.IntVar(value=self.mana_max_var.get())
        self.mana_progress_bar = self.add_bar(self.bars_frame, "Mana", self.mana_current, self.mana_max_var, "Mana.Horizontal.TProgressbar")
    
    def add_override_language(self):
        lang = self.override_lang_entry.get().strip()
        if lang:
            entry = ttk.Entry(self.language_entries_frame, font=("Segoe UI", 10))
            entry.insert(0, lang)
            entry.pack(fill="x", pady=3)
            self.language_entries.append(entry)
            self.override_lang_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Override language cannot be empty.")

    def add_language_programmatically(self, lang_name):
        # Prevent adding duplicates
        for entry in self.language_entries:
            if entry.get() == lang_name:
                return
        entry = ttk.Entry(self.language_entries_frame, font=("Segoe UI", 10))
        entry.insert(0, lang_name)
        entry.config(state="readonly")
        entry.pack(fill="x", pady=3)
        self.language_entries.append(entry)

    def create_language_entries(self):
        user_langs = [entry.get() for entry in self.language_entries if entry.get()]
        for widget in self.language_entries_frame.winfo_children():
            widget.destroy()
        self.language_entries.clear()

        mind = self.base_stats["Mind"]
        num_languages = 1 + (mind - 1) // 3
        self.language_label.config(text=f"\nLanguages (up to {num_languages}):")

        # Re-add all collected languages
        all_langs = []
        # Add the base number of empty slots first
        for i in range(num_languages):
            all_langs.append(user_langs[i] if i < len(user_langs) else "")

        # Add any extra/override languages
        if len(user_langs) > num_languages:
            all_langs.extend(user_langs[num_languages:])
        
        for lang_text in all_langs:
             entry = ttk.Entry(self.language_entries_frame, font=("Segoe UI", 10))
             entry.insert(0, lang_text)
             # Check if it was a special read-only language
             if lang_text in [f['special']['language'] for f in self.PREDEFINED_FEATURES.values() if 'special' in f and 'language' in f['special']]:
                 entry.config(state="readonly")
             entry.pack(fill="x", pady=3)
             self.language_entries.append(entry)


    def update_displayed_stats(self):
        for stat, label_widget in self.stat_display_labels.items():
            label_widget.config(text=str(self.base_stats[stat]))

        self.health_max_var.set(self.base_stats["Might"] * 3)
        self.stamina_max_var.set(self.base_stats["Agility"])
        self.grit_max_var.set(self.base_stats["Will"] * 2)

        if self.health_progress_bar:
            self.health_progress_bar.config(maximum=self.health_max_var.get())
            self.health_current.set(min(self.health_current.get(), self.health_max_var.get()))
        if self.stamina_progress_bar:
            self.stamina_progress_bar.config(maximum=self.stamina_max_var.get())
            self.stamina_current.set(min(self.stamina_current.get(), self.stamina_max_var.get()))
        if self.grit_progress_bar:
            self.grit_progress_bar.config(maximum=self.grit_max_var.get())
            self.grit_current.set(min(self.grit_current.get(), self.grit_max_var.get()))
        if hasattr(self, 'mana_progress_bar') and self.mana_progress_bar:
            self.mana_max_var.set(self.base_stats["Mind"] * 3)
            self.mana_progress_bar.config(maximum=self.mana_max_var.get())
            self.mana_current.set(min(self.mana_current.get(), self.mana_max_var.get()))

        self.create_language_entries()

if __name__ == "__main__":
    app = CharacterCreator()
    app.mainloop()