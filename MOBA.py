"""
MOBA Team Management System
Version: V0.2.0
Author: Namathieu (Updated by Gemini)

Change Log:
- Replaced the hybrid assignment algorithm (Brute-Force/Greedy) with the
  Hungarian algorithm (via SciPy) for guaranteed optimal team composition
  for any roster size.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from itertools import permutations
import numpy as np
from scipy.optimize import linear_sum_assignment

# --- NOTE: NEW DEPENDENCIES ---
# This version uses the Hungarian algorithm for optimal team assignment.
# You must install the scipy and numpy libraries to run it:
# pip install scipy numpy

class ModernTeamManagementApp:
    # --- CONFIGURABLE ROLE AND SKILL DEFINITIONS ---
    ROLES = {
        # Each role has primary and secondary skills (edit here to change role requirements)
        "Top Laner": {"primary": ["Bravery", "Composure", "Concentration"],
                      "secondary": ["Communication", "Vision"]},
        "Jungler": {"primary": ["Bravery", "Decision", "Vision", "Anticipation", "Communication", "Memory", "Teamwork"],
                    "secondary": ["Composure", "Concentration", "Leadership", "Flair"]},
        "Mid Laner": {"primary": ["Leadership", "Vision", "Anticipation", "Communication", "Flair"],
                      "secondary": ["Bravery", "Composure", "Decision", "Concentration", "Teamwork"]},
        "Bot Laner": {"primary": ["Accuracy", "Dexterity"],
                      "secondary": ["Composure", "Decision", "Determination", "Leadership", "Vision", "Teamwork", "Flair", "Concentration", "Communication", "Anticipation"]},
        "Support": {"primary": ["Leadership", "Vision", "Memory", "Teamwork", "Communication", "Anticipation"],
                    "secondary": ["Composure", "Decision", "Concentration"]}
    }

    # List of all possible skills (edit here to add/remove skills)
    SKILLS = [
        "Accuracy", "Bravery", "Composure", "Decision", "Determination",
        "Leadership", "Stamina", "Vision", "Anticipation", "Communication",
        "Concentration", "Dexterity", "Flair", "Memory", "Quickness", "Teamwork"
    ]

    # Color palette for UI (edit here for theme)
    COLORS = {
        'primary': '#2E3440',
        'secondary': '#3B4252',
        'accent': '#5E81AC',
        'success': '#A3BE8C',
        'warning': '#EBCB8B',
        'danger': '#BF616A',
        'light': '#ECEFF4',
        'text': '#2E3440',
        'text_light': '#4C566A'
    }

    def __init__(self, root):
        # --- MAIN APP STATE ---
        self.root = root
        self.root.title("🎮 Advanced Team Management System V0.2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.COLORS['light'])
        self.setup_styles()  # Set up custom styles
        self.players = []  # List of player dicts
        self.selected_player_index = None  # For editing
        self.current_mode = "add"  # "add" or "edit"
        self.create_widgets()  # Build UI
        self.center_window()  # Center window on screen

    # --- UI STYLING ---
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        # Button and frame styles (edit here for look & feel)
        style.configure('Modern.TButton',
                       background=self.COLORS['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        style.map('Modern.TButton',
                 background=[('active', '#4C7899')])
        style.configure('Success.TButton',
                       background=self.COLORS['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        style.configure('Danger.TButton',
                       background=self.COLORS['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=1)
        style.configure('Heading.TLabel',
                       background='white',
                       foreground=self.COLORS['text'],
                       font=('Segoe UI', 12, 'bold'))
        style.configure('Subheading.TLabel',
                       background='white',
                       foreground=self.COLORS['text_light'],
                       font=('Segoe UI', 10))

    def center_window(self):
        # Center the main window on the screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    # --- UI LAYOUT CREATION (Identical to previous version) ---
    def create_widgets(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        self.create_header(main_container)
        content_paned = ttk.PanedWindow(main_container, orient='horizontal')
        content_paned.pack(fill='both', expand=True, pady=(20, 0))
        left_panel = self.create_left_panel(content_paned)
        content_paned.add(left_panel, weight=1)
        right_panel = self.create_right_panel(content_paned)
        content_paned.add(right_panel, weight=1)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(header_frame, 
                               text="🎮 Team Management System",
                               font=('Segoe UI', 18, 'bold'),
                               foreground=self.COLORS['text'])
        title_label.pack(side='left')
        subtitle_label = ttk.Label(header_frame,
                                  text="Build and optimize your MOBA esports team composition",
                                  font=('Segoe UI', 10),
                                  foreground=self.COLORS['text_light'])
        subtitle_label.pack(side='left', padx=(10, 0))

    def create_left_panel(self, parent):
        left_frame = ttk.Frame(parent)
        form_card = ttk.LabelFrame(left_frame, text="Player Information", 
                                  style='Card.TFrame', padding=20)
        form_card.pack(fill='x', pady=(0, 20))
        info_frame = ttk.Frame(form_card)
        info_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(info_frame, text="Player Name:", 
                 style='Subheading.TLabel').grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.player_name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.player_name_var, 
                              font=('Segoe UI', 10), width=25)
        name_entry.grid(row=1, column=0, sticky='ew', padx=(0, 10))
        ttk.Label(info_frame, text="Age:", 
                 style='Subheading.TLabel').grid(row=0, column=1, sticky='w', pady=(0, 5))
        self.player_age_var = tk.IntVar()
        age_spinbox = ttk.Spinbox(info_frame, from_=16, to=35, width=8,
                                 textvariable=self.player_age_var, font=('Segoe UI', 10))
        age_spinbox.grid(row=1, column=1, sticky='w')
        info_frame.grid_columnconfigure(0, weight=1)
        self.create_skills_section(form_card)
        self.create_action_buttons(form_card)
        team_ops_card = ttk.LabelFrame(left_frame, text="Team Operations", 
                                      style='Card.TFrame', padding=20)
        team_ops_card.pack(fill='x')
        self.create_team_operations(team_ops_card)
        return left_frame

    def create_skills_section(self, parent):
        skills_frame = ttk.LabelFrame(parent, text="Player Skills (0-100)", padding=15)
        skills_frame.pack(fill='both', expand=True, pady=(15, 15))
        self.skill_vars = {}
        self.skill_scales = {}
        for idx, skill in enumerate(self.SKILLS):
            row = idx // 2
            col = (idx % 2) * 3
            ttk.Label(skills_frame, text=f"{skill}:", 
                     style='Subheading.TLabel').grid(row=row, column=col, sticky='w', padx=(0, 10), pady=5)
            self.skill_vars[skill] = tk.IntVar(value=50)
            scale = ttk.Scale(skills_frame, from_=0, to=100, 
                            variable=self.skill_vars[skill],
                            orient='horizontal', length=120)
            scale.grid(row=row, column=col+1, sticky='ew', padx=(0, 5), pady=5)
            self.skill_scales[skill] = scale
            value_label = ttk.Label(skills_frame, text="50", width=3,
                                   style='Subheading.TLabel')
            value_label.grid(row=row, column=col+2, pady=5)
            def update_label(value, label=value_label):
                label.config(text=str(int(float(value))))
            scale.config(command=update_label)
        for i in range(0, 6, 3):
            skills_frame.grid_columnconfigure(i+1, weight=1)

    def create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(15, 0))
        self.add_button = ttk.Button(button_frame, text="➕ Add Player", 
                                    command=self.add_player, style='Success.TButton')
        self.add_button.pack(side='left', padx=(0, 10))
        self.update_button = ttk.Button(button_frame, text="✏️ Update Player", 
                                       command=self.update_player, style='Modern.TButton',
                                       state='disabled')
        self.update_button.pack(side='left', padx=(0, 10))
        self.cancel_button = ttk.Button(button_frame, text="❌ Cancel", 
                                       command=self.cancel_edit, style='Danger.TButton',
                                       state='disabled')
        self.cancel_button.pack(side='left')
        ttk.Button(button_frame, text="🎲 Random Player", 
                  command=self.generate_random_player, 
                  style='Modern.TButton').pack(side='right')

    def create_team_operations(self, parent):
        ops_frame = ttk.Frame(parent)
        ops_frame.pack(fill='x')
        file_frame = ttk.Frame(ops_frame)
        file_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(file_frame, text="💾 Save Team", 
                  command=self.save_team, style='Modern.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(file_frame, text="📁 Load Team", 
                  command=self.load_team, style='Modern.TButton').pack(side='left')
        ttk.Button(ops_frame, text="🔍 Analyze Team Composition", 
                  command=self.evaluate_team, style='Success.TButton').pack(fill='x')

    def create_right_panel(self, parent):
        right_frame = ttk.Frame(parent)
        list_card = ttk.LabelFrame(right_frame, text="Team Roster", 
                                  style='Card.TFrame', padding=20)
        list_card.pack(fill='both', expand=True, padx=(20, 0))
        search_frame = ttk.Frame(list_card)
        search_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(search_frame, text="🔍 Search:", 
                 style='Subheading.TLabel').pack(side='left', padx=(0, 10))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        search_entry.bind('<KeyRelease>', self.filter_players)
        list_frame = ttk.Frame(list_card)
        list_frame.pack(fill='both', expand=True, pady=(0, 15))
        columns = ('Name', 'Age', 'Best Role', 'Best Score')
        self.player_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        self.player_tree.heading('Name', text='Player Name')
        self.player_tree.heading('Age', text='Age')
        self.player_tree.heading('Best Role', text='Best Role')
        self.player_tree.heading('Best Score', text='Score')
        self.player_tree.column('Name', width=150)
        self.player_tree.column('Age', width=60)
        self.player_tree.column('Best Role', width=120)
        self.player_tree.column('Best Score', width=80)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.player_tree.yview)
        self.player_tree.configure(yscrollcommand=scrollbar.set)
        self.player_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.player_tree.bind('<Double-1>', self.show_player_details)
        self.player_tree.bind('<<TreeviewSelect>>', self.on_player_select)
        mgmt_frame = ttk.Frame(list_card)
        mgmt_frame.pack(fill='x')
        ttk.Button(mgmt_frame, text="✏️ Edit Player", 
                  command=self.edit_selected_player, 
                  style='Modern.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(mgmt_frame, text="🗑️ Delete Player", 
                  command=self.delete_player, 
                  style='Danger.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(mgmt_frame, text="📊 View Details", 
                  command=self.show_selected_player_details, 
                  style='Modern.TButton').pack(side='left')
        return right_frame

    # --- PLAYER MANAGEMENT LOGIC (Identical to previous version) ---
    def generate_random_player(self):
        import random
        names = ["Phoenix", "Shadow", "Lightning", "Storm", "Blaze", "Frost", "Nova", "Titan", 
                "Viper", "Falcon", "Dragon", "Wolf", "Raven", "Eagle", "Tiger", "Shark"]
        name = f"{random.choice(names)}{random.randint(1, 99)}"
        age = random.randint(17, 28)
        self.player_name_var.set(name)
        self.player_age_var.set(age)
        for skill in self.SKILLS:
            self.skill_vars[skill].set(random.randint(0, 100))

    def add_player(self):
        if not self.validate_input(): return
        player_data = self.get_player_data()
        self.players.append(player_data)
        self.refresh_player_list()
        self.clear_inputs()
        messagebox.showinfo("Success", f"Player '{player_data['name']}' added successfully!")

    def update_player(self):
        if self.selected_player_index is None or not self.validate_input(): return
        player_data = self.get_player_data()
        self.players[self.selected_player_index] = player_data
        self.refresh_player_list()
        self.cancel_edit()
        messagebox.showinfo("Success", f"Player '{player_data['name']}' updated successfully!")

    def edit_selected_player(self):
        selection = self.player_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a player to edit.")
            return
        item_id = self.player_tree.item(selection[0])['values'][0]
        self.selected_player_index = next((i for i, p in enumerate(self.players) if p["name"] == item_id), None)
        if self.selected_player_index is None: return

        player = self.players[self.selected_player_index]
        self.player_name_var.set(player["name"])
        self.player_age_var.set(player["age"])
        for skill, value in player["skills"].items():
            self.skill_vars[skill].set(value)
        self.current_mode = "edit"
        self.add_button.config(state='disabled')
        self.update_button.config(state='normal')
        self.cancel_button.config(state='normal')

    def cancel_edit(self):
        self.current_mode = "add"
        self.selected_player_index = None
        self.add_button.config(state='normal')
        self.update_button.config(state='disabled')
        self.cancel_button.config(state='disabled')
        self.clear_inputs()

    def delete_player(self):
        selection = self.player_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a player to delete.")
            return
        item_id = self.player_tree.item(selection[0])['values'][0]
        player_index = next((i for i, p in enumerate(self.players) if p["name"] == item_id), None)

        if player_index is None: return
        player = self.players[player_index]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{player['name']}'?"):
            del self.players[player_index]
            self.refresh_player_list()
            if self.current_mode == "edit" and self.selected_player_index == player_index:
                self.cancel_edit()

    def validate_input(self):
        name = self.player_name_var.get().strip()
        age = self.player_age_var.get()
        if not name:
            messagebox.showerror("Input Error", "Player name is required.")
            return False
        if not 16 <= age <= 35:
            messagebox.showerror("Input Error", "Player age must be between 16 and 35.")
            return False
        existing_names = [p["name"] for i, p in enumerate(self.players) if i != self.selected_player_index]
        if name in existing_names:
            messagebox.showerror("Input Error", "Player name already exists.")
            return False
        return True

    def get_player_data(self):
        return {"name": self.player_name_var.get().strip(), "age": self.player_age_var.get(),
                "skills": {skill: var.get() for skill, var in self.skill_vars.items()}}

    def clear_inputs(self):
        self.player_name_var.set("")
        self.player_age_var.set(20)
        for var in self.skill_vars.values(): var.set(50)

    def filter_players(self, event=None):
        self.refresh_player_list()

    def refresh_player_list(self):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        search_term = self.search_var.get().lower()
        for player in self.players:
            if search_term and search_term not in player["name"].lower(): continue
            percentages = self.calculate_role_percentages(player)
            best_role = max(percentages.items(), key=lambda x: x[1])
            self.player_tree.insert('', 'end', values=(player["name"], player["age"], best_role[0], f"{best_role[1]:.1f}%"))

    def on_player_select(self, event=None):
        pass # This logic is now handled inside edit/delete functions to be more robust

    def show_selected_player_details(self):
        selection = self.player_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a player to view details.")
            return
        item_id = self.player_tree.item(selection[0])['values'][0]
        player = next((p for p in self.players if p["name"] == item_id), None)
        if player: self.show_player_details_window(player)

    def show_player_details(self, event=None):
        selection = self.player_tree.selection()
        if not selection: return
        item_id = self.player_tree.item(selection[0])['values'][0]
        player = next((p for p in self.players if p["name"] == item_id), None)
        if player: self.show_player_details_window(player)

    def show_player_details_window(self, player):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Player Details - {player['name']}")
        details_window.geometry("600x500")
        details_window.configure(bg=self.COLORS['light'])
        details_window.transient(self.root)
        details_window.grab_set()
        main_frame = ttk.Frame(details_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        info_frame = ttk.LabelFrame(main_frame, text="Player Information", padding=15)
        info_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(info_frame, text=f"Name: {player['name']}", font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        ttk.Label(info_frame, text=f"Age: {player['age']}", font=('Segoe UI', 10)).pack(anchor='w')
        skills_frame = ttk.LabelFrame(main_frame, text="Skills Breakdown", padding=15)
        skills_frame.pack(fill='both', expand=True, pady=(0, 15))
        for i, (skill, value) in enumerate(player["skills"].items()):
            row, col = i // 2, (i % 2) * 2
            ttk.Label(skills_frame, text=f"{skill}:", font=('Segoe UI', 9)).grid(row=row, column=col, sticky='w', padx=5, pady=2)
            ttk.Label(skills_frame, text=str(value), font=('Segoe UI', 9, 'bold')).grid(row=row, column=col+1, sticky='w', padx=5, pady=2)
        roles_frame = ttk.LabelFrame(main_frame, text="Role Fitness", padding=15)
        roles_frame.pack(fill='x')
        percentages = self.calculate_role_percentages(player)
        sorted_roles = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        for role, percentage in sorted_roles:
            role_frame = ttk.Frame(roles_frame)
            role_frame.pack(fill='x', pady=2)
            ttk.Label(role_frame, text=f"{role}:", width=15).pack(side='left')
            ttk.Label(role_frame, text=f"{percentage:.1f}%", font=('Segoe UI', 9, 'bold')).pack(side='left', padx=(5, 0))

    # --- SAVE/LOAD TEAM DATA (Identical to previous version) ---
    def save_team(self):
        if not self.players:
            messagebox.showwarning("Save Error", "No players to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Save Team")
        if file_path:
            try:
                with open(file_path, "w") as f: json.dump(self.players, f, indent=4)
                messagebox.showinfo("Success", f"Team saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save team: {str(e)}")

    def load_team(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Load Team")
        if file_path:
            try:
                with open(file_path, "r") as f: self.players = json.load(f)
                self.refresh_player_list()
                messagebox.showinfo("Success", f"Team loaded successfully from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load team: {str(e)}")

    # --- ROLE FIT CALCULATION LOGIC (Identical to previous version) ---
    def calculate_role_percentages(self, player):
        percentages = {}
        for role, criteria in self.ROLES.items():
            primary_skills = [player["skills"].get(skill, 0) for skill in criteria["primary"]]
            primary_score = sum(self.apply_diminishing_returns(s) for s in primary_skills)
            max_primary = len(criteria["primary"]) * 100
            primary_percentage = (primary_score / max_primary) * 100 if max_primary > 0 else 0
            
            age_multiplier = self.calculate_age_multiplier(player["age"])
            base_percentage = primary_percentage * age_multiplier
            
            role_bonus = self.calculate_role_bonus(player, role)

            secondary_bonus = 0
            if "secondary" in criteria and criteria["secondary"]:
                secondary_skills = [player["skills"].get(skill, 0) for skill in criteria["secondary"]]
                secondary_score = sum(self.apply_diminishing_returns(s) for s in secondary_skills)
                max_secondary = len(criteria["secondary"]) * 100
                secondary_percentage = (secondary_score / max_secondary) * 100 if max_secondary > 0 else 0
                secondary_bonus = min(15, (secondary_percentage / 100) * 15)

            final_percentage = base_percentage + role_bonus + secondary_bonus
            percentages[role] = round(max(0, min(final_percentage, 100)), 2)
        return percentages

    def apply_diminishing_returns(self, skill_value):
        if skill_value <= 70: return skill_value
        elif skill_value <= 85: return 70 + (skill_value - 70) * 0.8
        else: return 82 + (skill_value - 85) * 0.6

    def calculate_role_bonus(self, player, role):
        bonus, skills = 0, player["skills"]
        role_bonuses = {
            "Jungler": ([("Decision", 80), ("Vision", 80), ("Communication", 80)], 15),
            "Mid Laner": ([("Leadership", 80), ("Vision", 80), ("Flair", 80)], 15),
            "Bot Laner": ([("Accuracy", 90), ("Dexterity", 90)], 20),
            "Support": ([("Vision", 80), ("Communication", 80), ("Teamwork", 80)], 15),
            "Top Laner": ([("Bravery", 80), ("Composure", 80), ("Concentration", 80)], 15),
        }
        if role in role_bonuses:
            core_skills, b_val = role_bonuses[role]
            if all(skills.get(s, 0) >= threshold for s, threshold in core_skills):
                bonus += b_val
        return min(bonus, 25)

    def calculate_age_multiplier(self, age):
        if 18 <= age <= 22: return 1.0
        elif 23 <= age <= 25: return 0.98
        elif 26 <= age <= 28: return 0.95
        elif age < 18: return 0.90
        else: return 0.88

    # --- TEAM EVALUATION AND OPTIMIZATION (LOGIC REWRITTEN) ---
    def evaluate_team(self):
        if not self.players:
            messagebox.showwarning("Evaluate Error", "No players to evaluate.")
            return
        
        num_roles = len(self.ROLES)
        if len(self.players) < num_roles:
            messagebox.showwarning("Evaluate Error", f"Not enough players for a full team. Need at least {num_roles} players.")
            return

        # Pre-calculate role percentages for each player
        for player in self.players:
            player["percentages"] = self.calculate_role_percentages(player)

        best_assignment = self.find_optimal_assignment_hungarian()
        self.show_evaluation_results(best_assignment)

    def find_optimal_assignment_hungarian(self):
        """
        Finds the optimal assignment of players to roles using the Hungarian algorithm
        to maximize the total team score. This method guarantees the best possible
        lineup based on the calculated player percentages.
        """
        roles = list(self.ROLES.keys())
        players = self.players
        num_players = len(players)
        num_roles = len(roles)

        # Create a "profit" matrix where profit = player's score for a role.
        # We create a square matrix (num_players x num_players).
        # The first num_roles columns are real roles.
        # The remaining columns are "dummy/bench" roles with a score of 0.
        profit_matrix = np.zeros((num_players, num_players))
        for r_idx, player in enumerate(players):
            for c_idx, role in enumerate(roles):
                profit_matrix[r_idx, c_idx] = player["percentages"][role]
        
        # The Hungarian algorithm finds the minimum cost, so we convert our
        # maximization problem to a minimization one by inverting the scores.
        # cost = max_score - score
        cost_matrix = 100 - profit_matrix
        
        # Run the assignment algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        # Interpret the results
        assignment = {role: None for role in roles}
        for player_idx, role_idx in zip(row_ind, col_ind):
            # Only consider assignments to real roles (not dummy/bench roles)
            if role_idx < num_roles:
                role = roles[role_idx]
                player = players[player_idx]
                score = player["percentages"][role]
                assignment[role] = (player, score)
                
        return assignment

    # --- RESULTS DISPLAY (Mostly identical, ensures compatibility) ---
    def show_evaluation_results(self, assignment):
        results_window = tk.Toplevel(self.root)
        results_window.title("🏆 Team Composition Analysis")
        results_window.geometry("800x700")
        results_window.configure(bg=self.COLORS['light'])
        results_window.transient(self.root)
        results_window.grab_set()

        canvas = tk.Canvas(results_window, bg=self.COLORS['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Main content frame for padding
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        ttk.Label(content_frame, text="🏆 Optimal Team Composition", font=('Segoe UI', 16, 'bold')).pack(pady=(0,20))
        
        comp_frame = ttk.LabelFrame(content_frame, text="Starting Lineup", padding=20)
        comp_frame.pack(fill='x', pady=(0, 20))
        
        total_score, assigned_players = 0, 0
        for role, player_info in assignment.items():
            role_frame = ttk.Frame(comp_frame)
            role_frame.pack(fill='x', pady=5)
            ttk.Label(role_frame, text=f"🎮 {role}:", font=('Segoe UI', 11, 'bold'), width=15).pack(side='left')
            if player_info:
                player, score = player_info
                total_score += score
                assigned_players += 1
                ttk.Label(role_frame, text=f"{player['name']} (Age: {player['age']}) - {score:.1f}% fit", font=('Segoe UI', 10)).pack(side='left', padx=(10, 0))
                ttk.Label(role_frame, text=self.get_fit_text(score), font=('Segoe UI', 9, 'bold'), foreground=self.get_fit_color(score)).pack(side='right')
            else:
                ttk.Label(role_frame, text="⚠️ Position Vacant", font=('Segoe UI', 10), foreground=self.COLORS['danger']).pack(side='left', padx=(10, 0))

        if assigned_players > 0:
            avg_score = total_score / assigned_players
            stats_frame = ttk.LabelFrame(content_frame, text="Team Statistics", padding=20)
            stats_frame.pack(fill='x', pady=(0, 20))
            ttk.Label(stats_frame, text=f"Overall Team Synergy: {avg_score:.1f}%", font=('Segoe UI', 12, 'bold'), foreground=self.get_fit_color(avg_score)).pack()
            ttk.Label(stats_frame, text=f"Team Rating: {self.get_team_rating(avg_score)}", font=('Segoe UI', 11, 'bold')).pack(pady=(5,0))

        recommendations = self.get_detailed_recommendations(assignment)
        if recommendations:
            rec_frame = ttk.LabelFrame(content_frame, text="💡 Recommendations", padding=20)
            rec_frame.pack(fill='x', pady=(0, 20))
            rec_text = tk.Text(rec_frame, height=8, width=80, wrap='word', font=('Segoe UI', 9), bg='white', relief='flat', borderwidth=0)
            rec_text.pack(fill='both', expand=True)
            rec_text.insert('1.0', recommendations)
            rec_text.config(state='disabled')

        bench_players = [p for p in self.players if not any(pi and pi[0] == p for pi in assignment.values())]
        if bench_players:
            bench_frame = ttk.LabelFrame(content_frame, text="🏃 Bench Players", padding=20)
            bench_frame.pack(fill='x')
            for player in bench_players:
                percentages = player.get("percentages", {})
                best_role = max(percentages.items(), key=lambda x: x[1]) if percentages else ("Unknown", 0)
                ttk.Label(bench_frame, text=f"• {player['name']} (Age: {player['age']}) - Best as {best_role[0]}: {best_role[1]:.1f}%", font=('Segoe UI', 10)).pack(anchor='w')

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_fit_color(self, score):
        if score >= 80: return '#2E7D32' # Green
        elif score >= 65: return '#F57F17' # Orange
        else: return '#C62828' # Red

    def get_fit_text(self, score):
        if score >= 85: return "🌟 Excellent"
        elif score >= 75: return "✅ Good"
        elif score >= 60: return "⚠️ Average"
        else: return "❌ Poor"

    def get_team_rating(self, avg_score):
        if avg_score >= 85: return "🏆 S-Tier (Championship Level)"
        elif avg_score >= 75: return "🥇 A-Tier (Playoff Contender)"
        elif avg_score >= 65: return "🥈 B-Tier (Competitive)"
        elif avg_score >= 55: return "🥉 C-Tier (Developing)"
        else: return "📚 D-Tier (Needs Development)"

    def get_detailed_recommendations(self, assignment):
        recommendations = []
        for role, player_info in assignment.items():
            if player_info:
                player, score = player_info
                weak_primary = [s for s in self.ROLES[role]["primary"] if player["skills"].get(s, 0) < 65]
                if weak_primary: recommendations.append(f"• {player['name']} ({role}) needs work on: {', '.join(weak_primary)}.")
                if score < 70: recommendations.append(f"• Consider finding a stronger {role}. {player['name']}'s fit is only {score:.1f}%.")
                if player['age'] > 28: recommendations.append(f"• Plan for succession for {player['name']} (Age {player['age']}).")
            else:
                recommendations.append(f"• The {role} position is vacant and needs to be filled immediately.")
        
        return "\n".join(recommendations[:8]) if recommendations else "Team has solid primary skill coverage. Focus on synergy."

if __name__ == "__main__":
    # --- APP ENTRY POINT ---
    root = tk.Tk()
    app = ModernTeamManagementApp(root)
    root.mainloop()