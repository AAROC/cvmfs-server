import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Basic sanity tests.
def test_hosts_file(host):
    """Basic sanity checks."""
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


# Set some fixtures for the packages that have to be installed on a CVMFS
# server. See defaults/main.yml -> cvmfs_packages
@pytest.mark.parametrize('name', [
    ('cvmfs'),
    ('cvmfs-server'),
])
def test_packages(host, name):
    """
    Check that the relevant packages are installed.

    See http://cvmfs.readthedocs.io/en/stable/cpt-repo.html#installation
    """
    pkg = host.package(name)
    assert pkg.is_installed

# Set some fixtures for the directories that have to be available on a CVMFS
# server.


@pytest.mark.parametrize('dir', [
    ('/var/spool/cvmfs'),
    ('/srv/cvmfs'),
    ('/cvmfs'),
    ('/etc/cvmfs'),
    ('/etc/cvmfs/repositories.d'),
])
def test_directories(host, dir):
    """
    Check that the relevant directories are present.

    See http://cvmfs.readthedocs.io/en/stable/cpt-repo.html#sct-serveranatomy
    """
    path = host.file(dir)
    assert path.is_directory
