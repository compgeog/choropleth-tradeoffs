def get_shp_attribute_by_name(shp, attrname):
    """
    shp: shapex object
    """
    val = []
    for f in shp:
        val.append(f['properties'][attrname])
    return val
