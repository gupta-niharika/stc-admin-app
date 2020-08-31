#sabhi functions ke endpoints(routes) idhar hain

#importing the functions from the files
from .article import ArticleApi, ArticlesApi, ArticleGApi
from .auth import SignupApi, LoginApi, LogoutApi, DeleteApi
from .feed import FeedApi, FeedsApi
from .resources import ResourcesApi, ResourceDApi, ResourceGApi
from .project import ProjectApi, ProjectsApi
from .event import EventApi, EventsApi
from .github import GithubApi, GithubsApi

# attach in urls
def initialize_routes(api):
    api.add_resource(ArticlesApi, '/api/articles')          #article
    api.add_resource(ArticleApi, '/api/articles/<id>')      #article deletion
    api.add_resource(ArticleGApi, '/api/articles/<domain>')  #article domain wise

    api.add_resource(SignupApi, '/api/auth/signup')         #signup fro admin
    api.add_resource(LoginApi, '/api/auth/login')           #login for admin
    api.add_resource(LogoutApi, '/api/auth/logout')         #logout for admin
    api.add_resource(DeleteApi, '/api/auth/deleteadmin')    #delete admin

    api.add_resource(FeedsApi, '/api/feeds/<skip>')            #feed post
    api.add_resource(FeedApi, '/api/feeds/<id>')        #deleting feed post

    api.add_resource(ResourcesApi, '/api/resources')        #resources
    api.add_resource(ResourceDApi, '/api/resources/<id>')   #deleting a resource
    api.add_resource(ResourceGApi, '/api/resources/<domain>')  #domain wise resources

    api.add_resource(ProjectsApi, '/api/projects')          #projects
    api.add_resource(ProjectApi, '/api/projects/<id>')      #deleting a project

    api.add_resource(EventsApi, '/api/events')          #events
    api.add_resource(EventApi, '/api/events/<id>')      #deleting an event

    api.add_resource(GithubsApi, '/api/github')          #github
    api.add_resource(GithubApi, '/api/github/<id>')      #deleting a github post