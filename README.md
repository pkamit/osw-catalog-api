# osw-catalog-api
osw catalog api
1) git project
2) docker hub , take access tocken
3) git to setup secrets
4) create requirements.txt
5) create Dockerfile
6) create .dockerignore
7) $ docker-compose run --rm app sh -c "django-admin startproject app ."
8) docker compose for db setup
9) git hub actions is pending
==========
10) Updated user model and write the test cases
11) created super user
12) Test cases from admin sites
===================
13) drf spectacular installed and attached in url path
14) api schema view spectacular api view
15) api docs view spectacular swagger view
=============================
16) user api
17) delete migrations, models.py and admin.py because all of code in Core app
18) test create user email,password,name
19) test create article with attributes
19) test article with name exists error
=========================
20) we create serializers.py to implement api or test cases pass
21) serializers using by views
13) Generics views is the common set of api view that is close to database models.
Mixins

The mixin classes provide the actions that are used to provide the basic view behavior. Note that the mixin classes provide action methods rather than defining the handler methods, such as .get() and .post(), directly. This allows for more flexible composition of behavior.
14) generics api view: adding commanly required behaviour for listing and detail view
attributes: queryset and get_queryset
serilizer_class = for desirializing and validating imputs and serializing output
lookupfields
filter_backends
15) Methods:
get_queryset(self): queryset for listing and detail page , for manupulating default view
get_objects(self): for detail view and default to using the lookup_fields
get_serializer_class= it returns the class that should be used for serializer.
filter_queryset = for filtering queryset
16) Mixins:
comman behaviour off rest framework has been provided in mixin
including CRUD operation LIST, UPDATE, Destroy
mixin class provide the actions that used to provide basic view behaviour
mixin class provide action rather that defining handler https://www.youtube.com/watch?v=Ix-HjVQP0t4
LISTm CREATE RETRIEVE DESTROY UPDATE

17) API view : get put delete used but genericapiview with mixing doing awesome




======================================
django version
drf version
classes and objects
big images managed
write_only_fields = ['password']

