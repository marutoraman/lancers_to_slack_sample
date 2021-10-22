from engine.slack import Slack


def test_send_message2():
    res=Slack.send_message_webhook("https://hooks.slack.com/services/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","testメッセージ")
    print(res.text)