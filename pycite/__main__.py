def main():
    from pycite.pycite import PyCite
    import argparse

    args_parser = argparse.ArgumentParser()

    # Required arguments: Input file, output file

    args_parser.add_argument("-i", "--input-file", type=str, required=True,help="Path to an input file")
    args_parser.add_argument("-o", "--output-file", type=str, required=True, help="Path to an output file")
    args_parser.add_argument("-s", "--show-doi",type=str, required=False, help="Should DOIs be shown?")

    # Make boolean
    def make_bool(in_str):
        bools_dict = {"True":True, "TRUE":True,1:True,"1":True,
                      "T":True, "False": False, "F": False, "0": False,
                      "FALSE": FALSE, 0: False}
        return bools_dict[in_str]


    use_arguments = args_parser.parse_args()
    # Create a PyCite object
    use_object = PyCite(use_arguments.input_file, use_arguments.output_file,
                        show_doi=make_bool(use_arguments.show_doi))

    try:
        use_object.cite()
    except Exception:
        # TODO: Use specific Exception
        raise
    else:
        print("Thank you for using pycite, please provide feedback at https://github.com/Nelson-Gon/pycite")


if __name__=="__main__":
    main()


