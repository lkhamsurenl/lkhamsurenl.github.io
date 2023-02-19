import argparse
import subprocess
import os

PWD = os.path.dirname(os.path.realpath(__file__))

def main():
    # this method converts ipynb into HTML and puts into posts directory
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    if not args.file.endswith("ipynb"):
        raise Exception(f"Input must be ipynb file! {args.file}")

    # convert into html
    subprocess.run(["jupyter", "nbconvert", "--execute", "--to", "html", args.file])
    output_file = args.file.replace(".ipynb", ".html")

    # Remove extra line at the top
    with open(output_file, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(output_file, 'w') as fout:
        fout.writelines(data[1:])
    
    new_location = os.path.join(PWD, "_posts")

    # move to the new location
    subprocess.run(["mv", output_file, new_location])

    print(f"Converted {args.file} to {new_location}!")

if __name__ == "__main__":
    main()
