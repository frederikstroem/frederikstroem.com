import feedparser
import math

class Journal():
    def __init__(self):
        self.feedPath = "static/feed.xml"
        self.postsPerPage = 5

    def getFeed(self):
        return feedparser.parse(self.feedPath)

    def getLatestPosts(self, page=1):
        """Get latest posts."""

        feed = self.getFeed()

        lastPossiblePage = math.ceil(len(feed["entries"]) / self.postsPerPage)
        if lastPossiblePage < 1:
            lastPossiblePage = 1

        # Convert feeds to a better format.
        convertedFeed = []

        currentPage = page
        if currentPage > lastPossiblePage or currentPage < 1:
            currentPage = lastPossiblePage

        i = 0 + self.postsPerPage * (currentPage - 1)

        for j in range(self.postsPerPage):
            if i < len(feed["entries"]):
                convertedFeed.append({
                    "title": feed["entries"][i]["title"],
                    "published": feed["entries"][i]["published"],
                    "updated": feed["entries"][i]["updated"],
                    "summary": feed["entries"][i]["summary"],
                    "link": feed["entries"][i]["link"].replace("https://frederikstroem.com","")
                })
                i += 1
            else:
                break

        return convertedFeed

    def getPost(self, postId):
        """Returns post with the specified id."""

        feed = self.getFeed()

        for i in range(len(feed["entries"])):
            if feed["entries"][i]["link"].replace("https://frederikstroem.com/journal/","").replace("/", "") == postId:
                return {
                    "title": feed["entries"][i]["title"],
                    "published": feed["entries"][i]["published"],
                    "updated": feed["entries"][i]["updated"],
                    "summary": feed["entries"][i]["summary"],
                    "content": feed["entries"][i]["content"][0]['value'].replace("</br>", "")   # This fixes a parsing problem, probably not the best soulution though...
                }

        # If post cannot be found, return None.
        return None

    def getPaginationOverview(self, currentPage=1):
        returnValue = {
            # Booleans.
            "isFirstPage": None,
            "isLastPage": None,
            "isNextPageLast": None,
            "isPreviousPageFirst": None,

            # Integers.
            "currentPage": None,
            "nextPage": None,
            "previousPage": None,
            "firstPage": 1,
            "lastPage": None
        }

        feed = self.getFeed()

        lastPossiblePage = math.ceil(len(feed["entries"]) / self.postsPerPage)
        if lastPossiblePage < 1:
            lastPossiblePage = 1

        if currentPage > lastPossiblePage or currentPage < 1:
            currentPage = lastPossiblePage

        # isFirstPage
        if currentPage == 1:
            returnValue["isFirstPage"] = True
        else:
            returnValue["isFirstPage"] = False

        # isLastPage
        if currentPage == lastPossiblePage:
            returnValue["isLastPage"] = True
        else:
            returnValue["isLastPage"] = False

        # isNextPageLast
        if returnValue["isLastPage"]:
            pass
        elif currentPage + 1 == lastPossiblePage:
            returnValue["isNextPageLast"] = True
        else:
            returnValue["isNextPageLast"] = False

        # isPreviousPageFirst
        if returnValue["isFirstPage"]:
            pass
        elif currentPage - 1 == 1:
            returnValue["isPreviousPageFirst"] = True
        else:
            returnValue["isPreviousPageFirst"] = False

        # currentPage
        returnValue["currentPage"] = currentPage

        # nextPage
        if returnValue["isLastPage"]:
            pass
        else:
            returnValue["nextPage"] = currentPage + 1

        # previousPage
        if returnValue["isFirstPage"]:
            pass
        else:
            returnValue["previousPage"] = currentPage - 1

        # lastPage
        returnValue["lastPage"] = lastPossiblePage

        # Return data.
        return returnValue
