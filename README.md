# Zayokmz

install heidSQL
install python 3.9.1
install notepad++ 64 bit
install 7Z 64 bit


setup python paths

python -m pip install --upgrade pip
pip install mysql-connector-python
pip install elementpath
pip install prettify
pip install --upgrade lxml
pip install simple_salesforce


network 6461
Name   Zayo
Query SELECT count(*) FROM correlation_data.m6_circuit c WHERE exchange_carrier_circuit_id Like '701%/1%G%' 
color green
genarate yes

network 7385
Name   ELI
Query SELECT count(*) FROM correlation_data.m6_circuit c WHERE exchange_carrier_circuit_id Like '702%/1%G%' 
color red
genarate yes


