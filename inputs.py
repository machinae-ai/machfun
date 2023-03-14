from google.cloud import firestore

from firestore import contains_doc_by_id, contains_docs_by_id, print_col
# db = firestore.Client()

def start_runs_for_input(run_ref, input_id):
    """ finds incomplete runs with input id provided
    Args:
        run_ref (firestore.DocumentReference): run document reference.
        input_id (string): input id.
    """
    transaction = run_ref._client.transaction()
        
    cell_col_query_ref=run_ref.parent.parent.collection(u'cell').where(u'inputs', u'array_contains', input_id)
    
    # cell_col=run_ref.parent.parent.collection(u'cell').get()
    # print_col(cell_col)
    run_col_ref=run_ref.collection(u'run') 
    run_col_query_ref=run_ref.collection(u'run').where(u'status', u'in', ['running', 'completed'])
    input_col_ref=run_ref.collection(u'input')
    # city_ref = db.collection(u'cities').document(u'SF')

    @firestore.transactional
    def get_cells_and_runs_transaction(transaction, cell_col_ref, run_col_ref, run_col_query_ref, input_col_ref):
        
        cells=cell_col_ref.get(transaction=transaction)
        # snapshot = city_ref.get(transaction=transaction)
        
        print(f'found {cells} cells with input {input_id}')
        runs=run_col_query_ref.get(transaction=transaction)
        
        print(f'found {runs} runs with status running or completed')
        inputs=input_col_ref.get(transaction=transaction)
        
        
        print(f'found {inputs} inputs')
        
        
        for cell_doc in cells:
        
            print(f'process cell: {cell_doc.id} => {cell_doc.to_dict()}')
        
            # check if cell started running or already completed
            if contains_doc_by_id(runs, cell_doc.id):
              print(f'cell {cell_doc.id} already started or completed')
              continue
            
            if contains_docs_by_id(inputs, cell_doc.to_dict()['inputs']):
              print(f'all inputs are ready for {cell_doc.id}, start cell...')
              transaction.set(run_col_ref.document(cell_doc.id), 
                {**cell_doc.to_dict(),**{u'status': u'running'}})
            else:
              print(f'not all inputs are ready for {cell_doc.id}')
        
            # for input in cell_doc.to_dict()['input']:
            #     print(f'process input: {input}')
            #     input_doc=input_col_ref.document(input).get(transaction=transaction)
            #     print(f'found input: {input_doc.id} => {input_doc.to_dict()}')
            
        # transaction.update(city_ref, {
        #     u'population': snapshot.get(u'population') + 1
        # })

    get_cells_and_runs_transaction(transaction, cell_col_query_ref, run_col_ref, run_col_query_ref, input_col_ref)
    
    # print(f'find_run_with_input_id({input_id})')
    # run_collection = db.parent.collection(u'cell')
    # incomplete_runs = run_collection.where(u'status', u'==', 'running').get()
    # print(f'found {incomplete_runs} incomplete runs')
    # for doc in incomplete_runs:
    #   print(f'{doc.id} => {doc.to_dict()}')