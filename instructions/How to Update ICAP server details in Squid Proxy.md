## How to Update ICAP server details in Squid Proxy

In order to update ICAP server details in Squid Proxy you will need to have Access to Squid Proxy Machine. ( You can get that by requesting someone to add your SSH Public Key to Squid Proxy machine)

### How to Add Public SSH Key to Machine in order to Get Access
** step to follow on user machine who require access to squid proxy machine.

Use below command to obtain SSH key if you require new set pair

```shell
ssh-keygen
```
Navigate to .ssh folder under User folder if you are windows user.

Open the id_rsa.pub file using notepad and copy the contain from that file

** step to follow on squid Machine

run below command
```shell
nano ~/.ssh/authorized_keys
```
Paste the Public key in new line and Press CTRL + X
Type Y and Enter to save the file.

Once is done the new user got access to the Squid Machine

### How to Update ICAP Server Details
Note - The Current Setup only Support ICAP server IP address

In order to get IP address for ICAP Server if you are not aware please run below command
```shell
dig +short <icap server url>
```
Copy the ICAP server IP Address

Step 1 - Run below command to edit config
```shell
sudo nano /etc/squid/squid.conf
```
Step 2 - Replace the ICAP URL with New IP address

Step 3 - Press CTRL + X and Type Y and enter to save the new config

Step 4 -Run Below Command to apply new config
```shell
sudo squid -k reconfigure 
```
You have manage to now successfully change ICAP server URL in Squid Proxy.