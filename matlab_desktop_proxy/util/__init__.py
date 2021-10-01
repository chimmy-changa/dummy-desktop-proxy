# Copyright 2020 The MathWorks, Inc.
import signal
import socket
import sys
import argparse
from aiohttp import web
from matlab_desktop_proxy import mwi_environment_variables as mwi_env
from matlab_desktop_proxy.util import mwi_logger

logger = mwi_logger.get()


def is_python_version_newer_than_3_6():
    """Returns True if the python version being used is 3.7 or higher, else False.

    Returns:
        Boolean: True if python version >= 3.7, False otherwise.
    """
    return sys.version_info[:2] >= (3, 7)


def parse_cli_args():
    """Parses CLI arguments passed to the main() function.


    Returns:
        dict: Containing the parsed arguments
    """
    # Parse the --config flag provided to the console script executable.
    parsed_args = {}
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="A json file which stores the config specific to the environment ",
    )
    args = parser.parse_args()
    config = "default_config" if args.config is None else args.config

    parsed_args["config"] = config

    return parsed_args


def prepare_site(app, runner):
    """Prepares to launch a TCPSite. If MWI_APP_PORT env variable is set,
    it will setup a site to launch on that port, else will launch on a random available port.

    Args:
        app (Application): An aiohttp.web.Application to launch a site.
        runner (AppRunner): An aiohhtp.web.Apprunner

    Returns:
        [TCPSite]: A TCPSite on which the integration will start.
    """
    port = app["settings"]["app_port"]
    if port:
        logger.info(f"Using {mwi_env.get_env_name_app_port()} to launch the server")
        site = web.TCPSite(runner, host=app["settings"]["host_interface"], port=port)

    else:
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("", 0))
                p = s.getsockname()[1]
                s.close()
                logger.info(f"Trying to launch the site on port {p}")
                site = web.TCPSite(
                    runner, host=app["settings"]["host_interface"], port=p
                )
                break
            except:
                logger.info(f"Failed to launch the site on port {p}")

    return site


def __get_supported_termination_signals():
    """Returns supported set handlers for asynchronous events.

    Returns:
        List: Containing supported set handlers.
    """
    return [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM]


def add_signal_handlers(loop):
    """Adds signal handlers to event loop.
    This is necessary to shutdown the server safely when an interrupt is raised.

    Args:
        loop (loop): Asyncio event loop

    Returns:
        loop: Asyncio event loop with signal handlers added.
    """
    for signal in __get_supported_termination_signals():
        logger.info(f"Registering handler for signal: {signal} ")
        loop.add_signal_handler(signal, lambda: loop.stop())

    return loop
