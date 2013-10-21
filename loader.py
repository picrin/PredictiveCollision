import yaml
with open("controlled.log") as fileobject:
	for document in yaml.load_all(fileobject):
			print document

