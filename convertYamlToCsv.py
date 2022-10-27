import os
from types import SimpleNamespace

from yamlpath.common import Parsers
from yamlpath.wrappers import ConsolePrinter
from yamlpath import Processor
from yamlpath import YAMLPath
from yamlpath.exceptions import YAMLPathException
import csv

logging_args = SimpleNamespace(quiet=False, verbose=True, debug=False)
log = ConsolePrinter(logging_args)
yaml = Parsers.get_yaml_editor()


def parse(yaml_file, output_path, path_array):
	(yaml_data, doc_loaded) = Parsers.get_yaml_data(yaml, log, yaml_file)
	if not doc_loaded:
		# There was an issue loading the file; an error message has already been
		# printed via ConsolePrinter.
		exit(1)
	processor = Processor(log, yaml_data)
	parent_path = "items.kind"
	node_gen = processor.get_nodes(parent_path, mustexist=True)

	item_len = get_length(node_gen)
	table = []

	log.info("====> item_len: {}".format(item_len))
	for i in range(item_len):
		row = []
		for path in path_array:
			yaml_path = YAMLPath(("items[{}]." + path).format(i))
			row.append(find_value(processor, yaml_path))
		table.append(row)
	write_output(output_path, table)


def find_value(processor, yaml_path):
	try:
		for val in processor.get_nodes(yaml_path, mustexist=False):
			log.info("Got {} from '{}'.".format(val, yaml_path))
			if val.node is None:
				val = ""
			return val
			# Do something with each node_coordinate.node (the actual data)
	except YAMLPathException as ex:
		# If merely retrieving data, this exception may be deemed non-critical
		# unless your later code absolutely depends upon a result.
		log.error(ex)
		return "ERROR"


def get_length(node_gen):
	return len(list(node_gen))


def write_output(output_path, table):
	with open(output_path, mode='w', newline='', encoding='utf-8-sig') as output:
		writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerows(table)


yaml_path_deployment = [
	"kind", "metadata.name",
	"spec.template.spec.containers.resources.limits.cpu",
	"spec.template.spec.containers.resources.limits.memory",
	"spec.template.spec.containers.image",
	"spec.template.spec.containers[.=ports].ports.containerPort",
	"spec.template.spec.containers[.=readinessProbe].readinessProbe.httpGet",
	"spec.template.spec.containers[.=livenessProbe].livenessProbe.httpGet",
	"spec.template.spec.volumes[.=configMap].configMap.name",
	"spec.template.spec.volumes[.=persistentVolumeClaim].persistentVolumeClaim.claimName",
]

yaml_path_pv = [
	"kind", "metadata.name"
]

yaml_path_secret = [
	"kind", "metadata.name", "type"
]

yaml_path_configmap = [
	"kind", "metadata.name"
]

yaml_path_service = [
	"kind", "metadata.name", "spec.type",
	"spec.ports[.=port].port",
	"spec.ports[.=targetPort].targetPort",
	"spec.ports[.=nodePort].nodePort",
]

if __name__ == '__main__':
	parse("input/deployment.yaml", "output/deployment.csv", yaml_path_deployment)
	parse("input/pv.yaml", "output/pv.csv", yaml_path_pv)
	parse("input/secret.yaml", "output/secret.csv", yaml_path_secret)
	parse("input/configmap.yaml", "output/configmap.csv", yaml_path_configmap)
	parse("input/service.yaml", "output/service.csv", yaml_path_service)
	# parse("input/test.yaml", "output/test.csv", yaml_path_deployment)

