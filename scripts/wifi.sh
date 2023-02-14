#!/usr/bin/env bash

# Flags:
# -s  SSID 
# -p  Password
# -ap Access Point mode

Help()
{
   echo "Raspberry PI 4B WiFi Setup script."
   echo
   echo "usage: bash wifi.sh [-s] \"SSID\" [-p] \"PASSWORD\" [-a] [value] [-c] [value] [-h]"
   echo "options:"
   echo " s     WiFi SSID"
   echo " p     WiFi Password"
   echo " a     Access Point mode. Default SSID and password: Turtlebot4"
   echo " c     Send WiFi credentials to Create 3."
   echo " r     Regulatory domain. Default CA"
   echo " h     Print this help statement"
   echo
}

ap=0;
create3=0;

while getopts "s:p:cr:ha" flag
do
    case "${flag}" in
        s) ssid=${OPTARG};;
        p) password=${OPTARG};;
        a) ap=1;;
        c) create3=1;;
        r) domain=${OPTARG};;
        h)
            Help
            exit;;
        \?)
            echo "Error: Invalid flag"
            exit;;
    esac
done

# AP mode
if [ $ap -eq 1 ]
then
    if [ -z "$ssid" ] && [ -z "$password" ]
    then
        ssid="Turtlebot4";
        password="Turtlebot4";
    fi
else
    if [ -z "$ssid" ]
    then
        echo "Invalid ssid";
        Help
        exit 1
    fi
fi

# Comment out AP mode if not using
if [ $ap -eq 0 ]
then
    ap_comment="#";
else
    ap_comment="";
fi

if [ -z $domain ]
then 
    domain="CA";
fi

echo "SSID: $ssid";
echo "Password: $password";
echo "AP mode: $ap";
echo "Domain: $domain";
read -p "Press enter to apply these settings."

# Create netplan .yaml file
echo -e "network: \n\
    version: 2 \n\
    ethernets: \n\
        eth0: \n\
            dhcp4: true \n\
            optional: true \n\
            addresses: [192.168.185.3/24] \n\
        usb0: \n\
            dhcp4: false \n\
            optional: true \n\
            addresses: [192.168.186.3/24] \n\
    version: 2 \n\
    wifis: \n\
        renderer: NetworkManager \n\
        wlan0: \n\
            optional: true \n\
            access-points: \n\
                "$ssid": \n\
                    password: "$password" \n\
                   $ap_comment mode: ap \n\
                   $ap_comment band: 5GHz \n\
            dhcp4: true\n" | sudo tee /etc/netplan/50-cloud-init.yaml

# Add regulatory domain

#If reg domain already exists, replace it
if grep -Fq "REGDOMAIN=" /etc/default/crda 
then
    sudo sed -i "s/REGDOMAIN=.*/REGDOMAIN=$domain/g" /etc/default/crda
else
    echo "REGDOMAIN=$domain" | sudo tee -a /etc/default/crda
fi


#If country domain already exists, replace it
if grep -Fq "COUNTRY=" /etc/environment 
then
    sudo sed -i "s/COUNTRY=.*/COUNTRY=$domain/g" /etc/environment
else
    echo "COUNTRY=$domain" | sudo tee -a /etc/environment
fi

create3_domain=ETSI;

case $domain in
    AS|CA|FM|GU|KY|MP|PR|TW|UM|US|VI)
    create3_domain=FCC
    ;;

    JP|JP3)
    create3_domain=Japan
    ;;
esac

if [ $create3 -eq 1 ]
then
    curl -X POST -d "ssids=$ssid&pass=$password&countryids=$create3_domain" "http://192.168.186.2/wifi-action-change"
fi

sudo netplan generate
sudo netplan apply
