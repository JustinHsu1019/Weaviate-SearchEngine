with open('Data/initial_data.txt', 'r', encoding='utf-8') as dataset, open('Data/output.txt', 'w', encoding='utf-8') as output:
    for line in dataset:
        if line.startswith('home.jsp?id=131&parentpath=0,2&mcustomize=multimessages_view.jsp&dataserno=') and line.endswith(''):
            output.write(line)
