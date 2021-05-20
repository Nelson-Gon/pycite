def main():
    from pycite.pycite import PyCite
    import argparse

    args_parser = argparse.ArgumentParser()

    # Required arguments: Input file, output file

    args_parser.add_argument("-i", "--input-file", type=str, required=True,help="Path to an input file")
    args_parser.add_argument("-o", "--output-file", type=str, required=True, help="Path to an output file")

    use_arguments = args_parser.parse_args()
    # Create a PyCite object
    use_object = PyCite(use_arguments.input_file, use_arguments.output_file)

    try:
        use_object.cite()
    except Exception:
        # TODO: Use specific Exception
        raise
    else:
        print("Thank you for using pycite, please provide feedback at https://github.com/Nelson-Gon/pycite")


if __name__=="__main__":
    main()


