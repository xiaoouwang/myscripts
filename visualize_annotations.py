# This script is used to convert a xmi file *Common Analysis System* (CAS) to a format facilitating discussion of annotations  of argumentation mining.
# find . -iname '*.zip' -exec sh -c 'unzip -o -d "${0%.*}" "$0"' '{}' ';' to unzip all the zip files (annotations) recursively in the current directory
### Author: xow


# get all the folder names in the directory
import os
from collections import defaultdict
from cassis import *


def get_folder_names(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]


fns = get_folder_names(".")
# print(fns)
for fn in fns:
    type_path = f'{fn}/admin/TypeSystem.xml'
    annotation_path = f'{fn}/admin/admin.xmi'
    output_path = f'{fn}/{fn}_output.md'
    with open(type_path, 'rb') as f:
        typesystem = load_typesystem(f)
    with open(annotation_path, 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)
    with open(output_path, 'w') as f:
        f.write('''<table>
    <tr>
    <th> Text </th>
    <th style="width:50%"> Annotations </th>
    </tr>
    <td valign="top">
    ''')
        for lab in cas.select('custom.DocumentLabel'):
            f.write(f'{lab.label}\n\n')
        f.write((cas.sofa_string+"\n\n")*6)
        f.write('</td><td valign="top">\n')
    components = defaultdict(list)
    for sentence in cas.select('custom.Span'):
        components[sentence.label].append(sentence.get_covered_text())

    with open(output_path, 'a') as f:
        for key, value in components.items():
            f.write(f'\n## {key}s\n')
            for v in value:
                f.write(v+"\n\n")
            f.write('\n')
        f.write("## Relations\n")

    with open(annotation_path, 'rb') as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)

    with open(output_path, 'a') as f:
        for relation in cas.select('custom.Relation'):
            if relation.label == "Support":
                f.write(relation.Governor.get_covered_text())
                f.write("\n")
                f.write("\n")
                f.write(f'### {relation.label}')
                f.write("\n")
                f.write(relation.Dependent.get_covered_text())
                f.write("\n")
                f.write("<hr>")
                f.write("\n")
        for relation in cas.select('custom.Relation'):
            if relation.label == "Attack":
                f.write(relation.Governor.get_covered_text())
                f.write("\n")
                f.write("\n")
                f.write(f'### {relation.label}')
                f.write("\n")
                f.write(relation.Dependent.get_covered_text())
                f.write("\n")
                f.write("<hr>")
                f.write("\n")
        for relation in cas.select('custom.Relation'):
            if relation.label == "PSupport":
                f.write(relation.Governor.get_covered_text())
                f.write("\n")
                f.write("\n")
                f.write(f'### {relation.label}')
                f.write("\n")
                f.write(relation.Dependent.get_covered_text())
                f.write("\n")
                f.write("<hr>")
                f.write("\n")
        for relation in cas.select('custom.Relation'):
            if relation.label == "PAttack":
                f.write(relation.Governor.get_covered_text())
                f.write("\n")
                f.write("\n")
                f.write(f'### {relation.label}')
                f.write("\n")
                f.write(relation.Dependent.get_covered_text())
                f.write("\n")
                f.write("<hr>")
                f.write("\n")
        f.write('''</td>
    </tr>
    </table>''')
