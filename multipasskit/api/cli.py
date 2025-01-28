import click
import subprocess
from multipasskit.api.celerymultipass import celery_app
import uvicorn
from pathlib import Path
import shutil


def detect_init_system():
    """
    Detect whether the server is managed by systemd or init by checking PID 1.

    Returns:
        str: "systemd" if systemd is managing the system,
             "init" if init is managing the system,
             "unknown" if neither can be determined.
    """
    try:
        # Read the symbolic link for PID 1
        with open("/proc/1/comm", "r") as f:
            init_process = f.read().strip()

        # Check the name of the process
        if init_process == "systemd":
            return "systemd"
        elif init_process in ("init", "sysvinit"):
            return "init"
        else:
            return f"unknown (PID 1 is {init_process})"
    except Exception as e:
        return f"unknown (error: {e})"

def is_systemd():
    return "systemd" == detect_init_system()

@click.group()
def cli():
    pass

@cli.command(name="run-api")
@click.option("--port", "-p", default=8080, type=int, help="Server port (default: 8080)")
@click.option("--host", "-h", default="0.0.0.0", help="Server hostname or IP address.")
@click.option("--reload", default=False, is_flag=True, help="Reload on changes")
def runapi(host, port, reload):
    click.echo('Starting API server...')
    uvicorn.run("multipasskit.api.main:app", host=host, port=port, reload=reload)

@cli.command(name="run-celery")
@click.option(
    "--detach",
    "-D",
    default=False,
    is_flag=True,
    help="Start worker as a background process."
)
@click.option(
    "--loglevel",
    default='WARNING',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL']),
    help="Logging level.",
    show_default=True
)
@click.option(
    "--logfile",
    "-f",
    help="Log destination; defaults to stderr",
    type=click.Path()
)
def runcelery(detach, loglevel=None, logfile=None):
    args = ['worker']
    if logfile:
        args.append(f"--logfile={logfile}")
    if loglevel:
        args.append(f"--loglevel={loglevel}")
    if detach:
        args.append("--detach")

    active_workers = celery_app.control.inspect().active()
    if active_workers == None:
        try:
            celery_app.worker_main(argv=args)
        except Exception as e:
            click.echo(e.output)
            click.echo(e.stderr)
    else:
        click.echo("Celery worker is already running")

@cli.command(name="stop-celery")
def stopcelery():
    active_workers = celery_app.control.inspect().active()
    if active_workers:                       
        celery_app.control.shutdown()
        click.echo("Celery worker stopped")
    else:
        click.echo("Celery worker is not running")

def install_systemd_service(service_name, service_file):
    systemd_dir = "/usr/lib/systemd/system/"
    target_path = Path(systemd_dir) / service_name

    # Try to find the multipasskit binary
    multipasskit_path = shutil.which("multipasskit")

    if not multipasskit_path:
        # Default to a known path if not found
        multipasskit_path = "/usr/local/bin/multipasskit"
        click.echo(f"Warning: 'multipasskit' not found in PATH. Using default: {multipasskit_path}")

    try:
        click.echo(f"Installing {service_name} to {systemd_dir}")
        with open(service_file, "r") as f:
            service_content = f.read()

        # Replace the placeholder with the dynamic path
        service_content = service_content.replace("{MULTIPASSKIT_PATH}", multipasskit_path)

        # Write the final service file
        with open(target_path, "w") as f:
            f.write(service_content)

        subprocess.run(["systemctl", "daemon-reload"], check=True)
    except PermissionError:
        click.echo("Permission denied: Try running this script as root or with sudo.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to reload systemd daemon: {e}", err=True)

@cli.command(name="install-service")
def installservice():
    package_directory = Path(__file__).parent
    services_directory = package_directory / "utils" / "services"

    if is_systemd():
        click.echo("Detected systemd. Installing systemd services...")
        install_systemd_service("multipassapi.service", services_directory / "multipassapi.service")
        install_systemd_service("multipasscelery.service", services_directory / "multipasscelery.service")
        click.echo("Start services with:")
        click.echo("  sudo systemctl start multipassapi.service")
        click.echo("  sudo systemctl start multipasscelery.service")
    else:
        click.echo("Non-systemd OS detected. Service installation is currently unsupported.", err=True)

if __name__ == '__main__':
    cli()