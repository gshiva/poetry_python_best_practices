"""
Checks out a git repo while launching a tcpdump monitor

Output:
    JSON with the status and values for attributes that are being monitored
    such as checkout time, tcpdump pcap output file location.
"""

from typing import Any
import click
import subprocess
import git
import logging
import tempfile


logger = logging.getLogger(__name__)


def checkout_git_repo(git_repo_url: str) -> None:
    """
    Checkout a git repository.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        git.Repo.clone_from(url=git_repo_url, to_path=temp_dir)


def launch_tcpdump(interface: str, tcpdump_file: str) -> subprocess.Popen:
    """
    Launch tcpdump to monitor the tcp/ip traffic to a file.
    """
    tcpdump_process = subprocess.Popen(["tcpdump", "-i", interface, "-w", tcpdump_file])
    return tcpdump_process


def kill_tcpdump(tcpdump_process) -> Any:
    """
    Kill the tcp dump process
    """
    logger.info("Killing tcpdump process")
    tcpdump_process.kill()


@click.command()
@click.option(
    "--git_repo_url",
    prompt="Enter the URL to the repo",
    help="The path to the git repository",
    required=True,
)
def main(git_repo_url):
    """
    Launch tcpdump to monitor the git tcp/ip traffic and checkout the specified branch of the repo.

    Args:
    repo_path (str): The path to the git repository.

    Output:
        JSON with the status and values for attributes that are being monitored
        such as checkout time, tcpdump pcap output file location.
    """
    tcpdump_process = launch_tcpdump(interface="eth0", tcpdump_file="tcpdump.pcap")
    checkout_git_repo(git_repo_url=git_repo_url)
    kill_tcpdump(tcpdump_process=tcpdump_process)


if __name__ == "__main__":
    main()
