from enum import Enum

class DBReport(Enum):
    CREATE_OK = "create_ok"
    CREATE_ALREADY_EXISTS = "create_already_exists"
    CREATE_ERROR = "create_error"
    GET_OK = "get_ok"
    GET_NOT_FOUND = "get_not_found"
    GET_ERROR = "get_error"
    UPDATE_OK = "update_ok"
    UPDATE_NOT_FOUND = "update_not_found"
    UPDATE_ERROR = "update_error"
    DELETE_OK = "delete_ok"
    DELETE_NOT_FOUND = "delete_not_found"
    DELETE_ERROR = "delete_error"