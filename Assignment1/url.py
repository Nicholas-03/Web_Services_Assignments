class Url:
    urls = {}
    counter = 0

    @staticmethod
    def getId(num):
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return chars[0]
    
        result = []
        while num > 0:
            result.append(chars[num % 62])
            num //= 62
    
        return ''.join(reversed(result))
    
    @classmethod
    def getUrls(self):
        return list(self.urls.keys())

    @classmethod
    def addUrl(self, url):
        id = self.getId(self.counter)
        self.urls[id] = url
        self.counter += 1

        return id
