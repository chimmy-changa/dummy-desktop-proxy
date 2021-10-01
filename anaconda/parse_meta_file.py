import ruamel
from ruamel.yaml import YAML
from matlab_desktop_proxy import __version__
from matlab_desktop_proxy.default_config import default_config

yaml = YAML()
# yaml.preserve_quotes = True


def read_yaml_file(file_path):
    with open(file_path) as f:
        file_content = f.readlines()
    return file_content


def filter_content(content):
    jinja_text = content[:2]
    yaml_text = content[2:]

    return jinja_text, yaml_text


def modify_python_version(yaml_content):
    fields = ["host", "run"]

    for field in fields:
        try:
            python_index = yaml_content["requirements"][field].index("python")
            yaml_content["requirements"][field][python_index] = "python >=3.6"
        except ValueError:
            pass

    return yaml_content


def modify_about_section(yaml_content):
    yaml_content["about"]["license_file"] = "../../LICENSE.md"
    yaml_content["about"]["doc_url"] = default_config["url"]
    yaml_content["about"]["dev_url"] = default_config["url"]

    return yaml_content


def modify_extra_section(yaml_content):
    yaml_content["extra"]["recipe-maintainers"] = ["prabhakk-mw", "diningPhilosopher64"]
    return yaml_content


def write_modified_yaml(jinja_text, yaml_content, yaml_file_path):
    with open(yaml_file_path, "w") as f:
        f.write("".join(jinja_text))
        f.write("\n")

    with open(yaml_file_path, "a") as f:
        yaml.dump(yaml_content, f)

    pass


if __name__ == "__main__":
    content = read_yaml_file("dummy-desktop-proxy/meta.yaml")
    jinja_text, yaml_text = filter_content(content)

    yaml_content = yaml.load("".join(yaml_text))
    yaml_content = modify_python_version(yaml_content)
    yaml_content = modify_about_section(yaml_content)
    yaml_content = modify_extra_section(yaml_content)

    yaml_file_path = "dummy-desktop-proxy/meta.yaml"
    write_modified_yaml(jinja_text, yaml_content, yaml_file_path)
