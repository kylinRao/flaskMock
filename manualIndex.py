from flaskr import *
pdfPath = "static/pdf"
db = connect_db()
cur = db.execute('select savedFile from books;')
results =  cur.fetchall()
for fileName in os.listdir(pdfPath):
    if (fileName,) not in results:
        print fileName
        bookName, bookFileType = fileName.rsplit(".", 1)
        base64FileName = hashForString("md5", bookName) + "." + bookFileType
        db.execute(
            'insert into books (bookName,bookFileType,savedFile) VALUES ("{bookName}","{bookFileType}","{savedFile}")'.format(
                bookName=bookName, bookFileType=bookFileType, savedFile=base64FileName))
        db.commit()
        os.rename(os.path.join(pdfPath,fileName),os.path.join(pdfPath,base64FileName))

