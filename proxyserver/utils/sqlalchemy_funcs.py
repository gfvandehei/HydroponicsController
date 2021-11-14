def sqlobj_to_json(sqlobject: dict):
    sql_obj_copy = sqlobject.copy()
    del sql_obj_copy["_sa_instance_state"]
    return sql_obj_copy