import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askyesno

from assets.data import sql_requests


def window_center(self):
    """Централизует любые окна относительно экрана монитора

        Parameters
        ----------
        self: необходимое окно, которое нужно центровать
    """
    self.update_idletasks()
    width = self.winfo_width()
    frm_width = self.winfo_rootx() - self.winfo_x()
    root_width = width + 2 * frm_width
    height = self.winfo_height()
    titlebar_height = self.winfo_rooty() - self.winfo_y()
    root_height = height + titlebar_height + frm_width
    x = self.winfo_screenwidth() // 2 - root_width // 2
    y = self.winfo_screenheight() // 2 - root_height // 2
    self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    self.deiconify()


class App(tk.Tk):
    """
        About
        ----------
        Основное применение - запуск и осуществление полного цикла
        работы приложения

        Attributes
        ----------
        Представляют собой технические и стилевые характерики приложения при его запуске.

        Methods
        -------
    """

    def __init__(self):
        super().__init__()
        self.title('Library catalogue')
        self.geometry('698x660')
        self.iconbitmap(default='./assets/icons/favicon_main.ico')
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('mystyle.Treeview.Heading',
                        font=('Times New Roman', 12, 'bold'),
                        lightcolor='#242121', darkcolor='#242121')
        style.configure('mystyle.Treeview', font=('Times New Roman', 12),
                        lightcolor='#242121')

        columns = ('column_1', 'column_2', 'column_3', 'column_4', 'column_5')
        self.tree = ttk.Treeview(columns=columns, show='headings',
                                 style='mystyle.Treeview')
        self.tree.grid(row=0, column=0, sticky='nsew')

        window_center(self)
        sql_requests.create.connection_with_request()
        self.tree = self.create_tree_widget()
        self.menu = self.create_main_menu()

    def create_main_menu(self):
        """

            Parameters
            ----------
            bd: list, optional
        """
        menu = tk.Menu()
        menu.add_cascade(label='Обновить', command=self.update_tree)
        menu.add_cascade(label='Добавить книгу', command=self.btn_add)
        menu.add_cascade(label='Изменить книгу', command=self.btn_change)
        menu.add_cascade(label='Найти книгу', command=self.btn_find)
        menu.add_cascade(label='Удалить книгу', command=self.btn_delete)
        self.config(menu=menu)
        self.option_add('*tearOff', tk.FALSE)
        return menu

    def item_selected(self, event):
        """

            Parameters
            ----------
        """
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            self.select_item = item['values']
        return self.select_item

    def create_tree_widget(self, bd=None):
        """

            Parameters
            ----------
            bd: list, optional
        """
        self.tree.heading('column_1', text='Id', anchor='center')
        self.tree.heading('column_2', text='Author', anchor='center')
        self.tree.heading('column_3', text='Title', anchor='center')
        self.tree.heading('column_4', text='Year', anchor='center')
        self.tree.heading('column_5', text='Status', anchor='center')

        self.tree.column('#1', stretch=tk.NO, width=40, anchor='center')
        self.tree.column('#2', stretch=tk.NO, width=240, anchor='center')
        self.tree.column('#3', stretch=tk.NO, width=240, anchor='center')
        self.tree.column('#4', stretch=tk.NO, width=60, anchor='center')
        self.tree.column('#5', stretch=tk.NO, width=100, anchor='center')

        scrollbar = ttk.Scrollbar(orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        if bd:
            for item in bd:
                if item[4] == 1:
                    self.tree.insert("", tk.END, values=(
                        item[0], item[1], item[2], item[3], 'В наличии'))
                else:
                    self.tree.insert("", tk.END, values=(
                        item[0], item[1], item[2], item[3], 'Выдана'))
        else:
            for item in sql_requests.select.connection_with_request():
                if item[4] == 1:
                    self.tree.insert("", tk.END, values=(
                        item[0], item[1], item[2], item[3], 'В наличии'))
                else:
                    self.tree.insert("", tk.END, values=(
                        item[0], item[1], item[2], item[3], 'Выдана'))

        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        return self.tree

    def toplevel_window(self, btn_name):
        """

            Parameters
            ----------
        """
        add_window = tk.Toplevel()
        add_window.geometry('455x265')
        add_window.configure(background='white')
        window_center(add_window)

        def action():
            book_author = entry_author.get()
            book_title = entry_title.get()
            book_year = spinbox_year.get()

            if btn_name == 'btn_find':
                self.update_tree(
                    sql_requests.where.connection_with_request(book_author,
                                                               book_title,
                                                               book_year))
                add_window.destroy()
                return None

            select_status = combobox_status.get()
            book_status = f'{1 if select_status == "В наличии" else 0}'

            if (len(book_author) == 0 or len(book_title) == 0 or len(
                    book_year) == 0 or len(
                select_status) == 0) and btn_name != 'btn_find':
                showerror(title="Ошибка", message="Не все поля заполнены")
                return None

            if btn_name == 'btn_add':
                sql_requests.insert.connection_with_request(book_author,
                                                            book_title,
                                                            int(book_year),
                                                            int(book_status))
            elif btn_name == 'btn_change':
                book_id = self.select_item[0]
                sql_requests.update.connection_with_request(book_author,
                                                            book_title,
                                                            int(book_year),
                                                            int(book_status),
                                                            book_id)

            self.update_tree()
            add_window.destroy()

        # Названия полей модального окна
        label_author = ttk.Label(add_window, text='Автор:',
                                 font=('Times New Roman', 14),
                                 background='white')
        label_author.place(x=66, y=20)
        label_title = ttk.Label(add_window, text='Название:',
                                font=('Times New Roman', 14),
                                background='white')
        label_title.place(x=41, y=60)
        label_year = ttk.Label(add_window, text='Год:',
                               font=('Times New Roman', 14),
                               background='white')
        label_year.place(x=82, y=104)
        label_status = ttk.Label(add_window, text='Статус:',
                                 font=('Times New Roman', 14),
                                 background='white')
        label_status.place(x=61, y=144)

        # Поля модального окна для заполнения пользователем
        entry_author = ttk.Entry(add_window, font=('Times New Roman', 14),
                                 width=28)
        entry_author.place(x=140, y=20)

        entry_title = ttk.Entry(add_window, font=('Times New Roman', 14),
                                width=28)
        entry_title.place(x=140, y=60)

        spinbox_year = ttk.Spinbox(add_window, from_=1, to=2030,
                                   font=('Times New Roman', 14), width=5)
        spinbox_year.place(x=140, y=104)
        status = ['В наличии', 'Выдана']

        combobox_status = ttk.Combobox(add_window, values=status)
        combobox_status.place(x=138, y=146)

        # Формирование определенного вида модального окна
        if btn_name == 'btn_add':
            add_window.title('Добавить книгу')
            add_window.iconbitmap('./assets/icons/favicon_add.ico')
            btn_submit = ttk.Button(add_window, text='Добавить книгу',
                                    command=action)
        elif btn_name == 'btn_find':
            add_window.title('Найти книгу')
            add_window.iconbitmap('./assets/icons/favicon_find.ico')
            label_status.destroy()
            combobox_status.destroy()
            btn_submit = ttk.Button(add_window, text='Найти книгу',
                                    command=action)
        elif btn_name == 'btn_change':
            add_window.title('Изменить книгу')
            add_window.iconbitmap('./assets/icons/favicon_change.ico')
            btn_submit = ttk.Button(add_window, text='Изменить книгу',
                                    command=action)
            entry_author.insert(0, self.select_item[1])
            entry_title.insert(0, self.select_item[2])
            spinbox_year.insert(0, self.select_item[3])
            combobox_status.set('В наличии' if self.select_item[
                                                   4] == 'В наличии' else 'Выдана')

        btn_submit.place(x=180, y=208)

    # Методы для работы с кнопками основного меню
    ####################################################
    def btn_add(self):
        """

            Parameters
            ----------
        """
        self.toplevel_window('btn_add')

    def btn_change(self):
        """

            Parameters
            ----------
        """
        self.toplevel_window('btn_change')

    def btn_find(self):
        """

            Parameters
            ----------
        """
        self.toplevel_window('btn_find')

    def btn_delete(self):
        """

            Parameters
            ----------
        """
        result = askyesno(title="Удаление книги из библиотеки",
                          message="Подтвердить удаление?")
        if result:
            sql_requests.delete.connection_with_request(
                book_select=self.select_item[0])
            self.update_tree()
            showinfo("Результат", "Операция подтверждена", icon='info')
        else:
            showinfo("Результат", "Операция отменена", icon='warning')

    def update_tree(self, bd=None):
        """

            Parameters
            ----------
        """
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.tree = self.create_tree_widget(bd)


if __name__ == "__main__":
    app = App()
    app.mainloop()
