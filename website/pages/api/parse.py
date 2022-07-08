from io import BytesIO
from parser.page import Document

from nasse import Nasse, Request

nasse_app = Nasse(__name__)


@nasse_app.route('/<path:path>')
def hello(request: Request):
    new_io = BytesIO()
    file = request.files["data"]
    file.save(new_io)
    document = Document(new_io)
    return {"number": len(document.pages), "content": [page.as_dict(camelCase=True) for page in document.pages]}


app = nasse_app.flask  # Flask WSGI
