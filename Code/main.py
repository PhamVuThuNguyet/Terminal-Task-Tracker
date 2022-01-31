import typer
from database import complete as cpl
from database import delete as dlt
from database import insert, select_all
from database import update as udt
from model import Task
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console()

my_typer = typer.Typer()


@my_typer.command(short_help='add a task')
def add(task: str, tag: str):
    typer.echo(f"adding {task}, {tag}")
    new_task = Task(None, task, tag)
    insert(new_task)
    show()


@my_typer.command(short_help='delete a task')
def delete(id: int):
    typer.echo(f"deleting {id}")
    dlt(id - 1)
    show()


@my_typer.command(short_help='update data for a task')
def update(id: int, task: str = None, tag: str = None):
    typer.echo(f"updating {id}")
    udt(id - 1, task, tag)
    show()


@my_typer.command(short_help='update status for a task')
def complete(id: int):
    typer.echo(f"Task status changed successfully!")
    cpl(id - 1)
    show()


@my_typer.command(short_help='show your to do list')
def show():
    tasks = select_all()

    MARKDOWN = """# My task 💻"""
    md = Markdown(MARKDOWN)
    console.print(md)
    table = Table(show_header=True, header_style="bold #ffffff")
    table.add_column("ID", width=6, justify='center')
    table.add_column("Task", min_width=20, justify='center')
    table.add_column("Tag", min_width=10, justify='center')
    table.add_column("Status", min_width=8, justify='center')

    for id, tsk in enumerate(tasks, start=1):
        color = get_tag_color(tsk.tag)
        is_done = "✅" if tsk.status == 1 else "❌"
        table.add_row(f'[#ffffcc]{str(id)}[/#ffffcc]', f'[#ffffcc]{tsk.task}[/#ffffcc]',
                      f'[{color}]{tsk.tag}[/{color}]', is_done,
                      end_section=True)
    console.print(table)


def get_tag_color(tag):
    COLORS = {'Research': '#33ff33', 'School': '#66ffff', 'Self-Learning': '#33ff33', 'Sport': 'blue'}
    if tag in COLORS:
        return COLORS[tag]
    return '#ccffcc'


if __name__ == "__main__":
    my_typer()
