import grpc
import ftp_pb2
import ftp_pb2_grpc
import sys
from pathlib import Path
def help_cmd(cmd: str):
    if cmd == "upload":
        print("upload file_path [options]")
        print("available options:")
        print("\t--server server_address")
        print("\t--port server_port")

    if cmd == "download":
        print("download file_path [options]")
        print("available options:")
        print("\t--server server_address")
        print("\t--port server_port")

    if cmd == "help":
        print("shows the usage message")

def download_file(stub, filename):
    file_request = ftp_pb2.DownloadReq(name=filename)
    file_content_iterator = stub.Download(file_request)
    
    with open(f"./client/download/downloaded_{filename}", 'wb') as f:
        for chunk in file_content_iterator:
            f.write(chunk.data)

    print(f"Downloaded file: {filename}")

def upload_file(stub, filename):
    with open(f"{filename}", 'rb') as f:
        content = f.read()
        seq_no = 1
        file_name_original = Path(filename).name
        file_content = ftp_pb2.File(name=file_name_original, data=content)
        status = stub.Upload(iter([file_content]))

    print(status.message)

def run_grpc_client():
    server = "localhost"
    port = 50051
    if len(sys.argv) <= 2:
        print(f"usage: {sys.argv[0]} command")
        print(f"available commands:\n\tupload\n\tdownload\n\thelp")
    else:
        for i in sys.argv:
            for j in sys.argv:
                if j == "--port":
                    port = sys.argv[sys.argv.index(j) + 1]
                elif j == "--server":
                    server = sys.argv[sys.argv.index(j) + 1]
                if j == "help":
                    command = sys.argv[sys.argv.index(i) + 1]
                    help_cmd(command)
                    return
            channel = grpc.insecure_channel(f"{server}:{port}")
            ftp_stub = ftp_pb2_grpc.FTPStub(channel)
            
            if i == "download":
                file_path = sys.argv[sys.argv.index(i) + 1]
                download_file(ftp_stub, file_path)
            elif i == "upload":
                file_path = sys.argv[sys.argv.index(i) + 1]
                upload_file(ftp_stub, file_path)

if __name__ == '__main__':
    run_grpc_client()
