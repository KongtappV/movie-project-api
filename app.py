import sys
import os

if not os.path.exists("config.py"):
    print("Configuration 'config.py' not found.")
    exit(1)

from config import OPENAPI_AUTOGEN_DIR

if not os.path.exists(OPENAPI_AUTOGEN_DIR):
    print("Folder '{}' not found.  "
          "Execute openapi-generator to generate it, "
          "e.g.,".format(OPENAPI_AUTOGEN_DIR))
    print()
    print("  "
          "java -jar openapi-generator-cli-5.3.0.jar generate \\\n"
          "     -i openapi/movie-api.yaml \\\n"
          "     -o {} -g python-flask".format(OPENAPI_AUTOGEN_DIR))
    print()
    exit(1)

sys.path.append(OPENAPI_AUTOGEN_DIR)

try:
    import connexion
except ModuleNotFoundError:
    print("Please install all required packages by running:"
          " pip install -r requirements.txt")
    exit(1)

from autogen.openapi_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('movie-api.yaml',
                arguments={'title': 'Movie Review API'},
                pythonic_params=True)

    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
