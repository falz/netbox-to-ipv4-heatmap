#! /usr/bin/env python3
#	wopat wiscnet 2021-10
# 
# description:
#	Take a prefix from netbox, spit out output useable by ipv4-heatmap, which is at minimum one IP per line.
#	cannot use Netbox Export Template from this because ipv4-heatmap doesn't support prefixes, just IPs
#
# 	https://github.com/measurement-factory/ipv4-heatmap
#	http://maps.measurement-factory.com/
#
# dependencies:
#	yum install python3-pip
#	python3 -m pip install argparse pynetbox
#
# changelog:
#	2021-10-04	initial release
#	2021-11-13	cli arg parse for prefix
#
# usage:
#
#	create a txt file that ipv4-heatmap likes
#		./netbox-to-ipv4-heatmap.py -p 192.168.0.0/16 >/tmp/192.168.0.0-16.txt
#
#	generate a heatmap. tweak -A and -B to your liking.
#		./ipv4-heatmap -A 128 -B 8192 -y 192.168.0.0/16 -z 0 -o 192.168.png < /tmp/192.168.0.0-16.txt
#


from netaddr import *
import argparse
import pynetbox

##############################
# CONFIG
config = {}
config['netbox_url']		=	"https://netbox.example.com/"
config['netbox_api_token']	=	""


##############################
## FUNCTIONS

def parse_cli_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--prefix', required=True, help='Prefix to search for in Netbox. ie 10.0.0.0/8')
	args = vars(parser.parse_args())
	return(args)


def get_netbox_prefixes(config, prefix):
	#print("# Getting Netbox Prefixes..")
	nb = pynetbox.api(config['netbox_url'], config['netbox_api_token'])

	# 'within' should be same as https://netbox.example.com/api/ipam/prefixes/?within=10.10.0.0/8
	try:
		nb_ips = nb.ipam.prefixes.filter(within=prefix)
		return(nb_ips)
	except pynetbox.ContentError as e:
		print("Cannot connect to Netbox:", end='')
		print(e.error)
	except pynetbox.RequestError as e:
		print("Cannot connect to Netbox:", end='')
		print(e.error)
	except pynetbox.AllocationError as e:
		print("Cannot connect to Netbox:", end='')
		print(e.error)
	return(False)


def expand_ip_list(config, netbox_prefixes):
	ip_list = []

	# list will be of ipnetwork objects, not strings.
	for nb_prefix in netbox_prefixes:
		prefix_ipnetwork = IPNetwork(str(nb_prefix))

		nb_prefix_list = list(prefix_ipnetwork)
		nb_prefix_list_len = len(nb_prefix_list)

		for p in nb_prefix_list:
			#ip_list.append(p)
			print(str(p), nb_prefix_list_len)

	return(ip_list)


##############################
## MAIN

if __name__ == "__main__":
	args = parse_cli_args()
	prefix = args['prefix']

	netbox_prefixes = get_netbox_prefixes(config, prefix)

	if len(netbox_prefixes) > 0:
		#print("# Got", len(netbox_prefixes), "prefixes")
		ip_list = expand_ip_list(config, netbox_prefixes)
	else:
		print("No prefixes found within", prefix)

