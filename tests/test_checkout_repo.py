"""
Unit test git clone and tcpdump of a repo.
"""
from unittest import mock
from monitors.checkout_repo import checkout_git_repo, launch_tcpdump, kill_tcpdump


def test_parallel_processes():
    """
    Test the parallel processes of git clone and tcpdump.
    """
    # Mock git.Repo.clone_from
    with mock.patch("git.Repo.clone_from") as mock_clone_from:
        with mock.patch("tempfile.TemporaryDirectory") as mock_tempdir:
            # Mock subprocess.Popen for tcpdump
            with mock.patch("subprocess.Popen") as mock_popen_tcpdump:
                # Mock tcpdump_process.kill
                with mock.patch("subprocess.Popen.kill") as mock_kill:
                    # Call the function
                    checkout_git_repo(
                        "https://github.com/username/repo.git"
                    )
                    mock_popen_tcpdump.return_value = mock.Mock()
                    tcpdump_process = launch_tcpdump("eth0", "tcpdump.pcap")
                    kill_tcpdump(tcpdump_process)

                    # Mock subprocess.Popen for git clone
                    mock_clone_from.assert_called()
                    # Mock subprocess.Popen for tcpdump
                    mock_popen_tcpdump.assert_called_with(
                        ["tcpdump", "-i", "eth0", "-w", "tcpdump.pcap"]
                    )
