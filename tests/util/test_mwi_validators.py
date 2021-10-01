# Copyright 2021 The MathWorks, Inc.
"""Tests for functions in matlab_desktop_proxy/util/mwi_validators.py
"""

import pytest, os, tempfile, socket, random
from matlab_desktop_proxy.util import mwi_validators
from matlab_desktop_proxy import mwi_environment_variables as mwi_env
from matlab_desktop_proxy.util.mwi_exceptions import NetworkLicensingError


def test_validate_mlm_license_file_for_invalid_string(monkeypatch):
    """Check if validator raises expected exception"""
    # Delete the environment variables if they do exist
    env_name = mwi_env.get_env_name_network_license_manager()
    invalid_string = "/Invalid/String/"
    monkeypatch.setenv(env_name, invalid_string)
    nlm_conn_str = os.getenv(env_name)
    with pytest.raises(NetworkLicensingError) as e_info:
        conn_str = mwi_validators.validate_mlm_license_file(nlm_conn_str)
    assert invalid_string in str(e_info.value)


def test_validate_mlm_license_file_for_valid_server_syntax(monkeypatch):
    """Check if port@hostname passes validation"""
    env_name = mwi_env.get_env_name_network_license_manager()
    license_manager_address = "1234@1.2_any-alphanumeric"
    monkeypatch.setenv(env_name, license_manager_address)
    conn_str = mwi_validators.validate_mlm_license_file(os.getenv(env_name))
    assert conn_str == license_manager_address


def test_validate_mlm_license_file_for_valid_server_triad_syntax(monkeypatch):
    """Check if port@hostname passes validation"""
    env_name = mwi_env.get_env_name_network_license_manager()
    license_manager_address = (
        "1234@1.2_any-alphanumeric,1234@1.2_any-alphanumeric,1234@1.2_any-alphanumeric"
    )
    monkeypatch.setenv(env_name, license_manager_address)
    conn_str = mwi_validators.validate_mlm_license_file(os.getenv(env_name))
    assert conn_str == license_manager_address


def test_get_with_environment_variables(monkeypatch):
    """Check if path to license file passes validation"""
    env_name = mwi_env.get_env_name_network_license_manager()
    fd, path = tempfile.mkstemp()
    monkeypatch.setenv(env_name, path)
    try:
        conn_str = mwi_validators.validate_mlm_license_file(os.getenv(env_name))
        assert conn_str == str(path)
    finally:
        os.remove(path)


def test_validate_app_port_is_free_false():
    """Test to validate if supplied app port is free"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    with pytest.raises(SystemExit) as e:
        mwi_validators.validate_app_port_is_free(port)
    assert e.value.code == 1
    s.close()


def test_validate_app_port_is_free_true():
    """Test to validate if supplied app port is free"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    assert mwi_validators.validate_app_port_is_free(port) == port


def test_validate_env_configs_true():
    """Validate the default config which is used in this package."""
    config = mwi_validators.validate_env_configs("default_config")
    assert isinstance(config, dict)


def test_validate_env_configs_false():
    """Passing a non existent config should raise SystemExit exception"""

    with pytest.raises(SystemExit) as e:
        config = mwi_validators.validate_env_configs(str(random.randint(10, 100)))

    assert e.value.code == 1


def test_get_configs():
    """Test to check if atleast 1 env config is discovered.
    When this package is installed, we will have a default config.
    """
    configs = mwi_validators.__get_configs()

    assert len(configs.keys()) >= 1
