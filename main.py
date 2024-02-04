import yaml, shutil
from pathlib import Path

from openai import OpenAI
client = OpenAI()

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def update_yaml(file_path, data):
    # Reorder the data dictionary to ensure 'name' comes first
    reordered_data = {'name': data['name'], 'messages': data['messages']}
    
    with open(file_path, 'w') as file:
        yaml.safe_dump(reordered_data, file, sort_keys=False, default_flow_style=False, indent=2)

def create_folder(folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    return folder_name


def clear_yaml(yaml_content):
    yaml_content['name'] = ""
    for message in yaml_content['messages']:
        if message['role'] == 'user':
            message['content'] = "<add specifications here>"
            #for i in range(1, 6):  # Assuming there are 5 constraints
            #    message[f'constraint_{i}'] = ""

def copy_yaml_to_folder(source_path, folder_name):
    destination_path = f"{folder_name}/{Path(source_path).name}"
    shutil.copy(source_path, destination_path)

def create_specified_function(folder_name, file_name, prompt):
    code = generate_code_with_openai(prompt)
    code_content = code.content
    start_pattern = "```python\n"
    end_pattern = "```"
    start_idx = code_content.find(start_pattern)
    end_idx = code_content.rfind(end_pattern)
    if start_idx != -1 and end_idx != -1:
        code_content =  code_content[start_idx + len(start_pattern):end_idx]
    with open(f"{folder_name}/{file_name}.py", 'w') as file:
        file.write(str(code_content))

def create_unit_test(folder_name, file_name, test_prompt):
    test_code = generate_code_with_openai(test_prompt)
    test_code_content = test_code.content
    start_pattern = "```python\n"
    end_pattern = "```"
    start_idx = test_code_content.find(start_pattern)
    end_idx = test_code_content.rfind(end_pattern)
    if start_idx != -1 and end_idx != -1:
        test_code_content =  test_code_content[start_idx + len(start_pattern):end_idx]
    with open(f"{folder_name}/test_{file_name}.py", 'w') as file:
        file.write(str(test_code_content))

def generate_code_with_openai(prompt):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=prompt
    )
    try:
        # Accessing the first choice's text attribute directly, if completion.choices[0] is a ChatCompletionMessage object
        return completion.choices[0].message
    except AttributeError as e:
        # Fallback or error handling code here, e.g., logging the error
        print(f"Error accessing the completion text: {e}")
    return completion.choices[0].message

def main():
    yaml_path = 'input.yaml'
    yaml_content = read_yaml(yaml_path)
    name = yaml_content['name']
    folder_name = create_folder(name)
    
    # Copy the input.yaml to the new folder
    copy_yaml_to_folder(yaml_path, folder_name)
    
    # Process the messages to incorporate constraints into the user's message content
    messages = []
    for msg in yaml_content['messages']:
        if msg['role'] == 'user':

            # Add constraints to the user's message if they are not empty
            #constraints = [yaml_content[key] for key in ['constraint_1', 'constraint_2', 'constraint_3', 'constraint_4', 'constraint_5'] if yaml_content[key]]
            #msg['content'] += ' ' + ' '.join(constraints).strip()

            msg['content'] += " Important constraint No. 1: the method should be testtable with a pytest unit test, but the unit test should not be part of your answer."
            msg['content'] += f" Important constraint No. 2: the method of the testable method should be called '{name}'."
            msg['content'] += " Important constraint No. 3: I only want the pure python script in your answer, not any explanatory text."

        messages.append({"role": msg['role'], "content": msg['content']})
    
    print("will prompt the api with this requirement (messages): ", messages)
    create_specified_function(folder_name, name, messages)

    message_test = []
    message_test_prefix = """Can you please create a unit test with pytest and add a fixture to the test-method so that the test 
    is immediately executable with the pytest command, for the following functional specification: """
    for msg in yaml_content['messages']:
        if msg['role'] == 'user':

            # Add constraints to the user's message if they are not empty
            #constraints = [yaml_content[key] for key in ['constraint_1', 'constraint_2', 'constraint_3', 'constraint_4', 'constraint_5'] if yaml_content[key]]
            #msg['content'] += ' ' + ' '.join(constraints).strip()

            msg['content'] += " Important constraint No. 1: the method of the exiting method to be tested is called '{name}', and '{name}' is also the name of the module that contains the method."
            msg['content'] += " Important constraint No. 2: I only want the PURE PYTHON CODE for the unit test in your answer, not any additional explanatory text."

        message_test.append({"role": msg['role'], "content": message_test_prefix + msg['content']})
    
    print("will prompt the api with this requirement for a unit test: ", message_test)
    create_unit_test(folder_name, name, message_test)
    
    # Clear the YAML for the next run
    clear_yaml(yaml_content)
    update_yaml(yaml_path, yaml_content)
    
    print(f"Files {name}.py and test_{name}.py have been created under {folder_name}/.")
    print(f"The YAML file {yaml_path} has been reset for the next run.")
    print(f"Copy of input.yaml has been saved in {folder_name}/.")


if __name__ == "__main__":
    main()
