## Description

Manage virtual machine of Azure

Compile the file config.json

```<language>
{
  "subscriptions": [
    {
      "name": "my_name_alias_subscription",
      "subscription": {
        "subscription_id": "",
        "client_id": "",
        "secret": "",
        "tenant": ""
      }
    }
  ]
}
```
In <b>name</b> you can set an alias for a subscription while in subscription you compile the properties <b>subscription_id, client_id,secret</b> and <b>tenant</b> following the help in this [link](https://docs.microsoft.com/it-it/azure/azure-resource-manager/resource-group-create-service-principal-portal)




## Syntax

- azure_manage.py -h
- azure_manage.py -o (start|stop|deallocate|restart) -n my_name_alias_subscription -v name_vm -g group_name


If you have a proxy for connection you can set the variable PROXY in the script

For example:

```<language>
    PROXIES = {
      "http": "http://10.10.1.10:3128",
      "https": "http://10.10.1.10:1080",
    }
```

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Anyone and everyone is welcome to contribute.




