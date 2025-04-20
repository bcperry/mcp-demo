# Connect to and query Azure SQL Database using Python and the pyodbc driver

This quickstart describes how to use MCP to connect an MCP Client to a database in Azure SQL Database and perform queries using Python and the [Python SQL Driver - pyodbc](/sql/connect/python/pyodbc/python-sql-driver-pyodbc). This quickstart follows the recommended passwordless approach to connect to the database. You can learn more about passwordless connections on the [passwordless hub](/azure/developer/intro/passwordless-overview).

## Prerequisites

* An [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=azurefreeaccountpython/).
* An Azure SQL database configured with Microsoft Entra authentication. You can create one using the [Create database quickstart](./single-database-create-quickstart.md).
* The latest version of the [Azure CLI](/cli/azure/get-started-with-azure-cli).
* Visual Studio Code with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
* Python 3.8 or later. If you're using a Linux client machine, see [Install the ODBC driver](/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?tabs=linux#install-the-odbc-driver).

## Configure the database

#TODO
## Create the application

1. AFter creating a virtual environment, install the  the requirements.

    ```console
    pip install -r requirements.txt
    ```

## Configure the local connection string

For local development and connecting to Azure SQL Database, add the following `AZURE_SQL_CONNECTIONSTRING` environment variable. Replace the `<database-server-name>` and `<database-name>` placeholders with your own values. Example environment variables are shown for the Bash shell.

Interactive authentication provides a passwordless option when you're running locally. This option is recommended because you don't have to store or manage authentication secrets on your local system.

## [Interactive Authentication](#tab/sql-inter)

In Windows, Microsoft Entra Interactive Authentication can use Microsoft Entra multifactor authentication technology to set up connection. In this mode, by providing the sign in ID, an Azure Authentication dialog is triggered and allows the user to input the password to complete the connection.

```Bash
export AZURE_SQL_CONNECTIONSTRING='Driver={ODBC Driver 18 for SQL Server};Server=tcp:<database-server-name>.database.windows.net,1433;Database=<database-name>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
```

For more information, see [Using Microsoft Entra ID with the ODBC Driver](/sql/connect/odbc/using-azure-active-directory). If you use this option, look for the window that prompts you for credentials.


## Run and test the app locally

The app is ready to be tested locally.

1. Run the `app.py` file in Visual Studio Code.

    ```console
    uvicorn app:app --reload
    ```

## Deploy to Azure App Service

The app is ready to be deployed to Azure.

1. Create a *start.sh* file so that gunicorn in Azure App Service can run uvicorn. The *start.sh* has one line:

    ```console
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
    ```

1. Use the [az webapp up](/cli/azure/webapp#az-webapp-up) to deploy the code to App Service. (You can use the option `-dryrun` to see what the command does without creating the resource.)

    ```azurecli
    az webapp up \
        --resource-group <resource-group-name> \
        --name <web-app-name>         
    ```

1. Use the [az webapp config set](/cli/azure/webapp/config#az-webapp-config-set) command to configure App Service to use the *start.sh* file.

    ```azurecli
    az webapp config set \
        --resource-group <resource-group-name> \
        --name <web-app-name> \
        --startup-file start.sh
    ```

1. Use the [az webapp identity assign](/cli/azure/webapp/identity#az-webapp-identity-assign) command to enable a system-assigned managed identity for the App Service.

    ```azurecli
    az webapp identity assign \
        --resource-group <resource-group-name> \
        --name <web-app-name>
    ```

    In this quickstart, a system-assigned managed identity is used for demonstration. A user-assigned managed identity is more efficient in a broader range of scenarios. For more information, see [Managed identity best practice recommendations](/azure/active-directory/managed-identities-azure-resources/managed-identity-best-practice-recommendations). For an example of using a user-assigned managed identity with pyodbc, see [Migrate a Python application to use passwordless connections with Azure SQL Database](./azure-sql-passwordless-migration-python.md).

## Connect the App Service to Azure SQL Database

In the [Configure the database](#configure-the-database) section, you configured networking and Microsoft Entra authentication for the Azure SQL database server. In this section, you complete the database configuration and configure the App Service with a connection string to access the database server.

To run these commands you can use any tool or IDE that can connect to Azure SQL Database, including [SQL Server Management Studio (SSMS)](/sql/ssms/download-sql-server-management-studio-ssms), [Azure Data Studio](/azure-data-studio/what-is-azure-data-studio), and Visual Studio Code with the [SQL server mssql](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) extension. As well, you can use the Azure portal as described in [Quickstart: Use the Azure portal query editor to query Azure SQL Database](/azure/azure-sql/database/connect-query-portal).

1. Add a user to the Azure SQL Database with SQL commands to create a user and role for passwordless access.

    ```sql
    CREATE USER [<web-app-name>] FROM EXTERNAL PROVIDER
    ALTER ROLE db_datareader ADD MEMBER [<web-app-name>]
    ALTER ROLE db_datawriter ADD MEMBER [<web-app-name>]
    ```

    For more information, see [Contained Database Users - Making Your Database Portable](/sql/relational-databases/security/contained-database-users-making-your-database-portable). For an example that shows the same principle but applied to Azure VM, see [Tutorial: Use a Windows VM system-assigned managed identity to access Azure SQL](/azure/active-directory/managed-identities-azure-resources/tutorial-windows-vm-access-sql). For more information about the roles assigned, see [Fixed-database Roles](/sql/relational-databases/security/authentication-access/database-level-roles#fixed-database-roles).

    If you disable and then enable the App Service system-assigned managed identity, then drop the user and recreate it. Run `DROP USER [<web-app-name>]` and rerun the `CREATE` and `ALTER` commands. To see users, use `SELECT * FROM sys.database_principals`.

1. Use the [az webapp config appsettings set](/cli/azure/webapp/config/appsettings#az-webapp-config-appsettings-set) command to add an app setting for the connection string.

    ```azurecli
    az webapp config appsettings set \
        --resource-group <resource-group-name> \
        --name <web-app-name> \
        --settings AZURE_SQL_CONNECTIONSTRING="<connection-string>"
    ```

    For the deployed app, the connection string should resemble:

    ```
    Driver={ODBC Driver 18 for SQL Server};Server=tcp:<database-server-name>.database.windows.net,1433;Database=<database-name>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30
    ```

    Fill in the `<database-server-name>` and `<database-name>` with your values.

    The passwordless connection string doesn't contain a user name or password. Instead, when the app runs in Azure, the code uses `DefaultAzureCredential` from the [Azure Identity library](/python/api/overview/azure/Identity-readme) to get a token to use with `pyodbc`.

## Test the deployed application

Browse to the URL of the app to test that the connection to Azure SQL Database is working. You can locate the URL of your app on the App Service overview page.

```http
https://<web-app-name>.azurewebsites.net
```

Append */docs* to the URL to see the Swagger UI and test the API methods.  

Congratulations! Your application is now connected to Azure SQL Database in both local and hosted environments.

## Related content

- [Migrate a Python application to use passwordless connections with Azure SQL Database](./azure-sql-passwordless-migration-python.md) - Shows user-assigned managed identity.
- [Passwordless connections for Azure services](/azure/developer/intro/passwordless-overview)
- [Managed identity best practice recommendations](/azure/active-directory/managed-identities-azure-resources/managed-identity-best-practice-recommendations)