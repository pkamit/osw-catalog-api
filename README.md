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
=========================
Build Again:
    151  docker-compose down
    152  docker-compose down --volumes
    153  docker-compose build
    154  docker-compose up


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

18) Create action and attach serializer

=======================================
create
LIST
vIEW DETAIL
uPDATE
dELETE
/articles/
    - get - list all articles
    - post - create article
/articles/<article_id>
    - GET - Detail view of article
    - PUT/PATCH - Update article
    - DELETE - Delete article

- Create test case for articles api
- Create serializer -- > Viewsets --> url
    viewsets
        class ArticleViewSet(viewsets.ModelViewSet):
        serializer_class = serializers.ArticleSerializer
    url
        router = DefaultRouter()
        router.register('articles', views.ArticleViewSet)


======================================
Category Model
    name: Name of tag to create
    user: user who created category
/api/article/category
    POST- create a category
    PUT/PATCH - update categories
    DELETE - remove category
    GET - List available category

===============================================
Image fields:
    - pillow at requirements
    - configuration in dockerfile
        - jpg-dev, z-lib , zlib-dev,
        - vol web media , vol web static
    - in settings.py attach directory
    - set url path for debug made in dev environement
    - import uuid and os in models.py







django version
drf version
classes and objects
big images managed
write_only_fields = ['password']
API VIEW and Viewsets are base classes of DRF
APIVIEW:
    Foucused around HTTP methods
    class methods for http methods
        GET,POST,PUT,PATCH,DELETE
    Useful for non crud apis
        Bespoke logic(auth,jobs,external apis)
Viewsets:
    Focused around actions
        Retrieve , list, update, partial update , destroy
    Map to Django Models
    Use Routers to generate URLS
    Great for CRUD operations on models
    ========================================
    Refrences:

    https://www.youtube.com/watch?v=B3HGwFlBvi8

    multisites
    https://www.valentinog.com/blog/django-vhosts/

 30 Django E Commerce Product Attributes Variants Amazon style Size Color #1 [English]
https://www.youtube.com/watch?v=hhh6iv9TP7g
https://www.youtube.com/watch?v=HssciqnFjyA&list=PLSPMgrv4IuJ5tX9Sk7hjNrHsQRC3ppRtG&index=2
How to Install and Setup Django Oscar | E-Commerce Website | Django Oscar #1


https://replit.com/@tushantk/HumiliatingInterestingMarketing#product/models.py

Fixture to load data
https://youtu.be/8LHdbaV7Dvo?t=1258


To prepare Faker data
https://www.youtube.com/watch?v=8LHdbaV7Dvo

python manage.py dumpdata oscar.apps.catalogue.Product > products.json
python manage.py loaddata products.json
