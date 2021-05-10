class Article():

    def __init__(self, name, url, summary = ''):
        self.name = name
        self.url  = url
        self.summary = summary

    def get_name(self):
        return self.name

    def get_summary(self):
        return self.summary

    def get_url(self):
        return self.url

    def get_content(self):
        raise Exception("Not implemented")

    def __str__(self):
        return str(
            {
            "title":  self.name,
            "url":    self.url,
            "summary": self.summary
            }
        )