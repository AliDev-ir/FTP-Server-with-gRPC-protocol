import grpc
from concurrent import futures
import ftp_pb2
import ftp_pb2_grpc

# _ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FTPServicer(ftp_pb2_grpc.FTPServicer):
    def Download(self, request, context):
        try:
            seq_no = 1
            with open(f"./server/{request.name}", 'rb') as f:
                content = f.read()
                yield ftp_pb2.File(name=request.name, data=content)
        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File '{request.name}' not found.")

    def Upload(self, request_iterator, context):
        try:
            filename = ""
            content = b""
            for chunk in request_iterator:
                filename = chunk.name
                content += chunk.data
            with open(f"./server/{filename}", 'wb') as f:
                f.write(content)
            return ftp_pb2.UploadRes(message=f"File '{filename}' uploaded successfully")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error uploading file: {str(e)}")
            return ftp_pb2.UploadRes()

def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ftp_pb2_grpc.add_FTPServicer_to_server(FTPServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run_grpc_server()
