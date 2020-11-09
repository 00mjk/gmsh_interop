import gmsh


OUTPUT_TEMPLATE = """# GENERATED by gmsh_interop/contrib/gmsh-node-tuples.py
# GMSH_VERSION: %s
# DO NOT EDIT

triangle_data = %s

tetrahedron_data = %s

quadrangle_data = %s

hexahedron_data = %s
"""


TRIANGLE_ELEMENTS = {
        "MSH_TRI_3": 2,
        "MSH_TRI_6": 9,
        "MSH_TRI_10": 21,
        "MSH_TRI_15": 23,
        "MSH_TRI_21": 25,
        "MSH_TRI_28": 42,
        "MSH_TRI_36": 43,
        "MSH_TRI_45": 44,
        "MSH_TRI_55": 45,
        "MSH_TRI_66": 46,
        }


TETRAHEDRON_ELEMENTS = {
        "MSH_TET_4": 4,
        "MSH_TET_10": 11,
        "MSH_TET_20": 29,
        "MSH_TET_35": 30,
        "MSH_TET_56": 31,
        "MSH_TET_84": 71,
        "MSH_TET_120": 72,
        "MSH_TET_165": 73,
        "MSH_TET_220": 74,
        "MSH_TET_286": 75,
        }


QUADRANGLE_ELEMENTS = {
        "MSH_QUA_4": 3,
        "MSH_QUA_9": 10,
        "MSH_QUA_16": 36,
        "MSH_QUA_25": 37,
        "MSH_QUA_36": 38,
        "MSH_QUA_49": 47,
        "MSH_QUA_64": 48,
        "MSH_QUA_81": 49,
        "MSH_QUA_100": 50,
        "MSH_QUA_121": 51,
        }


HEXAHEHEDRON_ELEMENTS = {
        "MSH_HEX_8": 5,
        "MSH_HEX_27": 12,
        "MSH_HEX_64": 92,
        "MSH_HEX_125": 93,
        "MSH_HEX_216": 94,
        "MSH_HEX_343": 95,
        "MSH_HEX_512": 96,
        "MSH_HEX_729": 97,
        "MSH_HEX_1000": 98,
        }


def generate_node_tuples_from_gmsh(eltype, eldim, elvertices, domain="unit"):
    # {{{ get element

    name, dim, order, nnodes, nodes, nvertices = \
            gmsh.model.mesh.getElementProperties(eltype)
    assert dim == eldim
    assert nvertices == elvertices

    nodes = nodes.reshape(nnodes, dim) * order
    if domain == "unit":
        pass
    elif domain == "biunit":
        nodes = (1.0 + nodes) / 2.0
    else:
        raise ValueError(f"unknown domain: '{domain}'")

    # }}}

    return [tuple(node) for node in nodes.astype(int)]


def generate_node_tuples(filename):
    tri_data = {}
    tet_data = {}
    qua_data = {}
    hex_data = {}

    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)

    for order, (name, eltype) in enumerate(TRIANGLE_ELEMENTS.items()):
        node_tuples = generate_node_tuples_from_gmsh(eltype, 2, 3)
        tri_data[order + 1] = {
                "node_tuples": node_tuples,
                "element_type": eltype,
                "element_name": name,
                }

    for order, (name, eltype) in enumerate(TETRAHEDRON_ELEMENTS.items()):
        node_tuples = generate_node_tuples_from_gmsh(eltype, 3, 4)
        tet_data[order + 1] = {
                "node_tuples": node_tuples,
                "element_type": eltype,
                "element_name": name,
                }

    for order, (name, eltype) in enumerate(QUADRANGLE_ELEMENTS.items()):
        node_tuples = generate_node_tuples_from_gmsh(eltype, 2, 4, domain="biunit")
        qua_data[order + 1] = {
                "node_tuples": node_tuples,
                "element_type": eltype,
                "element_name": name,
                }

    for order, (name, eltype) in enumerate(HEXAHEHEDRON_ELEMENTS.items()):
        node_tuples = generate_node_tuples_from_gmsh(eltype, 3, 8, domain="biunit")
        hex_data[order + 1] = {
                "node_tuples": node_tuples,
                "element_type": eltype,
                "element_name": name,
                }

    gmsh.finalize()

    from pprint import pformat
    txt = (OUTPUT_TEMPLATE % (
        gmsh.GMSH_API_VERSION,
        pformat(tri_data, width=80),
        pformat(tet_data, width=80),
        pformat(qua_data, width=80),
        pformat(hex_data, width=80),
        )).replace('"', "")

    if filename is None:
        print(txt)
    else:
        with open(filename, "w") as fd:
            fd.write(txt)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default=None)
    args = parser.parse_args()

    generate_node_tuples(args.filename)
