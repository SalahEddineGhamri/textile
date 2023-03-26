from rich.console import Console
from rich.text import Text


console = Console()
text = Text()
text.append(" this is a text ")
text.append("\n")
text.append("     ╭──╮       ")
text.append("\n")
text.append("     │is│       ")
text.append("\n")
text.append("     ╰──╯")
text.append("\n")
text.append(" this is a text ")
console.print(text)
