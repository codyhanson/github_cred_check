#Credential Check
You shouldn't put sensitive credentials in your git repositories, whether they are public or private.
This tool helps you search through everything, to help identify things on Github that shouldn't be there.

There are two ways to search right now:

###AWS Credentials
To search github for AWS Access Key Id's, download a credential report from the IAM application. This CSV file contains
a list of users that the script will use the IAM API to search for Access Key ID's with.

###CSV File of tokens
If you want to search for other tokens that you shouldn't have in your code, you can specify them in a two column CSV file.

The format is <description, value>
```
Production Sendgrid Secret,abc123!@#
Database secret key,I@mS3cret!
```

###Required Config
For now, just edit the variables at the top of `github_cred_check.py`.

You need:
* AWS credentials exported to the ENV, so that Boto can use them.
* A valid Github API token.


###TODO
* Honor Github API rate-limiting
* Proper CLI interface (flags, options, help, etc).