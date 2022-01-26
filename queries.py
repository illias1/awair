DEVICE_BY_ID_QUERY = """
query DEVICE_BY_ID_QUERY($id: bpchar!) {
devices_by_pk(id: $id) {
    id
    status
    timezone
    type
    coordinates
  }
}
"""

DEVICES_QUERY = """
query DEVICES_QUERY($where: devices_bool_exp, $offset: Int) {
  devices(where: $where, offset: $offset) {
    id
    status
    timezone
    type
    coordinates
  }
}
"""

DEVICES_UPSERT_MUTATION = """
mutation DEVICES_UPSERT_MUTATION ($objects: [devices_insert_input!]!, $on_conflict: devices_on_conflict) {
  insert_devices(objects:$objects, on_conflict:$on_conflict) {
    affected_rows
    returning {
      id
    }
  }
}
"""

