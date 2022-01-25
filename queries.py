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
