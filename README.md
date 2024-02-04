*How to use:*  
  
describe your software specification in natural lange under the key "content" of role "user":  

`
name: 'sort_numbers'  
messages:  
- role: system  
  content: You are a helpful assistant.  
- role: user  
  content: 'Can you provide me with a python script to sort a list of numbers.'  
`

The system will create the implementation and a suggestion for a unit test under the folder specified by the key "name"  
The name of the module and the function containing the implementation will also be called by that name (if the AI gets that point right)  
The input.yaml will be stored in the same folder once the code is executed, and then it will be reset to initial values.  

After setting up the virtual environment, start with:  
python main.py  
