import unittest

from arangodb.api import Client, Database, Collection, Document
from arangodb.orm.fields import CharField, ForeignKeyField
from arangodb.orm.models import CollectionModel
from arangodb.query.advanced import Query, Traveser
from arangodb.query.utils.document import create_document_from_result_dict
from query.simple import SimpleQuery
from transaction.controller import Transaction, TransactionController


client = Client(hostname='localhost')

class ExtendedTestCase(unittest.TestCase):
    def assertDocumentsEqual(self, doc1, doc2):
        """
        """

        self.assertEqual(doc1.id, doc2.id)

        for prop in doc1.data:
            doc1_val = doc1.data[prop]
            doc2_val = doc2.data[prop]

            self.assertEqual(doc1_val, doc2_val)


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_and_delete_database(self):

        database_name = 'test_foo_123'

        db = Database.create(name=database_name)

        self.assertIsNotNone(db)

        Database.remove(name=database_name)

    def test_get_all_databases(self):
        databases = Database.get_all()

        self.assertTrue(len(databases) >= 1)

        for db in databases:
            self.assertTrue(isinstance(db, Database))


class CollectionTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_create_and_delete_collection_without_extra_db(self):

        collection_name = 'test_foo_123'

        col = Collection.create(name=collection_name)

        self.assertIsNotNone(col)

        Collection.remove(name=collection_name)

    def test_get_collection(self):

        collection_name = 'test_foo_123'

        col = Collection.create(name=collection_name)

        self.assertIsNotNone(col)

        retrieved_col = Collection.get_loaded_collection(name=collection_name)

        self.assertEqual(col.id, retrieved_col.id)
        self.assertEqual(col.name, retrieved_col.name)
        self.assertEqual(col.type, retrieved_col.type)

        Collection.remove(name=collection_name)


class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_document_access_values_by_attribute_getter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'
        doc.set(key='test', value=doc_attr_value)

        self.assertEqual(doc.test, doc_attr_value)

    def test_document_access_values_by_attribute_setter(self):
        doc = Document(id='', key='', collection='', api=client.api)
        # set this to true so it won't make requests to nothing
        doc.is_loaded = True
        doc_attr_value = 'foo_bar'

        doc.test = doc_attr_value

        self.assertEqual(doc.get(key='test'), doc_attr_value)


class AqlQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_aqlquery_123'
        self.db = Database.create(name=self.database_name)

        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.little_number = 33
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.little_number = 1
        self.col1_doc2.save()

        self.col1_doc3 = self.test_1_col.create_document()
        self.col1_doc3.little_number = 3
        self.col1_doc3.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.little_number = 2
        self.col2_doc1.save()

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_all_doc_from_1_collection(self):
        q = Query()
        q.append_collection(self.test_2_col.name)
        docs = q.execute()

        self.assertEqual(len(docs), 1)

        doc1 = docs[0]
        self.assertDocumentsEqual(doc1, self.col2_doc1)

    def test_filter_for_document(self):
        pass

    def test_sorting_asc_document_list(self):
        q = Query()
        q.append_collection(self.test_1_col.name)
        q.order_by('little_number')

        docs = q.execute()

        self.assertEqual(len(docs), 3)

        doc1 = docs[0]
        doc2 = docs[1]
        doc3 = docs[2]

        self.assertDocumentsEqual(doc1, self.col1_doc2)
        self.assertDocumentsEqual(doc2, self.col1_doc3)
        self.assertDocumentsEqual(doc3, self.col1_doc1)


class SimpleQueryTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_simple_query_123'
        self.db = Database.create(name=self.database_name)

        # Create test data
        self.test_1_col = self.db.create_collection('foo_1')
        self.test_2_col = self.db.create_collection('foo_2')

        self.col1_doc1 = self.test_1_col.create_document()
        self.col1_doc1.ta='fa'
        self.col1_doc1.save()

        self.col1_doc2 = self.test_1_col.create_document()
        self.col1_doc2.ta='fa'
        self.col1_doc2.save()

        self.col2_doc1 = self.test_2_col.create_document()
        self.col2_doc1.save()

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_col.name)
        Collection.remove(name=self.test_2_col.name)

        Database.remove(name=self.database_name)

    def test_get_document_by_example(self):
        uid = self.col1_doc1.key
        doc = SimpleQuery.get_by_example(collection=self.test_1_col, example_data={
            '_key': uid,
        })

        self.assertDocumentsEqual(doc, self.col1_doc1)

    def test_get_all_documents(self):

        docs = SimpleQuery.all(collection=self.test_1_col)

        self.assertEqual(len(docs), 2)

        doc1 = docs[0]
        doc2 = docs[1]

        self.assertNotEqual(doc1, doc2)


class TraveserTestCase(ExtendedTestCase):
    def setUp(self):
        self.database_name = 'testcase_simple_query_123'
        self.db = Database.create(name=self.database_name)

        # Create collections
        self.test_1_doc_col = self.db.create_collection('doc_col_1')
        self.test_1_edge_col = self.db.create_collection('edge_col_1', type=3)

        # Create test data
        self.doc1 = self.test_1_doc_col.create_document()
        self.doc1.ta='fa'
        self.doc1.save()

        self.doc2 = self.test_1_doc_col.create_document()
        self.doc2.ta='foo'
        self.doc2.save()

        # Create test relation
        self.edge1 = self.test_1_edge_col.create_edge(from_doc=self.doc1, to_doc=self.doc2, edge_data={
            'data': 'in_between'
        })

    def tearDown(self):
        # They need to be deleted
        Collection.remove(name=self.test_1_doc_col.name)
        Collection.remove(name=self.test_1_edge_col.name)

        Database.remove(name=self.database_name)

    def test_traverse_relation(self):
        result_list = Traveser.follow(
            start_vertex=self.doc1.id,
            edge_collection=self.test_1_edge_col.name,
            direction='outbound'
        )

        self.assertEqual(len(result_list), 1)

        result_doc = result_list[0]
        self.assertDocumentsEqual(result_doc, self.doc2)


class CollectionModelTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_collection_model_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_init_and_delete_collection_model(self):

        class TestModel(CollectionModel):
            pass

        TestModel.init()
        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "TestModel")

        TestModel.destroy()

    def test_own_name_init_and_delete(self):

        class TestModel(CollectionModel):
            collection_name = "test_model"

        TestModel.init()
        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "test_model")

        TestModel.destroy()

    def test_empty_name(self):

        class TestModel(CollectionModel):
            collection_name = ""

        TestModel.init()

        model_collection_name = TestModel.collection_instance.name

        self.assertEqual(model_collection_name, "TestModel")

        TestModel.destroy()

    def test_save_model_with_one_field_not_required(self):

        class TestModel(CollectionModel):

            test_field = CharField(required=False)

        TestModel.init()

        model_1 = TestModel()

        model_2 = TestModel()
        model_2.test_field = "model_2_text"

        model_1.save()
        model_2.save()

        all_docs = TestModel.collection_instance.documents()
        self.assertEqual(len(all_docs), 2)

        retrieved_model_1 = None
        retrieved_model_2 = None

        for doc in all_docs:
            if doc.get(key='_key') == model_1.document.get(key='_key'):
                retrieved_model_1 = doc
            else:
                retrieved_model_2 = doc

        if retrieved_model_1:
            self.assertEqual(retrieved_model_1.get('test_field'), None)
        if retrieved_model_2:
            self.assertEqual(retrieved_model_2.get('test_field'), "model_2_text")

        TestModel.destroy()

    def test_save_model_with_one_field_required(self):

        class TestModel(CollectionModel):

            test_field = CharField(required=True)

        TestModel.init()

        model_1 = TestModel()

        model_2 = TestModel()
        model_2.test_field = "model_2_text"

        try:
            model_1.save()
            self.assertTrue(False, 'Save needs to throw an exception because field is required and not set')
        except:
            pass

        model_2.save()

        all_docs = TestModel.collection_instance.documents()
        self.assertEqual(len(all_docs), 2)

        retrieved_model_1 = None
        retrieved_model_2 = None

        for doc in all_docs:
            if doc.get(key='_key') == model_1.document.get(key='_key'):
                retrieved_model_1 = doc
            else:
                retrieved_model_2 = doc

        if retrieved_model_1:
            self.assertEqual(retrieved_model_1.get('test_field'), None)
        if retrieved_model_2:
            self.assertEqual(retrieved_model_2.get('test_field'), "model_2_text")

        TestModel.destroy()


class CollectionModelForeignKeyFieldTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = 'testcase_foreign_key_field_123'
        self.db = Database.create(name=self.database_name)

    def tearDown(self):
        Database.remove(name=self.database_name)

    def test_foreign_key_field(self):

        class ForeignTestModel(CollectionModel):

            test_field = CharField(required=True)

        class TestModel(CollectionModel):

            other = ForeignKeyField(to=ForeignTestModel, required=True)

        # Init collections
        ForeignTestModel.init()
        TestModel.init()

        # Init models
        model_1 = ForeignTestModel()
        model_1.test_field = 'ddd'

        model_2 = TestModel()
        model_2.other = model_1

        # Save models
        model_1.save()
        model_2.save()

        all_test_models = TestModel.objects.all()
        self.assertEqual(len(all_test_models), 1)

        real_model = all_test_models[0]

        self.assertEqual(real_model.other.test_field, model_1.test_field)

        # Destroy collections
        ForeignTestModel.destroy()
        TestModel.destroy()


class TransactionTestCase(ExtendedTestCase):
    def setUp(self):

        self.database_name = 'testcase_transaction_123'
        self.db = Database.create(name=self.database_name)

        self.operating_collection = 'foo_test'
        self.test_1_col = Collection.create(name=self.operating_collection)

    def tearDown(self):
        Collection.remove(name=self.operating_collection)
        Database.remove(name=self.database_name)

    def test_create_document(self):

        trans = Transaction(collections={
            'write': [
                self.operating_collection,
            ]
        })

        # Uses already chosen database as usual
        collection = trans.collection(name=self.operating_collection)
        collection.create_document(data={
            'test': 'foo'
        })

        ctrl = TransactionController()

        transaction_result = ctrl.start(transaction=trans)

        transaction_doc = create_document_from_result_dict(transaction_result['result'], self.test_1_col.api)

        created_doc = SimpleQuery.get_by_example(self.test_1_col, example_data={
            '_id': transaction_doc.id
        })

        self.assertDocumentsEqual(transaction_doc, created_doc)

    def test_update_document(self):
        pass

if __name__ == '__main__':
    unittest.main()