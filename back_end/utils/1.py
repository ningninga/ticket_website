url = "https://leetcode.com/graphql/"

headers = {
    "Content-Type": "application/json",
}

query = """
query communitySolutions($questionSlug: String!, $skip: Int!, $first: Int!, $query: String, $orderBy: TopicSortingOption, $languageTags: [String!], $topicTags: [String!]) {
  questionSolutions(
    filters: {questionSlug: $questionSlug, skip: $skip, first: $first, query: $query, orderBy: $orderBy, languageTags: $languageTags, topicTags: $topicTags}
  ) {
    hasDirectResults
    totalNum
    solutions {
      id
      title
      commentCount
      topLevelCommentCount
      viewCount
      pinned
      isFavorite
      solutionTags {
        name
        slug
      }
      post {
        id
        status
        voteCount
        creationDate
        isHidden
        author {
          username
          isActive
          nameColor
          activeBadge {
            displayName
            icon
          }
          profile {
            userAvatar
            reputation
          }
        }
      }
      searchMeta {
        content
        contentType
        commentAuthor {
          username
        }
        replyAuthor {
          username
        }
        highlights
      }
    }
  }
}
"""

variables = {
    "first": 15,
    "languageTags": [],
    "topicTags": [],
    "query": "",
    "questionSlug": "two-sum",
    "skip": 0,
    "topicTags": [],
    "orderBy": "hot",
}

payload = {
    "operationName": "communitySolutions",
    "query": query,
    "variables": variables,
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    # print(json.dumps(data))
    # data_json = json.dumps(data)
    print(type(data))
    if 'data' in data and data['data']:
        solutions = data['data']['questionSolutions']['solutions']
        print(len(solutions))
        for i in range(len(solutions)):
            solution_id = solutions[i]['id']
            print(solution_id)
else:
    print("Error:", response.status_code)
