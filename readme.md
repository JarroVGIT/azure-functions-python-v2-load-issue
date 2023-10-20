# Azure Functions - Python V2 loading issue
There is an issue with Azure Functions when using Ptyhon V2 model, that is extremely hard to debug. Depending on where you are in your search, it might present itself as:
- The FunctionApp is successfully deployed, but the Function itself doesn't show up in the Portal, or
- You see in Application Insights that 1 Function was found, 0 were loaded, or
- The FunctionApp is successfully deployed, but your HTTP triggered function can not be reached. 

There are numerous examples on this issue, both on StackOverflow as on Github, for example [here](https://github.com/Azure/azure-functions-python-worker/issues/1262).

## A possible cause and solution
I found that whenever an exception is unhandled when loading your Function files (not yet executing), the Azure Runtime doesn't log that exception but rather just not load that specifc function. That is, if your code raises exceptions outside the scope of a Python function or class, you will never know. 

If you ran around the internet and found fellow sufferers on this issue, then you also know what most did to fix this. I've seen advice as _'make sure your imports are moved to inside your Function'_ and _'there cannot be any code between your imports and your `app=func.FunctionApp()` statement'_. That actually got me on the right track but is not a long term solution. The solution is to make sure you handle exceptions properly. Mistakes are easily made, just a few examples:
- You build your Function on Windows, perform a zip-deploy to Linux, and import a package that was specifically built for Windows.
- You want to get an App Setting as environment variable and set it as a constant, but the App Setting doesn't exist. 
- You created modules to neatly organize your code, but your import is off.

## Is this really true?
Yes. To demonstrate I've created this repo. To recreate this problem, do the following (replace $RESOUCEGROUP_NAME and $LOCATION with your own):
1. Clone this repo.
2. Create an resource group with `az group create -n $RESOURCEGROUP_NAME -l $LOCATION`
3. Deploy the FunctionApp and Application Insights with `az deployment group create -g $RESOURCEGROUP_NAME -f ./bicep/infra.bicep -p location=$LOCATION`
4. Deploy the FunctionApp code with `cd functionapp` and then `func azure functionapp publish <name of your functionapp>` 
5. Make sure the endpoints work (endpoints `normal_bp`, `properly_handled` and `from_root`)

The output of the above should end in
```
Remote build succeeded!
[2023-10-20T02:18:04.556Z] Syncing triggers...
Functions in funcappfuncv2issue7mg5dpbtq:
    func1 - [httpTrigger]
        Invoke url: https://funcappfuncv2issue7mg5dpbtq.azurewebsites.net/api/normal_bp

    func4 - [httpTrigger]
        Invoke url: https://funcappfuncv2issue7mg5dpbtq.azurewebsites.net/api/properly_handled

    main - [httpTrigger]
        Invoke url: https://funcappfuncv2issue7mg5dpbtq.azurewebsites.net/api/from_root
```

## Creating the eronous situation
So far, so good. Now on to the issues; try to uncomment line 22-23 or line 25-26 in `function_app.py`. This will either import a blueprint that is trying to access an non-existing package or a non-existing environment variable. Then, redeploy the function app with the `publish` command from step 4 above.

Now, the output of the `func` command will be more like:
```
Remote build succeeded!
[2023-10-20T02:23:08.811Z] Syncing triggers...
Functions in funcappfuncv2issue7mg5dpbtq:
(.venv) jarro@Jarros-MBP functionapp % 
```
If you go into Application Insights, you will a record in the `traces` table with something like 'Initializing function HTTP routes No HTTP routes mapped'.

## Conclusion
This illustrates situations that causes Functions to not appear in the Azure Portal. It can drive you nuts and it shouldn't. One might think this is all user-error and to some degree I would agree. However, it is hard to debug if you don't have the actual error causing this issue, especially if everything works great locally. 