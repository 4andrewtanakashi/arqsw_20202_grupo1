from util.utils import load_obj_to_file


class Grafo:

    def __init__(self, file):
        self.pseudo_adjacent_matrix = {}
        dictionary_data = load_obj_to_file(file)
        self.set_pseudo_adjacent_matrix(dictionary_data)



    def set_pseudo_adjacent_matrix (self, dictionary_data):
        for ele_dict_data in dictionary_data:
            name_class = ele_dict_data["name_obj"]
            self.pseudo_adjacent_matrix[name_class] = []
            if ele_dict_data["imports"] != []:
                method_outs = []
                for invocation_ele in ele_dict_data["invocation"]:
                    arr = invocation_ele.split('.')
                    if arr[0] != '' and (len(arr) > 1):
                        method_outs.append(arr[1].split('(')[0])
                    else:
                        method_outs.append(arr[0].split('(')[0])
                for import_ele in ele_dict_data["imports"]:
                    import_datas = import_ele.split('.')
                    import_datas = import_datas[len(import_datas)-1]

                    size_pam = len(self.pseudo_adjacent_matrix[name_class])
                    for ele_dict_data_compare in dictionary_data:
                        if ele_dict_data_compare["name_obj"] == import_datas:
                            i_met = 0
                            while (i_met < len(method_outs)) and (size_pam == len(self.pseudo_adjacent_matrix[name_class]) ):
                                if ele_dict_data_compare["method_names"].__contains__(method_outs[i_met]):
                                    self.pseudo_adjacent_matrix[name_class].append(ele_dict_data_compare["name_obj"])
                                i_met += 1
