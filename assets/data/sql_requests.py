import sqlite3


class Request:
    """
        About
        ----------
        Основное применение - выполнение любых запросов к базе данных.

        Attributes
        ----------
        name - имя для экземпляра класса, которое является отображением одного из типов запросов в sql

        Methods
        -------
        connection_with_request()
            основной метод класса - который представляет из себя подключение к базе данных, а затем исходя из атрибута его экземпляра осуществляет тот или иной запрос (при необходимости возвращая значения из базы данных), после окончания работы производит закрытие базы данных 
    """

    def __init__(self, name):
        self.name = name

    def connection_with_request(self, book_author=None, book_title=None,
                                book_year=None, book_status=None,
                                book_id=None, book_select=None):
        """

            Parameters
            ----------
        """
        connection = sqlite3.connect('./assets/data/library.db')
        cursor = connection.cursor()

        if self.name == 'INSERT':
            cursor.execute(
                'INSERT INTO Books (author, title, year, status) VALUES (?, ?, ?, ?)',
                (book_author, book_title, book_year, book_status))

        elif self.name == 'UPDATE':
            cursor.execute(
                f'UPDATE Books SET author = ?, title = ?, year = ?, status = ? WHERE id = ?',
                (book_author, book_title, book_year, book_status, book_id))

        elif self.name == 'DELETE':
            cursor.execute(f'DELETE FROM Books WHERE id = {book_select}')

        elif self.name == 'WHERE':
            cursor.execute(
                'SELECT * FROM Books WHERE author = ? OR title = ? OR year = ?',
                (book_author, book_title, book_year))
            books = cursor.fetchall()
            return books

        elif self.name == 'CREATE':
            cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                status INTEGER NOT NULL)''')

        elif self.name == 'SELECT':
            cursor.execute('SELECT * FROM Books')
            books = cursor.fetchall()
            return books

        connection.commit()
        connection.close()


# Создание экземпляров класса с разными видами 
# запросов в SQL
####################################################
insert = Request('INSERT')
update = Request('UPDATE')
delete = Request('DELETE')
where = Request('WHERE')
create = Request('CREATE')
select = Request('SELECT')