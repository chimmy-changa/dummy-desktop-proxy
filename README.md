# MATLAB Desktop Proxy
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mathworks/jupyter-matlab-proxy/MATLAB%20Jupyter%20Integration?logo=github)](https://github.com/mathworks/jupyter-matlab-proxy/actions)
[![PyPI badge](https://img.shields.io/pypi/v/matlab-desktop-proxy.svg?logo=pypi)](https://pypi.python.org/pypi/matlab-desktop-proxy)
[![codecov](https://codecov.io/gh/mathworks/matlab-desktop-proxy/branch/main/graph/badge.svg?token=ZW3SESKCSS)](https://codecov.io/gh/mathworks/matlab-desktop-proxy)

The matlab-desktop-proxy Python® package enables you to open a MATLAB® desktop in a web browser tab.
 
The MATLAB Desktop Proxy is under active development and you might find issues with the MATLAB graphical user interface. For support or to report issues, see the [Feedback](#feedback) section.


## Use the MATLAB Desktop Proxy

Once the `matlab-desktop-proxy` package installed, to use the integration, follow these steps:

1. Open a terminal and run the below command.
```bash
MWI_BASE_URL="" MWI_APP_PORT=8888 matlab-desktop-proxy-app
```


2. A new browser tab should open. If prompted to do so, enter credentials for a MathWorks account associated with a MATLAB license. If you are using a network license manager, then change to the Network License Manager tab and enter the license server address instead. To determine the appropriate method for your license type, consult [MATLAB Licensing Info](./MATLAB-Licensing-Info.md).

<p align="center">
  <img width="400" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/licensing_GUI.png">
</p>

3. Wait for the MATLAB session to start. This can take several minutes.

4. To manage the MATLAB integration, click the tools icon shown below.

<p align="center">
  <img width="100" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/tools_icon.png">
</p>

5. Clicking the tools icon opens a status panel with buttons like the ones below:

    <p align="center">
      <img width="800" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/status_panel.png">
    </p>


   The following options are available in the status panel (some options are only available in a specific context):

   * Start MATLAB Session — Start your MATLAB session. Available if MATLAB is stopped.
   * Restart MATLAB Session — Restart your MATLAB session. Available if MATLAB is running or starting.
   * Stop MATLAB Session — Stop your MATLAB session. Use this option if you want to free up RAM and CPU resources. Available if MATLAB is running or starting.
   * Sign Out — Sign out of MATLAB. Use this to stop MATLAB and sign in with an alternative account. Available if using online licensing.
   * Unset License Server Address — Unset network license manager server address. Use this to stop MATLAB and enter new licensing information. Available if using network license manager.
   * Feedback — Send feedback about the MATLAB Desktop Proxy. This action opens your default email application.
   * Help — Open a help pop-up for a detailed description of the options.


## Installation

The `matlab-desktop-proxy` package requires a Linux® operating system.

<!-- #FIXME: Create a new dockerfile and github repo for matlab-web-esktop-proxy -->
If you want to install this package in a Docker® image, see [Use MATLAB Desktop Proxy in a Docker Container](https://github.com/mathworks-ref-arch/matlab-integration-for-jupyter/tree/main/matlab). Otherwise, if you want to install the `matlab-desktop-proxy` package into a preexisting Jupyter environment, follow the instructions below.

To install the `matlab-desktop-proxy` package, follow these steps on a Linux OS:
<!-- #FIXME: Update this repo and remove the jupyter parts? -->
1. Install a MATLAB 64 bit Linux version. Make sure the the installation folder is on the system path. This integration supports MATLAB R2020b or later.
2. Install software packages that MATLAB depends on and software packages that this integration depends on. For a list of required software packages in a Debian based distribution, inspect [this Dockerfile](https://github.com/mathworks-ref-arch/matlab-integration-for-jupyter/blob/main/matlab/Dockerfile).
3. Install [Node and Node Package Manager](https://nodejs.org/en/) version 13 or higher.
4. Install the `matlab-desktop-proxy` package by executing:
```bash
python -m pip install matlab-desktop-proxy
```
<!-- TODO: Installation instruction for conda env -->

### Usage with JupyterHub

MATLAB Desktop Proxy can now be integrated with the JupyterHub ecosystem. Check [jupyter-matlab-proxy](https://github.com/mathworks/jupyter-matlab-proxy) on github for more information.

### Limitations

This package supports the same subset of MATLAB features and commands as MATLAB Online. For a full list supported products and limitations, see [Specifications and Limitations](https://www.mathworks.com/products/matlab-online/limitations.html). For a list of browser requirements, see [Cloud Solutions Browser Requirements](https://www.mathworks.com/support/requirements/browser-requirements.html). If you need to use functionality that is not yet supported, you can leverage the alternative [MATLAB Integration for Jupyter using VNC](https://github.com/mathworks/jupyter-matlab-vnc-proxy).
<!-- #FIXME: Update the above repo as well? -->

## Feedback

We encourage you to try this repository with your environment and provide feedback – the technical team is monitoring this repository. If you encounter a technical issue or have an enhancement request, send an email to `jupyter-support@mathworks.com`.
<!-- FIXME: Update the support url ? -->