import os
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================= SIMULATION CORE =================
def start_net_attack(method, target_ip, port, duration):
    clear()
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Initializing {method} Handshake...", total=None)
        time.sleep(1.5)

    console.print(Panel(Align.center(f"[bold yellow]STRESS TEST STARTED: {method}[/bold yellow]\n[white]Target: {target_ip}:{port} | Duration: {duration}s[/white]"), border_style="blue"))
    
    start_time = time.time()
    count = 0
    try:
        while time.time() - start_time < int(duration):
            p_size = random.randint(64, 1500)
            console.print(
                f"[bold cyan][{method}][/bold cyan] "
                f"[white]Payload:[/white] [green]{p_size} bytes[/green] | "
                f"[white]Status:[/white] [bold green]SENT[/bold green] | "
                f"[white]Thread:[/white] [magenta]{random.randint(1, 1024)}[/magenta]",
                style="dim"
            )
            count += 1
            time.sleep(0.02) # سرعة العرض
            if count % 50 == 0:
                console.print(f"[bold green]───> TOTAL TRAFFIC SENT: {count * p_size / 1024:.2f} KB[/bold green]")

        console.print(f"\n[bold green][✓] Stress Test Completed. Total Packets: {count}[/bold green]")
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Attack Terminated by User.[/bold red]")
    
    input("\nPress Enter to return to C2 Panel...")

# ================= UI ELEMENTS =================
def login():
    clear()
    console.print(Panel(Align.center("[bold cyan]C2 NETWORK COMMAND CENTER v4.0[/bold cyan]"), border_style="blue"))
    u = console.input("[blue]Access Key: [/blue]")
    p = console.input("[blue]Security Pin: [/blue]", password=True)
    return u == "rombo" and p == "rombo"

BANNER = """
[bold blue]
██████╗  ██████╗ ███╗   ███╗██████╗  ██████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗
██████╔╝██║   ██║██╔████╔██║██████╔╝██║   ██║
██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║
██║  ██║╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝
      [white]v4.0 NETWORK STRESSER - EDUCATIONAL TOOL[/white]
[/bold blue]
"""

def show_menu():
    table = Table(expand=True, border_style="blue")
    table.add_column("COMMAND EXAMPLE", justify="left", style="bold cyan")
    table.add_column("METHOD", justify="left", style="bold white")
    table.add_column("LAYER", justify="center", style="bold magenta")
    
    table.add_row("udpkill <ip> <port> <time>", "UDP Flood", "L4")
    table.add_row("tcpfools <ip> <port> <time>", "TCP Handshake", "L4")
    table.add_row("httpraw <ip> <port> <time>", "HTTP Request", "L7")
    table.add_row("cls", "Clear Screen", "-")
    table.add_row("exit", "Shutdown", "-")
    
    console.print(table)

# ================= MAIN LOGIC =================
def main():
    if not login():
        console.print("[bold red]ACCESS DENIED.[/bold red]")
        return

    while True:
        clear()
        console.print(BANNER)
        show_nodes_info = "[bold white]Nodes Online: [green]402[/green] | System Status: [green]Ready[/green][/bold white]"
        console.print(Align.center(show_nodes_info))
        show_menu()
        
        # هنا التعديل الأساسي: كياخد السطر كامل
        raw_cmd = console.input("[bold blue]Root@RoMbo:~# [/bold blue]").strip().split()

        if not raw_cmd:
            continue

        cmd = raw_cmd[0].lower()

        # معالجة أوامر الضرب (udpkill, tcpfools, httpraw)
        if cmd in ["udpkill", "tcpfools", "httpraw"]:
            if len(raw_cmd) == 4:
                method_name = cmd.upper()
                target_ip = raw_cmd[1]
                target_port = raw_cmd[2]
                target_time = raw_cmd[3]
                start_net_attack(method_name, target_ip, target_port, target_time)
            else:
                console.print("[bold yellow][!] Usage: method ip port time (e.g., udpkill 1.1.1.1 80 60)[/bold yellow]")
                time.sleep(2)
        
        elif cmd == "cls":
            clear()
        elif cmd == "exit":
            console.print("[bold red]Closing Connection...[/bold red]")
            break
        else:
            console.print(f"[bold yellow][!] Unknown command: {cmd}[/bold yellow]")
            time.sleep(1)

if __name__ == "__main__":
    main()
