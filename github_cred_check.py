__author__ = 'clh'

import requests
import boto

# Config
# required
github_api_token = 'Your Github API Token'
#limit the search scope to your user account, or organization.
search_username = 'YourUserName or Org Name'

# optional, but you should have at least one of these.
aws_key_report_file = './aws_key_report.csv'
extra_token_file = './extra_tokens.csv'


def print_key_info(key):
    print "key_id:{0}, status:{1}, owner:{2}".format(key['access_key_id'], key['status'], key['user_name'])


def search_github(key):
    print "Searching Github for token:{0}".format(key[1].rstrip())
    print "Token Description:{0}".format(key[0])
    params = {'access_token': github_api_token, 'q': "{0} user:{1}".format(key, search_username)}
    r = requests.get('https://api.github.com/search/code', params=params)
    body = r.json()
    print 'Found total count:{0}'.format(body['total_count'])
    for item in body['items']:
        print "Filename:{0}, link:{1}".format(item['name'], item['html_url'])


def main():
    #Assumes that your AWS credentials are exported in the local environment.
    iam = boto.connect_iam()
    user_names = []
    if aws_key_report_file:
        with open(aws_key_report_file) as report_fp:
            for line in report_fp:
                user_names.append(line.split(',')[0])
        #remove first two elements, they are the csv legend, and the <root_account>
        user_names = user_names[2:]
    else:
        print 'Skipping AWS credential check, no aws key report file specified'

    access_key_ids = []
    #do AWS key lookup.
    for user_name in user_names:
        keys = iam.get_all_access_keys(user_name)
        for key in keys['list_access_keys_response']['list_access_keys_result']['access_key_metadata']:
            print_key_info(key)
            access_key_ids.append(tuple(['AWS:' + key['user_name'], key['access_key_id']]))

    #Read in extra search terms
    if extra_token_file:
        with open(extra_token_file) as report_fp:
            for line in report_fp:
                print line.rstrip()
                access_key_ids.append(line.split(','))
    else:
        print 'Skipping extra credential check, no csv file specified'

    for key in access_key_ids:
        print '\n'
        search_github(key)


if __name__ == '__main__':
    main()