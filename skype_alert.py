# skpy can be installed from pip package 'pip install skpy'
#
import os
from skpy import Skype
from skpy import SkypeAuthException
import json
from subprocess import Popen, PIPE


# Skype user credentials to login, this user should be able to login to web.skype.com without any interruption(Captcha or Phone numver varification etc.)
# I have not tested this on skype for business, it works fine on normal skype.

credentials = {'username':'*********@outlook.com', \
               'password':'**********'}

# Following file is used to track group conversations.
group_info_file = '.groupinfo.json'

users = ['uzzam.javed', 'mustafaalam958', 'live:zeshan-95', 'nasirkamal707']


# username: skype username (str)
# password: skype user password (str)
# Stores login token in '.tokens-app'.
# Returns Skype object
def skype_login(username,password):
    sk = Skype(connect=False)
    sk.conn
    os.system('touch .tokens-app')
    sk.conn.setTokenFile(".tokens-app")
    try:
        sk.conn.readToken()
    except SkypeAuthException:
        sk.conn.setUserPwd(username, password)
        sk.conn.getSkypeToken()
    sk.conn
    return sk

# Creates skype group chat and maintains group ids locally. Existing groups can not be used until we have their group ids.
# If group name already exists in local storage, it prints 'Group Name Already Exists' and exits.
# Just sends 'Hi Guys' message on group creation.
# skype_user = Skype Object, usually from skype_login()
# group_name = Group conversation identifier (str) (Only local significance)
# group_members = (list) List of group members skype ids.

def skype_create_group(skype_user, group_name, group_members):
    if not os.path.exists(group_info_file):
        os.system('touch ' + group_info_file)
        groups = dict()
        groups['ids'] = dict()
    else:
        with open(group_info_file) as f:
            groups = json.load(f)
    
        if group_name in groups.keys():
            print 'Group Name Already Exists'
            return 0

    groups[group_name] = group_members
    ch = skype_user.chats.create(group_members)
    groups['ids'][group_name] = ch.id
    with open(group_info_file, 'w') as fp:
        json.dump(groups, fp)
    ch.sendMsg('Hi Guys')

# Returns dictionary of locally stored group names and members for troubleshooting.

def get_skype_groups():  # Returns list of groups and group members
    groups_dict = dict()
    with open(group_info_file) as f:
        groups = json.load(f)
    for group in groups.keys():
        if group != 'ids':
            groups_dict[group] = groups[group]
    return groups_dict

# Runs command and return standard output and error message
# command = (str)
def run_command(command):
    command_split = command.split(' ')
    process = Popen(command_split, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    return (output, err)

# Sends skype 'message' to 'user_id'.
# skype_user = Skype Object
# user_id = (str) skype id of receiver
# message = (str) Message to send

def send_to_person(skype_user, user_id, message):
    ch = skype_user.contacts[user_id].chat
    chat = skype_user.chats[ch.id]
    chat.sendMsg(message)

# Sends skype 'message' to group.
# skype_user = Skype Object
# group_name = local identifier of conversation group.
# message = (str) Message to send

def send_to_group(skype_user, group_name, message):
    with open(group_info_file) as f:
            groups = json.load(f)
    group_id = groups['ids'][group_name]
    ch = skype_user.chats[group_id]
    ch.sendMsg(message)


# format  standard output and error message to be sent.
def construct_msg(command, output, err):
    msg = 'COMMAND: ' + command + '\n-------- \nOUTPUT: \n' + output + '\n-------- \nERROR: \n' + err + '\n************************\n'
    return msg


# Executes command and sends standard output and error message to user.
def execute_and_skype_person(skype_user, command, receiver_id): # Command in string form
    (output, err) = run_command(command)
    message = construct_msg(command, output, err)
    send_to_person(skype_user, receiver_id, message)

# Executes command and sends standard output and error message to conversation group.
def execute_and_skype_group(skype_user, command, group_name): # Command in string form
    (output, err) = run_command(command)
    message = construct_msg(command, output, err)
    send_to_group(skype_user, group_name, message)


if __name__ == '__main__':
    # Skype user credentials to login, this user should be able to login to web.skype.com without any interruption
    # (Captcha or Phone numver varification etc.)
    # I have not tested this on skype for business, it works fine on normal skype.
    credentials = {'username':'*******@outlook.com', 'password':'*******'}
    users = ['uzzam.***', 'mustafaalam***', 'live:zeshan-***', 'nasirkamal***']
    skln = skype_login(credentials['username'],credentials['password'])
    skype_create_group(skype_user=skln, group_name='test', group_members=users)
    execute_and_skype_group(skype_user=skln, command='ls -ll', group_name='test')

