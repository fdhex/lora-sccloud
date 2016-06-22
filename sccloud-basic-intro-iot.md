# Deploy your own app on CF - a short intro

Further documentation can be found at the following address: https://docs.developer.swisscom.com/

## AppCloud Account

Confirm your account on the Swisscom Cloud, click on the links you received in the invitation emails. You need to accept the invitations again by going to developer.swisscom.com, clicking on the bell in the top right part of the screen, click on each of the two messages (organization invite and space invite) which appear and validate each one.

## Create a service

Create a service using the web ui: Click on "Create Service", select MongoDB, enter a service name and choose the Small plan.

## Download the CF CLI

Download the package for your OS here: https://github.com/cloudfoundry/cli#downloads

Install the CLI.

## Download the sources of the app

Clone with git or download the zip of the app sources here: https://github.com/fdhex/lora-sccloud. Unzip the sources if you downloaded the zip.

This is a simple python webapp which accepts POST requests on /lora, stores the body of the request in a MongoDB instance, and displays the latest stored value when doing a GET on /lora

You know need to deploy this app on the Swisscom Cloud.

Customize the manifest.yml. This is the file which tells CloudFoundry which services are necessary and which buildpack is to be used for a given application.

Update the name and host strings to a custom value. Change the service name below "services" to the name of the service you selected in the "Create a service" step. Save the updated file.

Your application is now ready to be deployed. Navigate using the terminal (cmd in Windows) to where you extracted the app sources. Run the following command:

	cf push
		
Your application is now pushed to the cloud. Once it is deployed you should be able to see a hello world message by going on a browser to [your-app-name].scapp.io. If it is working as expected you can now configure this route in the routing profile.

Add the following route to the default profile: http://[your-app-name].scapp.io/lora

Observe that data is being pushed to your webapp when you interact with your device.