
def print_col(col):
  """ prints collection
  Args:
      col (firestore.CollectionReference): collection snapshot.
  """
  for doc in col:
    print(f'{doc.id} => {doc.to_dict()}')

def contains_doc_by_id(col, id):
  """ checks if collection contains document with id
  Args:
      col (firestore.CollectionReference): collection snapshot.
      id (string): doc id.
  """
  for doc in col:
    if doc.id == id and doc.exists:
      return True  
  return False


def contains_docs_by_id(col, id_array):
  """ checks if collection contains documents with all ids from array
  Args:
      col (firestore.CollectionReference): collection snapshot.
      id (string): array of doc ids.
  """
  print(f'contains_docs_by_id({id_array})')
  arr=id_array
  for doc in col:
    print(f'check {doc.id} in {arr}')
    if doc.exists and doc.id in arr:
      arr.remove(doc.id)
  if len(arr) == 0:
    return True
  return False
