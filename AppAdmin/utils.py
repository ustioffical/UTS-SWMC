from django.db import connections


def DictinctFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def AutoGenerateCodeForModel(model, column, code_key):
    code = ""
    cursor = connections['default'].cursor()
    obj = model.objects.all()
    obj_count = len(obj)
    if obj_count == 0:
        code = code_key + '1'
    else:
        tbl = model._meta.db_table
        query = "SELECT SPLIT_PART(" + column + ", '-', 2)::INTEGER AS unique_code FROM " + tbl + " ORDER BY SPLIT_PART(" + column + ", '-', 2)::INTEGER DESC LIMIT 1"
        cursor.execute(query)
        query_list = DictinctFetchAll(cursor)
        get_code = query_list[0]["unique_code"]
        code_count = int(get_code) + 1
        auto_code = code_key + str(code_count)
        code = auto_code
    return code



