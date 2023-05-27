import os
import click
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

class Cli:
  def __init__(self):
    pass

  def create_directories(self):
    this_dir = Path(__file__).parent.parent

    src_path = str(this_dir / 'src')
    inc_path = str(this_dir / 'inc')
    build_path = str(this_dir / 'build')
    vscode_path = str(this_dir / '.vscode')

    for _dir in [src_path, inc_path, build_path, vscode_path]:
      if not os.path.exists(_dir):
        os.makedirs(_dir)

  def write_config_files(self, project, program):
    click.echo(f'project: {project}')
    click.echo(f'program: {program}')
    template_path = (Path(__file__).parent / ".." / ".templates").resolve()
    project_root = (Path(__file__).parent / ".." ).resolve()

    cmake_list_txt_template = template_path / 'CMakeLists.txt.j2'
    launch_json_template = template_path / 'launch.json.j2'
    tasks_json_template = template_path / 'tasks.json.j2'
    c_cpp_properties_template = template_path / 'c_cpp_properties.json.j2'

    c_template = template_path / 'c_file.c.j2'
    h_template = template_path / 'h_file.h.j2'

    assert cmake_list_txt_template.exists()
    assert launch_json_template.exists()
    assert tasks_json_template.exists()

    cmake_lists_text = project_root / 'CMakeLists.txt'
    launch_json = project_root / '.vscode' / 'launch.json'
    tasks_json = project_root / '.vscode' / 'tasks.json'
    c_cpp_properties = project_root / '.vscode' / 'c_cpp_properties.json'
    program_c_path = project_root / 'src' / f"{program}.c"
    program_h_path = project_root / 'inc' / f"{program}.h"

    data = {'project' : project, 'program' : program }

    for template_path, output_file_path in [
        [c_template, program_c_path],
        [h_template, program_h_path],
        [cmake_list_txt_template, cmake_lists_text],
        [c_cpp_properties_template, c_cpp_properties],
        [launch_json_template, launch_json],
        [tasks_json_template, tasks_json]]:
      env = Environment(
        loader=FileSystemLoader([str(template_path.parent)]),
        trim_blocks=True,
        lstrip_blocks=True
      )
      template = env.get_template(str(template_path.name))
      output_string = template.render(**data)
      with open(output_file_path, "w") as fp:
        fp.write(output_string)

cli_ctx = click.make_pass_decorator(Cli, ensure=True)

@click.command()
@click.option("--project", default=None, help="Set the project name")
@click.option("-p", "--program", default=None, help="Set the program name")
@cli_ctx
def cli(ctx, project=None, program=None):
  this_dir = Path(__file__).parent.parent

  if project is None:
    project = this_dir.name
  if program is None:
    program = project

  ctx.create_directories()
  ctx.write_config_files(project, program)
