# Copyright 2020-2021 The MathWorks, Inc.
"""This file contains validators for various runtime artefacts.
A validator is defined as a function which verifies the input and 
returns it unchanged if validation passes. 
Returning inputs allows validators to be used inline with the input.

Example: 
Original code: if( input ):
With validator: if (valid(input)):

Exceptions are thrown to signal failure.
"""
import sys
import socket
import errno
import pkg_resources
from matlab_desktop_proxy.util import mwi_logger
from matlab_desktop_proxy import mwi_environment_variables as mwi_env

logger = mwi_logger.get()


def validate_mlm_license_file(nlm_conn_str):
    """Validates and returns input if it passes validation.
    Throws exception when validation fails.
    The connection string should be in the form of port@hostname
    OR path to valid license file

    Args:
        nlm_conn_str (String): Contains the Network license manager connection string.

    Raises:
        NetworkLicensingError: A custom exception.

    Returns:
        String: Returns the same argument passed to this function if its valid.
    """
    import re
    import os
    from .mwi_exceptions import NetworkLicensingError

    if nlm_conn_str is None:
        return None

    # TODO: The JS validation of this setting does not allow file path locations
    # The JS validation occurs before reaching the set_licensing_info endpoint.

    # Regular expression to match port@hostname,
    # where port is any number and hostname is alphanumeric
    # regex = Start of Line, Any number of 0-9 digits , @, any number of nonwhite space characters with "- _ ." allowed
    # "^[0-9]+[@](\w|\_|\-|\.)+$"
    # Server triad is of the form : port@host1,port@host2,port@host3
    regex = "(^[0-9]+[@](\w|\_|\-|\.)+$)|(^[0-9]+[@](\w|\_|\-|\.)+),([0-9]+[@](\w|\_|\-|\.)+),([0-9]+[@](\w|\_|\-|\.)+$)"
    if not re.search(regex, nlm_conn_str):
        logger.debug("NLM info is not in the form of port@hostname")
        if not os.path.isfile(nlm_conn_str):
            logger.debug("NLM info is not a valid path to a license file")
            error_message = (
                f"MLM_LICENSE_FILE validation failed for {nlm_conn_str}. "
                f"If set, the MLM_LICENSE_FILE environment variable must be a string which is either of the form port@hostname"
                f" OR path to a valid license file."
            )
            logger.error(error_message)
            raise NetworkLicensingError(error_message)
        else:
            logger.info(
                f"MLM_LICENSE_FILE with value: {nlm_conn_str} is a path to a file. MATLAB will attempt to use it."
            )
    else:
        logger.info(
            f"MLM_LICENSE_FILE with value: {nlm_conn_str} is a license server, MATLAB will attempt to connect to it."
        )

    # Validation passed
    return nlm_conn_str


def validate_app_port_is_free(port):
    """Validates and returns port if its free else will error out and exit.

    Args:
        port (str|int): Port number either as a string or an integer.

    Raises:
        e: socket.error

    Returns:
        Boolean: True if provided port is occupied else False.
    """
    # If port is None, at launch, site will use a randomnly allocated port.
    if not port:
        logger.info(
            f"Environment variable {mwi_env.get_env_name_app_port()} was not set. Will use a random port at launch."
        )
        return port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", int(port)))
        s.close()

        # Was able to allocate port. Validation passed.
        return port
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            logger.error(
                f"The port {port} is not available. Please set another value for the environment variable {mwi_env.get_env_name_app_port()}"
            )
            sys.exit(1)
        else:
            raise e


def validate_base_url(base_url):
    if not base_url:
        logger.info(
            f'Environment variable {mwi_env.get_env_name_base_url()} was not set. Will launch at path: "/" '
        )
        return ""

    else:
        if not base_url.startswith("/"):
            logger.error(
                f'The value of Environment variable {mwi_env.get_env_name_base_url()} must start with "/" '
            )
            sys.exit(1)

        base_url = base_url[:-1] if base_url.endswith("/") else base_url

        return base_url


def validate_env_configs(config):
    """Validates config passed with available "matlab_desktop_proxy_configs" entry point in the same
    python environment.

    Args:
        config (str): Name of the configuration to use.

    Returns:
        Dict: Containing data specific to the environment in which MATLAB desktop proxy is being used in.
    """
    available_configs = __get_configs()
    if config in available_configs:
        logger.info(f"Successfully validated env config")
        return available_configs[config]
    else:
        logger.info(
            f"{config} is not a valid config. Available configs are : {available_configs.keys()}"
        )
        sys.exit(1)


def __get_configs():
    """Iterates over the 'entry_points' of the installed packages in the current python
    environment and loads the 'matlab_desktop_proxy_configs' entry point values into the 'configs' Dict.

    Returns:
        Dict: Contains all the values present in 'matlab_web_desktop_configs' entry_point from all the packages
        installed in the current environment.
    """
    configs = {}
    for entry_point in pkg_resources.iter_entry_points("matlab_desktop_proxy_configs"):
        configs[entry_point.name] = entry_point.load()

    return configs
