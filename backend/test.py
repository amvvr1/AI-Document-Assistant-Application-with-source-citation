from app.services.text_extraction import  ExtractText

h = ExtractText()

path = "backend/app/uploads/sub 38min 10k.pdf"

result = h.read_document(path)

print(result)