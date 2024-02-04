**How to use:**  
  
describe your software specification in natural language under the key "content" of role "user":  

```
name: 'sort_numbers'  
messages:  
- role: system  
  content: You are a helpful assistant.  
- role: user  
  content: 'Please provide me with a python script to sort a list of numbers.'  
```

The system will create the implementation and a suggestion for a unit test under the folder specified by the key "name". 
The module and the function containing the implementation will also be designated by that name (if the AI gets that point right). 
A copy of the input.yaml will also be stored in that folder once the code is executed, and then the original one will be reset to some initial values.  

After setting up the virtual environment, start with: 
```
python main.py
```
and inspect the results in the generated folder.
Execute the unit tests with:  
```
pytest
```

**remark**: use
```  
python main`_v2.py
```  
for slightly less flaky results. It lets the AI create the functional implementation and the unit test
in a single query.   
(At least the module import for the existing function to be tested by the testing-module works better like this; but especially
the tests for equality after numpy.NaN replacement are poor, since it fucks up the data types - float vs integer - almost all the time.)