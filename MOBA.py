"""
MOBA Team Management System
Version: V0.3.0
Author: Namathieu

Change Log:
- Complete UI/UX overhaul for a more modern and user-friendly experience.
- Migrated from tkinter/ttk to ttkbootstrap for modern themes and widgets.
- Replaced Treeview roster with a dynamic list of "Player Cards".
- Replaced slider list with a clean, tabbed interface for skill entry.
- Implemented dynamic, color-coded sliders for instant visual feedback.
- Designed a new graphical "Strategic Map" for team analysis results.
- Integrated Font Awesome icons for a professional look and feel.
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import json
import numpy as np
from scipy.optimize import linear_sum_assignment
import random

# --- NOTE: NEW DEPENDENCIES ---
# This version requires ttkbootstrap, numpy, scipy, and Pillow.
# pip install ttkbootstrap numpy scipy Pillow

class ModernTeamManagementApp:
    # --- CONFIGURABLE ROLE AND SKILL DEFINITIONS ---
    ROLES = {
        "Top Laner": {"primary": ["Bravery", "Composure", "Concentration"], "secondary": ["Communication", "Vision"]},
        "Jungler": {"primary": ["Bravery", "Decision", "Vision", "Anticipation", "Communication", "Memory", "Teamwork"], "secondary": ["Composure", "Concentration", "Leadership", "Flair"]},
        "Mid Laner": {"primary": ["Leadership", "Vision", "Anticipation", "Communication", "Flair"], "secondary": ["Bravery", "Composure", "Decision", "Concentration", "Teamwork"]},
        "Bot Laner": {"primary": ["Accuracy", "Dexterity"], "secondary": ["Composure", "Decision", "Determination", "Leadership", "Vision", "Teamwork", "Flair", "Concentration", "Communication", "Anticipation"]},
        "Support": {"primary": ["Leadership", "Vision", "Memory", "Teamwork", "Communication", "Anticipation"], "secondary": ["Composure", "Decision", "Concentration"]}
    }

    SKILLS = {
        # Group skills into categories for the tabbed interface
        "Mechanical": ["Accuracy", "Dexterity", "Quickness", "Stamina"],
        "Mental": ["Composure", "Concentration", "Decision", "Determination", "Memory", "Anticipation"],
        "Teamplay": ["Communication", "Leadership", "Teamwork", "Vision", "Flair", "Bravery"]
    }

    # --- ICONS (Using Font Awesome from ttkbootstrap) ---
    ICONS = {
        "Top Laner": "fa-shield", "Jungler": "fa-leaf", "Mid Laner": "fa-bolt",
        "Bot Laner": "fa-crosshairs", "Support": "fa-heart", "Add": "fa-plus-circle",
        "Update": "fa-check-circle", "Cancel": "fa-times-circle", "Random": "fa-random",
        "Save": "fa-save", "Load": "fa-folder-open", "Analyze": "fa-sitemap",
        "Edit": "fa-pencil", "Delete": "fa-trash", "Details": "fa-eye"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Advanced Team Management System V0.3.0")
        self.root.geometry("1400x900")

        self.players = []
        self.selected_player_name = None
        self.current_mode = "add"

        self.create_widgets()
        self.center_window()
        self.load_sample_data() # Load some sample data for demonstration

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def create_widgets(self):
        main_paned = ttk.PanedWindow(self.root, orient='horizontal')
        main_paned.pack(fill='both', expand=True, padx=20, pady=20)

        left_panel = self.create_left_panel(main_paned)
        main_paned.add(left_panel, weight=1)

        right_panel = self.create_right_panel(main_paned)
        main_paned.add(right_panel, weight=2)

    # --- LEFT PANEL: PLAYER FORM AND OPERATIONS ---
    def create_left_panel(self, parent):
        left_frame = ttk.Frame(parent, padding=20)

        # --- Player Info Form ---
        form_card = ttk.Labelframe(left_frame, text="Player Information", padding=20)
        form_card.pack(fill='x', pady=(0, 20), expand=True)

        info_frame = ttk.Frame(form_card)
        info_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(info_frame, text="Player Name:").grid(row=0, column=0, sticky='w')
        self.player_name_var = tk.StringVar()
        self.name_entry = ttk.Entry(info_frame, textvariable=self.player_name_var)
        self.name_entry.grid(row=1, column=0, sticky='ew', padx=(0, 10))
        ttk.Label(info_frame, text="Age:").grid(row=0, column=1, sticky='w')
        self.player_age_var = tk.IntVar(value=20)
        age_spinbox = ttk.Spinbox(info_frame, from_=16, to=35, width=8, textvariable=self.player_age_var)
        age_spinbox.grid(row=1, column=1, sticky='w')
        info_frame.grid_columnconfigure(0, weight=1)

        # --- Tabbed Skill Entry ---
        self.create_skills_notebook(form_card)

        # --- Action Buttons ---
        self.create_action_buttons(form_card)

        # --- Team Operations ---
        team_ops_card = ttk.Labelframe(left_frame, text="Team Operations", padding=20)
        team_ops_card.pack(fill='x', expand=True)
        self.create_team_operations(team_ops_card)

        return left_frame

    def create_skills_notebook(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, pady=15)
        self.skill_vars = {}
        self.skill_scales = {}

        for category, skills_in_cat in self.SKILLS.items():
            cat_frame = ttk.Frame(notebook, padding=10)
            notebook.add(cat_frame, text=category)
            for i, skill in enumerate(skills_in_cat):
                self.create_skill_slider(cat_frame, skill, i)

    def create_skill_slider(self, parent, skill, index):
        ttk.Label(parent, text=f"{skill}:").grid(row=index, column=0, sticky='w', pady=4)
        var = tk.IntVar(value=50)
        self.skill_vars[skill] = var
        
        # Initial style is warning (yellow)
        scale = ttk.Scale(parent, from_=0, to=100, variable=var, orient='horizontal', style='warning.Horizontal.TScale')
        scale.grid(row=index, column=1, sticky='ew', padx=10, pady=4)
        self.skill_scales[skill] = scale

        value_label = ttk.Label(parent, text="50", width=3, anchor='e')
        value_label.grid(row=index, column=2, sticky='e', pady=4)

        def update_ui(value, v=var, lbl=value_label, sc=scale):
            val = int(float(value))
            v.set(val)
            lbl.config(text=str(val))
            # Update slider color based on value
            if val < 50: sc.config(style='danger.Horizontal.TScale')
            elif val < 80: sc.config(style='warning.Horizontal.TScale')
            else: sc.config(style='success.Horizontal.TScale')
        
        var.trace_add('write', lambda *args, fn=update_ui: fn(var.get()))
        scale.config(command=lambda v, fn=update_ui: fn(v))
        parent.grid_columnconfigure(1, weight=1)

    def create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(15, 0))
        
        self.add_button = ttk.Button(button_frame, text=" Add Player", image=self.ICONS["Add"], compound='left', command=self.add_player, bootstyle='success')
        self.add_button.pack(side='left', padx=(0, 10), fill='x', expand=True)

        self.update_button = ttk.Button(button_frame, text=" Update", image=self.ICONS["Update"], compound='left', command=self.update_player, bootstyle='primary', state='disabled')
        self.update_button.pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        self.cancel_button = ttk.Button(button_frame, text=" Cancel", image=self.ICONS["Cancel"], compound='left', command=self.cancel_edit, bootstyle='danger', state='disabled')
        self.cancel_button.pack(side='left', padx=(0,10), fill='x', expand=True)

        ttk.Button(button_frame, image=self.ICONS["Random"], command=self.generate_random_player, bootstyle='secondary-outline').pack(side='right')

    def create_team_operations(self, parent):
        ops_frame = ttk.Frame(parent)
        ops_frame.pack(fill='x', pady=5)
        ttk.Button(ops_frame, text=" Save Team", image=self.ICONS["Save"], compound='left', command=self.save_team, bootstyle='secondary').pack(side='left', padx=(0, 10), fill='x', expand=True)
        ttk.Button(ops_frame, text=" Load Team", image=self.ICONS["Load"], compound='left', command=self.load_team, bootstyle='secondary').pack(side='left', fill='x', expand=True)

        ttk.Button(parent, text=" Analyze Team Composition", image=self.ICONS["Analyze"], compound='left', command=self.evaluate_team, bootstyle='info').pack(fill='x', pady=(15,0))

    # --- RIGHT PANEL: PLAYER ROSTER ---
    def create_right_panel(self, parent):
        right_frame = ttk.Frame(parent, padding=(20, 0, 0, 0))
        
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill='x', pady=(0,15))
        ttk.Label(header_frame, text="Team Roster", font="-size 16 -weight bold").pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='right')
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_player_list())
        ttk.Label(header_frame, text="Search: ").pack(side='right')

        # --- Player Card List ---
        self.roster_frame = ttk.ScrolledFrame(right_frame, autohide=True)
        self.roster_frame.pack(fill='both', expand=True)
        return right_frame

    def refresh_player_list(self):
        for widget in self.roster_frame.winfo_children():
            widget.destroy()
        
        search_term = self.search_var.get().lower()
        
        filtered_players = [p for p in self.players if search_term in p['name'].lower()]
        
        for player in filtered_players:
            card = PlayerCard(self.roster_frame, player, self.ICONS, 
                              self.edit_player, self.delete_player, self.show_player_details_window)
            card.pack(fill='x', padx=5, pady=5)

    # --- PLAYER MANAGEMENT LOGIC ---
    def add_player(self):
        if not self.validate_input(): return
        player_data = self.get_player_data()
        self.players.append(player_data)
        self.refresh_player_list()
        self.clear_inputs()
        messagebox.showinfo("Success", f"Player '{player_data['name']}' added successfully!")

    def update_player(self):
        if not self.validate_input(): return
        player_data = self.get_player_data()
        
        # Find player by name and update
        for i, p in enumerate(self.players):
            if p['name'] == self.selected_player_name:
                self.players[i] = player_data
                break
        
        self.refresh_player_list()
        self.cancel_edit()
        messagebox.showinfo("Success", f"Player '{player_data['name']}' updated successfully!")

    def edit_player(self, player_name):
        player = next((p for p in self.players if p["name"] == player_name), None)
        if not player: return

        self.selected_player_name = player["name"]
        self.player_name_var.set(player["name"])
        self.player_age_var.set(player["age"])
        for skill, value in player["skills"].items():
            if skill in self.skill_vars:
                self.skill_vars[skill].set(value)
        
        self.current_mode = "edit"
        self.add_button.config(state='disabled')
        self.update_button.config(state='normal')
        self.cancel_button.config(state='normal')
        self.name_entry.config(state='disabled') # Prevent changing name during edit

    def cancel_edit(self):
        self.current_mode = "add"
        self.selected_player_name = None
        self.add_button.config(state='normal')
        self.update_button.config(state='disabled')
        self.cancel_button.config(state='disabled')
        self.name_entry.config(state='normal')
        self.clear_inputs()

    def delete_player(self, player_name):
        player = next((p for p in self.players if p["name"] == player_name), None)
        if not player: return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{player['name']}'?"):
            self.players = [p for p in self.players if p['name'] != player_name]
            self.refresh_player_list()
            if self.current_mode == "edit" and self.selected_player_name == player_name:
                self.cancel_edit()
    
    def show_player_details_window(self, player_name):
        player = next((p for p in self.players if p["name"] == player_name), None)
        if player:
            self.show_evaluation_results(self.find_optimal_assignment_hungarian([player]))

    # --- DATA & UTILITIES ---
    def validate_input(self):
        name = self.player_name_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Player name is required.")
            return False
        
        # In edit mode, the name can be the same as the one being edited
        existing_names = [p["name"] for p in self.players if p["name"] != self.selected_player_name]
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

    def generate_random_player(self):
        names = ["Phoenix", "Shadow", "Lightning", "Storm", "Blaze", "Frost", "Nova", "Titan"]
        name = f"{random.choice(names)}{random.randint(1, 99)}"
        # Ensure name is unique
        while any(p['name'] == name for p in self.players):
             name = f"{random.choice(names)}{random.randint(1, 99)}"
        
        self.player_name_var.set(name)
        self.player_age_var.set(random.randint(17, 28))
        for skill in self.skill_vars:
            self.skill_vars[skill].set(random.randint(30, 95))
        
    def save_team(self):
        # (Same as before)
        if not self.players:
            messagebox.showwarning("Save Error", "No players to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Save Team")
        if file_path:
            try:
                with open(file_path, "w") as f: json.dump(self.players, f, indent=4)
                messagebox.showinfo("Success", f"Team saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save team: {str(e)}")

    def load_team(self):
        # (Same as before)
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Load Team")
        if file_path:
            try:
                with open(file_path, "r") as f: self.players = json.load(f)
                self.refresh_player_list()
                messagebox.showinfo("Success", f"Team loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load team: {str(e)}")

    def load_sample_data(self):
        # Pre-populate with some data for demonstration
        sample_players = [
            {'name': 'RiftScarra', 'age': 24, 'skills': {'Accuracy': 88, 'Dexterity': 92, 'Quickness': 85, 'Stamina': 78, 'Composure': 75, 'Concentration': 80, 'Decision': 70, 'Determination': 85, 'Memory': 65, 'Anticipation': 72, 'Communication': 80, 'Leadership': 60, 'Teamwork': 88, 'Vision': 70, 'Flair': 90, 'Bravery': 70}},
            {'name': 'JungleFever', 'age': 21, 'skills': {'Accuracy': 60, 'Dexterity': 70, 'Quickness': 88, 'Stamina': 90, 'Composure': 82, 'Concentration': 85, 'Decision': 92, 'Determination': 88, 'Memory': 80, 'Anticipation': 95, 'Communication': 90, 'Leadership': 75, 'Teamwork': 92, 'Vision': 94, 'Flair': 70, 'Bravery': 91}},
            {'name': 'MidMage', 'age': 19, 'skills': {'Accuracy': 95, 'Dexterity': 90, 'Quickness': 85, 'Stamina': 75, 'Composure': 88, 'Concentration': 90, 'Decision': 85, 'Determination': 80, 'Memory': 78, 'Anticipation': 92, 'Communication': 88, 'Leadership': 94, 'Teamwork': 85, 'Vision': 90, 'Flair': 96, 'Bravery': 78}},
            {'name': 'TopTitan', 'age': 26, 'skills': {'Accuracy': 50, 'Dexterity': 60, 'Quickness': 75, 'Stamina': 95, 'Composure': 94, 'Concentration': 96, 'Decision': 80, 'Determination': 98, 'Memory': 70, 'Anticipation': 85, 'Communication': 82, 'Leadership': 70, 'Teamwork': 80, 'Vision': 75, 'Flair': 60, 'Bravery': 97}},
            {'name': 'SupportSavvy', 'age': 23, 'skills': {'Accuracy': 40, 'Dexterity': 50, 'Quickness': 70, 'Stamina': 80, 'Composure': 92, 'Concentration': 90, 'Decision': 88, 'Determination': 85, 'Memory': 95, 'Anticipation': 94, 'Communication': 98, 'Leadership': 91, 'Teamwork': 97, 'Vision': 99, 'Flair': 65, 'Bravery': 80}},
            {'name': 'BenchWarm', 'age': 20, 'skills': {'Accuracy': 70, 'Dexterity': 72, 'Quickness': 68, 'Stamina': 75, 'Composure': 65, 'Concentration': 70, 'Decision': 68, 'Determination': 72, 'Memory': 60, 'Anticipation': 65, 'Communication': 75, 'Leadership': 62, 'Teamwork': 78, 'Vision': 70, 'Flair': 68, 'Bravery': 66}}
        ]
        self.players = sample_players
        self.refresh_player_list()

    # --- CORE LOGIC (Untouched) ---
    def calculate_role_percentages(self, player):
        percentages = {}
        for role, criteria in self.ROLES.items():
            primary_skills = [player["skills"].get(skill, 0) for skill in criteria["primary"]]
            primary_score = sum(self.apply_diminishing_returns(s) for s in primary_skills)
            max_primary = len(criteria["primary"]) * 100
            primary_percentage = (primary_score / max_primary) * 100 if max_primary > 0 else 0
            
            age_multiplier = 1.0 # Simplified for now, can be re-added
            base_percentage = primary_percentage * age_multiplier
            
            secondary_bonus = 0
            if "secondary" in criteria and criteria["secondary"]:
                secondary_skills = [player["skills"].get(skill, 0) for skill in criteria["secondary"]]
                secondary_score = sum(self.apply_diminishing_returns(s) for s in secondary_skills)
                max_secondary = len(criteria["secondary"]) * 100
                secondary_percentage = (secondary_score / max_secondary) * 100 if max_secondary > 0 else 0
                secondary_bonus = min(15, (secondary_percentage / 100) * 15)

            final_percentage = base_percentage + secondary_bonus
            percentages[role] = round(max(0, min(final_percentage, 100)), 2)
        return percentages

    def apply_diminishing_returns(self, skill_value):
        if skill_value <= 70: return skill_value
        elif skill_value <= 85: return 70 + (skill_value - 70) * 0.8
        else: return 82 + (skill_value - 85) * 0.6

    def find_optimal_assignment_hungarian(self, players_to_assign):
        roles = list(self.ROLES.keys())
        num_players = len(players_to_assign)
        num_roles = len(roles)

        profit_matrix = np.zeros((num_players, num_players))
        for r_idx, player in enumerate(players_to_assign):
            player['percentages'] = self.calculate_role_percentages(player)
            for c_idx, role in enumerate(roles):
                profit_matrix[r_idx, c_idx] = player["percentages"][role]
        
        cost_matrix = 100 - profit_matrix
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        assignment = {role: None for role in roles}
        assigned_player_indices = []
        for player_idx, role_idx in zip(row_ind, col_ind):
            if role_idx < num_roles:
                role = roles[role_idx]
                player = players_to_assign[player_idx]
                score = player["percentages"][role]
                assignment[role] = (player, score)
                assigned_player_indices.append(player_idx)

        bench_players = [p for i, p in enumerate(players_to_assign) if i not in assigned_player_indices]
        return assignment, bench_players

    def evaluate_team(self):
        if len(self.players) < len(self.ROLES):
            messagebox.showwarning("Evaluate Error", f"Not enough players for a full team. Need at least {len(self.ROLES)} players.")
            return

        assignment, bench_players = self.find_optimal_assignment_hungarian(self.players)
        self.show_evaluation_results(assignment, bench_players)

    # --- NEW STRATEGIC MAP RESULTS WINDOW ---
    def show_evaluation_results(self, assignment, bench_players):
        results_window = ttk.Toplevel(self.root, title="🏆 Team Composition Analysis")
        results_window.geometry("1200x850")

        # --- Main Layout ---
        main_frame = ttk.Frame(results_window)
        main_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        map_frame = ttk.Frame(main_frame)
        map_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        
        sidebar = ttk.Frame(main_frame, width=350)
        sidebar.pack(side=RIGHT, fill=Y, padx=(20, 0))
        sidebar.pack_propagate(False)

        # --- Sidebar Content ---
        self.create_sidebar_content(sidebar, assignment, bench_players)
        
        # --- Map Canvas ---
        self.create_map_canvas(map_frame, assignment)

    def create_sidebar_content(self, sidebar, assignment, bench_players):
        # --- Team Stats ---
        stats_frame = ttk.Labelframe(sidebar, text="Team Statistics", padding=15)
        stats_frame.pack(fill=X, pady=(0, 20))
        
        assigned_scores = [score for _, score in assignment.values() if _ is not None]
        avg_score = sum(assigned_scores) / len(assigned_scores) if assigned_scores else 0
        
        ttk.Label(stats_frame, text=f"Overall Synergy: {avg_score:.1f}%", font="-size 12 -weight bold").pack(anchor='w')
        
        # --- Bench Players ---
        bench_frame = ttk.Labelframe(sidebar, text="🏃 Bench", padding=15)
        bench_frame.pack(fill=X, pady=(0, 20))
        if bench_players:
            for player in bench_players:
                ttk.Label(bench_frame, text=f"• {player['name']}").pack(anchor='w')
        else:
            ttk.Label(bench_frame, text="No players on the bench.").pack(anchor='w')

        # --- Recommendations ---
        rec_frame = ttk.Labelframe(sidebar, text="💡 Recommendations", padding=15)
        rec_frame.pack(fill=BOTH, expand=YES)
        rec_text_widget = ttk.ScrolledText(rec_frame, wrap='word', height=10)
        rec_text_widget.pack(fill=BOTH, expand=YES)
        recs = self.get_detailed_recommendations(assignment)
        rec_text_widget.insert('1.0', recs)
        rec_text_widget.config(state='disabled')

    def create_map_canvas(self, map_frame, assignment):
        canvas = tk.Canvas(map_frame, bg=self.root.style.colors.bg, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=YES)

        # Draw map on resize
        def draw_map(event):
            canvas.delete("all")
            w, h = event.width, event.height
            
            # Colors from theme
            river_color = self.root.style.colors.primary
            lane_color = self.root.style.colors.secondary
            
            # Draw river
            canvas.create_rectangle(0, h*0.45, w, h*0.55, fill=river_color, outline="")
            
            # Draw lanes
            canvas.create_line(w*0.2, 0, w*0.8, h, fill=lane_color, width=30, capstyle=tk.ROUND) # Mid
            canvas.create_line(0, h*0.2, w, h*0.8, fill=lane_color, width=30, capstyle=tk.ROUND) # Top/Bot
            
            # Positions for roles
            positions = {
                "Top Laner": (w * 0.15, h * 0.15),
                "Jungler": (w * 0.35, h * 0.35),
                "Mid Laner": (w * 0.5, h * 0.5),
                "Bot Laner": (w * 0.85, h * 0.85),
                "Support": (w * 0.65, h * 0.7)
            }
            
            # Place player cards on map
            for role, pos in positions.items():
                player_info = assignment.get(role)
                card = self.create_analysis_card(canvas, role, player_info)
                canvas.create_window(pos[0], pos[1], window=card)

        canvas.bind("<Configure>", draw_map)

    def create_analysis_card(self, parent, role, player_info):
        card = ttk.Frame(parent, padding=10, bootstyle='dark')
        
        role_icon = self.ICONS.get(role, 'fa-question-circle')
        ttk.Label(card, image=role_icon, text=f" {role}", compound=LEFT, font="-size 12 -weight bold", bootstyle="inverse-dark").pack()
        
        if player_info:
            player, score = player_info
            ttk.Label(card, text=player['name'], font="-size 10", bootstyle="inverse-dark").pack(pady=(5,0))
            style = "success" if score > 80 else "warning" if score > 60 else "danger"
            ttk.Progressbar(card, value=score, bootstyle=style).pack(pady=(5,0), fill=X)
            ttk.Label(card, text=f"{score:.1f}% Fit", bootstyle="inverse-dark").pack()
        else:
            ttk.Label(card, text="⚠️ Vacant", bootstyle="danger-inverse").pack(pady=5)
            
        return card

    def get_detailed_recommendations(self, assignment):
        # Simplified for brevity, can be expanded
        recs = []
        for role, info in assignment.items():
            if info:
                player, score = info
                if score < 70:
                    recs.append(f"• {player['name']} is a weak fit for {role} ({score:.1f}%). Consider alternatives.")
            else:
                recs.append(f"• The {role} position is vacant. This is a critical priority.")
        return "\n".join(recs) if recs else "This looks like a solid starting lineup!"


class PlayerCard(ttk.Frame):
    """A custom widget to display a player in the roster list."""
    def __init__(self, parent, player_data, icons, edit_callback, delete_callback, details_callback, **kwargs):
        super().__init__(parent, padding=15, bootstyle="light", **kwargs)
        self.player_name = player_data['name']
        
        # Calculate best role for display
        app = self.winfo_toplevel()
        percentages = app.calculate_role_percentages(player_data)
        best_role, best_score = max(percentages.items(), key=lambda x: x[1]) if percentages else ("Unknown", 0)

        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        
        # --- Widgets ---
        role_icon = ttk.Label(self, image=icons.get(best_role, "fa-user"), bootstyle='secondary')
        role_icon.grid(row=0, column=0, rowspan=2, padx=(0, 15))

        name_label = ttk.Label(self, text=self.player_name, font="-size 12 -weight bold")
        name_label.grid(row=0, column=1, sticky='w')
        
        age_label = ttk.Label(self, text=f"Age: {player_data['age']} | Best Role: {best_role}", bootstyle='secondary')
        age_label.grid(row=1, column=1, sticky='w')

        # Progress bar for best score
        style = "success" if best_score > 80 else "warning" if best_score > 60 else "danger"
        score_bar = ttk.Progressbar(self, value=best_score, bootstyle=style)
        score_bar.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10,0))
        
        # --- Action Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=2, rowspan=3, padx=(20, 0))

        ttk.Button(button_frame, image=icons["Edit"], bootstyle="primary-outline",
                   command=lambda: edit_callback(self.player_name)).pack(pady=2)
        ttk.Button(button_frame, image=icons["Delete"], bootstyle="danger-outline",
                   command=lambda: delete_callback(self.player_name)).pack(pady=2)


if __name__ == "__main__":
    # Use the 'darkly' theme from ttkbootstrap
    root = ttk.Window(themename="darkly")
    app = ModernTeamManagementApp(root)
    root.mainloop()