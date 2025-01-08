import jinja2
import os


def render_makefile(template_dir, variables, output_dir):
    """
    Function to render the Makefile.j2 template and save it as Makefile in the specified output directory.
    """
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = 'Makefile.j2'  # Name of your Makefile template
    template = template_env.get_template(template_file)
    output_file_name = 'Makefile'  # The output file name
    output_path = os.path.join(output_dir, output_file_name)
    output = template.render(variables)
    with open(output_path, 'w') as file:
        file.write(output)
    print(f"Makefile generated at: {output_path}")


def render_json_template(template_path, variables, output_dir):
    """
    Special function to render the container-definition.json.j2 template
    and save it as {env}-container-definition.json in the terraform directory.
    """
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader)
    template_file = 'container-definition.json.j2'
    template = template_env.get_template(template_file)
    output_file_name = "container-definition.json"
    output_path = os.path.join(output_dir, output_file_name)
    output = template.render(variables)
    with open(output_path, 'w') as file:
        file.write(output)
    print(f"Container definition JSON generated at: {output_path}")


# Function to parse .tfvars file
def parse_tfvars(file_path):
    variables = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("[]").replace('"', '').split(", ")
                if len(value) == 1:
                    value = value[0]  # Convert single-item list to the value
                variables[key] = value
    return variables


# Function to render a Jinja template
def render_template(template_path, variables, output_path):
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(os.path.basename(template_path))
    output = template.render(variables)
    with open(output_path, 'w') as file:
        file.write(output)


# Main execution logic
if __name__ == "__main__":
    # Obtain the .tfvars file path from an environment variable
    tfvars_file = os.environ.get('TF_VARS_FILE')
    if not tfvars_file:
        raise ValueError("The TF_VARS_FILE environment variable is not set.")

    # Parse the .tfvars file
    variables = parse_tfvars(tfvars_file)

    # Directory containing your .tf.j2 and other .j2 template files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, '..', 'templates')

    # Define the output directory
    output_dir = os.path.join(script_dir, '..')
    os.makedirs(output_dir, exist_ok=True)

    # Render each .tf.j2 template
    for template_file in os.listdir(template_dir):
        if template_file.endswith('.tf.j2'):
            template_path = os.path.join(template_dir, template_file)
            output_file_name = template_file[:-3]  # Remove the '.j2' extension
            output_path = os.path.join(output_dir, output_file_name)
            render_template(template_path, variables, output_path)

    # Render the container-definition.json.j2 template
    container_def_template_path = os.path.join(template_dir, 'container-definition.json.j2')
    if os.path.exists(container_def_template_path):
        render_json_template(container_def_template_path, variables, output_dir)

    # Render the Makefile.j2 template
    # output_dir = os.path.dirname(script_dir)
    # render_makefile(template_dir, variables, script_dir)

    print("Templates rendered successfully.")
