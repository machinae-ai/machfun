# import fireo

# from fireo.models import Model
# from fireo.fields import TextField

# # fireo.connection(from_file="avtomat-40a28-firebase-adminsdk-q0zqt-7cd8741333.json")

# from fireo.models import Model
# from fireo.fields import TextField, NumberField
# from fireo.firestore import CollectionReference

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# Application Default credentials are automatically created.
cred = credentials.Certificate("avtomat-40a28-firebase-adminsdk-q0zqt-7cd8741333.json")
app = firebase_admin.initialize_app()

# Note: Use of CollectionRef stream() is prefered to get()
db = firestore.client()
docs = db.collection(u'user').where(u'themeMode', u'==', "dark").get()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

# class User(Model):
#     name = TextField()
#     age = NumberField()

# class Post(Model):
#     title = TextField()
#     content = TextField()
#     author = TextField()

#     # Define a subcollection called 'comments' for this Post model
#     class Meta:
#         collection_name = 'comments'

# # Get a reference to the 'Post' collection
# post_collection_ref = Post.collection()

# # Create a new 'Post' document
# new_post = Post(title='My First Post', content='This is the content of my first post', author='John')

# # Add a new comment to the subcollection of the new 'Post' document
# new_comment = User(name='Mary', age=30)
# comment_collection_ref = new_post.reference.collection('comments')
# comment_collection_ref.add(new_comment)

# # Query the subcollection of an existing 'Post' document
# existing_post = Post.collection.filter('title', '==', 'My First Post').fetch()[0]
# comment_collection_ref = existing_post.reference.collection('comments')
# comments = comment_collection_ref.fetch()

# # Iterate over the query results to access the 'User' documents in the subcollection
# for comment in comments:
#     # Access the fields of the 'User' document as needed
#     print(comment.name, comment.age)


# # class Cell(Model):
# #     name = TextField()
# #     type = TextField()
# #     input = TextField()

# #     # class Meta:
# #     #   collection_name = "project/cell"

# # # project_id = '1'
# # cell = Cell(input='none')
# # cells_ref = Cell.collection.filter('input', '==', 'none')
# # # cells_ref = Cell.collection.filter(input='none')
# # matching_cells = cells_ref.fetch()
# # for cell in matching_cells:
# #   print(cell.name, cell.type)

# # class City(Model):
# #     name = TextField()

# # cities = City.collection.filter('state', '==', 'CA').fetch()
