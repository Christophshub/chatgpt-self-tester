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

def prune_from_python_encapsulation(code_content):
    start_pattern = "```python\n"
    end_pattern = "```"
    start_idx = code_content.find(start_pattern)
    end_idx = code_content.rfind(end_pattern)
    if start_idx != -1 and end_idx != -1:
        code_content = code_content[start_idx + len(start_pattern):end_idx]
    # other variant seen:
    start_pattern = "```Python"
    end_pattern = "```"
    start_idx = code_content.find(start_pattern)
    end_idx = code_content.rfind(end_pattern)
    if start_idx != -1 and end_idx != -1:
        code_content = code_content[start_idx + len(start_pattern):end_idx]    
    return code_content

def create_files(folder_name, file_name, prompt):
    code = generate_code_with_openai(prompt)
    code_content = code.content
    separator_pattern = "-----"
    start_idx = code_content.find(separator_pattern)
    if start_idx != -1:
        code_content_1 = code_content[:start_idx]
        code_content_1 = prune_from_python_encapsulation(code_content_1)
        with open(f"{folder_name}/{file_name}.py", 'w') as file:
            file.write(str(code_content_1))
        code_content_2 =  code_content[start_idx + len(separator_pattern):]
        code_content_2 = prune_from_python_encapsulation(code_content_2)
        with open(f"{folder_name}/test_{file_name}.py", 'w') as file:
            file.write(str(code_content_2))
    else:
        raise Exception("separator not found!")
    
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
            msg_content_copy = msg['content']
            msg['content'] += " The following additional requirements obtain: I want the implementation of the requirement and a unit test for it two separate sections of the answer."
            msg['content'] += " The sections should be separated by -----."
            msg['content'] += " I should be able to save each of the two sections into a separate python file. The unit test should import the module and the function to be tested"
            msg['content'] += f" like this: from {name} import {name}. And most importantly, in your answer there should be no additional text whatsoever, only code that can be"
            msg['content'] += " executed by python, except from the separator -----."

        messages.append({"role": msg['role'], "content": msg['content']})
    
    print("will prompt the api with this requirement (messages): ", messages)
    create_files(folder_name, name, messages)

    # Clear the YAML for the next run
    clear_yaml(yaml_content)
    update_yaml(yaml_path, yaml_content)
    
    print(f"Files {name}.py and test_{name}.py have been created under {folder_name}/.")
    print(f"The YAML file {yaml_path} has been reset for the next run.")
    print(f"Copy of input.yaml has been saved in {folder_name}/.")


if __name__ == "__main__":
    main()
