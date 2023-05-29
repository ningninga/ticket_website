import requests
import json
import re

url = "https://leetcode.com/graphql/"

headers = {
    "Content-Type": "application/json",
}

query = """

    query communitySolution($topicId: Int!) {
  isSolutionTopic(id: $topicId)
  topic(id: $topicId) {
    id
    viewCount
    topLevelCommentCount
    favoriteCount
    subscribed
    title
    pinned
    solutionTags {
      name
      slug
    }
    hideFromTrending
    commentCount
    isFavorite
    post {
      id
      voteCount
      voteStatus
      content
      updationDate
      creationDate
      status
      isHidden
      author {
        isDiscussAdmin
        isDiscussStaff
        username
        nameColor
        activeBadge {
          displayName
          icon
        }
        profile {
          userAvatar
          reputation
        }
        isActive
      }
      authorIsModerator
      isOwnPost
    }
  }
  relatedSolutions(topicId: $topicId) {
    id
    post {
      author {
        username
        profile {
          userAvatar
        }
      }
    }
    title
    solutionTags {
      name
      slug
    }
  }
}
    
"""

variables = {
    "topicId": 2361743
}

payload = {
    "operationName": "communitySolution",
    "query": query,
    "variables": variables,
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    # print(json.dumps(data))
    # data_json = json.dumps(data)
    if 'data' in data and data['data']:
        content = data['data']['topic']['post']['content']
        # print(content)
    
        python_code = re.search(r"```Python.*?```", content, re.DOTALL)
        if python_code:
            python_code = python_code.group().replace("```Python []", "").replace("```", "").strip()

        print(python_code)
        f = open("python_code.py", "a")
        f.write(python_code)
        f.close
else:
    print("Error:", response.status_code)
