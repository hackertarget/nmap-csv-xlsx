## Nmap XML to CSV

There are many great projects and scripts around for generating Nmap reports from XML. With this script I needed a simple python script that I could easily customise the output **csv**.

Nmap XML has so much detailed information it is difficult to get an all in one reporting script that pulls everything you need for your reporting.

You may find this script useful as a template to extract any information you need into csv columns (each host on a row).

The default script extracts *open ports* only and shows **product** in the port column if found otherwise it shows **open**.

Also shows **ptr** for host and number of filtered ports (for an idea of firewall coverage).

    test@thematrix:~$ sudo nmap -F -sV -oX nmapresults 10.0.0.0/8
    test@thematrix:~$ python3 nmap-xml-to-csv.py nmapresults.xml

Here's why:
* Nmap Rocks.
* Security reporting is time consuming. Automate as much as you can.


### Built With

* [Python](https://python.org)
* [Nmap](https://nmap.org)
* [Nmap XML](https://nmap.org/book/output-formats-xml-output.html)

## CSV to XLSX

This script was built to build an XLSX document with multiple sheets for each Nmap port scanned range. However, it could be used to combine any csv's into an XLSX.

The example will combine test1, test2, test3 into a single xlsx (default.xlsx) with each csv on a sheet. Minor formatting changes have been applied.

    test@thematrix:~$ python3 csv-to-xlsx.py test1.csv test2.csv test3.csv

Here's why:
* Spreadsheets suck. Automate as much as you can.


### Built With

* [Python](https://python.org)
* [Python-Pandas](https://pandas.pydata.org/)

