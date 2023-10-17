#!/bin/sh
SUBSCRIPTION_ID="1159a8c6-7145-481b-8414-3ab21108ca60"
RESOURCE_GROUP="sicop"
CLUSTER_NAME="sicop"
az account set --subscription ${SUBSCRIPTION_ID}
az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${CLUSTER_NAME}