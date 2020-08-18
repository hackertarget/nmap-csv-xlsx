# A simple script to quickly extract elements from Nmap XML and output as csv
#
# Modify as required to generate custom csv output
#

import json
import re
import sys
import xml.etree.ElementTree
e = xml.etree.ElementTree.parse(sys.argv[1]).getroot()


# natural sort function from stackoverflow
# https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


results = {}
open_ports = []

# iterate through each host
for host in e.findall('.//host'):
    ptr = ''

    # get host ipaddress
    ipaddress = host.find('address').attrib['addr']

    # get extraports (to show filtered / closed ports)
    try:
        extraports = host.find('.//ports/extraports').attrib['count']
        extraports = extraports + ' '
        extraports = extraports + host.find('ports/extraports').attrib['state']
    except:
        extraports = ''

    # get PTR for ipaddress
    for hostname in host.findall('.//hostname'):
        if hostname.attrib['type'] == 'PTR':
            ptr = hostname.attrib['name']

    # cycle through open ports only - add to 'results' dictionary
    for port_tmp in host.findall('.//port'):
        if port_tmp.find('state').attrib['state'] == 'open':
            if ipaddress not in results.keys():
                results.update({ipaddress : { 'ports' : {}}})
            protocol = port_tmp.attrib['protocol']
            port = protocol + port_tmp.attrib['portid']
            open_ports.append(port)
            if port_tmp.find('service').attrib['name']:
                if 'product' in port_tmp.find('service').attrib:
                    service = port_tmp.find('service').attrib['product']
                    if 'version' in port_tmp.find('service').attrib:
                        service = '%s %s' % (service, port_tmp.find('service').attrib['version'])
                else:
                    service = 'open'
            else:
                service = 'open'
            results[ipaddress]['ports'].update({ port : service })

    # if host has open ports - add PTR and extraports to 'results' dict
    if ipaddress in results.keys():
        results[ipaddress].update({ 'extraports' : extraports, 'PTR' : ptr })


# results = { '7.7.7.7' : { 
#                            {'ports' : 
#                                 {'tcp80' : 'Apache', 
#                                  'tcp443' : 'open'},
#                            {'PTR' : 'rdns.example.com'},
#                            {'extraports' : '65530 filtered'}
#                         }
#           }

# ports = [ list of ports for columns ]
# ports get sorted using natural ordering - eg. ['tcp21', 'tcp111']

ports = list(set(open_ports))
ports = sorted(ports, key=natural_keys)

# print head of csv
head = []
head.append('ipaddress')
head.append('PTR')
head.append('Other Ports')
for port in ports:
    head.append(port)
print(','.join(head)) 

# cycle through results to print each host as a row
for ip in results:
    row = [ip, results[ip]['PTR'], results[ip]['extraports']] 
    for port in ports:
        if port in results[ip]['ports'].keys():
            row.append(results[ip]['ports'][port])
        else:
            row.append('')
    print(','.join(row))
