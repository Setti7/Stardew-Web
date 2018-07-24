#!/bin/bash

#Settings constants
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# Updating
printf "${BLUE}Updating repositories\n"
apt-get update

if [ $? -eq 0 ]; then
    printf "${GREEN}Updated repositories\n"
else
    printf "${RED}Failed updating repositories\n"
    return 0
fi


# Upgrading
printf "${BLUE}Upgrading\n"
apt-get upgrade -y

if [ $? -eq 0 ]; then
    printf "${GREEN}Upgraded\n"
else
    printf "${RED}Failed upgrading\n"
    return 0
fi


# Installing postgres and its dependencies
printf "${BLUE}Installing postgres and its dependencies\n"
apt-get install postgresql postgresql-contrib -y

if [ $? -eq 0 ]; then
    printf "${GREEN}Installed Postgres\n"
else
    printf "${RED}Failed installing Postgres\n"
    return 0
fi


# Installing apache2 and its dependencies
printf "${BLUE}Installing apache2 and its dependencies\n"
apt-get install python3-pip apache2 libapache2-mod-wsgi-py3 -y

if [ $? -eq 0 ]; then
    printf "${GREEN}Installed Apache2\n"
else
    printf "${RED}Failed installing Apache2\n"
    return 0
fi


# Setting apache2 firewall
printf "${BLUE}Setting apache2 firewall\n"
ufw allow 'Apache Full'

if [ $? -eq 0 ]; then
    printf "${GREEN}Firewall set for Apache2\n"
else
    printf "${RED}Failed setting firewall for Apache2\n"
    return 0
fi


# Creating databases and admin user
printf "${BLUE}Creating databases and admin user\n"
su - postgres
createuser admin
createdb Stardew_Web_DB

if [ $? -eq 0 ]; then
    printf "${GREEN}Done\n"
    printf "${NC}Please run this commands inside psql:\n"
    printf "alter user admin with encrypted password 'SenhaDataBase77';\n"
    printf "grant all privileges on database \"Stardew_Web_DB\" to admin;\n"
else
    printf "${RED}Failed creting users or database\n"
    return 0
fi
