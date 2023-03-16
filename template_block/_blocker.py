def block_answer(
        answer=None, 
        user=None, 
        link=None):
    return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Answer",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": answer,
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Go to the <{}|message> \n*Posted by:* <@{}>".format(link, user)
                    }
                ]
            }
        ]


def block_setup(
        answer="Indexing the conversations :building_construction:", 
        ):
    return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": answer,
                    "emoji": True
                }
            },
            {
                "type": "divider"
            }
        ]