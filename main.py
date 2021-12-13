import tkinter as tk
from tkinter import ttk
import requests
from models import Assignment, ClassModel
from tkinter import *
from tkinter import messagebox, Spinbox
from copy import deepcopy
from tkmacosx import Button, CircleButton
from dynamicGrid import DynamicGrid
from datetime import date
from tkinter import ttk
import webbrowser
from pprint import pprint
from Utilities import utilities
import json
from datetime import datetime
from fpdf import FPDF

class UVA_Grader:
    def __init__(self):

        self.util = utilities()
        self.width, self.height = 800, 1600
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.label_font = tk.font.Font(family="Fira Code", size=20,
                                       weight='bold')
        self.root.option_add("*Font", self.label_font)
        # Logo related data
        self.logo_canvas = None
        self.logo = None
        self.logo_label = None

        # create data for main canvas
        self.main_canvas = None
        self.class_list = None
        self.class_dropdown = None
        self.dropdown: tk.OptionMenu = None

        # store class : assignments
        self.assignment_dict = dict()

        self.create_logo()
        self.config_main_canvas()
        self.root.geometry("800x1600")

        # Dynamic grid used for card type instances
        self.dynamicGrid: DynamicGrid = None
        self.main_scrollbar: Scrollbar = None
        self.main_frame: tk.Frame = None
        self.root.mainloop()

        # tkinter data used for student listbox
        self.student_data: list = None
        self.listbox_selection = None
        self.navigation_frame : Frame = None
        self.notebook_frame: Frame = None
        self.stats_notebook: ttk.Notebook = None
        self.student_frame: ttk.Notebook = None
        self.assn_canvas = tk.Canvas = None
        self.assn_frame: ttk.Frame = None
        self.selected_student: dict = None
        self.scroll_frame: tk.Frame = None
        self.assn_editor: tk.Text = None
        self.long_str: str = None
    def config_main_canvas(self):
        self.main_canvas = tk.Canvas(self.root, width=self.width,
                                     height=self.height, bg="#272727")
        self.main_canvas.pack(fill=tk.X)

    def create_logo(self):
        self.toolbar = Frame(self.main_canvas, bd=1, relief=FLAT,
                             bg="gray", height=65, )
        self.toolbar.pack(side=TOP, fill=X)
        # self.logo_canvas = tk.Canvas(self.toolbar, width=self.width,
        #                              height=65, relief=FLAT)
        # self.logo_canvas.pack(fill=tk.X)

        self.logo = tk.PhotoImage(
            file='/Users/drewsmith/PycharmProjects/uva_grader/menu.png'
                 '').subsample(12, 12)
        self.class_logo = tk.PhotoImage(
            file='/Users/drewsmith/PycharmProjects/uva_grader/pdf.png'
                 '').subsample(9, 9)
        self.home_button = CircleButton(self.toolbar, radius=30,
                                        overrelief="flat",
                                        overforeground='#00C78C',
                                        focuscolor="#272727",
                                        justify=tk.LEFT,
                                        relief="flat",
                                        bg="#272727", borderless=1,
                                        image=self.logo)

        self.class_button = CircleButton(self.toolbar, radius=30,
                                         justify=tk.LEFT,
                                         relief="flat",
                                         bg="#272727", borderless=1,
                                         image=self.class_logo,
                                         padx=100)
        # self.home_btn_frame.pack()
        self.home_button.pack(side=LEFT)
        self.class_button.pack(side=RIGHT, padx=10)

        # build popup menu
        self.popup = tk.Menu(self.root, tearoff=0, bg="white", title="Main "
                                                                     "Menu")
        self.popup.add_command(label="Import Class ID",
                               command=self.import_class)
        self.popup.add_separator()
        self.popup.add_command(label="Add Assignment(s)",
                               command=self.build_assignments)
        self.popup.add_separator()
        self.popup.add_command(label="Update submissions",
                               command=self.update_students)
        self.popup.add_separator()
        self.popup.add_command(label="Get Class Stats",
                               command=self.begin_class_data_collection)

        self.popup.add_separator()
        self.popup.add_command(label="Generate Reports")
        self.home_button.bind("<Button>", self.menu_popup)
        # self.logo = Image.open(
        #     '/Users/drewsmith/PycharmProjects/uva_grader/ONLINEJUDGE.png')
        # # self.logo = ImageTk.PhotoImage(self.logo)
        # self.logo = ImageTk.PhotoImage(
        #     Image.open('/Users/drewsmith/PycharmProjects/uva_grader'
        #                '/ONLINEJUDGE.png').resize((75, 60),
        #                                           Image.ANTIALIAS))
        # self.logo_label = tk.Label(image=self.logo)
        # self.logo_label.image = self.logo
        # self.logo_label.pack()
        self.root.title('UVA Grader')

    def menu_popup(self, event):
        self.popup.tk_popup(x=0, y=120)

    def update_students(self):
        print('Class update beginning')

        self.clear_main_canvas()
        options = self.util.get_class_list()
        pprint(f'Options returned from api {options}')
        options = [x for x in options if not x.startswith('raw')]
        pprint(f'Options returned from api {options}')
        self.selected_class = tk.StringVar()

        options_cb = ttk.Combobox(self.main_canvas,
                                  state="readonly",
                                  textvariable=self.selected_class,
                                  font=self.label_font, justify="center")

        options_cb['values'] = options[0:]
        options_cb.current(0)
        options_cb['state'] = 'readonly'
        # options_cb.pack(fill=tk.X, padx=5, pady=5)

        options_cb.place(relx=0.5, rely=.025, anchor=CENTER)
        options_cb.bind("<<ComboboxSelected>>", self.begin_class_update)
    def begin_class_update(self, event):
        response = self.util.update_class_submissions(event.widget.get())
        if response['status'] == 'Success':
            self.clear_main_canvas()
    def get_student_data(self, class_name):
        student= self.util.get_class_data(class_name)
        print(student)
    def begin_class_data_collection(self):
        print('Class data began')

        self.clear_main_canvas()
        options = self.util.get_class_list()
        options = [x for x in options if not x.startswith('raw')]

        self.selected_class = tk.StringVar()

        options_cb = ttk.Combobox(self.toolbar,
                                  state="readonly",
                                  textvariable=self.selected_class,
                                  font=self.label_font,
                                  justify="center")

        options_cb['values'] = options[0:]
        options_cb.current(0)
        options_cb['state'] = 'readonly'
        # options_cb.pack(fill=tk.X, padx=5, pady=5)

        options_cb.place(relx=.5, rely=.5, anchor=CENTER)
        options_cb.bind("<<ComboboxSelected>>", self.student_call_back)


    def student_call_back(self, event):
        self.navigation_frame = tk.LabelFrame(self.main_canvas,
                                              text="STUDENTS", labelanchor="n",
                                              relief=tk.FLAT)
        self.navigation_frame.place(relwidth=.2, relheight=1)
        self.notebook_frame = tk.Frame(self.main_canvas)
        width_ofNav = self.navigation_frame.winfo_width()
        print(width_ofNav)
        self.notebook_frame.place(x=360,
                                  relwidth=.8,
                                  relheight=1)
        listfont =tk.font.Font(family="Fira Code", size=20,
                                       weight='bold')
        self.student_data  = self.util.get_class_data(event.widget.get())
        label = LabelFrame(self.navigation_frame, text="STUDENTS")
        label.place(x=0, y=0)
        listbox = Listbox(self.navigation_frame,

                          bg="#828489",
                          activestyle='dotbox',
                          font=listfont,
                          fg="#192938")
        for index in range(len(self.student_data)):
            name = f'{self.student_data[index]["first"]}' \
                   f' {self.student_data[index]["last"]}'
            listbox.insert(index, f'{name}')
        listbox.bind("<<ListboxSelect>>", self.listbox_item_event)

        self.stats_notebook = ttk.Notebook(self.notebook_frame)
        self.stats_notebook.place(relwidth=1, relheight=1)
        style = ttk.Style()
        style.configure('TNotebook', tabposition='nw', background="white")
        style.configure('TNotebook.Tab', background="#828489")

        self.assn_frame = ttk.Frame(self.stats_notebook, height=280, width=400)
        self.student_frame = ttk.Frame(self.stats_notebook, height=280,
                                       width=400)
        style.configure('TFrame', background='green')
        self.assn_frame.pack(fill='both', expand=True)
        self.student_frame.pack(fill='both', expand=True)
        self.stats_notebook.add(self.assn_frame, text="Assignments")
        self.stats_notebook.add(self.student_frame, text="Student Info")
        listbox.place(relx=0.05, rely=.0, relheight=1, relwidth=.90)

    def listbox_item_event(self, event):
        widget = event.widget
        selection = widget.curselection()

        self.listbox_selection = widget.get(selection[0])
        print(f'listbox={self.listbox_selection}')
        self.listbox_selection = self.listbox_selection.split(' ')
        first = self.listbox_selection[0]
        last = self.listbox_selection[1]


        self.listbox_selection = ' '.join(self.listbox_selection)
        selected_item = None
        for item in self.student_data:
            name = f"{item['first']} {item['last']}"
            print(f"Comparison of {name} === {self.listbox_selection}")
            if name == self.listbox_selection:
                print('Student has been found')
                self.selected_student = item
                self.build_student_frame()
                break
    def build_student_frame(self):
        for widget in self.student_frame.winfo_children():
            widget.destroy()
        full_name = f"{self.selected_student['first']} " \
                    f"{self.selected_student['last']}"
        name_label0 = ttk.Label(self.student_frame, text="Student:")
        name_label0.place(x=0, y=5)
        name_label1 = ttk.Label(self.student_frame,
                                text=f'{self.selected_student["first"]} '
                                     f'{self.selected_student["last"]}')
        name_label1.place(x=400, y=5)
        for k, v in self.selected_student.items():
            if k == "slack_username":
                slack_user_lbl = ttk.Label(self.student_frame,
                                           text="Slack Username:")
                slack_name_lbl = ttk.Label(self.student_frame,
                                           text=v)
                slack_user_lbl.place(x=0, y=50)
                slack_name_lbl.place(x=400, y =50)
            elif k == 'judgeID':
                judge_id_lbl = ttk.Label(self.student_frame,
                                         text="UVA Online User ID:")
                judge_user_id_lbl = ttk.Label(self.student_frame,
                                           text=v)
                judge_id_lbl.place(x=0, y=100)
                judge_user_id_lbl.place(x=400, y=100)
            elif k == 'userName':
                judge_username_lbl = ttk.Label(self.student_frame,
                                                text="UVA Username:")
                judge_name_lbl = ttk.Label(self.student_frame,
                                           text=v)
                judge_username_lbl.place(x=0, y=150)
                judge_name_lbl.place(x=400, y=150)
            elif k=='github_username':
                github_username_lbl = ttk.Label(self.student_frame,
                                                text="Github Username:")
                github_name_lbl = ttk.Label(self.student_frame,
                                            text = v)
                github_username_lbl.place(x=0, y=200)
                github_name_lbl.place(x=400, y=200)
            elif k == 'github':
                github_link_lbl = ttk.Label(self.student_frame,
                                            text="Github Link")
                github_git_link_lbl = ttk.Label(self.student_frame,
                                               text=v)
                github_git_link_lbl.configure(foreground="#03245c")
                github_link_lbl.place(x=0, y=250)
                github_git_link_lbl.place(x=400, y=250)
                github_git_link_lbl.bind("<Button-1>", self.prep)
            elif k == 'solved_problems':
                solved_lbl = ttk.Label(self.student_frame, text="Solved "
                                                              "Problems:")
                solved_lbl.place(x=0, y=300)
                yvalue = 300
                completed_list = []

                for key, value in v.items():
                    print(key)
                    print(value)
                    assn = key
                    required = 0
                    achieved = 0
                    split_grades = ''
                    for key0, value0 in value.items():
                        if key0 == 'percent_achieved':
                            percent = value0

                        elif key0 == 'required':
                            required = value0
                        elif key0 == 'weight':
                            weight = value0
                            if percent:
                                percent_weight = zip(percent, weight)
                                grades = []
                                index = 0
                                for item in percent_weight:
                                    grades.append( item[0] * item[1])

                                    grades.sort(reverse=True)

                        elif key0 == 'complete' and value0 == True:
                            str_grades = [str(x) for x in grades]
                            split_grades = '\n\t '.join(str_grades)
                            grade_string = f"{assn} :    {split_grades}"

                            ttk.Label(self.student_frame,
                                      text=grade_string).place(x=400,
                                                                       y=yvalue)
                            yvalue += 50
                        elif key0 == 'required':
                            required = value0
                        elif key0 == 'achieved':
                            achieved = value0
                            assn_string = f'{assn} :    {achieved}/{required}'



                self.build_assignment_frame(v, full_name)

    def build_assignment_frame(self, assignments, full_name):
        for widgets in self.assn_frame.winfo_children():
            widgets.destroy()
        self.assn_canvas = tk.Canvas(self.assn_frame, bg="green")
        self.assn_canvas.pack(fill='both', expand=True)
        scroll = Scrollbar(self.assn_canvas, command=self.assn_canvas.yview)
        self.assn_canvas.config(yscrollcommand=scroll.set, scrollregion=(0, 0,
                                                                     100, 1000))
        scroll.pack(side=RIGHT, fill=Y)
        # self.scroll_frame = Frame(self.assn_canvas)
        # self.scroll_frame.pack(fill=BOTH, expand=True)
        self.assn_editor = tk.Text(self.assn_canvas, yscrollcommand=scroll.set)
        self.assn_editor.pack(fill=BOTH, expand=True)
        # a_str = '\n'.join('{} {}'.format(k,d) for k,d in assignments)
        # b_str = '\n'.join(f'{key}: {value} ')
        # assn_editor.insert('1.0', a_str)
        self.long_str = f"{full_name}\n\n"
        required = 0
        completed = 0
        self.graded_sum = 0.0
        self.assn_count = 0
        for k,v in assignments.items():
            k_str = str(k)
            self.assn_count +=1
            self.long_str = f'{self.long_str}{k_str}:\n'

            for key, value in v.items():
                if key == 'assn_num':
                    key_str = 'Assignment'
                    value_str = str(value)
                    self.long_str =  f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'uva_numbers':
                    key_str = 'Assigned Numbers'
                    value = [str(x) for x in value]
                    value_str = ', '.join(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'percent_achieved':
                    key_str = 'Percent Achieved'
                    value = [str(x) for x in value]
                    percent_value = value
                    value_str = ', '.join(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'title':
                    key_str = "Titles"
                    value_str = '\n\t\t'.join(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'weight':
                    key_str = "Weighted Values"
                    value = [str(x) for x in value]
                    weight_value = value
                    value_str = '\n\t\t\t'.join(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'required':
                    key_str = "Required Solves"
                    required = value
                    value_str = str(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'achieved':
                    key_str = "Achieved Number of Problems"
                    completed = value
                    value_str = str(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == "date_time_due":
                    key_str = 'Due Date and Time'
                    value_str = str(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == "unix_due_time":
                    due_time = str(value)
                    key_str = "Unix Due Time"
                    value_str = str(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'unix_sub_time':
                    submit_time = str(value)
                    key_str = "Unix Submission Time"
                    value_str = str(value)
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                elif key == 'penalties':
                    key_str = "Penalties"
                    value = [str(x) for x in value]
                    value_str = str('\n\t\t   '.join(value))
                    self.long_str = f'{self.long_str}\t{key_str}:\t{value_str}\n'
                    if weight_value and percent_value:
                        prct_weight =zip(weight_value, percent_value)
                        grades = []
                        for item in prct_weight:
                            grades.append(float(item[0]) * float(item[1]))

                        grade_str = [str(x) for x in grades]
                        grade_str = str('\n\t\t'.join(grade_str))
                        self.long_str = f'{self.long_str}\tGrades:\t{grade_str}\n'
                        grades.sort()
                        self.long_str = f'{self.long_str}\tSubmitted {completed} out of '\
                                   f'{required} required assignments.\n'
                        sum = 0.0
                        for i in range(completed):
                            sum += grades[i]
                        self.graded_sum += sum
                        self.long_str = f'{self.long_str}\tTotal Grade:\t{str(sum)}\n'
                        self.long_str = f'{self.long_str}\tDays since submit: {(int(submit_time)-int(due_time))*3600*24}\n'





        self.assn_editor.delete('1.0', END)
        self.assn_editor.insert('1.0', self.long_str)
        self.long_str = ''
        print(f'Grade Average {self.graded_sum/self.assn_count}')
        self.grade_sum = 0
        self.assn_count = 0

    def prep(self,event):
        print('i am prepping for link')

        event.widget.focus_set()  # give keyboard focus to the label
        event.widget.bind('<Key>', self.open_link(event.widget.cget('text')))
    def open_link(self, address):
        print('this should be opening link')
        webbrowser.open_new(address)
    def build_student_assignment_tab(self):
        name_label = ttk.Label(self.assn_frame, text="Hell you piece of shit")

    def combo_call_back(self, event):
        print('Combo Call back')
        if event.widget.get() != "Select a class":
            semester = event.widget.get()
            self.clear_main_canvas()
            self.main_canvas.pack_forget()
            print(event.widget.get())
            student_submissions = self.util.get_class_data(semester)
            self.main_frame = tk.Frame(self.root, bg='#272727',
                                       relief=tk.RIDGE, borderwidth=3)
            self.main_frame.pack(anchor=W, fill=tk.BOTH,
                                 expand=True,
                                 side=tk.LEFT)
            self.main_scrollbar = tk.Scrollbar(self.main_frame,
                                               orient=tk.VERTICAL)
            self.main_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
            # pprint(student_submissions)
            class_assignments = self.util.get_class_assn(semester)
            self.combine_assn_with_submissions(class_assignments,
                                               student_submissions)
            frame_list = []
            height = 0
            # for assignment in class_assignments:
            #     frame = tk.Frame(self.main_frame, width=self.width, bg="green")
            #     frame.pack()
            #     frame_list.append(frame)

    def combine_assn_with_submissions(self, class_assignments,
                                      student_submissions):
        for item in class_assignments:
            print(item)
        ...

    def collect_assignments(self, event):
        print('WTAF')
        print(event.widget.get())
        print(self.selected_class.get())

    def import_class(self):
        self.clear_main_canvas()
        print('Import class was clicked')
        self.title_font = tk.font.Font(family="Fira Code", size=28,
                                       weight='bold')
        self.title_label = tk.Label(self.main_canvas, text="Create a new "
                                                           "class",
                                    bg="#272727", font=self.title_font)
        self.title_label.place(relx=.25, y=3)
        self.id_label = tk.Label(self.main_canvas,
                                 text="Roster Google Document ID:",
                                 bg='#272727')
        self.id_label.place(x=5, y=100)
        self.id_text = tk.Text(self.main_canvas, height=1, width=30,
                               bg="white", fg="black")
        self.id_text.place(x=350, y=100)
        self.semester = tk.Label(self.main_canvas,
                                 text="Class Semester: ", bg='#272727')

        self.semester.place(x=5, y=150)
        self.semester_text = tk.Text(self.main_canvas, height=1, width=30,
                                     bg="white", fg="black")
        self.semester_text.place(x=350, y=150)

        self.submit_class_btn = Button(self.main_canvas, text="Submit Class",
                                       font=self.label_font)
        self.submit_class_btn.place(x=550, y=250)
        self.submit_class_btn.bind('<Button-1>', self.submit_class)
        # self.id_text.pack(side=TOP, pady=30)
        # self.id_label.pack(side=TOP, pady=30)
        # self
        self.main_canvas.update()

    def submit_class(self, event):
        print('Submit class is being called')
        semester = self.semester_text.get("1.0", 'end-1c')
        document_id = self.id_text.get("1.0", 'end-1c')
        len_semester = len(semester)
        len_document_id = len(document_id)

        if ((not len_semester) or (not len_document_id)):
            # if entered user failed to supply needed info
            messagebox.showerror('error', 'Empty fields are not allowed!')
        else:
            # both text fields were supplied with data, begging import ops
            datetoday = date.today()
            class_name = f'{semester}_{str(datetoday.year)}'

            data = dict()
            data['semester'] = class_name
            data['document_id'] = document_id

            print()
            self.util.create_new_class(data)
            self.semester.place_forget()
            self.semester_text.place_forget()
            self.id_label.place_forget()
            self.id_text.place_forget()
            self.submit_class_btn.place_forget()
            update_submissions = tk.messagebox.askyesno(
                title=f'Update?',
                message=f"Do you wish to update {class_name} submissions.")
            if update_submissions:
                print('User chose to update class submissions')
                response = self.util.update_class_submissions(class_name)
                view_pie_chart = tk.messagebox.askyesno(
                    title='Stats',
                    message='Would you like to view student stats?'
                )
    def focus_next_windows(self, event):
        event.widget.tk_focusNext().focus()
        return 'break'

    def clear_main_canvas(self):
        print('Clear main canvas being called')
        for widget in self.main_canvas.place_slaves():
            widget.place_forget()
            widget.pack_forget()
        print('Deleting main canvas')
        self.main_canvas.delete('all')
        self.main_canvas.update()

    def build_assignments(self):
        self.clear_main_canvas()
        # classes = self.util.get_class_list()
        # variable = StringVar(self.main_canvas, 'Select a semester')
        # self.dropdown=tk.OptionMenu(self.main_canvas, variable, *classes,
        #                             command=self.opt_menu_select)
        # self. dropdown.config(font=self.label_font, bg="#272727")
        # self.dropdown.place(relx=0.5, rely=.025, anchor=CENTER)
        self.clear_main_canvas()
        options = self.util.get_class_list()

        self.selected_class = tk.StringVar()

        self.options_cb = ttk.Combobox(self.main_canvas,
                                       state="readonly",
                                       textvariable=self.selected_class,
                                       font=self.label_font, justify="center")

        self.options_cb['values'] = options[0:]
        self.options_cb.current(0)
        self.options_cb['state'] = 'readonly'
        # options_cb.pack(fill=tk.X, padx=5, pady=5)

        self.options_cb.place(relx=0.5, rely=.025, anchor=CENTER)
        self.options_cb.bind("<<ComboboxSelected>>", self.opt_menu_select)

    def opt_menu_select(self, event):
        semester = event.widget.get()
        # self.dropdown.place_forget()
        self.options_cb.place_forget()
        title = f"Add Assignment to {semester}"
        title_lbl = Label(self.main_canvas, text=title, font=self.label_font,
                          bg="#272727")
        title_lbl.place(x=200, y=10)
        # Enter Assignment numbers
        assn_lbl = tk.Label(self.main_canvas, text="Assignment Number:",
                            font=self.label_font, bg="#272727")
        assn_text = tk.Text(self.main_canvas, height=3, width=20,
                            bg="#F5F0F6", fg="black",
                            font=self.label_font)
        assn_text.config(insertbackground="black")
        assn_text.bind("<Tab>", self.focus_next_windows)
        title_lbl = tk.Label(self.main_canvas, text="Title(s)",
                             font=self.label_font, bg="#272727")
        title_text = tk.Text(self.main_canvas, height=3, width=20,
                             bg="#F5F0F6", fg="black", font=self.label_font)
        title_text.bind("<Tab>", self.focus_next_windows)
        title_text.config(insertbackground="black")
        # Enter UVA  ID seperated by commas
        id_lbl = tk.Label(self.main_canvas, text="UVA ID(s)",
                          font=self.label_font, bg="#272727")
        id_text = tk.Text(self.main_canvas, height=3, width=20,
                          bg="#F5F0F6", fg="black", font=self.label_font,
                          )
        id_text.bind("<Tab>", self.focus_next_windows)
        id_text.config(insertbackground="black")
        # 3nter percentage
        prct_label = tk.Label(self.main_canvas, text="Percentage values",
                              font=self.label_font, bg="#272727")

        prct_text = tk.Text(self.main_canvas, height=3, width=20,
                            bg="#F5F0F6", fg="black", font=self.label_font)
        prct_text.config(insertbackground="black")
        prct_text.bind("<Tab>", self.focus_next_windows)
        # Enter Percentage

        weight_lbl = tk.Label(self.main_canvas, text="Weight(s)",
                              font=self.label_font, bg="#272727")
        weight_text = tk.Text(self.main_canvas, height=3, width=20,
                              bg="#F5F0F6", fg="black", font=self.label_font)
        weight_text.bind("<Tab>", self.focus_next_windows)
        weight_text.config(insertbackground="black")

        assn_lbl.place(x=10, y=100)
        assn_text.place(x=275, y=102)

        title_lbl.place(x=10, y=200)
        title_text.place(x=275, y=200)

        id_lbl.place(x=10, y=300)
        id_text.place(x=275, y=302)

        prct_label.place(x=10, y=400)
        prct_text.place(x=275, y=402)

        weight_lbl.place(x=10, y=500)
        weight_text.place(x=275, y=500)
        today = date.today()
        due_label = tk.Label(self.main_canvas, text="Due Date:", bg="#272727",
                             font=self.label_font)
        calendar_frame = Frame(self.main_canvas, height=200, width=200,
                               bg="#F5F0F6")
        calendar_frame.bind("<Tab>", self.focus_next_windows)

        # cal = tkcalendar.Calendar(calendar_frame, selctmode='day',
        #                           year=today.year, month=today.month,
        #                           day=today.day)
        # cal = tkcalendar.dateentry(calendar_frame, width=20, background='darkblue',
        # cal = tkcalendar.dateentry(calendar_frame, width=20,
        # background='darkblue',
        #                 foreground="white", borderwidhth=2)
        from tkcalendar import Calendar, DateEntry

        cal = DateEntry(calendar_frame, width=20, background='darkblue',
                        foreground='white', borderwidth=2,
                        date_pattern='yyyy/mm/dd', font='Arial 20')
        cal.pack(fill=tk.BOTH, expand=1)
        due_label.place(x=10, y=600)
        calendar_frame.place(x=275, y=600)
        hour_string = StringVar()
        min_string = StringVar()
        time_label = tk.Label(self.main_canvas, text="Time Due:",
                              font=self.label_font, bg="#272727")

        time_text = tk.Text(self.main_canvas, height=1, width=20,
                            bg="#F5F0F6", fg="black", font=self.label_font)
        required_label = tk.Label(self.main_canvas, text="Required Solves",
                                  font=self.label_font, bg="#272727")

        required_text = tk.Text(self.main_canvas, height=1, width=20,
                                bg="#F5F0F6", fg="black", font=self.label_font)
        required_text.bind("<Tab>", self.focus_next_windows)
        time_text.config(insertbackground="black", )
        time_text.bind("<Tab>", self.focus_next_windows)
        submit_btn = tk.Button(self.main_canvas, height=2, width=12,
                               text='Add Assignment', font=self.label_font,
                               command=lambda : self.validate_assignment(


                                   dict(semester=semester,
                                        assn_number=str(assn_text.get("1.0",
                                                                      "end-1c")),
                                        title=title_text.get("1.0", "end-1c")
                                        .split(','),
                                        uva_id=id_text.get("1.0", "end-1c")
                                        .replace(' ', '').split(','),
                                        percent=prct_text.get("1.0", "end-1c")
                                        .replace(' ', '').split(','),
                                        weight=weight_text.get("1.0", "end-1c")
                                        .replace(' ', '').split(','),
                                        due_date=f'{str(cal.get_date())} '
                                                 f''
                                                 f''
                                                 f'{time_text.get("1.0","end-1c")}:00',
                                        time_due=f'{time_text.get("1.0","end-1c")}',
                                        required=required_text.get("1.0",
                                                                   "end-1c"))))
        time_before = time_text.get("1.0", "end-1c")
        time_label.place(x=10, y=650)
        time_text.place(x=275, y=650)
        required_label.place(x=10, y=700)
        required_text.place(x=275, y=700)
        submit_btn.place(x=350, y=800)

    def validate_assignment(self, assignment: Assignment):
        response = self.util.add_class_assignment(assignment)
        if response['status'] == 'OK':
            self.clear_main_canvas()
        print(response)

    def get_class_list(self):
        url = f'{self.api_addy}/class_list'
        self.classes = requests.get(url, auth=self.credentials)
        self.classes = self.classes.content
        self.classes = self.decode_bytes(self.classes)

    def get_class_students(self, class_name):
        # @app.get('/class/{class_name}')
        url = f'{self.api_addy}/class/{class_name}'
        students = requests.get(url, auth=self.credentials)
        pprint(self.decode_bytes(students.content))

    def get_all_students(self):
        students = f'{self.api_addy}/all_classes'
        print(students)
        self.classes = requests.get(students, auth=self.credentials)

        self.classes = self.decode_bytes(self.classes)

        # self.classes = self.classes.content
        # self.classes = json.loads(self.classes.decode('utf-8'))

    def dummy_request(self):
        url = f'{self.api_addy}/'
        result = requests.get(url, auth=self.credentials)
        pprint(self.bytes_to_dict(result.content))

    def listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            class_name = event.widget.get(index)
            print(f'Data from ListBox selection = {class_name}')
            self.get_class_students(class_name)
            # self.class_frame.pack_forget()


if __name__ == '__main__':
    grader = UVA_Grader()
