from parse import parse

name = "/hello/{name}"
names = "/hello/fazliddin"
result = parse(name, names)
print(result)