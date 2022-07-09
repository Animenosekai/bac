from io import BytesIO
from parser import Document

from nasse import Nasse, Request, Response
from nasse.models import Login

nasse_app = Nasse(__name__)


@nasse_app.route('/<path:path>', methods="POST", login=Login(no_login=True))
def hello(request: Request):
    new_io = BytesIO()
    file = request.files["data"]
    file.save(new_io)
    document = Document(new_io)
    return Response({"number": len(document.pages), "content": [page.as_dict(camelCase=True) for page in document.pages]})


app = nasse_app.flask  # Flask WSGI
