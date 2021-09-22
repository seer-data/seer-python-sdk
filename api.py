### NECESSARY PYTHON PACKAGES
# python 3.7.10
import numpy as np  # 1.20.2 
import requests     # 2.25.1
import json         # 2.0.9

### BACK-END HELPER FUNCTIONS
endpoint = "https://backend.seerplatform.com"

"""
See training material for details of Suitcases, Insights, and the seer-python-sdk API.
"""

def get_suitcase(suitcase_id, xtkn, endpoint=endpoint):
    """
    Arguments: suitcase_id (int)
    Returns: The corresponding suitcase content
    """
    url = endpoint+"/suitcases/{}".format(suitcase_id)
    response = requests.get(url, headers={'content-type':'application/json', 'x-token':xtkn})
    suitcase = response.json()['data']['suitcase']
    return suitcase

def get_insight(insight_id, xtkn, endpoint=endpoint):
    """
    Arguments: insight_ids (list of ints)
    Returns: List of Insights corresponding to the supplied Insight IDs
    """
    ## Retrieve the insight
    url = endpoint+"/insights/{}".format(insight_id)
    response = requests.get(url, headers={'content-type':'application/json', 'x-token':xtkn})
    insight = response.json()['data']['insight']
    return insight

def get_insight_json(insight):
    """
    Arguments: insight (json)
    Returns: Insight JSON object from within the supplied Insight
    """
    return json.loads(insight['json'])

def update_insight_json(insight, insight_json):
    """
    Arguments: insight (json), insight_json (json)
    Returns: Insight JSON object from within the supplied Insight
    """
    json_dump = json.dumps(insight_json)
    insight['json'] = json_dump
    return insight

def delete_insight(insight_id, xtkn, endpoint=endpoint):
    """
    Arguments: insight_id
    Returns: None. Deleted insight corresponding to the Insight ID provided.
    """
    url = endpoint+"/insights/{}".format(insight_id)
    response = requests.delete(url,  headers={'content-type':'application/json', 'x-token':xtkn})
    return response

def create_new_insight(insight, xtkn, suitcase_id, endpoint=endpoint):
    """
    Arguments: insight (json), dest_suitcase (int)
    Returns: None. Creates new insights in the Suitcase provided from the Insight objects provided.
    Notes: Could be an improvement to return list of insight_ids created.
    To create a brand new insight, post the necessary insight data to the back-end without an insight ID.
    """
    ## Post to dest_suitcase
    url = endpoint + '/insights'
    postData = {'key': insight['key'], 'name': insight['name'], 'json': insight['json'], 'subheading': insight['subheading'], "suitcase_id": suitcase_id}
    response = requests.post(url,  headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
    return response

def save_over_insight(insight, xtkn, insight_id, endpoint=endpoint):
    """
    Arguments: insight_json (json), insight_id (int)
    Returns: None. Writes Insight JSON object to existing insight at Insight ID provided.
    To over-write an existing insight, post the necessary insight data to the back-end with the insight ID.
    """
    url = endpoint+"/insights/{}".format(insight_id)
    ## Put the insight back into the database
    postData = {'key': insight['key'], 'name': insight['name'], 'json': insight['json'], 'subheading': insight['subheading']}
    response = requests.put(url, headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
    return response

def duplicate_suitcase(suitcase_id, xtkn, endpoint=endpoint):
    """
    Arguments: suitcase_id (int)
    Returns: ID for duplicate of suitcase identified by suitcase_id.
    """
    url = endpoint+'/suitcases/'+str(suitcase_id)+'/copies'
    response = requests.post(url, headers={'content-type':'application/json', 'x-token':xtkn})
    response_json = response.json()
    new_suitcase_id = response_json['data']['suitcase']['id']
    return new_suitcase_id

def update_suitcase(data, suitcase_id, xtkn, endpoint=endpoint):
    """
    This function gets passed "suitcase" which is the same type of object as is returned by the function "get_suitcase", and the suitcase_id 
    for the suitcase that should be saved over, and saves over it. This does not work for sharing Suitcases.
    data e.g. data = {name: new_name, description: new_description}
    """
    url = endpoint+"/suitcases/{}".format(suitcase_id)
    postData = data
    response = requests.put(url, headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
    return response

# def create_new_suitcase(suitcase, xtkn, endpoint=endpoint):
#     """
#     This function should create a brand new empty suitcase and return the "suitcase" object for it. 
#     """
#     pass

def share_suitcase(invites, suitcase_id, xtkn, endpoint=endpoint):
    """
    invites should be formatted as a list of dicts: [{"user_id":2,"read_only":true}, {"user_id":3,"read_only":true}]
    """
    url = endpoint+"/suitcases/{}/users".format(suitcase_id)
    postData = {"accesses":invites}
    response = requests.post(url, headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
    return response

def remove_user_from_suitcase(user_id, suitcase_id, xtkn, endpoint=endpoint):
    url = endpoint+"/suitcases/{}/users/{}".format(suitcase_id,user_id)
    response = requests.delete(url, headers={'content-type':'application/json', 'x-token':xtkn})
    return response

def make_suitcase_public_link(suitcase_id, xtkn, endpoint=endpoint):
    '''
    Arguments: suitcase_id, endpoint(default Seer endpoint)
    Returns: response, key
    '''
    url = endpoint+"/suitcases/{}".format(suitcase_id)
    postData = {"link_share":True}
    response = requests.put(url, headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
    key = None
    if response.ok:
        # Get suitcase
        suitcase = get_suitcase(suitcase_id)
        # Get key
        key = suitcase['key']
    return response, key

# def transfer_suitcase_ownership(new_owner_user_id, suitcase_id, xtkn, endpoint=endpoint):
#     """
#     Careful, transferring ownership is a one-way function, will restrict what you can do with the suitcase after you are no longer the owner.
#     """
#     url = endpoint+"/suitcases/{}".format(suitcase_id)
#     postData = {"user_id":new_owner_user_id}
#     response = requests.put(url, headers={'content-type':'application/json', 'x-token':xtkn}, data=json.dumps(postData))
#     return response

def delete_suitcase(suitcase_id, xtkn, endpoint=endpoint):
    """
    Arguments: suitcase_id
    Returns: None. Deleted suitcase corresponding to the Suitcase ID.
    """
    url = endpoint+"/suitcases/{}".format(suitcase_id)
    response = requests.delete(url,  headers={'content-type':'application/json', 'x-token':xtkn})
    return response