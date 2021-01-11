
## Download Packer binary 

Run following command to download packer binary
```shell
wget https://releases.hashicorp.com/packer/1.5.6/packer_1.5.6_linux_amd64.zip -O packer.zip
```

We now need to unzip the compressed file:
```shell
unzip packer.zip
```
Then we need to move the resulting binary to the appropriate place, which can be /usr/bin/, to share across users or anywhere within the desired users' $PATH settings.
```shell
sudo mv packer /usr/bin/
```
That's it! We can confirm that Packer is working and see a command list with this:
```shell
packer --help
```