# netbox-to-ipv4-heatmap
Generate iplist file from Netbox for use with [ipv4-heatmap](https://github.com/measurement-factory/ipv4-heatmap) project will which "Generate Hilbert curve heatmaps of the IPv4 address space."


# Using

```
./netbox-to-ipv4-heatmap.py  --help
usage: netbox-to-ipv4-heatmap.py [-h] -p PREFIX

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Prefix to search for in Netbox. ie 10.0.0.0/8
```

# Example
Create 'iplist' file from netbox:
```
./netbox-to-ipv4-heatmap.py -p 192.168.0.0/16 >/tmp/192.168.0.0-16.txt
```

Generate image using `ipv4-heatmap` and the iplist file:
```
./ipv4-heatmap -A 128 -B 8192 -y 192.168.0.0/16 -z 0 -o 192.168.png < /tmp/192.168.0.0-16.txt
```

Consider tweaking `-A` and `-B` values.

Example output from four different /16's:

![2](https://github.com/falz/netbox-to-ipv4-heatmap/assets/707319/90ce0587-e021-4a40-81d6-a7799b1dd91c)
![1](https://github.com/falz/netbox-to-ipv4-heatmap/assets/707319/d6db69f7-acb5-47a8-9b84-0020277e2986)
![4](https://github.com/falz/netbox-to-ipv4-heatmap/assets/707319/4080b27b-4f43-47a1-95e1-c29d9dac7ce2)
![3](https://github.com/falz/netbox-to-ipv4-heatmap/assets/707319/affa0369-a6d0-4f7f-950d-24ebd4169f8c)
